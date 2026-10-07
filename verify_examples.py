from k_theory_engine import analyse_formula, VALIDATION_EXAMPLES, periodic_table_records

ok=0
print('KIREMIRE K-THEORY STRUCTURAL CALCULATOR — VERSION 1')
print('Validation run')
print('-'*72)
for f,e in VALIDATION_EXAMPLES.items():
    r=analyse_formula(f)
    passed=(abs(r.K-e['K'])<1e-9 and r.n==e['n'] and abs(r.q-e['q'])<1e-9 and abs(r.cve-e['cve'])<1e-9 and r.family==e['family'])
    ok+=int(passed)
    print(f"{f:24s} K={r.K:g} n={r.n} q={r.q:g} VE={r.cve:g} {r.family:14s} {'PASS' if passed else 'CHECK'}")
print('-'*72)
print(f'{ok}/{len(VALIDATION_EXAMPLES)} regression examples passed.')
print(f'{len(periodic_table_records())} periodic-table element symbols represented.')
