# Molecular SO₂ Calculator

A Python command-line calculator that estimates molecular sulfur dioxide (SO₂) from free SO₂, pH, temperature and alcohol content using the equations described by Jenkins et al. [1].

**Status:** the corrected implementation has been checked against the equations in the supplied 2020 *Papers in Press* article. Experimental accuracy and the scientific validity of the entire software input range have not been established.

## Requirements

- Python 3.10 or later.
- Running the calculator requires only the Python standard library.
- Running the automated tests additionally requires `pytest`, listed in `requirements-dev.txt`.

## Run the calculator

Open a terminal in the project folder containing `main.py`.

### Windows / PowerShell

```powershell
python main.py
```

### Linux / macOS

```bash
python3 main.py
```

### Example session

```text
Insert free SO2 value (0-80 mg/L): 30
Insert pH value (2.80-4.00): 3.20
Insert temperature (0.0-40.0 °C): 20.0
Insert alcoholic degree (0.00-20.00 %vol): 12.00
Molecular SO2: 1.599 mg/L
```

This is a calculated example using the corrected coefficients, not an experimental reference measurement. Displaying three decimal places does not imply that experimental accuracy is 0.001 mg/L.

## Inputs and formats

All interval endpoints below are included. These are **software input limits**, not independently established scientific validity limits.

| Input | Unit | Accepted interval | Required format | Example |
|---|---|---|---|---|
| `free_so2` | mg/L as SO₂ | 0–80 | Numeric input accepted by Python `float`; use a decimal point | `30` or `30.5` |
| `ph` | Dimensionless | 2.80–4.00 | Exactly two decimal digits | `3.20` |
| `temp` | °C | 0.0–40.0 | Exactly one decimal digit | `20.0` |
| `alc` | % vol | 0.00–20.00 | Exactly two decimal digits | `12.00` |

- Leading and trailing spaces are removed.
- A decimal comma is accepted for pH, temperature and alcohol: `3,20`, `20,0`, `12,00`.
- A decimal comma is **not** converted for free SO₂: use `30.5`, not `30,5`.
- pH, temperature and alcohol reject missing decimals, incorrect decimal counts, an explicit plus sign and scientific notation. Free SO₂ accepts scientific notation if the resulting value is within its interval.
- Ordinary invalid input causes the same field to be requested again.
- Enter alcohol as a percentage, e.g. `12.00` for 12% vol, not `0.12`.

The validation is performed by `control_input()`. Direct calls to the calculation functions do not enforce these intervals.

## Scientific source and equations

The coefficients below are transcribed from [1], page 6 (Equation 1) and page 7 (Equations 2–5), in the supplied *Papers in Press* version published online March 13, 2020.

Let T denote temperature in °C, E denote alcohol content in % vol, and I denote ionic strength, entered numerically in mol/L according to the source convention. The returned concentration uses the same unit as free SO₂, normally mg/L as SO₂.

### Thermodynamic dissociation parameter — Equation 1

$$
pK_T = 0.655664 + 0.0698386T + 0.02015E - 0.000621693T^2
$$

### Ionic correction coefficients — Equations 2 and 3

$$
A = 0.482724 + 0.000883782T + 0.00443752E + 0.00000595973T^2 + 0.0000489638E^2
$$

$$
B = 1.61645 + 0.000935347T + 0.00479931E + 0.00000492357T^2 + 0.0000315093E^2
$$

### Mixed dissociation parameter — Equation 4

$$
pK_M = pK_T - \frac{A\sqrt{I}}{1+B\sqrt{I}}
$$

The default is `ionic_strength = 0.056` mol/L. The article treats this as an assumed typical value and cites a typical wine ionic-strength interval of 0.016–0.100 mol/L (page 7, lines 144–148). This is not a measurement of an individual wine, nor a guarantee that a particular sample lies in that interval.

### Molecular SO₂ — Equation 5

$$
[\mathrm{SO_2}]_{\mathrm{molecular}} = \frac{[\mathrm{SO_2}]_{\mathrm{free}}}{1+10^{\mathrm{pH}-pK_M}}
$$

The article describes the predictive equations as regressions built from tables by Usseglio-Tomasset and Bosia (1984). Those original tables have not yet been independently checked in this project. The supplied prepublication PDF also states that the final published version may contain changes; the final version and any errata have not yet been verified.

## Coefficient corrections

The corrected package makes three changes relative to the earlier implementation:

| Config field | Earlier value | Value printed in [1] | Source |
|---|---|---|---|
| `M2` | `0.00883782` | `0.000883782` | Equation 2 |
| `M3` | `0.004437522` | `0.00443752` | Equation 2 |
| `Q3` | `0.000479931` | `0.00479931` | Equation 3 |

For free SO₂ = 30 mg/L, pH = 3.20, T = 20 °C and alcohol = 12% vol, the earlier implementation gives approximately 1.504 mg/L; the corrected implementation gives approximately 1.599 mg/L. This comparison illustrates a code correction, not experimental validation.

## Code structure

| Component | Purpose |
|---|---|
| `Config` / `CFG` | Immutable dataclass and default instance holding coefficients and ionic strength |
| `control_input()` | Collect and validate interactive inputs; return `(free_so2, ph, temp, alc)` |
| `pKt_quad(temp, alc, cfg=CFG)` | Compute Equation 1 |
| `A_quad(temp, alc, cfg=CFG)` | Compute Equation 2 |
| `B_quad(temp, alc, cfg=CFG)` | Compute Equation 3 |
| `ionic_ratio(temp, alc, cfg=CFG)` | Compute the correction term in Equation 4 |
| `pKm(temp, alc, cfg=CFG)` | Compute Equation 4 |
| `mol_SO2(free_so2, ph, temp, alc, cfg=CFG)` | Compute Equation 5 |
| `main()` | Run the interactive workflow and print the result |

A dataclass groups related values. `frozen=True` prevents normal reassignment of its fields; `slots=True` restricts instance storage. Neither option validates the scientific or numerical suitability of custom values.

### Use from Python

```python
from main import mol_SO2

result = mol_SO2(free_so2=30, ph=3.20, temp=20.0, alc=12.00)
print(f"{result:.3f} mg/L")  # 1.599 mg/L
```

A custom immutable configuration can be created using `dataclasses.replace`:

```python
from dataclasses import replace
from main import CFG, mol_SO2

# Illustrative API usage only; no new sample-specific assumption is introduced.
cfg = replace(CFG, ionic_strength=0.056)
result = mol_SO2(30, 3.20, 20.0, 12.00, cfg=cfg)
```

## Automated tests

Run from the project root, with `tests/`, `pytest.ini` and `requirements-dev.txt` installed alongside `main.py`.

### Windows / PowerShell

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

### Linux / macOS

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -q
```

`pytest` runs the automated checks. A regression test detects changes from a specified expected behavior; it does not by itself establish scientific accuracy.

The corrected package was verified with Python 3.12 and pytest 9.2.0:

```text
157 passed, 3 skipped
```

This records the package verification result, not an automatically updated GitHub CI status.

| Test file | Coverage |
|---|---|
| `tests/test_article_equations.py` | Printed coefficients and independent Decimal evaluation of Equations 1–5, plus the documented example |
| `tests/test_formulas.py` | Individual terms and signs, equation composition, zero ionic strength, algebraic identities, linearity in free SO₂, decreasing output with increasing pH, and Config behavior |
| `tests/test_inputs.py` | All 16 combinations of interactive interval endpoints, invalid formats and out-of-range inputs, repeated prompts, accepted formats and output formatting |
| `tests/test_scientific_pending.py` | Three explicitly skipped placeholders for unresolved scientific validation |

The article-equation checks use Python Decimal arithmetic at 50-digit precision and values transcribed independently of production Config. Their numerical tolerance of `1e-12` concerns floating-point agreement, not measurement uncertainty. Test grids are finite algebraic probes, not proof of validity throughout a continuous domain.

The new article checks were also run against the earlier `main.py`: 28 failed and 15 passed, demonstrating that these checks detect the coefficient discrepancies.

To exclude the pending scientific placeholders:

```bash
python -m pytest -q -m "not scientific"
```

## Scientific limitations and remaining validation

Three scientific topics remain unresolved and are deliberately marked as skipped rather than passed:

1. Whether the assumed ionic strength of 0.056 mol/L is suitable for a specific sample.
2. Agreement with independent experimental measurements of molecular SO₂ across the intended domain.
3. Scientifically supported validity intervals and acceptable experimental errors.

Next steps are to check the original source tables, quantify the regression approximation against those tables, and compare predictions with suitable independent measurements. The calculated pKm values in Table 4 of [1] are not independent experimental measurements of pKm.

The calculator propagates the free-SO₂ concentration supplied by the user. It does not remove analytical bias. The article distinguishes apparent free SO₂ measured by conventional methods from “truly” free SO₂ and discusses overestimation associated with weakly bound forms, particularly in red wines (pages 3–4).

No maximum experimental error or protection threshold is established by this implementation.

## Known implementation limitations

- Calculation functions and custom Config values are not validated. Negative ionic strength, unsuitable custom coefficients or extreme direct inputs may cause errors or invalid results.
- The strict decimal parser uses `str.isdigit()`. Some Unicode characters may pass that check but fail conversion to `float`, which is not caught in the pH, temperature and alcohol loops.
- Input-range enforcement exists only in the interactive workflow.
- Automated checks establish only the behaviors they exercise; they are not a guarantee that all possible inputs are handled.

## References

1. Jenkins, T. W., Howe, P. A., Sacks, G. L., and Waterhouse, A. L. (2020). *Determination of Molecular and “Truly” Free Sulfur Dioxide in Wine: A Comparison of Headspace and Conventional Methods*. American Journal of Enology and Viticulture. DOI: [10.5344/ajev.2020.19052](https://doi.org/10.5344/ajev.2020.19052). Version checked: supplied *Papers in Press* PDF, published online March 13, 2020, particularly pages 6–7, Equations 1–5.
2. [pytest documentation](https://docs.pytest.org/en/stable/) — test execution, parametrization, monkeypatch and skipped tests.
