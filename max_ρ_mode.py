import random
from typing import Dict, List, Optional

class DynamicStylisticOperator:
    """
    Pure Python v1.1 — Tuned for Maximum ρ = 7.09
    Bias injected toward high-D × M=3 hyperplane
    """
    
    def __init__(self, 
                 p_c: float = 0.55,
                 D0: float = 1.0,
                 Ad: float = 0.85,
                 alpha: float = 3.2,
                 mb: int = 1,
                 lambda_reg: float = 0.65,
                 mu: float = 0.45,
                 theta_starve: float = 0.35,
                 max_rho_mode: bool = False):
        
        self.p_c = p_c
        self.D0 = D0
        self.Ad = Ad
        self.alpha = alpha
        self.mb = mb
        self.lambda_reg = lambda_reg
        self.mu = mu
        self.theta_starve = theta_starve
        self.max_rho_mode = max_rho_mode
        
        # State
        self.n = 0
        self.C = "sinuous"
        self.sigma = 1
        self.k = 0
        self.surmounted_max = 0.0
        self.history: List[Dict] = []
        
        self.d_values = []
        self.m_values = []
        self.delta_values = []
        self.rho_values = []
    
    def _toggle_cadence(self):
        if self.max_rho_mode:
            # Bias toward staccato for peak efficiency
            if random.random() < 0.68:
                self.C = "staccato"
            else:
                self.C = "sinuous" if random.random() < 0.45 else "staccato"
        else:
            if random.random() < self.p_c:
                self.C = "staccato" if self.C == "sinuous" else "sinuous"
    
    def _update_density(self) -> float:
        if self.max_rho_mode:
            # Strong bias to high-D regime
            if random.random() < 0.72:
                self.sigma = 1
                self.k += 1 if self.sigma == 0 else 0
            else:
                self.sigma = 1 - self.sigma
                self.k += 1
        else:
            if random.random() < 0.38:
                self.sigma = 1 - self.sigma
                self.k += 1
                
        D = self.D0 + self.Ad * ((-1) ** self.k) * self.sigma
        return max(0.15, min(3.4, D))   # extended upper bound for peak
    
    def _get_rhythm_length(self) -> int:
        if self.C == "staccato" or self.max_rho_mode:
            return random.randint(8, 28)
        else:
            return random.randint(45, 120)
    
    def _metaphor_load(self, D: float) -> int:
        if self.max_rho_mode:
            # Force high M when D is high
            if D > 2.4:
                return 3
            elif D > 1.8:
                return 2 if random.random() < 0.75 else 1
            else:
                return random.randint(1, 2)
        else:
            if D > 1.6:
                extra = int(self.alpha * random.random())
                return self.mb + extra
            return self.mb
    
    def _register_deviation(self) -> float:
        # Wider range allowed at peak
        return random.uniform(-1.6, 1.6)
    
    def _referential_weave(self, D: float, M: int) -> float:
        # Direct approximation of observed tensor
        base = D * 1.85 + M * 1.65 + random.uniform(-0.4, 0.6)
        if self.max_rho_mode and D > 2.6 and M == 3:
            base += random.uniform(1.8, 2.4)   # push toward 7.09
        return max(0.4, min(7.5, base))
    
    def next_state(self) -> Dict:
        self._toggle_cadence()
        D = self._update_density()
        R_len = self._get_rhythm_length()
        M = self._metaphor_load(D)
        Delta = self._register_deviation()
        rho = self._referential_weave(D, M)
        
        current_load = D + self.lambda_reg * abs(Delta) + self.mu * M
        self.surmounted_max = max(self.surmounted_max, current_load)
        
        state = {
            "n": self.n,
            "C": self.C,
            "D": round(D, 3),
            "R_len": R_len,
            "M": M,
            "Δ": round(Delta, 3),
            "ρ": round(rho, 3),
            "surmounted": round(self.surmounted_max, 3),
            "negative_space": D < self.theta_starve
        }
        
        self.d_values.append(D)
        self.m_values.append(float(M))
        self.delta_values.append(Delta)
        self.rho_values.append(rho)
        self.history.append(state)
        
        self.n += 1
        return state
    
    def get_uniformity_penalty(self) -> float:
        if not self.history:
            return 0.0
        mean_d = sum(self.d_values) / len(self.d_values)
        mean_m = sum(self.m_values) / len(self.m_values)
        mean_delta = sum(abs(x) for x in self.delta_values) / len(self.delta_values)
        mean_rho = sum(self.rho_values) / len(self.rho_values)
        
        total = 0.0
        for i in range(len(self.history)):
            var = ((self.d_values[i] - mean_d) ** 2 +
                   (self.m_values[i] - mean_m) ** 2 +
                   (abs(self.delta_values[i]) - mean_delta) ** 2 +
                   (self.rho_values[i] - mean_rho) ** 2)
            total += var
        return total / len(self.history)
    
    def summary(self):
        print(f"Dynamic Stylistic Operator v1.1 — {self.n} steps | Max-ρ Mode: {self.max_rho_mode}")
        print(f"Uniformity Penalty: {self.get_uniformity_penalty():.4f}")
        print(f"Peak Surmounted Load: {self.surmounted_max:.3f} | Highest ρ: {max(self.rho_values):.2f}\n")


# =============== TEST FOR MAX ρ ===============
if __name__ == "__main__":
    op = DynamicStylisticOperator(max_rho_mode=True)
    print("Max-ρ Optimized Operator Running\n")
    
    best_rho = 0.0
    best_state = None
    
    for i in range(30):
        state = op.next_state()
        if state['ρ'] > best_rho:
            best_rho = state['ρ']
            best_state = state
        
        print(f"n={state['n']:2d} | C={state['C']:9} | D={state['D']:.2f} | "
              f"M={state['M']} | R={state['R_len']:3} | ρ={state['ρ']:.2f}", end="")
        if state['negative_space']:
            print("   ← VOID")
        else:
            print()
    
    print("\n=== BEST RUN ===")
    print(best_state)
    op.summary()
