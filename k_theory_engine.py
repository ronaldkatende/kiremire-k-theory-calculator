from __future__ import annotations

from dataclasses import dataclass, asdict
import math
import re
from typing import Iterable

# -----------------------------------------------------------------------------
# Kiremire-style skeletal-number periodic table
# -----------------------------------------------------------------------------
# Published table pattern (Kiremire 2019):
# d-block groups 3..12: K = (18-G)/2, skeletal valence V=2K
# main-group groups 1,2,13..18: K = (8-Gv)/2, V=2K
# Atomic number is deliberately not used by the calculator.
# f-block values are not assigned here because the published table used for
# validation does not provide a single unambiguous general value for each.

# symbol, period, group, block
_ELEMENT_ROWS = [
    ("H",1,1,"s"),("He",1,18,"p"),
    ("Li",2,1,"s"),("Be",2,2,"s"),("B",2,13,"p"),("C",2,14,"p"),("N",2,15,"p"),("O",2,16,"p"),("F",2,17,"p"),("Ne",2,18,"p"),
    ("Na",3,1,"s"),("Mg",3,2,"s"),("Al",3,13,"p"),("Si",3,14,"p"),("P",3,15,"p"),("S",3,16,"p"),("Cl",3,17,"p"),("Ar",3,18,"p"),
    ("K",4,1,"s"),("Ca",4,2,"s"),("Sc",4,3,"d"),("Ti",4,4,"d"),("V",4,5,"d"),("Cr",4,6,"d"),("Mn",4,7,"d"),("Fe",4,8,"d"),("Co",4,9,"d"),("Ni",4,10,"d"),("Cu",4,11,"d"),("Zn",4,12,"d"),("Ga",4,13,"p"),("Ge",4,14,"p"),("As",4,15,"p"),("Se",4,16,"p"),("Br",4,17,"p"),("Kr",4,18,"p"),
    ("Rb",5,1,"s"),("Sr",5,2,"s"),("Y",5,3,"d"),("Zr",5,4,"d"),("Nb",5,5,"d"),("Mo",5,6,"d"),("Tc",5,7,"d"),("Ru",5,8,"d"),("Rh",5,9,"d"),("Pd",5,10,"d"),("Ag",5,11,"d"),("Cd",5,12,"d"),("In",5,13,"p"),("Sn",5,14,"p"),("Sb",5,15,"p"),("Te",5,16,"p"),("I",5,17,"p"),("Xe",5,18,"p"),
    ("Cs",6,1,"s"),("Ba",6,2,"s"),("La",6,3,"d"),
    ("Ce",6,None,"f"),("Pr",6,None,"f"),("Nd",6,None,"f"),("Pm",6,None,"f"),("Sm",6,None,"f"),("Eu",6,None,"f"),("Gd",6,None,"f"),("Tb",6,None,"f"),("Dy",6,None,"f"),("Ho",6,None,"f"),("Er",6,None,"f"),("Tm",6,None,"f"),("Yb",6,None,"f"),("Lu",6,3,"d"),
    ("Hf",6,4,"d"),("Ta",6,5,"d"),("W",6,6,"d"),("Re",6,7,"d"),("Os",6,8,"d"),("Ir",6,9,"d"),("Pt",6,10,"d"),("Au",6,11,"d"),("Hg",6,12,"d"),("Tl",6,13,"p"),("Pb",6,14,"p"),("Bi",6,15,"p"),("Po",6,16,"p"),("At",6,17,"p"),("Rn",6,18,"p"),
    ("Fr",7,1,"s"),("Ra",7,2,"s"),("Ac",7,3,"d"),
    ("Th",7,None,"f"),("Pa",7,None,"f"),("U",7,None,"f"),("Np",7,None,"f"),("Pu",7,None,"f"),("Am",7,None,"f"),("Cm",7,None,"f"),("Bk",7,None,"f"),("Cf",7,None,"f"),("Es",7,None,"f"),("Fm",7,None,"f"),("Md",7,None,"f"),("No",7,None,"f"),("Lr",7,None,"f"),
    ("Rf",7,4,"d"),("Db",7,5,"d"),("Sg",7,6,"d"),("Bh",7,7,"d"),("Hs",7,8,"d"),("Mt",7,9,"d"),("Ds",7,10,"d"),("Rg",7,11,"d"),("Cn",7,12,"d"),("Nh",7,13,"p"),("Fl",7,14,"p"),("Mc",7,15,"p"),("Lv",7,16,"p"),("Ts",7,17,"p"),("Og",7,18,"p"),
]

ELEMENTS = {s:{"symbol":s,"period":p,"group":g,"block":b} for s,p,g,b in _ELEMENT_ROWS}


def group_valence_electrons(symbol: str) -> int | None:
    info = ELEMENTS.get(symbol)
    if not info or info["group"] is None:
        return None
    g = int(info["group"])
    if symbol == "H":
        return 1
    if symbol == "He":
        return 2
    if info["block"] == "d":
        return g
    if g in (1,2):
        return g
    if 13 <= g <= 18:
        return g - 10
    return None


def skeletal_number(symbol: str) -> float | None:
    info = ELEMENTS.get(symbol)
    if not info:
        return None
    gv = group_valence_electrons(symbol)
    if gv is None:
        return None
    if symbol in {"H","He"}:
        target = 2
    else:
        target = 18 if info["block"] == "d" else 8
    return (target - gv) / 2.0


def skeletal_valence(symbol: str) -> float | None:
    k = skeletal_number(symbol)
    return None if k is None else 2.0*k


def periodic_table_records() -> list[dict]:
    out=[]
    for s,p,g,b in _ELEMENT_ROWS:
        gv=group_valence_electrons(s)
        k=skeletal_number(s)
        out.append({
            "Element":s,"Period":p,"Group":g if g is not None else "f-block",
            "Block":b,"Valence e (G)":gv if gv is not None else "—",
            "K":k if k is not None else "—",
            "Skeletal valence V=2K":skeletal_valence(s) if k is not None else "—",
            "Target shell":(2 if s in {"H","He"} else (18 if b=="d" else (8 if b in {"s","p"} else "author rule needed"))),
        })
    return out

# -----------------------------------------------------------------------------
# Ligand/fragments in the neutral/covalent bookkeeping used in the papers.
# K contribution = -(donated electrons)/2.
# -----------------------------------------------------------------------------
LIGANDS = {
    "CO": (2.0, "2e carbonyl donor"),
    "L": (2.0, "generic 2e ligand L"),
    "PR3": (2.0, "phosphine-type 2e donor"),
    "PPh3": (2.0, "triphenylphosphine-type 2e donor"),
    "NH3": (2.0, "2e donor"),
    "H2O": (2.0, "2e donor"),
    "H": (1.0, "1e H contribution in neutral/covalent counting"),
    "F": (1.0, "1e X-type contribution"),
    "Cl": (1.0, "1e X-type contribution"),
    "Br": (1.0, "1e X-type contribution"),
    "I": (1.0, "1e X-type contribution"),
    "CN": (1.0, "default X-type 1e contribution; binding mode can require review"),
    "Cp": (5.0, "5e Cp contribution in neutral counting"),
    "Cp*": (5.0, "5e Cp* contribution in neutral counting"),
    "C5H5": (5.0, "Cp-like 5e contribution"),
    "C2H4": (2.0, "simple eta2 alkene 2e contribution"),
    "NO": (3.0, "default 3e neutral NO; geometry/charge can change counting"),
    "bz": (6.0, "benzene-type 6e donor"),
    # Interstitial atoms in parentheses can be treated as electron donors.
    "(C)": (4.0, "parenthesized interstitial carbon: 4e contribution"),
    "(B)": (3.0, "parenthesized interstitial boron: 3e contribution"),
    "(N)": (5.0, "parenthesized interstitial nitrogen: 5e contribution"),
}

@dataclass
class Component:
    label: str
    count: int
    role: str                 # skeleton / ligand / manual
    k_per_unit: float | None
    target_e: int | None      # 18 or 8 for skeletal atoms
    valence_e_per_unit: float | None
    note: str = ""
    confidence: str = "high"

@dataclass
class Analysis:
    formula: str
    charge: int
    components: list[dict]
    n: int | None
    K: float | None
    q: float | None
    cve: float | None
    direct_valence_e: float | None
    series4: str | None
    series14: str | None
    family: str | None
    bonds_label: str | None
    configurations: list[str]
    primary_configuration: str | None
    K_n: str | None
    y: float | None
    z: float | None
    Kp: str | None
    Kstar: str | None
    VE0: float | None
    six_equations: list[dict]
    theory_modules: list[str]
    warnings: list[str]
    steps: list[str]


def _fmt(x: float | int | None) -> str:
    if x is None:
        return "—"
    if abs(float(x)-round(float(x))) < 1e-9:
        return str(int(round(float(x))))
    return f"{float(x):g}"


def _strip_charge(text: str) -> tuple[str,int]:
    s = re.sub(r"\s+","",text).replace("−","-").replace("⁻","-").replace("⁺","+")
    if not s:
        raise ValueError("Please enter a chemical formula.")
    # Parenthesized terminal charge first, then conventional ^2-, 2-, +, -.
    pats=[r"\((\d*)([+-])\)$",r"\^?(\d*)([+-])$"]
    for pat in pats:
        m=re.search(pat,s)
        if m:
            mag=int(m.group(1)) if m.group(1) else 1
            q=mag if m.group(2)=="+" else -mag
            return s[:m.start()],q
    return s,0


def _element_component(sym: str, count: int, *, has_transition: bool) -> tuple[Component,list[str]]:
    warnings=[]
    info=ELEMENTS.get(sym)
    if info is None:
        raise ValueError(f"Unknown element symbol '{sym}'.")

    if sym == "H":
        return Component("H",count,"ligand",-0.5,None,1.0,"H contributes 1e; K/unit=-0.5"),warnings

    k=skeletal_number(sym)
    gv=group_valence_electrons(sym)
    if info["block"] == "f":
        warnings.append(f"{sym}: the published skeletal-number table used here does not assign a single automatic f-block K value. Use the advanced component editor if Professor Kiremire supplies one.")
        return Component(sym,count,"manual",None,18,gv,"f-block value requires Professor Kiremire's rule","review"),warnings

    # In a mixed transition-metal formula, bare main-group atoms can be either
    # skeletal or interstitial. Default to skeletal, but expose the assumption.
    if has_transition and info["block"] in {"s","p"} and sym not in {"H"}:
        warnings.append(f"{sym}: treated as a main-group skeletal atom. If it is interstitial/ligand-like in this formula, change its role in Advanced review.")

    target=18 if info["block"]=="d" else 8
    return Component(sym,count,"skeleton",k,target,gv,
                     f"K=({target}-{gv})/2 from the published skeletal-number pattern"),warnings


def _parse_plain_segment(seg: str, *, has_transition: bool) -> tuple[list[Component],list[str]]:
    comps=[]; warnings=[]; pos=0
    # ligand placeholders before element parsing
    token_re=re.compile(r"(Cp\*|Cp|PPh3|PR3|NH3|H2O|C2H4|CN|NO|bz|L)(\d*)|([A-Z][a-z]?)(\d*)")
    while pos < len(seg):
        m=token_re.match(seg,pos)
        if not m:
            raise ValueError(f"Cannot parse formula near '{seg[pos:]}'. Use Advanced review for unusual notation.")
        if m.group(1):
            lig=m.group(1); cnt=int(m.group(2) or 1)
            donation,note=LIGANDS[lig]
            comps.append(Component(lig,cnt,"ligand",-donation/2,None,donation,note,
                                   "review" if lig in {"NO","CN"} else "high"))
        else:
            sym=m.group(3); cnt=int(m.group(4) or 1)
            c,w=_element_component(sym,cnt,has_transition=has_transition)
            comps.append(c); warnings.extend(w)
        pos=m.end()
    return comps,warnings


def parse_formula(text: str) -> tuple[list[Component],int,list[str]]:
    core,charge=_strip_charge(text)
    warnings=[]

    # Detect whether transition metals appear anywhere in elemental text.
    syms=re.findall(r"[A-Z][a-z]?", core)
    has_transition=any(s in ELEMENTS and ELEMENTS[s]["block"]=="d" for s in syms)

    comps: list[Component]=[]
    # Simple non-nested parenthetical groups.
    groups=[]
    def repl(m):
        groups.append((m.group(1),int(m.group(2) or 1)))
        return ""
    outside=re.sub(r"\(([A-Za-z0-9*]+)\)(\d*)",repl,core)
    if "(" in outside or ")" in outside:
        raise ValueError("Nested/unrecognized parentheses are not handled by the simple formula parser. Use Advanced review.")

    # Outside atoms / ligands.
    oc,ow=_parse_plain_segment(outside,has_transition=has_transition)
    comps.extend(oc);warnings.extend(ow)

    # Parenthetical groups are usually ligands/fragments in the work being automated.
    for g,cnt in groups:
        key=f"({g})"
        if g in LIGANDS:
            donation,note=LIGANDS[g]
            comps.append(Component(f"({g})",cnt,"ligand",-donation/2,None,donation,note,
                                   "review" if g in {"NO","CN"} else "high"))
        elif key in LIGANDS:
            donation,note=LIGANDS[key]
            comps.append(Component(key,cnt,"ligand",-donation/2,None,donation,note))
        else:
            # If group is elemental, estimate neutral donation from group valence sum.
            try:
                inner,iw=_parse_plain_segment(g,has_transition=False)
                if all(x.valence_e_per_unit is not None for x in inner):
                    donated=sum(float(x.valence_e_per_unit)*x.count for x in inner)
                    comps.append(Component(f"({g})",cnt,"ligand",-donated/2,None,donated,
                                           "Parenthesized fragment treated as electron donor; verify if skeletal." ,"review"))
                    warnings.append(f"({g}) was treated as a ligand/interstitial fragment donating {donated:g}e per group; verify this role.")
                else:
                    raise ValueError
            except Exception:
                comps.append(Component(f"({g})",cnt,"manual",None,None,None,
                                       "Unknown parenthetical fragment; enter K/unit in Advanced review","review"))
                warnings.append(f"({g}) requires manual K/electron assignment.")
    return comps,charge,warnings


def family_from_q(q: float) -> str:
    # Integer-even values are canonical 4n+q families.
    if abs(q-2)<1e-9: return "closo"
    if abs(q-4)<1e-9: return "nido"
    if abs(q-6)<1e-9: return "arachno"
    if abs(q-8)<1e-9: return "hypho"
    if abs(q-10)<1e-9: return "klado / very open"
    if q <= 0 and abs(q/2-round(q/2))<1e-9:
        y=int(round(1-q/2))
        names={1:"mono-capped",2:"bi-capped",3:"tri-capped",4:"tetra-capped",5:"penta-capped",6:"hexa-capped"}
        return names.get(y,f"{y}-capped")
    if q>2:
        return f"open 4n+{_fmt(q)} family"
    return f"4n{('+' if q>=0 else '')}{_fmt(q)} family"


CLOSO_GEOMETRIES={
    1:"single skeletal center",
    2:"two-vertex edge / dimeric reference",
    3:"triangle",
    4:"tetrahedron",
    5:"trigonal bipyramid",
    6:"octahedron",
    7:"pentagonal bipyramid",
    8:"8-vertex closo deltahedron (commonly dodecahedral/D2d reference)",
    9:"tricapped trigonal prism",
    10:"bicapped square antiprism",
    11:"11-vertex closo deltahedron",
    12:"icosahedron",
    13:"13-vertex closo deltahedral reference",
}


def closo_geometry(n:int) -> str:
    return CLOSO_GEOMETRIES.get(n,f"{n}-vertex closo deltahedral reference")


def structural_configurations(n:int,q:float) -> tuple[list[str],str,float|None,float|None,str|None,str|None,float|None]:
    configs=[]
    y=z=VE0=None; kp=kstar=None

    if abs(q-2)<1e-9:
        primary=closo_geometry(n)
        configs.append(f"Closo family: {primary}.")
        configs.append("Other graphical isomers can share the same K(n); K-theory gives the family constraint before a unique 3D structure is asserted.")
        return configs,primary,y,z,kp,kstar,VE0

    if q>2 and abs(q/2-round(q/2))<1e-9:
        removed=int(round((q-2)/2))
        parent_n=n+removed
        parent=closo_geometry(parent_n)
        fam=family_from_q(q)
        primary=f"{fam} framework derived from a {parent_n}-vertex closo parent ({parent}) by opening/removing {removed} vertex{'es' if removed!=1 else ''}"
        configs.append(primary+".")
        configs.append("Multiple geometrical isomers may satisfy the same K(n); enumerate graphically rather than claim a unique shape without extra information.")
        return configs,primary,y,z,kp,kstar,VE0

    if q<=0 and abs(q/2-round(q/2))<1e-9:
        y=float(1-q/2)
        z=float(n-y)
        kp=f"C^{_fmt(y)}C[M{_fmt(z)}]"
        kstar=f"C^{_fmt(y)} + D^{_fmt(z)}"
        VE0=2*z+2
        if z>0:
            nucleus=closo_geometry(int(round(z))) if abs(z-round(z))<1e-9 else f"D^{_fmt(z)} nucleus"
            primary=f"{_fmt(y)}-capped configuration around a {nucleus}"
            configs.append(primary+".")
            configs.append(f"Capping descriptor: Kp={kp}; clan descriptor: K*={kstar}.")
        elif abs(z)<1e-9:
            primary=f"fully capped limiting configuration with zero-size closo nucleus in the formal K* description"
            configs.append(primary+".")
            configs.append(f"Kp={kp}; K*={kstar}.")
        else:
            primary=f"formal black-hole / negative-nucleus regime (z={_fmt(z)})"
            configs.append(primary+".")
            configs.append("This is a formal K-theory regime that requires Professor Kiremire's structural interpretation; no literal 3D nucleus is invented by the program.")
        return configs,primary,y,z,kp,kstar,VE0

    primary="non-canonical/non-even 4n+q case"
    configs.append("The computed q does not land on the standard even-step family ladder. Review component assignments, charge, or fragment electron counting.")
    return configs,primary,y,z,kp,kstar,VE0


def _series_text(base:int,q:float) -> str:
    if abs(q)<1e-9: return f"{base}n"
    return f"{base}n{'+' if q>0 else ''}{_fmt(q)}"


def _theory_modules(components:list[Component], family:str|None, y:float|None,z:float|None) -> list[str]:
    mods=["4n/14n series", "skeletal-number K bookkeeping", "K(n) categorization", "8e/18e rule check"]
    syms={c.label.strip("()") for c in components if c.role=="skeleton"}
    labels={c.label.strip("()") for c in components}
    if "CO" in labels: mods += ["transition-metal carbonyl analysis", "ligand/linkage accounting"]
    if "B" in syms: mods += ["borane/carborane/metalloborane clan analysis"]
    if "Au" in syms: mods += ["gold-cluster capping/graph analysis"]
    if any(s in syms for s in {"S","Se","Te"}) and "CO" in labels: mods += ["carbonyl-chalcogenide/hydrocarbon-equivalence strand"]
    if y is not None: mods += ["capping theory Kp", "clan/nucleus descriptor K*"]
    if z is not None and z<0: mods += ["black-hole / negative-nucleus formal regime"]
    mods += ["graph/shape interpretation", "isolobal/same-K comparison", "primary-cluster/formula-generation framework"]
    # preserve order
    return list(dict.fromkeys(mods))


def analyse_components(formula:str, components:Iterable[Component|dict], charge:int=0, warnings:Iterable[str]=()) -> Analysis:
    comps=[]
    for c in components:
        comps.append(c if isinstance(c,Component) else Component(**c))
    w=list(warnings)
    if not comps: raise ValueError("No components were supplied.")

    unknown=[c.label for c in comps if c.k_per_unit is None]
    if unknown:
        w.append("K could not be finalized because these components need an author-confirmed K value: "+", ".join(unknown))
        return Analysis(formula,charge,[asdict(c) for c in comps],None,None,None,None,None,None,None,None,None,[],None,None,None,None,None,None,[],[],w,[])

    skeleton=[c for c in comps if c.role=="skeleton"]
    n=sum(c.count for c in skeleton)
    if n<=0: raise ValueError("At least one skeletal atom is required.")

    K=sum(c.count*float(c.k_per_unit) for c in comps) + charge/2.0
    q=4*n-2*K
    cve=sum(c.count*float(c.target_e) for c in skeleton if c.target_e is not None) - 2*K

    # Direct valence electron cross-check where each component has an electron contribution.
    direct=0.0; direct_ok=True
    for c in skeleton:
        if c.valence_e_per_unit is None: direct_ok=False; break
        direct += c.count*float(c.valence_e_per_unit)
    if direct_ok:
        for c in comps:
            if c.role=="ligand":
                if c.valence_e_per_unit is None: direct_ok=False; break
                direct += c.count*float(c.valence_e_per_unit)
        direct -= charge  # + charge removes electrons; negative charge adds electrons
    else:
        direct=None

    series4=_series_text(4,q)
    all_tm=all(c.target_e==18 for c in skeleton)
    series14=_series_text(14,q) if all_tm else None
    fam=family_from_q(q)
    configs,primary,y,z,kp,kstar,VE0=structural_configurations(n,q)

    # Six CVE equations. Only equations whose capping variables exist are evaluated.
    six=[]
    six.append({"Equation":"VE = 18n - 2K (transition-metal form)","Value":18*n-2*K if all_tm else None,"Applicable":all_tm})
    six.append({"Equation":f"VE = 14n + q (transition-metal series)","Value":14*n+q if all_tm else None,"Applicable":all_tm})
    if VE0 is not None:
        six.append({"Equation":"VE = VE0 + 12n","Value":VE0+12*n,"Applicable":True})
        six.append({"Equation":"VE = VE0 + 12y + 12z","Value":VE0+12*y+12*z,"Applicable":True})
        six.append({"Equation":"VE = 12y + 14z + 2","Value":12*y+14*z+2,"Applicable":True})
        six.append({"Equation":"VE = VE(Dz) + 12y, VE(Dz)=14z+2","Value":14*z+2+12*y,"Applicable":True})
    else:
        six.extend([
            {"Equation":"VE = VE0 + 12n","Value":None,"Applicable":False},
            {"Equation":"VE = VE0 + 12y + 12z","Value":None,"Applicable":False},
            {"Equation":"VE = 12y + 14z + 2","Value":None,"Applicable":False},
            {"Equation":"VE = VE(Dz) + 12y","Value":None,"Applicable":False},
        ])

    steps=[]
    steps.append("Compute each skeletal-element K value from its valence-electron deficit relative to 8e (main group) or 18e (transition metal).")
    for c in comps:
        steps.append(f"{c.label}: {c.count} × K/unit {_fmt(c.k_per_unit)} = {_fmt(c.count*float(c.k_per_unit))} ({c.role}).")
    if charge:
        steps.append(f"Charge contribution: Q/2 = {_fmt(charge/2)}.")
    steps.append(f"Total skeletal-linkage number K = {_fmt(K)}.")
    steps.append(f"Skeletal count n = {n}; therefore q = 4n - 2K = {_fmt(q)} and series = {series4}.")
    steps.append(f"Cluster valence electrons = Σ(target shell electrons) - 2K = {_fmt(cve)}.")

    if direct_ok and direct is not None and abs(direct-cve)>1e-6:
        w.append(f"Direct valence-electron cross-check ({_fmt(direct)}) differs from K-derived CVE ({_fmt(cve)}); review component roles/donation conventions.")

    return Analysis(
        formula=formula,charge=charge,components=[asdict(c) for c in comps],n=n,K=K,q=q,cve=cve,
        direct_valence_e=direct if direct_ok else None,series4=series4,series14=series14,
        family=fam,bonds_label=f"K = {_fmt(K)} skeletal linkages",configurations=configs,
        primary_configuration=primary,K_n=f"{_fmt(K)}({n})",y=y,z=z,Kp=kp,Kstar=kstar,VE0=VE0,
        six_equations=six,theory_modules=_theory_modules(comps,fam,y,z),warnings=w,steps=steps
    )


def analyse_formula(text:str) -> Analysis:
    comps,charge,w=parse_formula(text)
    return analyse_components(text,comps,charge,w)


def same_k_elements(target_k:float,tol:float=1e-9) -> list[dict]:
    out=[]
    for r in periodic_table_records():
        if isinstance(r["K"],(int,float)) and abs(float(r["K"])-target_k)<=tol:
            out.append(r)
    return out


def theory_atlas() -> list[dict]:
    return [
        {"Area":"4n/14n series and Wade–Mingos expansion","What V1 does":"Computes q, 4n+q and 14n+q where applicable; maps standard family ladder."},
        {"Area":"Skeletal numbers and 8e/18e rules","What V1 does":"Uses published K table pattern; reports group-valence G, K and skeletal valence V=2K."},
        {"Area":"Transition-metal carbonyls","What V1 does":"Counts metal skeletal K, CO/H/charge contributions, K(n), CVE and family."},
        {"Area":"Boranes, carboranes and metalloboranes","What V1 does":"Treats B/C as main-group skeletons and H as electron contribution; computes clan/family descriptors."},
        {"Area":"Capping theory","What V1 does":"For q≤0 computes caps y, nucleus z, Kp=C^yC[Mz], K*=C^y+D^z and VE0."},
        {"Area":"Graph/shape interpretation","What V1 does":"Gives reference closo geometry or capped/open parent construction; explicitly avoids inventing a unique isomer."},
        {"Area":"Golden clusters","What V1 does":"Same K/capping machinery applies to Au skeletal atoms; ligand assumptions remain editable."},
        {"Area":"Matryoshka / inside-out capping","What V1 does":"Flags as a specialized structural interpretation; exact inside-out placement is not automatically invented without a validated rule."},
        {"Area":"Black-hole / negative-nucleus regimes","What V1 does":"Detects formal z<0 cases and labels them for K-theory interpretation rather than literal geometry."},
        {"Area":"Primary clusters and formula generation","What V1 does":"Provides K(n), series and elemental K values required for formula-generation workflows; full inverse generator is reserved for the research extension."},
        {"Area":"Isolobal/same-K comparison","What V1 does":"Finds periodic-table elements sharing a K value and exposes the common skeletal-number class."},
        {"Area":"Six CVE equations","What V1 does":"Displays all six transition-metal/capping forms and cross-checks them when their variables are defined."},
    ]


# Published-style examples used for regression tests.
VALIDATION_EXAMPLES = {
    "Rh6(CO)16": {"K":11,"n":6,"q":2,"cve":86,"family":"closo"},
    "Os10(CO)26^2-": {"K":23,"n":10,"q":-6,"cve":134,"family":"tetra-capped"},
    "B6H6^2-": {"K":11,"n":6,"q":2,"cve":26,"family":"closo"},
    "B5H9": {"K":8,"n":5,"q":4,"cve":24,"family":"nido"},
    "C2B10H12": {"K":23,"n":12,"q":2,"cve":50,"family":"closo"},
    "P4": {"K":6,"n":4,"q":4,"cve":20,"family":"nido"},
    "Bi5^3+": {"K":9,"n":5,"q":2,"cve":22,"family":"closo"},
    "Mn2(CO)10": {"K":1,"n":2,"q":6,"cve":34,"family":"arachno"},
    "Fe3(CO)12": {"K":3,"n":3,"q":6,"cve":48,"family":"arachno"},
    "Co4(CO)12": {"K":6,"n":4,"q":4,"cve":60,"family":"nido"},
    "Os6(CO)18": {"K":12,"n":6,"q":0,"cve":84,"family":"mono-capped"},
    "Fe2Co2(CO)12": {"K":7,"n":4,"q":2,"cve":58,"family":"closo"},
    "Pd35(CO)23L15": {"K":102,"n":35,"q":-64,"cve":426,"family":"33-capped"},
}
