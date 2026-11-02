from itertools import product
import pytest
import main as m

DEFAULT = ['40', '3.20', '20.0', '11.50']

def feed(monkeypatch, tokens):
    values = iter(tokens)
    calls = []
    def fake_input(prompt):
        calls.append(prompt)
        try:
            return next(values)
        except StopIteration:
            pytest.fail('Unexpected extra input request')
    monkeypatch.setattr('builtins.input', fake_input)
    return calls

@pytest.mark.parametrize('tokens', list(product(('0','80'),('2.80','4.00'),('0.0','40.0'),('0.00','20.00'))))
def test_all_inclusive_corners(monkeypatch, tokens):
    calls = feed(monkeypatch, tokens)
    assert m.control_input() == tuple(map(float,tokens))
    assert len(calls) == 4

@pytest.mark.parametrize('index,raw', [
    (0,'abc'),(0,'-0.01'),(0,'80.01'),(0,'nan'),(0,'inf'),(0,'-inf'),(0,'12,5'),
    (1,'2.79'),(1,'4.01'),(1,'3'),(1,'3.2'),(1,'3.200'),(1,'+3.20'),
    (1,'3.2e0'),(1,'3..20'),(1,'nan'),(1,''),
    (2,'-0.1'),(2,'40.1'),(2,'20'),(2,'20.00'),(2,'2e1'),(2,'inf'),
    (3,'-0.01'),(3,'20.01'),(3,'11'),(3,'11.5'),(3,'11.500'),(3,'nan'),
])
def test_invalid_token_reprompts_same_field(monkeypatch,capsys,index,raw):
    tokens = DEFAULT.copy()
    tokens.insert(index,raw)
    calls = feed(monkeypatch,tokens)
    assert m.control_input() == (40,3.2,20,11.5)
    assert len(calls) == 5 and calls[index] == calls[index+1]
    assert capsys.readouterr().out.strip()

@pytest.mark.parametrize('tokens,expected', [
    ([' 40 ',' 3,20 ',' 20,0 ',' 11,50 '], (40,3.2,20,11.5)),
    (['4e1','03.20','020.0','011.50'], (40,3.2,20,11.5)),
    (['12.5','3.20','20.0','11.50'], (12.5,3.2,20,11.5)),
])
def test_current_accepted_formats(monkeypatch,tokens,expected):
    feed(monkeypatch,tokens)
    assert m.control_input() == expected

def test_main_output(monkeypatch,capsys):
    feed(monkeypatch,DEFAULT)
    m.main()
    expected = m.mol_SO2(40,3.2,20,11.5)
    assert capsys.readouterr().out == f'Molecular SO2: {expected:.3f} mg/L\n'
