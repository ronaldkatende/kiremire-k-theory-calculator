from pathlib import Path
import math
import pandas as pd
import streamlit as st

from k_theory_engine import (
    analyse_formula, analyse_components, parse_formula, Component,
    periodic_table_records, same_k_elements, theory_atlas,
    VALIDATION_EXAMPLES, LIGANDS, _fmt
)

st.set_page_config(
    page_title="Kiremire K-Theory Structural Calculator",
    page_icon="⚛",
    layout="wide"
)

import streamlit as st

st.set_page_config(
    page_title="Kiremire K-Theory Structural Calculator",
    page_icon="⚛",
    layout="wide"
)

st.markdown("""
<style>

/* Main body text */
.stApp {
    font-size: 51px;
}

p, li, div {
    font-size: 51px;
    line-height: 1.55;
}

/* Main title */
h1 {
    font-size: 92px !important;
    line-height: 1.15 !important;
}

/* Section headings */
h2 {
    font-size: 72px !important;
}

h3 {
    font-size: 58px !important;
}

/* Input labels */
label,
[data-testid="stWidgetLabel"] p {
    font-size: 44px !important;
    font-weight: 600 !important;
}

/* Text input */
input {
    font-size: 48px !important;
    min-height: 52px !important;
}

/* Buttons */
.stButton > button {
    font-size: 46px !important;
    font-weight: 600 !important;
    min-height: 54px !important;
    padding: 0.6rem 1.4rem !important;
}

/* Result labels */
[data-testid="stMetricLabel"] p {
    font-size: 42px !important;
    font-weight: 600 !important;
}

/* Result values */
[data-testid="stMetricValue"] {
    font-size: 72px !important;
    font-weight: 700 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 44px !important;
}

/* Expanders */
[data-testid="stExpander"] summary {
    font-size: 42px !important;
    font-weight: 600 !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    font-size: 34px !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {max-width: 1220px; padding-top: 1.7rem;}
.hero {border-bottom: 1px solid #bbb; padding-bottom: 0.7rem; margin-bottom: 1rem;}
.hero h1 {font-size: 2.05rem; margin-bottom: .15rem;}
.hero p {margin: .15rem 0; color:#444;}
.kcard {border:1px solid #c9c9c9; border-radius:7px; padding:16px 16px 13px 16px; min-height:145px; background:white;}
.kcard .head {font-size:.82rem; text-transform:uppercase; letter-spacing:.04em; color:#555; margin-bottom:.45rem;}
.kcard .value {font-size:2rem; font-weight:700; line-height:1.05; color:#111;}
.kcard .sub {font-size:.9rem; color:#555; margin-top:.55rem;}
.simple-note {border-left:3px solid #555; padding:.55rem .8rem; background:#f7f7f7;}
.smallcaps {font-size:.82rem; text-transform:uppercase; letter-spacing:.04em; color:#555;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>Kiremire K-Theory Structural Calculator — Version 1</h1>
<p><b>Theory:</b> Prof. Enos M. R. Kiremire &nbsp; | &nbsp; <b>Computational implementation:</b> Ronald Katende</p>
<p>Enter a formula. The calculator returns three outputs, i.e., <b>valence electrons, skeletal bonds/linkages, and possible structural configurations</b>.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Version 1 scope")
    st.write("Faithful computationalization first: formula → valence electrons → K linkages → K(n)/series → possible configurations.")
    st.caption("The research extension—new inverse design, prediction, industrial screening and commercialization—is deliberately kept outside Version 1.")
    st.divider()
    st.markdown("**Quick examples**")
    st.code("Rh6(CO)16\nOs10(CO)26^2-\nB6H6^2-\nB5H9\nC2B10H12\nFe2Co2(CO)12\nPd35(CO)23L15")

main, periodic, atlas, validation, advanced = st.tabs([
    "Formula → 3 answers", "K-Theory periodic table", "Theory coverage",
    "Validation examples", "Advanced review"
])


def result_cards(r):
    c1,c2,c3=st.columns([1,1,1.4])
    c1.markdown(f"""<div class="kcard"><div class="head">1 · Cluster valence electrons</div><div class="value">{_fmt(r.cve)}</div><div class="sub">CVE / VE derived from K-theory bookkeeping</div></div>""",unsafe_allow_html=True)
    c2.markdown(f"""<div class="kcard"><div class="head">2 · Skeletal bonds / linkages</div><div class="value">K = {_fmt(r.K)}</div><div class="sub">K(n) = {r.K_n}; K is the skeletal-linkage number</div></div>""",unsafe_allow_html=True)
    cfg=r.primary_configuration or "Requires author review"
    c3.markdown(f"""<div class="kcard"><div class="head">3 · Possible configuration(s)</div><div class="value" style="font-size:1.35rem">{cfg}</div><div class="sub">Family: {r.family or '—'}; series: {r.series4 or '—'}</div></div>""",unsafe_allow_html=True)


def detail_panel(r):
    st.markdown("### K-theory descriptors")
    cols=st.columns(7)
    vals=[("n",r.n),("K(n)",r.K_n),("q",_fmt(r.q)),("4n+q",r.series4),("14n+q",r.series14 or "—"),("Family",r.family),("VE₀",_fmt(r.VE0))]
    for col,(lab,val) in zip(cols,vals): col.metric(lab,val if val is not None else "—")

    if r.Kp or r.Kstar:
        a,b,c,d=st.columns(4)
        a.metric("caps y",_fmt(r.y)); b.metric("nucleus z",_fmt(r.z)); c.metric("Kp",r.Kp or "—"); d.metric("K*",r.Kstar or "—")

    st.markdown("### Possible configurations")
    for x in r.configurations:
        st.write("• "+x)

    with st.expander("Show the calculation", expanded=False):
        for i,s in enumerate(r.steps,1): st.write(f"{i}. {s}")
        if r.direct_valence_e is not None:
            st.write(f"**Independent formula-electron cross-check:** {_fmt(r.direct_valence_e)} electrons.")

    with st.expander("Six cluster-valence-electron equations", expanded=False):
        df=pd.DataFrame(r.six_equations)
        df["Value"]=df["Value"].apply(lambda x:"—" if x is None or (isinstance(x,float) and math.isnan(x)) else _fmt(x))
        st.dataframe(df,width="stretch",hide_index=True)

    with st.expander("Which parts of Kiremire's theory this analysis touches", expanded=False):
        st.write(" · ".join(r.theory_modules))

    if r.warnings:
        st.warning("\n\n".join(r.warnings))


with main:
    st.markdown("### Enter the chemical formula")
    p1,p2=st.columns([3,1])
    formula=p1.text_input("Formula",value="Rh6(CO)16",placeholder="e.g. Rh6(CO)16",label_visibility="collapsed")
    go=p2.button("Analyse formula",type="primary",width="stretch")
    st.caption("Charges may be written as ^2-, 2-, + or -. Common Kiremire ligands such as CO, H, L, Cp/Cp*, phosphines and halides are supported.")

    if go or "last_formula" not in st.session_state:
        try:
            st.session_state["analysis"]=analyse_formula(formula)
            st.session_state["last_formula"]=formula
        except Exception as e:
            st.session_state["analysis_error"]=str(e)
    elif formula != st.session_state.get("last_formula"):
        pass

    if st.session_state.get("last_formula")==formula and "analysis" in st.session_state:
        r=st.session_state["analysis"]
        if r.K is None:
            st.error("This formula contains a component whose K value is not yet fixed in the published rule set used by Version 1. Open Advanced review to supply Professor Kiremire's value.")
            if r.warnings: st.warning("\n\n".join(r.warnings))
        else:
            result_cards(r)
            st.markdown("<br>",unsafe_allow_html=True)
            detail_panel(r)
    elif "analysis_error" in st.session_state:
        st.error(st.session_state["analysis_error"])

    st.divider()
    st.markdown("### What the three outputs mean")
    st.markdown("""
<div class="simple-note">
<b>Valence electrons</b> give the cluster electron count. <b>K</b> is the skeletal-linkage/bond number extracted from the formula. <b>Possible configurations</b> are inferred from K(n), the 4n+q family and, where relevant, the capping/nucleus descriptors. The calculator does not pretend that K(n) always fixes one unique three-dimensional isomer.
</div>
""",unsafe_allow_html=True)

with periodic:
    st.markdown("### K-Theory periodic table")
    st.write("This view is deliberately organized around **valence electrons, skeletal number K and skeletal valence V=2K**. Atomic numbers are not used in the calculations or shown in the table.")
    img=Path(__file__).parent/"assets"/"k_theory_periodic_table.png"
    st.image(str(img),width="stretch")
    st.caption("Main-group and d-block K values follow the published skeletal-number pattern. H is treated as K=0.5 as an element; when H acts as a ligand its contribution is K=-0.5. f-block entries remain marked for Professor Kiremire's author-confirmed rule rather than being invented by the software.")

    df=pd.DataFrame(periodic_table_records())
    c1,c2=st.columns([1,2])
    element=c1.selectbox("Inspect an element",df["Element"].tolist(),index=df["Element"].tolist().index("Rh"))
    rec=df[df["Element"]==element].iloc[0]
    c2.dataframe(pd.DataFrame([rec]),width="stretch",hide_index=True)
    if isinstance(rec["K"],(int,float)):
        same=same_k_elements(float(rec["K"]))
        st.write(f"**Same-K elements (K={rec['K']}):** "+", ".join(x["Element"] for x in same))

with atlas:
    st.markdown("### Major strands of Professor Kiremire's K-theory represented in Version 1")
    st.dataframe(pd.DataFrame(theory_atlas()),width="stretch",hide_index=True)
    st.info("Version 1 computationalizes the published arithmetic, categorization and structural constraints. Exact graph-isomer enumeration, fully automatic Matryoshka placement, and new inverse-design algorithms are reserved for the next research phase unless Professor Kiremire provides an explicit rule that makes them deterministic.")

with validation:
    st.markdown("### Regression examples")
    st.write("These examples are used to check that the implementation reproduces the expected K-theory arithmetic.")
    rows=[]
    for formula,exp in VALIDATION_EXAMPLES.items():
        try:
            r=analyse_formula(formula)
            ok=(abs(r.K-exp['K'])<1e-9 and r.n==exp['n'] and abs(r.q-exp['q'])<1e-9 and abs(r.cve-exp['cve'])<1e-9)
            rows.append({"Formula":formula,"K":_fmt(r.K),"n":r.n,"q":_fmt(r.q),"CVE":_fmt(r.cve),"Family":r.family,"Status":"PASS" if ok else "CHECK"})
        except Exception as e:
            rows.append({"Formula":formula,"Status":"ERROR: "+str(e)})
    st.dataframe(pd.DataFrame(rows),width="stretch",hide_index=True)

    st.markdown("### One-click demonstration")
    demo=st.selectbox("Example",list(VALIDATION_EXAMPLES),index=0)
    r=analyse_formula(demo)
    result_cards(r)

with advanced:
    st.markdown("### Advanced component review")
    st.write("The front page is intentionally simple. This page exists so Professor Kiremire can correct an unusual fragment, ligand, f-block element or interstitial atom without changing the program.")
    af=st.text_input("Formula to decompose",value="Rh6(CO)16",key="advanced_formula")
    try:
        comps,charge,warns=parse_formula(af)
        df=pd.DataFrame([c.__dict__ for c in comps])
        ed=st.data_editor(df,num_rows="dynamic",width="stretch",hide_index=True,
            column_config={
                "count":st.column_config.NumberColumn("count",min_value=0,step=1),
                "role":st.column_config.SelectboxColumn("role",options=["skeleton","ligand","manual"]),
                "k_per_unit":st.column_config.NumberColumn("K/unit",step=0.5,format="%.2f"),
                "target_e":st.column_config.NumberColumn("target e",step=1),
                "valence_e_per_unit":st.column_config.NumberColumn("valence e/unit",step=0.5),
            })
        charge=int(st.number_input("Signed charge",value=int(charge),step=1))
        if st.button("Recalculate reviewed components",type="primary"):
            data=[]
            for row in ed.to_dict("records"):
                # pandas may turn blank numerics into nan: normalize to None.
                for key in ["k_per_unit","target_e","valence_e_per_unit"]:
                    v=row.get(key)
                    if v is not None and isinstance(v,float) and math.isnan(v): row[key]=None
                data.append(Component(**row))
            rr=analyse_components(af,data,charge,warns)
            if rr.K is None: st.error("At least one K/unit value is still missing.")
            else:
                result_cards(rr); detail_panel(rr)
    except Exception as e:
        st.error(str(e))

st.divider()
st.caption("Version 1 is a computational implementation of Professor Kiremire's published K-theory relationships. It does not claim quantum-chemical stability, synthesis feasibility, biological activity or a unique 3D isomer where the K-theory constraints permit alternatives.")
