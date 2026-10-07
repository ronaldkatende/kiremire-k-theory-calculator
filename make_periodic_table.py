from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from k_theory_engine import ELEMENTS, group_valence_electrons, skeletal_number

# Standard main-table positions. Lanthanides/actinides shown in two detached rows.
rows = {
1: [('H',1),('He',18)],
2: [('Li',1),('Be',2),('B',13),('C',14),('N',15),('O',16),('F',17),('Ne',18)],
3: [('Na',1),('Mg',2),('Al',13),('Si',14),('P',15),('S',16),('Cl',17),('Ar',18)],
4: [('K',1),('Ca',2),('Sc',3),('Ti',4),('V',5),('Cr',6),('Mn',7),('Fe',8),('Co',9),('Ni',10),('Cu',11),('Zn',12),('Ga',13),('Ge',14),('As',15),('Se',16),('Br',17),('Kr',18)],
5: [('Rb',1),('Sr',2),('Y',3),('Zr',4),('Nb',5),('Mo',6),('Tc',7),('Ru',8),('Rh',9),('Pd',10),('Ag',11),('Cd',12),('In',13),('Sn',14),('Sb',15),('Te',16),('I',17),('Xe',18)],
6: [('Cs',1),('Ba',2),('La',3),('Hf',4),('Ta',5),('W',6),('Re',7),('Os',8),('Ir',9),('Pt',10),('Au',11),('Hg',12),('Tl',13),('Pb',14),('Bi',15),('Po',16),('At',17),('Rn',18)],
7: [('Fr',1),('Ra',2),('Ac',3),('Rf',4),('Db',5),('Sg',6),('Bh',7),('Hs',8),('Mt',9),('Ds',10),('Rg',11),('Cn',12),('Nh',13),('Fl',14),('Mc',15),('Lv',16),('Ts',17),('Og',18)],
}
lan=['Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu']
act=['Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr']

fig,ax=plt.subplots(figsize=(18,10))
ax.set_xlim(0,19); ax.set_ylim(-1,11); ax.axis('off')

for period,items in rows.items():
    y=9-period
    for sym,g in items:
        x=g-1
        k=skeletal_number(sym); ve=group_valence_electrons(sym)
        rect=Rectangle((x,y),0.94,0.88,fill=False,linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x+0.47,y+0.59,sym,ha='center',va='center',fontsize=10,fontweight='bold')
        if k is None:
            ax.text(x+0.47,y+0.31,'K: —',ha='center',va='center',fontsize=7)
            ax.text(x+0.47,y+0.13,'V: —',ha='center',va='center',fontsize=7)
        else:
            kval=int(k) if float(k).is_integer() else k
            v=2*k; vv=int(v) if float(v).is_integer() else v
            ax.text(x+0.47,y+0.31,f'K: {kval}',ha='center',va='center',fontsize=7)
            ax.text(x+0.47,y+0.13,f'V: {vv}  G: {ve}',ha='center',va='center',fontsize=6.5)

for row_idx,(label,series) in enumerate([('Lanthanides',lan),('Actinides',act)]):
    y=1-row_idx
    ax.text(0.2,y+0.42,label,ha='left',va='center',fontsize=9)
    for j,sym in enumerate(series):
        x=3+j
        rect=Rectangle((x,y),0.94,0.78,fill=False,linewidth=0.8,linestyle='--')
        ax.add_patch(rect)
        ax.text(x+0.47,y+0.48,sym,ha='center',va='center',fontsize=9,fontweight='bold')
        k=skeletal_number(sym)
        if k is None:
            ax.text(x+0.47,y+0.20,'K: review',ha='center',va='center',fontsize=6.5)
        else:
            ax.text(x+0.47,y+0.20,f'K: {k:g}',ha='center',va='center',fontsize=6.5)

ax.text(9,10.35,'K-Theory Periodic Table — Skeletal Number and Skeletal Valence',ha='center',fontsize=16,fontweight='bold')
ax.text(9,9.90,'Each cell shows K and V=2K; G is the group-valence electron count. Atomic numbers are intentionally omitted.',ha='center',fontsize=10)
ax.text(9,-0.55,'Published K-pattern implemented for main-group and d-block elements. f-block cells remain marked for Professor Kiremire’s author-confirmed rule.',ha='center',fontsize=9)
fig.tight_layout()
out=Path(__file__).parent/'assets'/'k_theory_periodic_table.png'
fig.savefig(out,dpi=220,bbox_inches='tight')
print(out)
