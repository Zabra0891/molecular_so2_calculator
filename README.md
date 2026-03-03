# Molecular SO₂ Calculator (pH, Temperature, Alcohol)

This project is a small Python script that calculates **molecular SO₂** starting from **free SO₂**, using:
- **pH**
- **temperature (°C)**
- **alcohol (% vol)**

The calculation uses:
1. a quadratic model for **pKt**
2. quadratic coefficients **A** and **B**
3. an **ionic strength correction** to compute **pKm**
4. the final molecular SO₂ equation:  
   `molecular_SO2 = free_so2 / (1 + 10^(pH - pKm))`

---

## Features

- Interactive input from terminal
- Input validation (numeric values + ranges)
- **Format validation** for *pH* and *temperature*: they must be entered with **exactly 2 decimal digits** (e.g. `3.20`, `20.00`)
- Modular functions (easy to reuse in other scripts or notebooks)

---

## Requirements

- Python 3.x
- No external libraries required (only Python standard library: `math`)

---

## How to Run (Linux Mint / Ubuntu)

1. Save the script (example: `main.py`).
2. Open a terminal in the folder where the file is located.
3. Run with Python 3:

```bash
python3 main.py
```

> If your system does not recognize the `python` command (common on many Linux distributions), use `python3` as shown above.
> Optional: if you *really* want `python` to point to `python3`, you can install the package `python-is-python3`.

---

## Input Validation Rules

### Numeric ranges

| Parameter | Unit | Allowed range |
|---|---:|---:|
| free_so2 | mg/L | 0 – 80 |
| pH | - | 2.8 – 4.0 |
| temp | °C | 0 – 40 |
| alc | % vol | 0 – 20 |

### Required format (important)

- **pH must be entered with exactly 2 decimals**  
  ✅ `3.20` (accepted)  
  ✅ `3,20` (accepted: comma is converted to dot)  
  ❌ `3.2` (rejected)  
  ❌ `3` (rejected)

- **Temperature must be entered with exactly 2 decimals**  
  ✅ `20.00` (accepted)  
  ✅ `0.50` (accepted)  
  ✅ `20,00` (accepted: comma is converted to dot)  
  ❌ `20` (rejected)  
  ❌ `20.0` (rejected)

If the input is not numeric, out of range, or not in the required format (for pH/temp), the program will ask again.

---

## Code Structure

- `control_input()`  
  Collects and validates the four user inputs (including 2-decimal format for pH and temperature).

- `pKt_quad(temp, alc)`  
  Computes pKt (quadratic model).

- `A_quad(temp, alc)` and `B_quad(temp, alc)`  
  Compute the A and B coefficients (quadratic models).

- `ionic_ratio(temp, alc)`  
  Computes the ionic correction term using `IONIC_STRENGTH`.

- `pKm(temp, alc)`  
  Computes pKm = pKt − ionic correction.

- `mol_SO2(free_so2, ph, temp, alc)`  
  Computes molecular SO₂ from free SO₂.

- `main()`  
  Runs the interactive workflow.

---

## Notes

- `IONIC_STRENGTH` is currently set to a fixed value:
  - `IONIC_STRENGTH = 0.056`

If you plan to adapt the model, you can expose this parameter as an input or compute it dynamically.

---

## Example Session

Example inputs:

- free_so2 = `25`
- pH = `3.20`  (must have 2 decimals)
- temp = `20.00` (must have 2 decimals)
- alc = `12.5`

Output:

- `Molecular SO2: ...`

---

## License

Choose a license if you plan to publish the repository (e.g., MIT).