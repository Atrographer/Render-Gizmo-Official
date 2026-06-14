import random
import math

# ==================== ORIGINAL DATA ====================
data = [
    {"n":1,  "C":"staccato", "D":0.25, "R":11,  "M":0,  "Δ":-0.90, "ρ":1.37},
    {"n":2,  "C":"sinuous",  "D":2.49, "R":73,  "M":3,  "Δ":-1.07, "ρ":6.67},
    {"n":3,  "C":"sinuous",  "D":0.25, "R":92,  "M":0,  "Δ":-0.48, "ρ":0.85},
    {"n":4,  "C":"staccato", "D":2.64, "R":15,  "M":1,  "Δ":-0.84, "ρ":4.65},
    {"n":5,  "C":"sinuous",  "D":0.25, "R":74,  "M":0,  "Δ":-0.54, "ρ":0.93},
    {"n":6,  "C":"sinuous",  "D":3.35, "R":52,  "M":1,  "Δ":1.10,  "ρ":5.68},
    {"n":7,  "C":"staccato", "D":0.25, "R":15,  "M":0,  "Δ":-0.16, "ρ":0.46},
    {"n":8,  "C":"staccato", "D":2.84, "R":23,  "M":3,  "Δ":-1.12, "ρ":7.09},
    {"n":9,  "C":"staccato", "D":0.25, "R":10,  "M":2,  "Δ":-1.36, "ρ":3.85},
    {"n":10,"C":"sinuous",  "D":2.92, "R":135, "M":1,  "Δ":-0.99, "ρ":5.11},
    {"n":11,"C":"staccato", "D":0.25, "R":24,  "M":0,  "Δ":0.88,  "ρ":1.35},
    {"n":12,"C":"staccato", "D":2.96, "R":13,  "M":1,  "Δ":-1.20, "ρ":5.42},
    {"n":13,"C":"sinuous",  "D":0.25, "R":78,  "M":1,  "Δ":-0.55, "ρ":1.89},
    {"n":14,"C":"sinuous",  "D":3.25, "R":133, "M":2,  "Δ":0.76,  "ρ":6.10},
    {"n":15,"C":"staccato", "D":0.25, "R":10,  "M":0,  "Δ":0.83,  "ρ":1.29},
    {"n":16,"C":"sinuous",  "D":2.65, "R":64,  "M":1,  "Δ":0.68,  "ρ":4.45},
    {"n":17,"C":"staccato", "D":0.25, "R":28,  "M":0,  "Δ":1.46,  "ρ":2.07},
    {"n":18,"C":"sinuous",  "D":2.77, "R":72,  "M":1,  "Δ":1.45,  "ρ":5.53},
    {"n":19,"C":"sinuous",  "D":0.25, "R":59,  "M":0,  "Δ":-1.80, "ρ":2.50},
    {"n":20,"C":"staccato", "D":3.28, "R":25,  "M":3,  "Δ":-0.18, "ρ":6.36},
]

PEAK_RHO = 7.09

# ==================== HELPER FUNCTIONS ====================
def mean(values):
    return sum(values) / len(values)

def std_dev(values):
    m = mean(values)
    return (sum((x - m) ** 2 for x in values) / len(values)) ** 0.5

# ==================== MONTE CARLO SIMULATION ====================
def monte_carlo_simulation(n_simulations=100_000, noise_level=0.6):
    random.seed(42)  # for reproducibility
    
    simulated_rhos = []
    peak_reached = 0
    high_performers = 0  # ρ >= 6.0
    
    for _ in range(n_simulations):
        # Sample a real run as base
        base = random.choice(data)
        
        # Option 1: Bootstrap + Noise on ρ
        sim_rho = base["ρ"] + random.gauss(0, noise_level)
        
        # Option 2: Stronger model based on D and M (recommended)
        d_effect = base["D"] * 1.85          # from correlation ~0.92
        m_effect = base["M"] * 1.35
        base_pred = 0.4 + d_effect + m_effect
        
        # Blend both approaches
        sim_rho = 0.6 * sim_rho + 0.4 * base_pred
        
        # Add extra stochastic noise
        sim_rho += random.gauss(0, 0.4)
        
        # Bound to realistic range
        sim_rho = max(0.3, min(PEAK_RHO + 0.1, sim_rho))
        
        simulated_rhos.append(sim_rho)
        
        if sim_rho >= PEAK_RHO:
            peak_reached += 1
        if sim_rho >= 6.0:
            high_performers += 1
    
    # Results
    results = {
        "n_simulations": n_simulations,
        "mean_rho": round(mean(simulated_rhos), 3),
        "std_rho": round(std_dev(simulated_rhos), 3),
        "min_rho": round(min(simulated_rhos), 3),
        "max_rho": round(max(simulated_rhos), 3),
        "prob_peak": round(peak_reached / n_simulations, 5),
        "prob_high": round(high_performers / n_simulations, 4),   # P(ρ ≥ 6.0)
        "median_rho": round(sorted(simulated_rhos)[n_simulations//2], 3)
    }
    
    return results


# ==================== RUN THE SIMULATION ====================
if __name__ == "__main__":
    print("Running Monte Carlo Simulation...\n")
    stats = monte_carlo_simulation(n_simulations=100000, noise_level=0.55)
    
    print("MONTE CARLO RESULTS")
    print("=" * 50)
    print(f"Simulations          : {stats['n_simulations']:,}")
    print(f"Mean ρ               : {stats['mean_rho']}")
    print(f"Std Dev ρ            : {stats['std_rho']}")
    print(f"Median ρ             : {stats['median_rho']}")
    print(f"Min ρ                : {stats['min_rho']}")
    print(f"Max ρ                : {stats['max_rho']}")
    print(f"Probability of Peak (ρ=7.09) : {stats['prob_peak']*100:.3f}%")
    print(f"Probability of High (ρ≥6.0)  : {stats['prob_high']*100:.2f}%")
    
    # Distribution summary
    print("\nDistribution Buckets:")
    buckets = [0,1,2,3,4,5,6,7.09]
    counts = [0] * (len(buckets)-1)
    for rho in simulated_rhos:   # Note: this uses the last run's list
        for i in range(len(buckets)-1):
            if buckets[i] <= rho < buckets[i+1]:
                counts[i] += 1
                break
    for i in range(len(counts)):
        pct = counts[i] / stats['n_simulations'] * 100
        print(f"  {buckets[i]:4.1f} - {buckets[i+1]:4.1f} : {pct:5.1f}%")
