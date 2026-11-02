"""Transcription checks, NOT experimental validation.
Source: uploaded Papers in Press Jenkins et al., DOI 10.5344/ajev.2020.19052,
p.6 Eq.1; p.7 Eqs.2-5 and lines 144-148.
Expected values are recalculated from printed equations using Decimal,
never obtained from production Config or production functions.
Grid boundaries are algebraic probes, not scientifically validated limits.
"""
from decimal import Decimal as D, localcontext
from itertools import product
import pytest
import main as m

COEFFICIENTS = {
    'N1':'0.655664', 'N2':'0.0698386', 'N3':'0.02015', 'N4':'0.000621693',
    'M1':'0.482724', 'M2':'0.000883782', 'M3':'0.00443752',
    'M4':'0.00000595973', 'M5':'0.0000489638',
    'Q1':'1.61645', 'Q2':'0.000935347', 'Q3':'0.00479931',
    'Q4':'0.00000492357', 'Q5':'0.0000315093', 'ionic_strength':'0.056',
}

@pytest.mark.parametrize('name,printed', list(COEFFICIENTS.items()))
def test_config_matches_printed_article(name,printed):
    assert getattr(m.CFG,name) == float(printed)

def article_reference(free,ph,temp,alc):
    with localcontext() as ctx:
        ctx.prec=50
        f,h,t,a=map(lambda x:D(str(x)),(free,ph,temp,alc))
        pk=D('.655664')+D('.0698386')*t+D('.02015')*a-D('.000621693')*t*t
        aa=D('.482724')+D('.000883782')*t+D('.00443752')*a+D('.00000595973')*t*t+D('.0000489638')*a*a
        bb=D('1.61645')+D('.000935347')*t+D('.00479931')*a+D('.00000492357')*t*t+D('.0000315093')*a*a
        root=D('.056').sqrt()
        ratio=aa*root/(1+bb*root)
        km=pk-ratio
        mol=f/(1+D(10)**(h-km))
        return tuple(map(float,(pk,aa,bb,ratio,km,mol)))

@pytest.mark.parametrize('temp,alc,ph',list(product((0,20,40),(0,10,20),(2.8,3.2,4))))
def test_equations_1_to_5_against_article(temp,alc,ph):
    expected=article_reference(40,ph,temp,alc)
    actual=(m.pKt_quad(temp,alc),m.A_quad(temp,alc),m.B_quad(temp,alc),
            m.ionic_ratio(temp,alc),m.pKm(temp,alc),m.mol_SO2(40,ph,temp,alc))
    # Numerical agreement only; no claim about experimental uncertainty.
    assert actual == pytest.approx(expected,rel=1e-12,abs=1e-12)

def test_documented_example():
    assert m.mol_SO2(30,3.2,20,12) == pytest.approx(1.5990314672451933,rel=1e-12)
