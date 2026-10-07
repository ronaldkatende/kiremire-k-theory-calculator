# Kiremire K-Theory Structural Calculator — Version 1

**Theory:** Prof. Enos M. R. Kiremire  
**Computational implementation:** Ronald Katende

Version 1 is intentionally simple. A user enters a chemical formula and the program prominently returns:

1. **Cluster valence electrons (CVE / VE)**
2. **Number of skeletal bonds/linkages, K**
3. **Possible structural configuration(s)**

The detailed panel then shows K(n), q, 4n+q / 14n+q series, family/clan, capping descriptors Kp and K*, nucleus/cap counts, VE0 and the six CVE equations when applicable.

## Run on Windows

Double-click `run_windows.bat`, or open Anaconda Prompt in this folder and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Main examples

- `Rh6(CO)16`
- `Os10(CO)26^2-`
- `B6H6^2-`
- `B5H9`
- `C2B10H12`
- `Fe2Co2(CO)12`
- `Pd35(CO)23L15`

## Periodic table

The app includes a K-theory periodic table organized around:

- valence-electron count `G`;
- skeletal number `K`;
- skeletal valence `V=2K`.

Atomic numbers are deliberately omitted because the implemented K rules are valence-based. The main-group and d-block pattern is taken from Kiremire's published tables. Hydrogen is shown as elemental `K=0.5`, consistent with Kiremire's later explanation; when hydrogen acts as a ligand its contribution is `K=-0.5`.

The software recognizes every current chemical element symbol. The f-block is visibly marked **author rule needed** because the published table used for this implementation does not supply a single general K assignment for every lanthanide/actinide. Version 1 therefore refuses to invent these values; Professor Kiremire can enter them through the Advanced review page.

## Important boundary

This is **Phase I: faithful computationalization**. It does not claim that K-theory alone proves chemical stability, synthesis feasibility, pharmaceutical activity, or a unique 3D structure. New inverse-design, prediction and commercialization algorithms should be developed as a separate research extension and clearly attributed as such.

## Deploy as a website from GitHub

This folder is GitHub/Streamlit-ready. Upload its contents to a GitHub repository, then deploy `app.py` with Streamlit Community Cloud. See `DEPLOY_STREAMLIT.md` for the exact steps.

No passwords, API keys, databases, or external services are required for Version 1.
