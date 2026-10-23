(() => {
  "use strict";
  const VERSION = "v0.27.7";
  const INDEX_URL = `https://cdn.jsdelivr.net/pyodide/${VERSION}/full/`;
  let runtimePromise;

  async function runtime() {
    if (!runtimePromise) {
      if (typeof window.loadPyodide !== "function") {
        throw new Error("The Pyodide script did not load. Check the network or use the expected output and offline .py file.");
      }
      runtimePromise = window.loadPyodide({ indexURL: INDEX_URL }).then(async (pyodide) => {
        await pyodide.loadPackage(["numpy", "matplotlib", "scikit-learn"]);
        return pyodide;
      }).catch((error) => {
        runtimePromise = null;
        throw error;
      });
    }
    return runtimePromise;
  }

  for (const button of document.querySelectorAll("[data-pyodide-run]")) {
    button.addEventListener("click", async () => {
      const cell = button.closest("[data-python-cell]");
      const editor = cell?.querySelector("[data-python-code]");
      const output = cell?.querySelector("[data-cell-output]");
      const plot = cell?.querySelector("[data-cell-plot]");
      const status = cell?.querySelector("[data-cell-status]");
      if (!editor || !output || !status) return;

      button.disabled = true;
      button.textContent = "Loading Python…";
      output.textContent = "";
      status.classList.remove("cell-error");
      status.textContent = "First run downloads the Python runtime and scientific packages; this can take a few minutes on slow Wi-Fi.";
      if (plot) { plot.hidden = true; plot.removeAttribute("src"); }

      let stdout = "";
      try {
        const pyodide = await runtime();
        pyodide.setStdout({ batched: (line) => { stdout += `${line}\n`; } });
        pyodide.setStderr({ batched: (line) => { stdout += `stderr: ${line}\n`; } });
        await pyodide.runPythonAsync(editor.value);
        output.textContent = stdout.trim() || "Code finished. See the cell result above or inspect variables in the starter code.";
        if (plot) {
          try {
            const image = pyodide.runPython("plot_base64 if 'plot_base64' in globals() else ''");
            const value = image?.toString?.() || "";
            image?.destroy?.();
            if (value) { plot.src = `data:image/png;base64,${value}`; plot.hidden = false; }
          } catch (_error) { /* A plot is optional for cells without plot_base64. */ }
        }
        status.textContent = "Cell finished in this browser. Nothing was uploaded.";
      } catch (error) {
        output.textContent = stdout.trim();
        status.classList.add("cell-error");
        status.textContent = `${error.message || error} The printed expected output remains available; you can continue without running Python.`;
      } finally {
        button.disabled = false;
        button.textContent = "Run this Python cell";
      }
    });
  }
})();
