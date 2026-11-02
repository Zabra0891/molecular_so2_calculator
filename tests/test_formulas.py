"""Regression values describe implementation, not scientific reference data."""
import math
from dataclasses import FrozenInstanceError, replace
from itertools import product
import pytest
import main as m

@pytest.mark.parametrize('name,prefix,terms', [
    ('pKt_quad', 'N', (1, 3, 5, -9)),
    ('A_quad', 'M', (1, 3, 5, 9, 25)),
    ('B_quad', 'Q', (1, 3, 5, 9, 25)),
])
def test_each_coefficient_and_sign(name, prefix, terms):
    zero = {f'{p}{i}': 0.0 for p,n in [('N',4),('M',5),('Q',5)] for i in range(1,n+1)}
    for i, expected in enumerate(terms, 1):
        cfg = replace(m.CFG, **(zero | {f'{prefix}{i}': 1.0}))
        assert getattr(m, name)(3, 5, cfg) == expected

@pytest.mark.parametrize('temp,alc', list(product((0, 10, 20, 30, 40), (0, 5, 10, 15, 20))))
def test_composition_and_zero_ionic_strength(temp, alc):
    root = math.sqrt(0.056)
    correction = m.A_quad(temp, alc)*root/(1+m.B_quad(temp, alc)*root)
    assert m.ionic_ratio(temp, alc) == pytest.approx(correction)
    assert m.pKm(temp, alc) == pytest.approx(m.pKt_quad(temp, alc)-correction)
    assert 0 < correction < m.pKt_quad(temp, alc)
    cfg = replace(m.CFG, ionic_strength=0)
    assert m.ionic_ratio(temp, alc, cfg) == 0
    assert m.pKm(temp, alc, cfg) == m.pKt_quad(temp, alc, cfg)

@pytest.mark.parametrize('temp,alc,ph', list(product((0,20,40),(0,10,20),(2.8,3.4,4))))
def test_molecular_internal_consistency(temp, alc, ph):
    value = m.mol_SO2(40, ph, temp, alc)
    assert math.isfinite(value) and 0 < value < 40
    assert m.mol_SO2(0, ph, temp, alc) == 0
    assert m.mol_SO2(80, ph, temp, alc) == pytest.approx(2*value)
    assert m.mol_SO2(40, ph+0.01, temp, alc) < value
    # Inverse algebraic identity for the implemented final equation.
    assert math.log10(40/value-1) == pytest.approx(ph-m.pKm(temp,alc))

@pytest.mark.parametrize('temp,alc', list(product((0,20,40),(0,10,20))))
def test_half_fraction_at_ph_equal_pkm(temp, alc):
    # Algebraic probe outside the interactive pH interval, not an enological claim.
    assert m.mol_SO2(40,m.pKm(temp,alc),temp,alc) == 20

def test_config_immutable_and_custom_config_propagates():
    cfg = m.Config()
    with pytest.raises(FrozenInstanceError):
        cfg.N1 = 0
    assert not hasattr(cfg, '__dict__')
    custom = replace(cfg, N1=cfg.N1+1)
    before = m.mol_SO2(40,3.2,20,10)
    after = m.mol_SO2(40,3.2,20,10,custom)
    assert after > before
    assert m.pKm(20,10,custom) == pytest.approx(m.pKm(20,10)+1)
    assert m.CFG == cfg


