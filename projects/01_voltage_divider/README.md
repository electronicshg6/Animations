# Voltage Divider Animation

This folder contains the assets and Manim scene for a short video explaining how a resistor voltage divider works.

## Video Outline

- **0–5 s:** Introduce the circuit: two resistors in series dividing an input voltage.
- **5–15 s:** Derive and display the equation for the output voltage:
  \(V_{out} = V_{in} \frac{R_2}{R_1 + R_2}\).
- **15–25 s:** Numerical example: with \(V_{in}=12\,\text{V}\), \(R_1=10\,\text{k}\Omega\) and \(R_2=10\,\text{k}\Omega\), we get \(V_{out}=6\,\text{V}\).
- **25–45 s:** Discuss loading: connecting a load resistor changes the effective \(R_2\) to the parallel combination \(R_2 \parallel R_L\), which causes voltage droop.
- **45–60 s:** Tease future videos: mention that voltage regulators can maintain a constant output despite load changes.

## Running the Animation

Make sure you have installed the repository in editable mode:

```bash
pip install -e .
```

Then run Manim from the project root:

```bash
manim -pqh projects/01_voltage_divider/scene.py VoltageDivider
```

The rendered video will be saved in the `media/` folder.  Adjust the quality flags (`-ql`, `-qm`, `-qh`) as needed.