#!/usr/bin/env python3
"""Synthetic Socket.IO smoke/load test; never use real student identities."""
from __future__ import annotations

import argparse
import asyncio
import sys
import uuid

import socketio


async def exercise_client(index: int, args: argparse.Namespace) -> tuple[bool, str]:
    client = socketio.AsyncClient(reconnection=False, logger=False, engineio_logger=False)
    joined = asyncio.Event()
    question_ready = asyncio.Event()
    answer_saved = asyncio.Event()
    state: dict[str, object] = {}
    errors: list[str] = []

    @client.on("joined")
    async def on_joined(data: dict) -> None:
        joined.set()

    @client.on("question_state")
    async def on_question(data: dict) -> None:
        state["question"] = data
        question_ready.set()

    @client.on("answer_ack")
    async def on_ack(data: dict) -> None:
        answer_saved.set()

    @client.on("join_error")
    async def on_join_error(data: dict) -> None:
        errors.append(str(data.get("message", "join error")))
        joined.set()

    @client.on("answer_error")
    async def on_answer_error(data: dict) -> None:
        errors.append(str(data.get("message", "answer error")))
        answer_saved.set()

    try:
        await client.connect(
            args.url.rstrip("/"),
            transports=["websocket", "polling"],
            wait_timeout=args.timeout,
        )
        participant_id = f"load-{uuid.uuid4().hex}"
        await client.emit("join_session", {
            "participant_id": participant_id,
            "display_name": f"Synthetic {index + 1}",
            "github_username": "",
            "session_code": args.session_code.upper(),
        })
        await asyncio.wait_for(joined.wait(), timeout=args.timeout)
        if errors:
            return False, errors[0]
        await asyncio.wait_for(question_ready.wait(), timeout=args.timeout)
        question = state.get("question")
        if not isinstance(question, dict):
            return False, "server did not send a question"
        answer: str
        if question.get("type") == "mcq":
            choices = question.get("choices", [])
            answer = str(choices[0]["key"]) if choices else "A"
        else:
            answer = "synthetic"
        await client.emit("submit_answer", {"participant_id": participant_id, "question_id": question["id"], "answer": answer})
        await asyncio.wait_for(answer_saved.wait(), timeout=args.timeout)
        if errors:
            return False, errors[0]
        return True, "ok"
    except Exception as exc:  # report every synthetic client's failure in the final summary
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        if client.connected:
            await client.disconnect()


async def run(args: argparse.Namespace) -> int:
    semaphore = asyncio.Semaphore(args.concurrency)

    async def limited(index: int) -> tuple[bool, str]:
        async with semaphore:
            await asyncio.sleep(index * 0.001)
            return await exercise_client(index, args)

    results = await asyncio.gather(*(limited(index) for index in range(args.clients)))
    connected = sum(ok for ok, _ in results)
    errors = [(index + 1, reason) for index, (ok, reason) in enumerate(results) if not ok]
    print(f"Synthetic clients: {args.clients}")
    print(f"Connections and answer acknowledgements: {connected}/{args.clients}")
    print(f"Failures: {len(errors)}")
    for index, reason in errors[:20]:
        print(f"  client {index}: {reason}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} additional failures")
    print("This is a synthetic smoke test, not a capacity guarantee; rehearse on the real classroom network.")
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Quiz base address, e.g. http://192.168.1.20:8000")
    parser.add_argument("--session-code", default="MDC301W1")
    parser.add_argument("--clients", type=int, default=200)
    parser.add_argument("--concurrency", type=int, default=40, help="Maximum simultaneous synthetic connects")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args()
    if not 1 <= args.clients <= 1000 or not 1 <= args.concurrency <= args.clients:
        parser.error("--clients must be 1..1000 and --concurrency 1..--clients")
    try:
        return asyncio.run(run(args))
    except KeyboardInterrupt:
        print("Load test interrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
