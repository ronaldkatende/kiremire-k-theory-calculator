# Source basis for Version 1

The code was organized around the following public Kiremire publications and descriptions.

1. **Unification and Expansion of Wade–Mingos Rules with Elementary Number Theory** (2015), Oriental Journal of Chemistry. Introduces/uses the empirical `k = 1/2(E-V)` formulation and cluster series.
2. **The Main Group Elements, Fragments, Compounds and Clusters Obey the 4n Rule and Form 4n Series** (2016), International Journal of Chemistry. Develops the 4n/14n relationship between main-group and transition-metal systems.
3. **A Hypothetical Model for the Formation of Transition Metal Carbonyl Clusters Based upon 4n Series Skeletal Numbers** (2016), International Journal of Chemistry. Assigns K values to skeletal elements/ligands and uses linkage conservation and 8e/18e rules.
4. **The Outstanding Applications of Skeletal Numbers to Chemical Clusters** (2017), International Journal of Chemistry. Uses skeletal numbers for categorization, shape prediction, isolobal matching and tentative ligand assignment.
5. **Graph Theory of Chemical Series and Broad Categorization of Clusters** (2018), International Journal of Chemistry. Develops graph/capping categorization.
6. **Graph Theory of Capping Golden Clusters** (2018), International Journal of Chemistry. Extends capping/graph ideas to gold clusters and black-hole/nuclear descriptors.
7. **Generating Cluster Formulas Using the Primary Clusters and the K(n) Parameters** (2018), International Journal of Chemistry. Connects primary clusters, K(n) and formula generation.
8. **Inside out Capping Clusters: Matryoshka Series** (2018), International Journal of Chemistry. Introduces inside-out capping / Matryoshka structural interpretation.
9. **The Capping Theory of Chemical Elements and Clusters Based on 4N Series and Skeletal Numbers** (2018), International Journal of Chemistry. Gives published skeletal-number tables for main-group and transition-metal elements and capping/nuclear ideas.
10. **The Capping Theory of Chemical Clusters Based on 12N/14N Series** (2018), International Journal of Chemistry. Gives `Kp=C^yC[Mx]`, cluster genesis/baseline and CVE relations.
11. **Categorization of Metalloboranes using Skeletal Numbers** (2019), International Journal of Chemistry and Research.
12. **Categorization of Transition Metal Carbonyl Clusters using Skeletal Numbers and the Six Fundamental Equations for calculating Cluster Valence Electrons (CVE)** (2019), International Journal of Chemistry and Research. Gives the six CVE equations used in Version 1.
13. **Categorization of Boranes Into Clan Series** (2020), International Journal of Chemistry. Applies clan/family categorization and six-equation CVE framework to boranes.
14. Kiremire's later public explanation of **convergence theory** describes elemental K as the number of electron pairs/equivalents needed to reach the stable shell and explicitly gives `H(K=0.5)`.

## Core identities implemented

For standard K-theory bookkeeping:

- transition-metal skeletal element: `K=(18-G)/2`;
- main-group skeletal element: `K=(8-G)/2` (period-1 H/He use the 2e shell);
- one donated electron contributes `K=-0.5`;
- signed charge contributes `Q/2` to K;
- `K(n)` records total K and skeletal count n;
- `q = 4n - 2K`;
- standard family series `S=4n+q`, with transition-metal CVE form `VE=14n+q`;
- general K-derived electron bookkeeping `VE = sum(target shell electrons over skeletal atoms) - 2K`;
- capping form for q<=0: `y=1-q/2`, `z=n-y`, `Kp=C^yC[Mz]`, `K*=C^y+D^z`, `VE0=2z+2`;
- six CVE forms are displayed when capping variables are defined.

The app labels any rule outside the published/validated implementation as requiring author review instead of silently guessing.
