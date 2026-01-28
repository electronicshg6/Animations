# Electronics Animations Repository

This repository contains code and assets to build animated electronics educational videos using **Manim** and **CircuitikZ**.  It is structured to promote reuse of common functionality and aesthetics across multiple projects.

## Structure

The tree below outlines the major components of the project.  Each new video should live in its own numbered folder under `projects/` to keep scenes and assets self‑contained.

```
electronics-animations/
├─ README.md              # this file
├─ pyproject.toml         # Python project metadata and dependencies
├─ manim.cfg              # Manim configuration (quality, frame rate)
├─ .gitignore             # files and directories to exclude from Git
├─ src/
│  └─ electroanim/        # reusable library code
│     ├─ __init__.py
│     ├─ aesthetics.py    # colour palette and style definitions
│     ├─ tex.py           # helper to build Tex templates with CircuitikZ
│     ├─ circuitikz.py    # helper to load CircuitikZ draw files as Manim objects
│     ├─ helpers.py       # common animation helper functions
│     └─ scene_base.py    # base Scene class setting global styles
└─ projects/
   └─ 01_voltage_divider/ # first animation project
      ├─ README.md        # narration and timing notes for the video
      ├─ assets/
      │  └─ circuit/
      │     └─ divider.tikz # CircuitikZ draw code for the voltage divider circuit
      └─ scene.py         # Manim scene implementing the animation
```

## Getting Started

1. Install the dependencies in editable mode:

   ```bash
   pip install -e .
   ```

2. Render a project by running Manim.  For example, to render the voltage divider scene:

   ```bash
   manim -pqh projects/01_voltage_divider/scene.py VoltageDivider
   ```

   The `-pqh` flags tell Manim to preview the video (`-p`), use high quality (`-q`), and to write the output to the default media directory.

3. Extend the repository by adding new projects under the `projects/` directory.  Use the existing files as a template for new circuits and scenes.

## Using CircuitikZ with Manim

Circuit diagrams are defined using CircuitikZ.  Each `.tikz` file should contain only the draw commands for the diagram (no `\begin{circuitikz}` wrappers).  The helper in `src/electroanim/circuitikz.py` loads these draw snippets into Manim's `Tex` objects using a custom LaTeX template that imports the `circuitikz` package.

If you decide to pre‑compile complex diagrams into SVGs instead, you can use `SVGMobject` in Manim to load the resulting files.  See the comments in `circuitikz.py` for details.

## License

This project is licensed under the MIT License.  See the [LICENSE](LICENSE) file for details.