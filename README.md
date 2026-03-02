# so2_mol — Molecular SO₂ (H₂SO₃) calculator for wine

A small, dependency-free Python module to estimate **molecular SO₂** from **free SO₂**, **pH**, **temperature**, **alcoholic strength**, and **ionic strength**, following the **OIV Type IV “molecular method”** approach.

---

## What the project does

### Outputs (typical)
- **Molecular SO₂ (mg/L)** — the antimicrobial-active fraction (H₂SO₃).
- **Molecular SO₂ (%)** of free SO₂.
- Intermediate values for traceability (e.g., **pKₜ**, **pKₘ**, coefficients **A** and **B**, etc.).

### Why it matters (oenology)
Molecular SO₂ is the biologically active form of free SO₂; at a fixed free SO₂, **pH** has the strongest impact on the molecular fraction, while **temperature**, **ABV**, and **ionic strength** shift the effective dissociation constant and therefore the molecular percentage.

---

## Scientific model (equations)

This implementation follows the OIV “molecular method” relationships:

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

---

## Input parameters

| Parameter | Unit | Typical range | Notes |
|---|---:|---:|---|
| `pH` | – | 2.8–4.0 | Major driver of molecular fraction |
| `free_so2` | mg/L | 0–80 | “Free SO₂” as measured analytically |
| `temp_c` | °C | 0–40 | Use wine bulk/storage temperature |
| `abv` | % v/v | 0–20 | Alcoholic strength |
| `ionic_strength` | mol/L | ~0.016–0.056 | Often approximated as **0.038** |

---

## Project structure (recommended)

You can keep the repository minimal. A typical layout is:

```
so2_mol/
├─ README.md
├─ .gitignore
└─ src/
   ├─ __init__.py
   └─ main.py        # your functions / calculations
```

---

## Requirements

- Python **3.10+**
- No external dependencies (standard library only, e.g. `math`)

---

## Usage

### Option A — import and call functions (recommended)

Example (adapt names to your module/function names):

```python
from src.main import molecular_so2_mg_l

mso2 = molecular_so2_mg_l(
    pH=3.10,
    free_so2=30.0,     # mg/L
    temp_c=20.0,       # °C
    abv=12.5,          # % v/v
    ionic_strength=0.038
)

print(f"Molecular SO2: {mso2:.3f} mg/L")
```

### Option B — run as a script

If `src/main.py` includes a `main()` entry point:

```bash
python src/main.py
```

---

## Validation checklist

To verify results:
- Compare computed molecular % or mg/L against **OIV Table III** for the same **pH**, **T**, **ABV**, and \(I=0.038\).
- If you compare with online calculators, ensure they use the same **pK model** and the same ionic strength assumption; different choices can produce different mSO₂ values.

---

## Glossary (quick IT concepts)

- **Module**: a Python file (`.py`) that provides reusable code you can `import`.
- **API (Application Programming Interface)**: the public “surface” of functions/classes you expose for others (or yourself) to call.
- **CLI (Command Line Interface)**: a program you run from the terminal with arguments (you can add this later with `argparse`).

---

## References / Sources

- OIV Compendium method: *OIV-MA-AS323-04C — Sulfur dioxide (molecular method), Type IV method*.  
  (Equations for \(mSO_2\) and the \(pK_M\) correction; plus reference tables.)
- AWRI technical note: *Understanding molecular SO₂ calculators* (discussion of mSO₂ equation and why calculators differ).

---

## Disclaimer

This repository provides **calculation utilities** and does not replace laboratory measurement, winery SOPs, or legal/compliance checks. Always confirm analytical inputs (pH, free SO₂, temperature) and interpret results within your production context.