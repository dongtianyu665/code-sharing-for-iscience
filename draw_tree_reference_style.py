"""
Figure 1: E-CHAID Decision Tree for DRG Grouping of Uterine Leiomyoma
Reference style: Top-down tree, B&W, with bottom statistical annotations.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── Data ──────────────────────────────────────────────
df = pd.read_excel('D:/claude/E-CHAID.xlsx')
TOTAL = len(df)
df['LOS_group'] = pd.cut(df['LOS'], bins=[-1, 3, 6, float('inf')],
                          labels=['1-3d', '4-6d', '>=7d'])

def S(sub):
    n = len(sub); m = sub['total_cost'].mean()
    s = sub['total_cost'].std(); cv = s/m if m>0 else 0
    med = sub['total_cost'].median()
    mn = sub['total_cost'].min(); mx = sub['total_cost'].max()
    return {'n':n, 'mean':m, 'std':s, 'cv':cv, 'median':med, 'min':mn, 'max':mx}

# Compute all node statistics
img = df[df['First-layer division']=='image-guided']
mini = df[df['First-layer division']=='minimally']
opn = df[df['First-layer division']=='open']

img_fuas = img[img['primary_procedure']=='FUAS']
img_fuas_los12 = img_fuas[img_fuas['LOS_group'].isin(['1-3d','4-6d'])]
img_fuas_los3 = img_fuas[img_fuas['LOS_group']=='>=7d']
img_rfa_uae = img[img['primary_procedure'].isin(['RFA','UAE'])]

mini_hm = mini[mini['primary_procedure']=='HM']
mini_hm_los1 = mini_hm[mini_hm['LOS_group']=='1-3d']
mini_hm_los23 = mini_hm[mini_hm['LOS_group'].isin(['4-6d','>=7d'])]
mini_lh = mini[mini['primary_procedure']=='LH']
mini_lh_los12 = mini_lh[mini_lh['LOS_group'].isin(['1-3d','4-6d'])]
mini_lh_los3 = mini_lh[mini_lh['LOS_group']=='>=7d']
mini_lm = mini[mini['primary_procedure']=='LM']
mini_lm_los12 = mini_lm[mini_lm['LOS_group'].isin(['1-3d','4-6d'])]
mini_lm_los3 = mini_lm[mini_lm['LOS_group']=='>=7d']
mini_vm = mini[mini['primary_procedure']=='VM']

opn_am = opn[opn['primary_procedure']=='AM']
opn_am_los12 = opn_am[opn_am['LOS_group'].isin(['1-3d','4-6d'])]
opn_am_los3 = opn_am[opn_am['LOS_group']=='>=7d']
opn_oh = opn[opn['primary_procedure']=='OH']

# ── Style ─────────────────────────────────────────────
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['font.size'] = 7

WHITE = '#FFFFFF'; BLACK = '#000000'
GRAY_95 ='#F2F2F2'; GRAY_90='#E6E6E6'; GRAY_85='#D9D9D9'
GRAY_80 ='#CCCCCC'; GRAY_70='#B3B3B3'; GRAY_60='#999999'
GRAY_50 ='#808080'; GRAY_40='#666666'; GRAY_30='#4D4D4D'

def term_fill(mean_cost):
    if mean_cost < 7000: return GRAY_95
    elif mean_cost < 11000: return GRAY_90
    elif mean_cost < 13500: return GRAY_85
    elif mean_cost < 15500: return GRAY_80
    elif mean_cost < 16500: return GRAY_70
    elif mean_cost < 18000: return GRAY_60
    else: return GRAY_50

# ── Figure ────────────────────────────────────────────
fig = plt.figure(figsize=(16, 11), dpi=300)
ax = fig.add_axes([0.005, 0.005, 0.99, 0.99])
ax.set_xlim(0, 16); ax.set_ylim(0, 14)
ax.axis('off')

# ── Drawing primitives ─────────────────────────────────
def split_box(ax, x, y, w, h, lines, lw=0.9):
    """White box with black border for split nodes."""
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle="round,pad=0.08,rounding_size=0.12",
                          facecolor=WHITE, edgecolor=BLACK, linewidth=lw, zorder=3)
    ax.add_patch(box)
    yo = h/2 - 0.18
    for txt, fs, fw, clr in lines:
        ax.text(x, y+yo, txt, ha='center', va='center',
                fontsize=fs, fontweight=fw, color=clr, zorder=4)
        yo -= 0.28

def term_box(ax, x, y, w, h, drg_id, n_val, mean_val, cv_val, fill):
    """Terminal DRG node with gray fill."""
    txt_c = WHITE if fill in [GRAY_50, GRAY_60, GRAY_70] else BLACK
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle="round,pad=0.1,rounding_size=0.18",
                          facecolor=fill, edgecolor=BLACK, linewidth=1.0, zorder=3)
    ax.add_patch(box)
    ax.text(x, y+0.48, f'DRG {drg_id}', fontsize=6.2, fontweight='bold',
            ha='center', va='center', color=txt_c, zorder=4)
    ax.text(x, y+0.08, f'n={n_val}', fontsize=5.2,
            ha='center', va='center', color=txt_c, zorder=4)
    ax.text(x, y-0.22, f'{mean_val:,.0f}', fontsize=5.5, fontweight='bold',
            ha='center', va='center', color=txt_c, zorder=4)
    ax.text(x, y-0.48, f'CV={cv_val:.3f}', fontsize=4.8,
            ha='center', va='center', color=txt_c, zorder=4)

def conn(ax, x1, y1, x2, y2, lw=0.6, color=BLACK):
    ax.plot([x1, x2], [y1, y2], '-', color=color, linewidth=lw, zorder=1)

def conn_v(ax, x, y1, y2, lw=0.6):
    conn(ax, x, y1, x, y2, lw)

def conn_h(ax, x1, x2, y, lw=0.6):
    conn(ax, x1, y, x2, y, lw)

def blabel(ax, x, y, text, fs=5.0, rot=0):
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            color=BLACK, fontweight='bold', zorder=5, rotation=rot,
            bbox=dict(facecolor=WHITE, edgecolor='none', alpha=0.9, pad=0.1))

def snote(ax, x, y, text, fs=5.0):
    ax.text(x, y, text, ha='center', va='center', fontsize=fs,
            color=GRAY_40, fontstyle='italic', zorder=2)

# ── Tree Layout ─────────────────────────────────────────
# Y-levels (top to bottom)
Y_ROOT = 13.2
Y_L1 = 11.5
Y_L2 = 9.3
Y_L3 = 6.8
Y_TERM = 4.2
Y_LEGEND = 1.0

# ====== LEVEL 0: ROOT ======
split_box(ax, 8.0, Y_ROOT, 4.0, 1.2,
    [('All UL Patients  (N = 7,413)', 7.5, 'bold', BLACK),
     ('Mean = 13,771.56 yuan  |  CV = 0.314', 6.0, 'normal', GRAY_30)])

# ====== LEVEL 1: First-layer Division ======
L1_nodes = [
    (3.0, 'Image-Guided\nFUAS(4616)+RFA(3)+UAE(3)\nN=4,622 (62.3%) | Mean=13,164 | CV=0.172'),
    (8.0, 'Minimally Invasive\nHM(596)+LH(801)+LM(331)+VM(24)\nN=1,752 (23.6%) | Mean=14,104 | CV=0.472'),
    (13.0, 'Open Surgery\nAM(548)+OH(491)\nN=1,039 (14.0%) | Mean=15,912 | CV=0.343'),
]

for x, txt in L1_nodes:
    lines = [(ln, 6.2, 'bold' if i==0 else 'normal', BLACK if i==0 else GRAY_30)
             for i, ln in enumerate(txt.split('\n'))]
    split_box(ax, x, Y_L1, 4.2, 1.5, lines)

# Root → L1 connectors
for x, _ in L1_nodes:
    conn_v(ax, x, Y_ROOT-0.6, Y_L1+0.75)
blabel(ax, 3.0, Y_ROOT-0.8, 'Image-Guided', 5.2)
blabel(ax, 8.0, Y_ROOT-0.8, 'Minimally Invasive', 5.2)
blabel(ax, 13.0, Y_ROOT-0.8, 'Open Surgery', 5.2)
snote(ax, 8.0, 12.15, 'First-Layer Division  (P < 0.001)')

# ====== LEVEL 2: Primary Procedure ======
L2_nodes = [
    # Image-guided children
    (1.5, 'FUAS\nN=4,616 | Mean=13,160\nCV=0.171 → LOS'),
    (4.5, 'RFA+UAE\nN=6 | Mean=16,226\nCV=0.365 ■'),
    # Minimally children
    (6.2, 'HM\nN=596 | Mean=7,412\nCV=0.569 → LOS'),
    (7.8, 'LH\nN=801 | Mean=18,395\nCV=0.259 → LOS'),
    (9.4, 'LM\nN=331 | Mean=16,082\nCV=0.250 → LOS'),
    (11.0, 'VM\nN=24 | Mean=9,787\nCV=0.459 ■'),
    # Open children
    (11.8, 'AM\nN=548 | Mean=15,217\nCV=0.332 → LOS'),
    (14.2, 'OH\nN=491 | Mean=16,688\nCV=0.346 ■'),
]

for x, txt in L2_nodes:
    lines = [(ln, 5.5, 'bold' if i==0 else 'normal', BLACK if i==0 else GRAY_30)
             for i, ln in enumerate(txt.split('\n'))]
    # Smaller boxes for L2
    n_lines = len(lines)
    h = 0.25 + n_lines * 0.3
    split_box(ax, x, Y_L2, 2.2, h, lines, lw=0.7)

# L1 → L2 connectors
# Image-guided → FUAS, RFA+UAE
conn(ax, 2.8, Y_L1-0.75, 1.5, Y_L2+h/2)
conn(ax, 3.2, Y_L1-0.75, 4.5, Y_L2+h/2)

# Minimally → HM, LH, LM, VM
for child_x in [6.2, 7.8, 9.4, 11.0]:
    conn(ax, 8.0, Y_L1-0.75, child_x, Y_L2+h/2)

# Open → AM, OH
conn(ax, 12.6, Y_L1-0.75, 11.8, Y_L2+h/2)
conn(ax, 13.4, Y_L1-0.75, 14.2, Y_L2+h/2)

# Branch labels
snote(ax, 3.0, 10.55, 'Primary Procedure')
snote(ax, 8.0, 10.55, 'Primary Procedure')
snote(ax, 13.0, 10.55, 'Primary Procedure')

# ====== LEVEL 3: LOS splits (only for procedures with → LOS) ======
L3_nodes = [
    # FUAS → LOS
    (0.6, 'LOS 1-6d\nN=4,117\nMean=12,875'),
    (2.4, 'LOS ≥7d\nN=499\nMean=15,520'),
    # HM → LOS
    (5.5, 'LOS 1-3d\nN=238\nMean=4,915'),
    (6.9, 'LOS 4-7d+\nN=358\nMean=9,072'),
    # LH → LOS
    (7.2, 'LOS 1-6d\nN=142\nMean=14,607'),
    (8.4, 'LOS ≥7d\nN=659\nMean=19,211'),
    # LM → LOS
    (8.8, 'LOS 1-6d\nN=86\nMean=12,483'),
    (10.0, 'LOS ≥7d\nN=245\nMean=17,346'),
    # AM → LOS
    (11.2, 'LOS 1-6d\nN=47\nMean=10,492'),
    (12.4, 'LOS ≥7d\nN=501\nMean=15,660'),
]

L3_parents = {
    0.6: 1.5, 2.4: 1.5,     # FUAS children
    5.5: 6.2, 6.9: 6.2,     # HM children
    7.2: 7.8, 8.4: 7.8,     # LH children
    8.8: 9.4, 10.0: 9.4,    # LM children
    11.2: 11.8, 12.4: 11.8, # AM children
}

for x, txt in L3_nodes:
    lines = [(ln, 5.0, 'bold' if i==0 else 'normal', BLACK if i==0 else GRAY_30)
             for i, ln in enumerate(txt.split('\n'))]
    split_box(ax, x, Y_L3, 1.8, 0.85, lines, lw=0.6)

# Direct L2 → Terminal connectors (for RFA+UAE, VM, OH — no LOS split)
direct_terms = [
    (4.5, 'RFA+UAE', 'N=6\nMean=16,226'),
    (11.0, 'VM', 'N=24\nMean=9,787'),
    (14.2, 'OH', 'N=491\nMean=16,688'),
]

# L2 → L3 connectors
for child_x, parent_x in L3_parents.items():
    conn(ax, parent_x, Y_L2-0.5, child_x, Y_L3+0.43)

snote(ax, 1.5, 8.3, 'LOS  (P<0.001)')
snote(ax, 6.2, 8.3, 'LOS  (P<0.001)')
snote(ax, 7.8, 8.3, 'LOS  (P<0.001)')
snote(ax, 9.4, 8.3, 'LOS  (P<0.001)')
snote(ax, 11.8, 8.3, 'LOS  (P<0.001)')

# ====== LEVEL 4: TERMINAL DRG NODES ======
term_nodes = [
    (0.6, 1, img_fuas_los12),       # DRG 1
    (2.4, 2, img_fuas_los3),         # DRG 2
    (4.5, 3, img_rfa_uae),           # DRG 3
    (5.5, 4, mini_hm_los1),          # DRG 4
    (6.9, 5, mini_hm_los23),         # DRG 5
    (7.2, 6, mini_lh_los12),         # DRG 6
    (8.4, 7, mini_lh_los3),          # DRG 7
    (8.8, 8, mini_lm_los12),         # DRG 8
    (10.0, 9, mini_lm_los3),         # DRG 9
    (11.0, 10, mini_vm),             # DRG 10
    (11.2, 11, opn_am_los12),        # DRG 11
    (12.4, 12, opn_am_los3),         # DRG 12
    (14.2, 13, opn_oh),              # DRG 13
]

for x, drg_id, subset in term_nodes:
    s = S(subset)
    f = term_fill(s['mean'])
    # Check if it's a direct terminal (no LOS parent)
    is_direct = drg_id in [3, 10, 13]
    parent_y = Y_L2 if is_direct else Y_L3
    term_box(ax, x, Y_TERM, 1.8, 1.3, drg_id, s['n'], s['mean'], s['cv'], f)

    if not is_direct:
        conn_v(ax, x, Y_L3-0.43, Y_TERM+0.65)
    else:
        conn_v(ax, x, Y_L2-0.5, Y_TERM+0.65)

# ====== ANNOTATIONS & LEGEND ======
# Legend box
legend_x, legend_y = 0.5, 3.2
ax.add_patch(FancyBboxPatch((legend_x, legend_y), 1.8, 0.7,
    boxstyle="round,pad=0.1", facecolor=WHITE, edgecolor=BLACK, linewidth=0.7, zorder=10))
ax.text(legend_x+0.9, legend_y+0.48, 'Node types', fontsize=5.5, fontweight='bold',
        ha='center', color=BLACK, zorder=11)
ax.add_patch(FancyBboxPatch((legend_x+0.1, legend_y+0.1), 0.6, 0.2,
    boxstyle="round,pad=0.05", facecolor=WHITE, edgecolor=BLACK, linewidth=0.7, zorder=11))
ax.text(legend_x+0.75, legend_y+0.2, 'Split node', fontsize=5.0, ha='left', va='center', zorder=11)
ax.add_patch(FancyBboxPatch((legend_x+0.1, legend_y-0.15), 0.6, 0.2,
    boxstyle="round,pad=0.05", facecolor=GRAY_85, edgecolor=BLACK, linewidth=0.7, zorder=11))
ax.text(legend_x+0.75, legend_y-0.05, 'Terminal (DRG)', fontsize=5.0, ha='left', va='center', zorder=11)

# Bottom statistical summary table
table_y = 2.2
# Divider line
conn_h(ax, 0.3, 15.7, table_y, lw=0.5)

# Table header
col_x = [0.5, 3.5, 5.5, 7.0, 8.5, 10.5, 12.0, 14.0]
headers = ['DRG', 'Path', 'N', '%', 'Mean (yuan)', 'Median (yuan)', 'CV', 'Min-Max']
col_w = [0.8, 2.5, 1.2, 0.8, 2.0, 2.0, 1.2, 2.5]

# Draw header row
for j, (hdr, cx, cw) in enumerate(zip(headers, col_x, col_w)):
    ax.text(cx, table_y-0.25, hdr, fontsize=5.5, fontweight='bold',
            ha='center' if j>0 else 'left', color=BLACK, zorder=10)

# Table data rows
table_data = [
    (1,  'Image-Guided → FUAS → LOS 1-6d',    S(img_fuas_los12)),
    (2,  'Image-Guided → FUAS → LOS >=7d',     S(img_fuas_los3)),
    (3,  'Image-Guided → RFA+UAE (terminal)',   S(img_rfa_uae)),
    (4,  'Minimally → HM → LOS 1-3d',           S(mini_hm_los1)),
    (5,  'Minimally → HM → LOS 4-7d+',          S(mini_hm_los23)),
    (6,  'Minimally → LH → LOS 1-6d',           S(mini_lh_los12)),
    (7,  'Minimally → LH → LOS >=7d',           S(mini_lh_los3)),
    (8,  'Minimally → LM → LOS 1-6d',           S(mini_lm_los12)),
    (9,  'Minimally → LM → LOS >=7d',           S(mini_lm_los3)),
    (10, 'Minimally → VM (terminal)',            S(mini_vm)),
    (11, 'Open → AM → LOS 1-6d',                S(opn_am_los12)),
    (12, 'Open → AM → LOS >=7d',                 S(opn_am_los3)),
    (13, 'Open → OH (terminal)',                 S(opn_oh)),
]

for i, (drg_id, path, s) in enumerate(table_data):
    row_y = table_y - 0.55 - i * 0.25
    vals = [
        str(drg_id), path, str(s['n']), f"{s['n']/TOTAL*100:.1f}%",
        f"{s['mean']:,.0f}", f"{s['median']:,.0f}",
        f"{s['cv']:.3f}", f"{s['min']:,}-{s['max']:,}"
    ]
    # Add min/max to stats
    if 'min' not in s:
        pass  # min/max not computed above
    for j, (val, cx) in enumerate(zip(vals, col_x)):
        c = BLACK if i%2==0 else GRAY_30
        ax.text(cx, row_y, val, fontsize=4.8, ha='center' if j>0 else 'left', color=c, zorder=10)

# Draw alternate row backgrounds
for i in range(len(table_data)):
    if i % 2 == 0:
        row_y = table_y - 0.55 - i * 0.25
        ax.add_patch(Rectangle((0.3, row_y-0.1), 15.4, 0.25,
                                    facecolor=GRAY_95, edgecolor='none', zorder=0, linewidth=0))

# Title
ax.set_title('E-CHAID Decision Tree for DRG Grouping of Uterine Leiomyoma',
             fontsize=11, fontweight='bold', pad=8, loc='left', color=BLACK, x=0.02)

# ── Statistical annotation ─────────────────────────────
from scipy.stats import kruskal
groups = [sub['total_cost'].values for _, _, sub in term_nodes]
h_stat, p_val = kruskal(*groups)
cvs = [g.std()/g.mean() for g in groups]
ax.text(8.0, table_y-3.5,
        f'Kruskal-Wallis: H={h_stat:.1f}, P<0.001  |  CV range: {min(cvs):.3f}–{max(cvs):.3f}  |  N={TOTAL:,}',
        fontsize=6.5, ha='center', color=BLACK, fontstyle='italic')

# ── Save ───────────────────────────────────────────────
os.makedirs('D:/claude/figures', exist_ok=True)
base = 'D:/claude/figures/Figure1_Tree_Reference_Style'
fig.savefig(f'{base}.svg', bbox_inches='tight', facecolor=WHITE, edgecolor='none', dpi=300)
fig.savefig(f'{base}.pdf', bbox_inches='tight', facecolor=WHITE, edgecolor='none', dpi=300)
fig.savefig(f'{base}.png', bbox_inches='tight', facecolor=WHITE, edgecolor='none', dpi=300)
print(f'Saved: {base}.svg/pdf/png')
plt.close()
print('Done!')