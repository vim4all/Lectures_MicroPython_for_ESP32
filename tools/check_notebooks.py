"""Check the course notebooks.

1. Every notebook is valid nbformat; lab notebooks keep the MicroPython kernelspec.
2. Lecture book conventions (see the PDF export in tools/regenerate_pdfs.py):
   * every ``##``/``###`` heading inside a chapter ends with ``{-}`` (otherwise LaTeX numbers it twice);
   * every ``\\begin{selfcheckbox}`` raw-LaTeX cell is closed by an ``\\end{selfcheckbox}`` cell;
   * every code cell (diagram) is tagged ``remove_input`` (source hidden in the PDF) and ``hide-input``.
3. (unless --no-exec) the lecture book executes top to bottom without errors and every diagram cell
   (one that calls ``plt.show()``) produces exactly one figure.

The lab notebooks hold MicroPython code for the ESP32 board and are not executed here.

Usage:
    python tools/check_notebooks.py            # structure + execution
    python tools/check_notebooks.py --no-exec  # structure only (fast)
    python tools/check_notebooks.py --inplace  # also save executed outputs (figures) into the lecture book
"""
import argparse
import os
import re
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent.parent
LECTURE = ROOT / "Lecture_Course_MicroPython_ESP32.ipynb"
LABS = sorted(ROOT.glob("Lab_work_*.ipynb"))


def check_lab(nb):
    ks = nb.metadata.get("kernelspec", {})
    return [] if ks.get("language") == "micropython" else [f"kernelspec is {ks.get('name')!r}, expected micropython"]


def check_lecture(nb):
    problems, in_chapter, box_open = [], False, None
    for i, c in enumerate(nb.cells):
        src = c.source
        if c.cell_type == "markdown":
            for line in src.splitlines():
                if re.match(r"# 📘 Розділ \d+\.", line):
                    in_chapter = True
                elif in_chapter and re.match(r"#{2,6} ", line) and not line.rstrip().endswith("{-}"):
                    problems.append(f"cell {i}: heading without {{-}}: {line.strip()[:60]}")
            if "\\begin{selfcheckbox}" in src:
                if box_open is not None:
                    problems.append(f"cell {i}: selfcheckbox opened again, previous one from cell {box_open} not closed")
                box_open = i
            if "\\end{selfcheckbox}" in src:
                if box_open is None:
                    problems.append(f"cell {i}: selfcheckbox closed but not opened")
                box_open = None
        elif c.cell_type == "code":
            tags = set(c.metadata.get("tags", []))
            missing = {"remove_input", "hide-input"} - tags
            if missing:
                problems.append(f"cell {i}: code cell without tag(s) {', '.join(sorted(missing))}")
    if box_open is not None:
        problems.append(f"cell {box_open}: selfcheckbox never closed")
    return problems


def execute(nb, inplace):
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError

    client = NotebookClient(nb, timeout=600, kernel_name=os.environ.get("CHECK_KERNEL", "python3"),
                            resources={"metadata": {"path": str(ROOT)}})
    try:
        client.execute()
    except CellExecutionError as e:
        return [str(e).splitlines()[-1] if str(e) else "cell execution error"]
    problems = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        # warnings of the local Python installation (e.g. matplotlib's Axes3D) do not belong in the book
        c.outputs = [o for o in c.outputs if o.output_type != "stream"]
        if "plt.show()" in c.source:
            n = sum("image/png" in o.get("data", {}) for o in c.outputs)
            if n != 1:
                problems.append(f"cell {i}: expected 1 figure, got {n}")
    if inplace and not problems:
        nbformat.write(nb, LECTURE)
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-exec", action="store_true")
    ap.add_argument("--inplace", action="store_true")
    args = ap.parse_args()

    failed = False
    for path in [LECTURE, *LABS]:
        nb = nbformat.read(path, as_version=4)
        try:
            nbformat.validate(nb)
            problems = []
        except nbformat.ValidationError as e:
            problems = [f"invalid notebook: {e.message}"]
        if path == LECTURE:
            problems += check_lecture(nb)
            if not args.no_exec and not problems:
                problems += execute(nb, args.inplace)
        else:
            problems += check_lab(nb)
        for p in problems:
            print(f"FAIL {path.name}: {p}")
        failed |= bool(problems)
        if not problems:
            print(f"OK   {path.name}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
