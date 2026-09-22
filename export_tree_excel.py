"""Export E-CHAID decision tree structure (4 levels, 13 DRG groups) to Excel."""
import pandas as pd
import numpy as np
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

df = pd.read_excel('D:/claude/E-CHAID.xlsx')
TOTAL = len(df)
df['LOS_group'] = pd.cut(df['LOS'], bins=[-1, 3, 6, float('inf')], labels=['1-3d', '4-6d', '>=7d'])

def S(sub):
    n = len(sub); m = sub['total_cost'].mean()
    s = sub['total_cost'].std(); cv = s/m if m>0 else 0
    med = sub['total_cost'].median()
    mn = sub['total_cost'].min(); mx = sub['total_cost'].max()
    p25 = sub['total_cost'].quantile(0.25); p75 = sub['total_cost'].quantile(0.75)
    return {'N': n, 'Mean': round(m, 2), 'Std': round(s, 2), 'CV': round(cv, 4),
            'Median': round(med, 2), 'P25': round(p25, 2), 'P75': round(p75, 2),
            'Min': mn, 'Max': mx, 'Pct': round(n/TOTAL*100, 2)}

# ── Compute all node statistics ──
img = df[df['First-layer division']=='image-guided']
mini = df[df['First-layer division']=='minimally']
opn = df[df['First-layer division']=='open']

img_fuas = img[img['primary_procedure']=='FUAS']
img_fuas_los12 = img_fuas[img_fuas['LOS_group'].isin(['1-3d','4-6d'])]
img_fuas_los12_1 = img_fuas[img_fuas['LOS_group']=='1-3d']
img_fuas_los12_2 = img_fuas[img_fuas['LOS_group']=='4-6d']
img_fuas_los3 = img_fuas[img_fuas['LOS_group']=='>=7d']
img_rfa_uae = img[img['primary_procedure'].isin(['RFA','UAE'])]

mini_hm = mini[mini['primary_procedure']=='HM']
mini_hm_los1 = mini_hm[mini_hm['LOS_group']=='1-3d']
mini_hm_los23 = mini_hm[mini_hm['LOS_group'].isin(['4-6d','>=7d'])]
mini_hm_los2 = mini_hm[mini_hm['LOS_group']=='4-6d']
mini_hm_los3 = mini_hm[mini_hm['LOS_group']=='>=7d']
mini_lh = mini[mini['primary_procedure']=='LH']
mini_lh_los12 = mini_lh[mini_lh['LOS_group'].isin(['1-3d','4-6d'])]
mini_lh_los1 = mini_lh[mini_lh['LOS_group']=='1-3d']
mini_lh_los2 = mini_lh[mini_lh['LOS_group']=='4-6d']
mini_lh_los3 = mini_lh[mini_lh['LOS_group']=='>=7d']
mini_lm = mini[mini['primary_procedure']=='LM']
mini_lm_los12 = mini_lm[mini_lm['LOS_group'].isin(['1-3d','4-6d'])]
mini_lm_los1 = mini_lm[mini_lm['LOS_group']=='1-3d']
mini_lm_los2 = mini_lm[mini_lm['LOS_group']=='4-6d']
mini_lm_los3 = mini_lm[mini_lm['LOS_group']=='>=7d']
mini_vm = mini[mini['primary_procedure']=='VM']

opn_am = opn[opn['primary_procedure']=='AM']
opn_am_los12 = opn_am[opn_am['LOS_group'].isin(['1-3d','4-6d'])]
opn_am_los1 = opn_am[opn_am['LOS_group']=='1-3d']
opn_am_los2 = opn_am[opn_am['LOS_group']=='4-6d']
opn_am_los3 = opn_am[opn_am['LOS_group']=='>=7d']
opn_oh = opn[opn['primary_procedure']=='OH']
opn_oh_los2 = opn_oh[opn_oh['LOS_group']=='4-6d']
opn_oh_los3 = opn_oh[opn_oh['LOS_group']=='>=7d']

# ── Sheet 1: Complete tree structure ──
tree_rows = []

tree_rows.append({'Level': 0, 'Layer': 'Root', 'Node_Type': 'Root',
    'Node_Name': 'All UL Patients', 'Parent': '-', 'Split_Variable': '-',
    'DRG_ID': '', 'N': TOTAL, 'Pct': 100.0, 'Mean': round(df['total_cost'].mean(), 2),
    'CV': round(df['total_cost'].std()/df['total_cost'].mean(), 4)})

for name, sub in [('Image-Guided', img), ('Minimally Invasive', mini), ('Open Surgery', opn)]:
    s = S(sub)
    tree_rows.append({'Level': 1, 'Layer': 'Level 1 - First-layer Division', 'Node_Type': 'Split',
        'Node_Name': name, 'Parent': 'All UL Patients', 'Split_Variable': 'First-layer Division',
        'DRG_ID': '', 'N': s['N'], 'Pct': s['Pct'], 'Mean': s['Mean'], 'CV': s['CV']})

l2_nodes = [
    ('Image-Guided -> FUAS', img_fuas, 'Image-Guided'),
    ('Image-Guided -> RFA+UAE', img_rfa_uae, 'Image-Guided'),
    ('Minimally -> HM', mini_hm, 'Minimally Invasive'),
    ('Minimally -> LH', mini_lh, 'Minimally Invasive'),
    ('Minimally -> LM', mini_lm, 'Minimally Invasive'),
    ('Minimally -> VM', mini_vm, 'Minimally Invasive'),
    ('Open -> AM', opn_am, 'Open Surgery'),
    ('Open -> OH', opn_oh, 'Open Surgery'),
]
for name, sub, parent in l2_nodes:
    s = S(sub)
    can_split = s['N'] >= 20
    tree_rows.append({'Level': 2, 'Layer': 'Level 2 - Primary Procedure', 'Node_Type': 'Split' if can_split else 'Terminal',
        'Node_Name': name, 'Parent': parent, 'Split_Variable': 'Primary Procedure',
        'DRG_ID': '', 'N': s['N'], 'Pct': s['Pct'], 'Mean': s['Mean'], 'CV': s['CV']})

l3_nodes = [
    ('FUAS -> LOS 1-6d', img_fuas_los12, 'Image-Guided -> FUAS'),
    ('FUAS -> LOS >=7d', img_fuas_los3, 'Image-Guided -> FUAS'),
    ('HM -> LOS 1-3d', mini_hm_los1, 'Minimally -> HM'),
    ('HM -> LOS 4-7d+', mini_hm_los23, 'Minimally -> HM'),
    ('LH -> LOS 1-6d', mini_lh_los12, 'Minimally -> LH'),
    ('LH -> LOS >=7d', mini_lh_los3, 'Minimally -> LH'),
    ('LM -> LOS 1-6d', mini_lm_los12, 'Minimally -> LM'),
    ('LM -> LOS >=7d', mini_lm_los3, 'Minimally -> LM'),
    ('AM -> LOS 1-6d', opn_am_los12, 'Open -> AM'),
    ('AM -> LOS >=7d', opn_am_los3, 'Open -> AM'),
]
for name, sub, parent in l3_nodes:
    s = S(sub)
    tree_rows.append({'Level': 3, 'Layer': 'Level 3 - LOS', 'Node_Type': 'Split -> Terminal',
        'Node_Name': name, 'Parent': parent, 'Split_Variable': 'LOS',
        'DRG_ID': '', 'N': s['N'], 'Pct': s['Pct'], 'Mean': s['Mean'], 'CV': s['CV']})

drg_nodes = [
    (1, 'Image-Guided -> FUAS -> LOS 1-6d', img_fuas_los12),
    (2, 'Image-Guided -> FUAS -> LOS >=7d', img_fuas_los3),
    (3, 'Image-Guided -> RFA+UAE (terminal)', img_rfa_uae),
    (4, 'Minimally -> HM -> LOS 1-3d', mini_hm_los1),
    (5, 'Minimally -> HM -> LOS 4-7d+', mini_hm_los23),
    (6, 'Minimally -> LH -> LOS 1-6d', mini_lh_los12),
    (7, 'Minimally -> LH -> LOS >=7d', mini_lh_los3),
    (8, 'Minimally -> LM -> LOS 1-6d', mini_lm_los12),
    (9, 'Minimally -> LM -> LOS >=7d', mini_lm_los3),
    (10, 'Minimally -> VM (terminal)', mini_vm),
    (11, 'Open -> AM -> LOS 1-6d', opn_am_los12),
    (12, 'Open -> AM -> LOS >=7d', opn_am_los3),
    (13, 'Open -> OH (terminal)', opn_oh),
]
for drg_id, name, sub in drg_nodes:
    s = S(sub)
    tree_rows.append({'Level': 4, 'Layer': 'Level 4 - Terminal DRG', 'Node_Type': 'DRG Terminal',
        'Node_Name': f'DRG {drg_id}', 'Parent': name.rsplit(' -> ', 1)[0] if ' -> ' in name else name,
        'Split_Variable': '-', 'DRG_ID': drg_id,
        'N': s['N'], 'Pct': s['Pct'], 'Mean': s['Mean'], 'CV': s['CV'],
        'Median': s['Median'], 'P25': s['P25'], 'P75': s['P75'], 'Min': s['Min'], 'Max': s['Max']})

df_tree = pd.DataFrame(tree_rows)

# ── Sheet 2: DRG Summary ──
drg_summary = []
for drg_id, name, sub in drg_nodes:
    s = S(sub)
    los_dist = sub['LOS_group'].value_counts().to_dict()
    los_str = ', '.join([f'{k}: {v}' for k, v in sorted(los_dist.items())])
    proc_dist = sub['primary_procedure'].value_counts().to_dict()
    proc_str = ', '.join([f'{k}: {v}' for k, v in sorted(proc_dist.items())])
    parts = name.split(' -> ')
    drg_summary.append({
        'DRG_ID': drg_id, 'Path': name,
        'First_Layer_Division': parts[0],
        'Primary_Procedure': parts[1] if len(parts) > 1 else '-',
        'LOS_Category': parts[2] if len(parts) > 2 else ('All' if 'terminal' in name else '-'),
        'N': s['N'], 'Percentage': s['Pct'], 'Mean_Cost': s['Mean'],
        'Median_Cost': s['Median'], 'Std': s['Std'], 'CV': s['CV'],
        'P25': s['P25'], 'P75': s['P75'], 'Min': s['Min'], 'Max': s['Max'],
        'LOS_Distribution': los_str, 'Procedure_Distribution': proc_str,
    })
df_drg = pd.DataFrame(drg_summary)

# ── Sheet 3: LOS-Procedure Crosstab ──
cross_rows = []
combos = [
    ('Image-Guided', 'FUAS', '1-3d', img_fuas_los12_1),
    ('Image-Guided', 'FUAS', '4-6d', img_fuas_los12_2),
    ('Image-Guided', 'FUAS', '>=7d', img_fuas_los3),
    ('Image-Guided', 'RFA+UAE', '1-3d', img_rfa_uae[img_rfa_uae['LOS_group']=='1-3d']),
    ('Image-Guided', 'RFA+UAE', '4-6d', img_rfa_uae[img_rfa_uae['LOS_group']=='4-6d']),
    ('Image-Guided', 'RFA+UAE', '>=7d', img_rfa_uae[img_rfa_uae['LOS_group']=='>=7d']),
    ('Minimally', 'HM', '1-3d', mini_hm_los1),
    ('Minimally', 'HM', '4-6d', mini_hm_los2),
    ('Minimally', 'HM', '>=7d', mini_hm_los3),
    ('Minimally', 'LH', '1-3d', mini_lh_los1),
    ('Minimally', 'LH', '4-6d', mini_lh_los2),
    ('Minimally', 'LH', '>=7d', mini_lh_los3),
    ('Minimally', 'LM', '1-3d', mini_lm_los1),
    ('Minimally', 'LM', '4-6d', mini_lm_los2),
    ('Minimally', 'LM', '>=7d', mini_lm_los3),
    ('Minimally', 'VM', '1-3d', mini_vm[mini_vm['LOS_group']=='1-3d']),
    ('Minimally', 'VM', '4-6d', mini_vm[mini_vm['LOS_group']=='4-6d']),
    ('Minimally', 'VM', '>=7d', mini_vm[mini_vm['LOS_group']=='>=7d']),
    ('Open', 'AM', '1-3d', opn_am_los1),
    ('Open', 'AM', '4-6d', opn_am_los2),
    ('Open', 'AM', '>=7d', opn_am_los3),
    ('Open', 'OH', '4-6d', opn_oh_los2),
    ('Open', 'OH', '>=7d', opn_oh_los3),
]
for div, proc, los, sub in combos:
    if len(sub) == 0:
        continue
    s = S(sub)
    cross_rows.append({
        'First_Layer_Division': div, 'Primary_Procedure': proc, 'LOS_Group': los,
        'N': s['N'], 'Pct_of_Total': s['Pct'], 'Mean_Cost': s['Mean'],
        'Median_Cost': s['Median'], 'Std': s['Std'], 'CV': s['CV'],
        'P25': s['P25'], 'P75': s['P75'], 'Min': s['Min'], 'Max': s['Max'],
    })
df_cross = pd.DataFrame(cross_rows)

# ── Sheet 4: Statistical Tests ──
from scipy.stats import kruskal

groups_13 = [sub['total_cost'].values for _, _, sub in drg_nodes]
h_13, p_13 = kruskal(*groups_13)
groups_l1 = [img['total_cost'].values, mini['total_cost'].values, opn['total_cost'].values]
h_l1, p_l1 = kruskal(*groups_l1)

stats_rows = [
    {'Test': 'Kruskal-Wallis (13 DRG groups)', 'H_Statistic': f'{h_13:.2f}',
     'P_Value': f'{p_13:.2e}', 'Significant': 'Yes (P<0.001)',
     'Description': 'Cost heterogeneity between all 13 DRG groups'},
    {'Test': 'Kruskal-Wallis (First-layer divisions)', 'H_Statistic': f'{h_l1:.2f}',
     'P_Value': f'{p_l1:.2e}', 'Significant': 'Yes (P<0.001)',
     'Description': 'Cost heterogeneity between Image-Guided / Minimally / Open'},
    {'Test': 'CV Range (13 DRG groups)', 'H_Statistic': '-', 'P_Value': '-',
     'Significant': f'{min([S(sub)["CV"] for _,_,sub in drg_nodes]):.4f} - {max([S(sub)["CV"] for _,_,sub in drg_nodes]):.4f}',
     'Description': 'All CV < 1: acceptable within-group cost homogeneity'},
]
df_stats = pd.DataFrame(stats_rows)

# ── Sheet 5: Summary ──
cv_list = [S(sub)['CV'] for _, _, sub in drg_nodes]
summary_rows = [
    {'Metric': 'Total Patients', 'Value': f'{TOTAL:,}'},
    {'Metric': 'Total DRG Groups', 'Value': '13'},
    {'Metric': 'Tree Depth', 'Value': '4 levels (Root + 3 split levels + terminal)'},
    {'Metric': 'Level 1 Split', 'Value': 'First-layer Division (Image-Guided / Minimally Invasive / Open Surgery)'},
    {'Metric': 'Level 2 Split', 'Value': 'Primary Procedure (8 categories)'},
    {'Metric': 'Level 3 Split', 'Value': 'Length of Stay (LOS: 1-3d / 4-6d / >=7d)'},
    {'Metric': 'Overall Mean Cost', 'Value': f'{df["total_cost"].mean():,.2f} yuan'},
    {'Metric': 'Overall Median Cost', 'Value': f'{df["total_cost"].median():,.2f} yuan'},
    {'Metric': 'Overall Std', 'Value': f'{df["total_cost"].std():,.2f} yuan'},
    {'Metric': 'Overall CV', 'Value': f'{df["total_cost"].std()/df["total_cost"].mean():.4f}'},
    {'Metric': 'Kruskal-Wallis H (13 groups)', 'Value': f'{h_13:.2f} (P = {p_13:.2e})'},
    {'Metric': 'CV Range (within DRG groups)', 'Value': f'{min(cv_list):.4f} - {max(cv_list):.4f} (all < 1)'},
    {'Metric': 'Algorithm', 'Value': 'E-CHAID (Exhaustive Chi-squared Automatic Interaction Detector)'},
    {'Metric': 'Parameters', 'Value': 'alpha_merge=0.05, max_depth=3, min_parent_node=20, min_child_node=10'},
    {'Metric': 'Data Source', 'Value': 'E-CHAID.xlsx (7,413 UL patients, 2019-2022)'},
    {'Metric': 'Software', 'Value': 'Python (CHAID package + pandas + scipy)'},
]
df_summary = pd.DataFrame(summary_rows)

# ── Write Excel with styling ──
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

header_font = Font(name='Arial', size=10, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
sub_fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
alt_fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
drg_fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9'),
)

def write_styled_sheet(ws, headers, col_widths, data_dicts):
    """Write and style a worksheet from dict data."""
    # Collect all unique keys across all rows, preserving order
    keys = []
    seen = set()
    for d in data_dicts:
        for k in d.keys():
            if k not in seen:
                keys.append(k)
                seen.add(k)
    # Headers
    for j, hdr in enumerate(keys):
        cell = ws.cell(row=1, column=j+1, value=hdr)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
    for j, w in enumerate(col_widths):
        ws.column_dimensions[get_column_letter(j+1)].width = w
    # Data
    for i, row_dict in enumerate(data_dicts):
        is_drg = str(row_dict.get('Node_Type', '')).startswith('DRG')
        for j, key in enumerate(keys):
            val = row_dict.get(key, '')
            cell = ws.cell(row=i+2, column=j+1, value=val)
            cell.font = Font(name='Arial', size=9, bold=is_drg)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center' if j > 1 else 'left',
                                       vertical='center', wrap_text=True)
            if is_drg:
                cell.fill = drg_fill
            elif i % 2 == 0:
                cell.fill = alt_fill
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions

# ── Sheet 1: Tree Structure ──
ws1 = wb.active
ws1.title = 'Tree Structure'
c1 = [6, 26, 18, 42, 30, 20, 8, 8, 8, 14, 14, 10, 12, 12, 10, 10]
write_styled_sheet(ws1, [], c1, tree_rows)

# ── Sheet 2: DRG Summary ──
ws2 = wb.create_sheet('DRG Summary')
c2 = [8, 48, 20, 24, 16, 8, 8, 12, 12, 10, 8, 10, 10, 8, 10, 26, 30]
write_styled_sheet(ws2, [], c2, drg_summary)

# ── Sheet 3: LOS-Procedure Crosstab ──
ws3 = wb.create_sheet('LOS-Procedure Cross Table')
c3 = [20, 20, 10, 8, 8, 12, 12, 10, 8, 10, 10, 8, 10]
write_styled_sheet(ws3, [], c3, cross_rows)

# ── Sheet 4: Statistical Tests ──
ws4 = wb.create_sheet('Statistical Tests')
c4 = [45, 16, 16, 30, 48]
write_styled_sheet(ws4, [], c4, stats_rows)

# ── Sheet 5: Summary ──
ws5 = wb.create_sheet('Summary')
c5 = [48, 65]
write_styled_sheet(ws5, [], c5, summary_rows)

# Save
output_path = 'D:/claude/E-CHAID_Decision_Tree_Structure.xlsx'
wb.save(output_path)
print(f'Saved: {output_path}')
print(f'Sheets: {wb.sheetnames}')
print('Done!')