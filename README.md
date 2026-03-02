# so2_mol — Molecular SO₂ (H₂SO₃) calculator for wine

A small, dependency-free Python module to estimate **molecular SO₂** from **free SO₂**, **pH**, **temperature**, and **alcoholic strength (ABV)**, using the **OIV Type IV “molecular method”** relationship for the molecular fraction.

> Note: **ionic strength (`I`) is currently a global constant in the code** (default `I = 0.056`). To use a different ionic strength (e.g., 0.038), edit the `I` value in `main.py`.

---

## What the project does

### Outputs (typical)
- **Molecular SO₂ (mg/L)** — the antimicrobial-active fraction (H₂SO₃).
- **Molecular SO₂ (%)** of free SO₂.
- Intermediate values for traceability (e.g., **pKₜ**, **pKₘ**, coefficients **A** and **B**).

### Why it matters (oenology)
Molecular SO₂ is the biologically active form of free SO₂. At fixed free SO₂, **pH** has the strongest impact on the molecular fraction, while **temperature**, **ABV**, and **ionic strength** shift the effective dissociation constant and therefore the molecular percentage.

---

## Scientific model (equations)

This implementation follows the OIV “molecular method” relationships.

### 1) Molecular fraction of free SO₂
\[
[H_2SO_3] = \frac{L}{10^{(pH - pK_M)} + 1}
\]
where \(L = [H_2SO_3] + [HSO_3^-]\) (i.e., **free SO₂**).

Practical form (used in code, base-10):
\[
mSO_2\; (mg/L) = \frac{Free\;SO_2\; (mg/L)}{1 + 10^{(pH - pK_M)}}
\]

### 2) Mixed dissociation constant correction (ionic strength)
\[
pK_M = pK_T - \frac{A\sqrt{I}}{1 + B\sqrt{I}}
\]
- \(I\) = ionic strength  
- \(A, B\) vary with **temperature** and **alcoholic strength**

> Implementation note: `pK_T`, `A`, and `B` are computed via quadratic models (coefficients embedded in `main.py`) to avoid lookup tables.

---

## Input parameters (current API)

| Parameter | Unit | Typical range | Notes |
|---|---:|---:|---|
| `free_so2` | mg/L | 0–80 | “Free SO₂” as measured analytically |
| `pH` | – | 2.8–4.0 | Major driver of molecular fraction |
| `temp` | °C | 0–40 | Use wine bulk/storage temperature |
| `alc` | % v/v | 0–20 | Alcoholic strength (ABV) |
| `I` | – | ~0.016–0.056 | **Global constant** in code (`I = 0.056`) |

---

## Project structure

Current (simple) layout:

```
so2_mol/
├─ README.md
├─ .gitignore
└─ main.py      # functions + script entry point
```

---

## Requirements

- Python **3.10+**
- No external dependencies (standard library only: `math`)

> On many Linux distributions the command is `python3` (not `python`).

---

## API (functions)

The module exposes these main building blocks:
- `pKt_quad(temp, alc)` → computes pKₜ (quadratic model)
- `A_quad(temp, alc)` / `B_quad(temp, alc)` → coefficients A and B (quadratic models)
- `ionic_ratio(temp, alc)` → ionic correction term
- `pKm(temp, alc)` → corrected pKₘ
- `mol_SO2(free_so2, pH, temp, alc)` → **molecular SO₂ (mg/L)**

---

## Usage

### Option A — import and call functions (recommended)

```python
from main import mol_SO2, pKm, I

free_so2 = 30.0   # mg/L
pH = 3.10
temp = 20.0       # °C
alc = 12.5        # % v/v

mso2 = mol_SO2(free_so2, pH, temp, alc)

print(f"Molecular SO2: {mso2:.3f} mg/L")
print(f"Molecular % of free: {100 * mso2 / free_so2:.2f}%")
print(f"pKm: {pKm(temp, alc):.4f}")
print(f"I (ionic strength): {I:.3f}")
```

One-liner from the terminal (run from the project root):

```bash
python3 -c "from main import mol_SO2; print(mol_SO2(30.0, 3.10, 20.0, 12.5))"
```

### Option B — run as a script

`main.py` includes a script entry point (`if __name__ == '__main__':`), so you can run:

```bash
python3 main.py
```

Edit the example values at the bottom of `main.py` to match your wine parameters.

---

## Validation checklist

To verify results:
- Compare computed molecular SO₂ (mg/L) or molecular % against OIV reference tables for the same **pH**, **T**, **ABV**, and ionic strength \(I\).
- If you compare with online calculators, ensure they use the same **pK model** and the same ionic strength assumption; different choices can produce different results.

---

## Glossary (quick IT concepts)

- **Module**: a Python file (`.py`) that provides reusable code you can `import`.
- **Entry point**: the section guarded by `if __name__ == "__main__":` that runs only when the file is executed as a script.
- **API (Application Programming Interface)**: the public “surface” of functions you expose for others (or yourself) to call.

---

## References / Sources

- OIV Compendium method (Type IV): **OIV-MA-AS323-04C — Sulfur dioxide (molecular method)**  
  https://www.oiv.int/de/node/2091/download/pdf
- Python documentation: `__main__` (top-level code environment)  
  https://docs.python.org/3/library/__main__.html
- Python documentation: import system (modules/packages)  
  https://docs.python.org/3/reference/import.html

---

## Disclaimer

This repository provides **calculation utilities** and does not replace laboratory measurement, winery SOPs, or legal/compliance checks. Always confirm analytical inputs (pH, free SO₂, temperature) and interpret results within your production context.