import math
from k_theory_engine import analyse_formula, skeletal_number, group_valence_electrons, VALIDATION_EXAMPLES


def test_periodic_table_known_values():
    assert skeletal_number('Rh') == 4.5
    assert skeletal_number('Os') == 5.0
    assert skeletal_number('Au') == 3.5
    assert skeletal_number('B') == 2.5
    assert skeletal_number('C') == 2.0
    assert skeletal_number('O') == 1.0
    assert skeletal_number('Cl') == 0.5
    assert skeletal_number('Ne') == 0.0
    assert group_valence_electrons('Rh') == 9
    assert group_valence_electrons('C') == 4


def test_validation_examples():
    for formula,exp in VALIDATION_EXAMPLES.items():
        r=analyse_formula(formula)
        assert math.isclose(r.K,exp['K'])
        assert r.n==exp['n']
        assert math.isclose(r.q,exp['q'])
        assert math.isclose(r.cve,exp['cve'])
        assert r.family==exp['family']


def test_os_capping():
    r=analyse_formula('Os10(CO)26^2-')
    assert r.y==4
    assert r.z==6
    assert r.Kp=='C^4C[M6]'
    assert r.Kstar=='C^4 + D^6'
    assert r.VE0==14


def test_closo_configuration():
    r=analyse_formula('Rh6(CO)16')
    assert 'octahedron' in r.primary_configuration.lower()


def test_carborane():
    r=analyse_formula('C2B10H12')
    assert r.K_n=='23(12)'
    assert r.series4=='4n+2'
    assert r.direct_valence_e==50
