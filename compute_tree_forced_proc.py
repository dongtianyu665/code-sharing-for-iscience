"""Compute tree statistics with forced structure:
Level 1: First-layer division
Level 2: Primary Procedure (within each branch)
Level 3: LOS (let E-CHAID choose)
"""
import pandas as pd
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from CHAID import Tree

df = pd.read_excel('D:/claude/E-CHAID.xlsx')
df['LOS_group'] = pd.cut(df['LOS'], bins=[-1, 3, 6, float('inf')], labels=[1, 2, 3])

TOTAL_N = len(df)

print("=" * 70)
print("FORCED TREE: Level 1 = First-layer division, Level 2 = Primary Procedure")
print("=" * 70)

# ============================================================
# Level 1 → Level 2: manual split
# ============================================================
all_terminal_nodes = []

for div_name in ['image-guided', 'minimally', 'open']:
    branch = df[df['First-layer division'] == div_name]
    print(f"\n{'─'*60}")
    print(f"Level 1: {div_name}  (n={len(branch)}, mean={branch['total_cost'].mean():,.2f})")

    procs = sorted(branch['primary_procedure'].unique())

    for proc in procs:
        sub = branch[branch['primary_procedure'] == proc]
        if len(sub) < 15:
            continue  # skip tiny groups

        print(f"\n  Level 2: {proc}  (n={len(sub)}, mean={sub['total_cost'].mean():,.2f})")

        # Try E-CHAID within this subgroup (using LOS)
        i_vars = {'LOS_group': 'ordinal'}
        try:
            tree = Tree.from_pandas_df(
                df=sub, i_variables=i_vars, d_variable='total_cost',
                dep_variable_type='continuous',
                alpha_merge=0.05, max_depth=1, min_parent_node_size=20,
                min_child_node_size=10, is_exhaustive=True,
            )
            tree.print_tree()
        except Exception as e:
            print(f"    Tree error: {e}")

        # LOS breakdown
        for los_val in [1, 2, 3]:
            s = sub[sub['LOS_group'] == los_val]
            if len(s) > 0:
                print(f"    LOS {los_val}: n={len(s)}, mean={s['total_cost'].mean():,.2f}, cv={s['total_cost'].std()/s['total_cost'].mean():.3f}")

# ============================================================
# Handle RFA + UAE merging
# ============================================================
print(f"\n{'─'*60}")
print("Special: RFA + UAE (image-guided, n very small)")
rfa_uae = df[(df['First-layer division'] == 'image-guided') &
             (df['primary_procedure'].isin(['RFA', 'UAE']))]
print(f"  Combined RFA+UAE: n={len(rfa_uae)}, mean={rfa_uae['total_cost'].mean():,.2f}")

# ============================================================
# Build final tree structure
# ============================================================
print(f"\n{'='*70}")
print("FINAL TREE STRUCTURE")
print(f"{'='*70}")

# Level 1: First-layer division
# Level 2: Primary Procedure within each branch
# Level 3: LOS within each procedure (if significant split)

# Image-guided: FUAS, RFA+UAE
# Minimally: HM, LH, LM, VM
# Open: AM, OH

tree_def = {
    'image-guided': {
        'n': len(df[df['First-layer division'] == 'image-guided']),
        'mean': df[df['First-layer division'] == 'image-guided']['total_cost'].mean(),
        'procedures': {
            'FUAS': {
                'n': len(df[(df['First-layer division']=='image-guided') & (df['primary_procedure']=='FUAS')]),
                'mean': df[(df['First-layer division']=='image-guided') & (df['primary_procedure']=='FUAS')]['total_cost'].mean(),
                'los_splits': {}
            },
            'RFA+UAE': {
                'n': len(df[(df['First-layer division']=='image-guided') & (df['primary_procedure'].isin(['RFA','UAE']))]),
                'mean': df[(df['First-layer division']=='image-guided') & (df['primary_procedure'].isin(['RFA','UAE']))]['total_cost'].mean(),
                'los_splits': {}
            }
        }
    },
    'minimally': {
        'n': len(df[df['First-layer division'] == 'minimally']),
        'mean': df[df['First-layer division'] == 'minimally']['total_cost'].mean(),
        'procedures': {
            'HM': {
                'n': len(df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='HM')]),
                'mean': df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='HM')]['total_cost'].mean(),
                'los_splits': {}
            },
            'LH': {
                'n': len(df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='LH')]),
                'mean': df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='LH')]['total_cost'].mean(),
                'los_splits': {}
            },
            'LM': {
                'n': len(df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='LM')]),
                'mean': df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='LM')]['total_cost'].mean(),
                'los_splits': {}
            },
            'VM': {
                'n': len(df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='VM')]),
                'mean': df[(df['First-layer division']=='minimally') & (df['primary_procedure']=='VM')]['total_cost'].mean(),
                'los_splits': {}
            },
        }
    },
    'open': {
        'n': len(df[df['First-layer division'] == 'open']),
        'mean': df[df['First-layer division'] == 'open']['total_cost'].mean(),
        'procedures': {
            'AM': {
                'n': len(df[(df['First-layer division']=='open') & (df['primary_procedure']=='AM')]),
                'mean': df[(df['First-layer division']=='open') & (df['primary_procedure']=='AM')]['total_cost'].mean(),
                'los_splits': {}
            },
            'OH': {
                'n': len(df[(df['First-layer division']=='open') & (df['primary_procedure']=='OH')]),
                'mean': df[(df['First-layer division']=='open') & (df['primary_procedure']=='OH')]['total_cost'].mean(),
                'los_splits': {}
            },
        }
    }
}

# Compute LOS splits within each procedure
for div_name, div_data in tree_def.items():
    for proc_name, proc_data in div_data['procedures'].items():
        sub = df[(df['First-layer division'] == div_name) &
                 (df['primary_procedure'].isin(['RFA','UAE'] if proc_name == 'RFA+UAE' else [proc_name]))]
        proc_data['los_splits'] = {}
        for los_val in [1, 2, 3]:
            los_sub = sub[sub['LOS_group'] == los_val]
            if len(los_sub) > 0:
                proc_data['los_splits'][los_val] = {
                    'n': len(los_sub),
                    'mean': los_sub['total_cost'].mean(),
                    'median': los_sub['total_cost'].median(),
                    'std': los_sub['total_cost'].std(),
                    'cv': los_sub['total_cost'].std() / los_sub['total_cost'].mean() if los_sub['total_cost'].mean() != 0 else 0,
                }
        print(f"\n{div_name} → {proc_name} (n={proc_data['n']}, mean={proc_data['mean']:,.2f})")
        for los_val, los_data in proc_data['los_splits'].items():
            print(f"  LOS {los_val}: n={los_data['n']}, mean={los_data['mean']:,.2f}, cv={los_data['cv']:.3f}")

# ============================================================
# Determine if LOS split is needed per procedure
# ============================================================
print(f"\n{'='*70}")
print("LOS SPLIT SIGNIFICANCE (within each procedure)")
print(f"{'='*70}")

for div_name, div_data in tree_def.items():
    for proc_name, proc_data in div_data['procedures'].items():
        sub = df[(df['First-layer division'] == div_name) &
                 (df['primary_procedure'].isin(['RFA','UAE'] if proc_name == 'RFA+UAE' else [proc_name]))]
        if len(sub) < 20 or sub['LOS_group'].nunique() < 2:
            print(f"\n{div_name} → {proc_name}: N too small or single LOS, no split")
            proc_data['split_los'] = False
            continue

        from scipy.stats import kruskal
        los_groups = [sub[sub['LOS_group']==g]['total_cost'].values for g in sub['LOS_group'].unique() if len(sub[sub['LOS_group']==g]) > 5]
        if len(los_groups) >= 2:
            h, p = kruskal(*los_groups)
            split = p < 0.05
            proc_data['split_los'] = split
            print(f"\n{div_name} → {proc_name}: Kruskal-Wallis H={h:.1f}, p={p:.4f}, split={split}")
        else:
            proc_data['split_los'] = False
            print(f"\n{div_name} → {proc_name}: not enough LOS groups")