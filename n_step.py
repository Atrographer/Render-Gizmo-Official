import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== DATA ====================
data = {
    'n': list(range(1,21)),
    'C': ['staccato','sinuous','sinuous','staccato','sinuous','sinuous','staccato',
          'staccato','staccato','sinuous','staccato','staccato','sinuous','sinuous',
          'staccato','sinuous','staccato','sinuous','sinuous','staccato'],
    'D': [0.25,2.49,0.25,2.64,0.25,3.35,0.25,2.84,0.25,2.92,0.25,2.96,0.25,3.25,
          0.25,2.65,0.25,2.77,0.25,3.28],
    'R': [11,73,92,15,74,52,15,23,10,135,24,13,78,133,10,64,28,72,59,25],
    'M': [0,3,0,1,0,1,0,3,2,1,0,1,1,2,0,1,0,1,0,3],
    'Δ': [-0.90,-1.07,-0.48,-0.84,-0.54,1.10,-0.16,-1.12,-1.36,-0.99,0.88,-1.20,
          -0.55,0.76,0.83,0.68,1.46,1.45,-1.80,-0.18],
    'ρ': [1.37,6.67,0.85,4.65,0.93,5.68,0.46,7.09,3.85,5.11,1.35,5.42,1.89,6.10,
          1.29,4.45,2.07,5.53,2.50,6.36],
    'Peak_ρ': [7.09]*20
}

df = pd.DataFrame(data)

# ==================== SUMMARY ====================
print("Summary Statistics")
print(df[['D','R','M','Δ','ρ']].describe().round(2))

print("\nBy Type (C):")
print(df.groupby('C')[['D','R','M','Δ','ρ']].mean().round(2))

# ==================== PLOTS ====================
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top-left: ρ vs D by type
sns.scatterplot(data=df, x='D', y='ρ', hue='C', style='C', s=100, ax=axes[0,0])
axes[0,0].set_title('ρ vs D by Type')

# Top-right: ρ vs R by type
sns.scatterplot(data=df, x='R', y='ρ', hue='C', style='C', s=100, ax=axes[0,1])
axes[0,1].set_title('ρ vs R by Type')

# Bottom-left: Distribution of Δ
sns.histplot(data=df, x='Δ', hue='C', kde=True, multiple="stack", ax=axes[1,0])
axes[1,0].set_title('Distribution of Δ')

# Bottom-right: Boxplot of ρ by type
sns.boxplot(data=df, x='C', y='ρ', ax=axes[1,1])
axes[1,1].set_title('ρ by Type')

plt.tight_layout()
plt.savefig('analysis_plots.png', dpi=200, bbox_inches='tight')
plt.show()

# Optional: correlations
print("\nCorrelations with ρ:")
print(df[['D','R','M','Δ','ρ']].corr()['ρ'].round(3))
