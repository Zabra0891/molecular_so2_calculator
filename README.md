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
- **Format validation**:
  - *pH*: exactly **2 decimal digits** (e.g. `3.20`)
  - *temperature*: exactly **1 decimal digit** (e.g. `20.0`)
  - *alcohol*: exactly **2 decimal digits** (e.g. `11.50`)
- Model coefficients stored in an immutable `Config` dataclass (`frozen=True, slots=True`)
- Full type hints on all functions
- Modular functions (easy to reuse in other scripts or notebooks)

---

## Requirements

- Python 3.10+
- No external libraries required (only Python standard library: `math`, `dataclasses`)

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

| Parameter | Unit  | Allowed range |
|-----------|------:|--------------:|
| free_so2  | mg/L  | 0 – 80        |
| pH        | -     | 2.80 – 4.00   |
| temp      | °C    | 0.0 – 40.0    |
| alc       | % vol | 0.00 – 20.00  |

### Required format (important)

- **pH must be entered with exactly 2 decimals**  
  ✅ `3.20` (accepted)  
  ✅ `3,20` (accepted: comma is converted to dot)  
  ❌ `3.2` (rejected)  
  ❌ `3` (rejected)

- **Temperature must be entered with exactly 1 decimal**  
  ✅ `20.0` (accepted)  
  ✅ `20,0` (accepted: comma is converted to dot)  
  ❌ `20` (rejected)  
  ❌ `20.00` (rejected)

- **Alcohol must be entered with exactly 2 decimals**  
  ✅ `11.50` (accepted)  
  ✅ `11,50` (accepted: comma is converted to dot)  
  ❌ `11` (rejected)  
  ❌ `11.5` (rejected)

If the input is not numeric, out of range, or not in the required format, the program will ask again.

---

## Code Structure

- `Config` (dataclass, frozen)  
  Immutable container for all model coefficients and ionic strength (`ionic_strength = 0.056`). A single global instance `CFG` is used as default.

- `control_input() -> tuple[float, float, float, float]`  
  Collects and validates the four user inputs (format: 2 decimals for pH and alcohol, 1 decimal for temperature).

- `pKt_quad(temp, alc, cfg) -> float`  
  Computes pKt (quadratic model in temp and alc).

- `A_quad(temp, alc, cfg) -> float` and `B_quad(temp, alc, cfg) -> float`  
  Compute the A and B coefficients (quadratic models).

- `ionic_ratio(temp, alc, cfg) -> float`  
  Computes the ionic correction term using `cfg.ionic_strength`.

- `pKm(temp, alc, cfg) -> float`  
  Computes pKm = pKt − ionic correction.

- `mol_SO2(free_so2, ph, temp, alc, cfg) -> float`  
  Computes molecular SO₂ from free SO₂.

- `main() -> None`  
  Runs the interactive workflow.

---

## Notes

- `ionic_strength` is currently set to a fixed value inside `Config`:  
  `ionic_strength: float = 0.056`  
  If you plan to adapt the model, you can expose this parameter as an input or compute it dynamically by passing a custom `Config` instance.

- The result is displayed with **exactly 3 decimal places** (e.g. `Molecular SO2: 0.276 mg/L`).

---

## Example Session