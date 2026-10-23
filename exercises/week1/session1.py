"""Session 1 starter: name the prediction problem before choosing a model."""

# A tiny, invented table. The target is a value the team wants to predict.
rows = [
    {"hour": 8, "rain_mm": 0, "station": "A", "rides_next_hour": 18},
    {"hour": 9, "rain_mm": 1, "station": "A", "rides_next_hour": 15},
    {"hour": 8, "rain_mm": 0, "station": "B", "rides_next_hour": 31},
]

feature_names = ["hour", "rain_mm", "station"]
target_name = "rides_next_hour"
print("features:", feature_names)
print("target:", target_name)

# TODO: Is this a supervised or unsupervised example? Explain why in a comment.
# TODO: Put these lifecycle steps in order: inspect, evaluate, frame, deploy,
#       split, fit, monitor.

lifecycle = ["frame", "inspect", "split", "fit", "evaluate", "deploy", "monitor"]
print("lifecycle:", " -> ".join(lifecycle))
# Expected lifecycle: frame -> inspect -> split -> fit -> evaluate -> deploy -> monitor
