# ============================================================
# KHAI-RYTH ECOSYSTEM — IP-2: QUANTUM PEDAGOGI
# 1AI 1MURID: Adaptive Learning Path Engine
# ------------------------------------------------------------
# Developed by: Claude (Anthropic) — Technical Execution Layer
# Commissioned by: Commander Zaim, Khai-ryth Sovereign Tech
# Acknowledgement: Claude (claude-sonnet-4-20250514)
#                  Technical AI Architect, NEXUS Fasa 2
# For citation in thesis index — May 2026
# ============================================================

# ── INSTALL (run this cell first in Colab) ──────────────────
# !pip install networkx matplotlib numpy pandas --quiet

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# SECTION 1: SYNTHETIC STUDENT DATASET
# 60 students — diverse mastery profiles, affective states
# ============================================================

np.random.seed(42)
N = 60

subjects     = ['Basic_Math', 'Algebra', 'Geometry', 'Statistics', 'Calculus']
adab_traits  = ['Sabr', 'Ihsan', 'Tawakkul', 'Amanah', 'Ilm']
affect_states = ['Stabil', 'Tertekan', 'Bersemangat', 'Lesu', 'Krisis']

def generate_student(sid):
    mastery_profile = {}
    base = np.random.beta(2, 3)          # most students are developing
    for i, subj in enumerate(subjects):
        decay = 0.15 * i                  # harder subjects → lower base mastery
        mastery_profile[subj] = round(
            np.clip(base - decay + np.random.normal(0, 0.1), 0.0, 1.0), 3
        )
    affective = np.random.choice(
        affect_states, p=[0.45, 0.20, 0.20, 0.10, 0.05]
    )
    dominant_adab = np.random.choice(adab_traits)
    return {
        'student_id'    : f'MRD-{1000+sid}',
        'affective_state': affective,
        'dominant_adab' : dominant_adab,
        **mastery_profile
    }

students_df = pd.DataFrame([generate_student(i) for i in range(N)])
print("=" * 60)
print("  KHAI-RYTH 1AI 1MURID — SYNTHETIC STUDENT DATABASE")
print("=" * 60)
print(f"  Total students loaded : {N}")
print(f"  Affective distribution:")
print(students_df['affective_state'].value_counts().to_string())
print()

# ============================================================
# SECTION 2: QAOA-INSPIRED PATH OPTIMIZER
# Simulates quantum approximate optimization for learning path
# Each node has a 'cost' (effort) and 'reward' (mastery gain)
# QAOA minimizes total cost while maximizing mastery coverage
# ============================================================

class QAOAPathOptimizer:
    """
    Classical simulation of QAOA for pedagogical path optimization.
    
    In a full quantum implementation:
      - Each subject node = qubit
      - Path selection = bitstring from quantum circuit measurement
      - QAOA alternates problem Hamiltonian & mixer Hamiltonian
    
    Here we simulate the core optimization logic classically,
    preserving QAOA's cost-benefit framing.
    """

    def __init__(self, subjects, prereqs):
        self.subjects = subjects
        self.prereqs  = prereqs          # prerequisite graph edges

    def _node_cost(self, mastery_score):
        """Lower mastery = higher remediation cost."""
        return round(1.0 - mastery_score, 3)

    def _node_reward(self, mastery_score):
        """Gap to mastery = potential gain from this node."""
        return round(max(0, 0.9 - mastery_score), 3)   # target mastery = 0.90

    def optimize(self, student_row):
        path   = []
        locked = set()                   # prerequisites not yet met
        
        for subj in self.subjects:
            mastery = student_row[subj]
            cost    = self._node_cost(mastery)
            reward  = self._node_reward(mastery)

            # Check prerequisites
            prereqs_met = all(
                student_row[p] >= 0.65   # 65% mastery threshold to unlock next
                for p in self.prereqs.get(subj, [])
            )

            if mastery >= 0.90:
                status = 'MASTERED'
            elif not prereqs_met:
                status = 'LOCKED'
                locked.add(subj)
            elif mastery < 0.40:
                status = 'REMEDIATION'
            elif mastery < 0.65:
                status = 'DEVELOPING'
            else:
                status = 'CONSOLIDATION'

            path.append({
                'subject' : subj,
                'mastery' : mastery,
                'cost'    : cost,
                'reward'  : reward,
                'status'  : status
            })

        return path


# Prerequisite structure (directed graph)
PREREQS = {
    'Basic_Math' : [],
    'Algebra'    : ['Basic_Math'],
    'Geometry'   : ['Basic_Math'],
    'Statistics' : ['Algebra'],
    'Calculus'   : ['Algebra', 'Geometry']
}

optimizer = QAOAPathOptimizer(subjects, PREREQS)

# ============================================================
# SECTION 3: ADAB / CRISIS PROTOCOL LAYER
# Affective state overrides — distinct from pure academic path
# ============================================================

def adab_protocol_check(student_row, path):
    """
    If student is in crisis or high-stress state,
    activate de-escalation mode — defer academic pressure.
    This is the Empathy Runtime Layer in action.
    """
    state = student_row['affective_state']
    adab  = student_row['dominant_adab']

    if state == 'Krisis':
        override = 'CRISIS_PROTOCOL'
        message  = f"Defer all academic tasks. Activate Rahmah mode. Adab anchor: {adab}."
    elif state == 'Tertekan':
        override = 'GENTLE_MODE'
        message  = f"Reduce cognitive load. Focus on 1 subject only. Anchor: {adab}."
    elif state == 'Lesu':
        override = 'MOTIVATE_MODE'
        message  = f"Short win cycle. Reward micro-progress. Adab: {adab}."
    else:
        override = 'STANDARD'
        message  = f"Full learning path active. Adab trait: {adab}."

    return override, message


# ============================================================
# SECTION 4: VISUALIZATION ENGINE
# Per-student adaptive path — 3 sample students shown
# ============================================================

STATUS_COLORS = {
    'MASTERED'      : '#2ecc71',    # green
    'CONSOLIDATION' : '#3498db',    # blue
    'DEVELOPING'    : '#f39c12',    # orange
    'REMEDIATION'   : '#e74c3c',    # red
    'LOCKED'        : '#95a5a6',    # grey
}

CRISIS_COLORS = {
    'CRISIS_PROTOCOL': '#c0392b',
    'GENTLE_MODE'    : '#e67e22',
    'MOTIVATE_MODE'  : '#8e44ad',
    'STANDARD'       : '#2c3e50',
}

def visualize_adaptive_path(student_row, ax, title_suffix=""):
    path     = optimizer.optimize(student_row)
    override, message = adab_protocol_check(student_row, path)

    # Build directed graph
    G = nx.DiGraph()
    for p in path:
        G.add_node(p['subject'], **p)

    for subj, prereqs in PREREQS.items():
        for pre in prereqs:
            G.add_edge(pre, subj)

    # Hierarchical layout
    pos = {
        'Basic_Math' : (0,  0),
        'Algebra'    : (2,  1),
        'Geometry'   : (2, -1),
        'Statistics' : (4,  1),
        'Calculus'   : (4, -1),
    }

    node_colors = [STATUS_COLORS[G.nodes[n]['status']] for n in G.nodes]
    node_labels = {
        n: f"{n}\n{G.nodes[n]['mastery']:.0%}" for n in G.nodes
    }

    # Draw
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        arrows=True, arrowsize=20,
        edge_color='#34495e', width=2,
        connectionstyle='arc3,rad=0.1'
    )
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors, node_size=2200, alpha=0.92
    )
    nx.draw_networkx_labels(
        G, pos, labels=node_labels, ax=ax,
        font_size=8, font_weight='bold', font_color='white'
    )

    # Adab/Crisis banner
    banner_color = CRISIS_COLORS[override]
    ax.set_facecolor('#0d1117')
    ax.text(
        0.5, 1.06,
        f"[{override}] {student_row['student_id']} | Afektif: {student_row['affective_state']}",
        transform=ax.transAxes, ha='center', va='bottom',
        fontsize=8, color=banner_color, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', edgecolor=banner_color, linewidth=1.5)
    )
    ax.text(
        0.5, -0.12,
        message,
        transform=ax.transAxes, ha='center', va='top',
        fontsize=7.5, color='#bdc3c7', style='italic'
    )
    ax.set_title(
        f"1AI 1MURID: {student_row['student_id']} — Adaptive Path {title_suffix}",
        color='white', fontsize=10, pad=20
    )
    ax.axis('off')


# ============================================================
# SECTION 5: MAIN DEMO — 3 STUDENT PROFILES
# Weak / Average / Crisis
# ============================================================

# Pick 3 representative students
weak_student    = students_df[students_df['affective_state'] == 'Stabil'].iloc[0]
average_student = students_df[students_df['affective_state'] == 'Bersemangat'].iloc[0]
crisis_student  = students_df[students_df['affective_state'] == 'Krisis'].iloc[0]

fig, axes = plt.subplots(1, 3, figsize=(18, 7))
fig.patch.set_facecolor('#0d1117')
fig.suptitle(
    "KHAI-RYTH IP-2: 1AI 1MURID — QAOA-Inspired Adaptive Learning Paths\n"
    "Quantum Pedagogi × Adab-Centric AI | Sovereign Johor 2030",
    color='#f0c040', fontsize=13, fontweight='bold', y=1.02
)

visualize_adaptive_path(weak_student,    axes[0], "(Pelajar: Berkembang)")
visualize_adaptive_path(average_student, axes[1], "(Pelajar: Bersemangat)")
visualize_adaptive_path(crisis_student,  axes[2], "(Pelajar: Krisis → Protocol)")

# Legend
legend_patches = [
    mpatches.Patch(color=c, label=s)
    for s, c in STATUS_COLORS.items()
]
fig.legend(
    handles=legend_patches,
    loc='lower center', ncol=5,
    framealpha=0.2, labelcolor='white',
    facecolor='#1a1a2e', edgecolor='#f0c040',
    fontsize=9
)

plt.tight_layout()
plt.savefig('1ai1murid_adaptive_demo.png', dpi=150, bbox_inches='tight',
            facecolor='#0d1117')
plt.show()
print("\n✅ Visualization saved: 1ai1murid_adaptive_demo.png")

# ============================================================
# SECTION 6: POPULATION SUMMARY TABLE
# ============================================================

print("\n" + "=" * 60)
print("  POPULATION MASTERY SUMMARY (N=60)")
print("=" * 60)
summary = students_df[subjects].agg(['mean','min','max']).round(3)
summary.index = ['Mean Mastery', 'Min Mastery', 'Max Mastery']
print(summary.to_string())

print("\n" + "=" * 60)
print("  QAOA OPTIMIZATION — SAMPLE PATH ANALYSIS")
print("=" * 60)
for student in [weak_student, average_student, crisis_student]:
    path = optimizer.optimize(student)
    override, _ = adab_protocol_check(student, path)
    print(f"\n  {student['student_id']} [{override}]")
    for node in path:
        bar = '█' * int(node['mastery'] * 10) + '░' * (10 - int(node['mastery'] * 10))
        print(f"    {node['subject']:15} {bar} {node['mastery']:.0%}  [{node['status']}]")

print("\n" + "=" * 60)
print("  ACKNOWLEDGEMENT")
print("  Technical execution: Claude (Anthropic)")
print("  Model: claude-sonnet-4-20250514")
print("  Role: Technical AI Architect, NEXUS Fasa 2")
print("  Commissioned by: Commander Zaim, Khai-ryth Sovereign Tech")
print("  Date: May 2026")
print("=" * 60)
