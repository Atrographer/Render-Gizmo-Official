import random
from typing import Dict, List

class DynamicStylisticOperator:
    """
    Pure Python implementation of the taught Core Equation:
    V(n) = (C(n), D(n), R(n), M(n), Δ(n), ρ(n))
    """
    
    def __init__(self, 
                 p_c: float = 0.55,      # cadence toggle bias
                 D0: float = 1.0,        # base diction density
                 Ad: float = 0.85,       # density amplitude
                 alpha: float = 3.2,     # metaphor multiplier
                 mb: int = 1,            # base metaphor load
                 lambda_reg: float = 0.65,
                 mu: float = 0.45,
                 theta_starve: float = 0.35):
        
        self.p_c = p_c
        self.D0 = D0
        self.Ad = Ad
        self.alpha = alpha
        self.mb = mb
        self.lambda_reg = lambda_reg
        self.mu = mu
        self.theta_starve = theta_starve
        
        # State
        self.n = 0
        self.C = "sinuous"
        self.sigma = 1
        self.k = 0
        self.surmounted_max = 0.0
        self.history: List[Dict] = []
        
        # For uniformity penalty calculation
        self.d_values = []
        self.m_values = []
        self.delta_values = []
        self.rho_values = []
    
    def _toggle_cadence(self):
        if random.random() < self.p_c:
            self.C = "staccato" if self.C == "sinuous" else "sinuous"
    
    def _update_density(self) -> float:
        if random.random() < 0.38:
            self.sigma = 1 - self.sigma
            self.k += 1
        D = self.D0 + self.Ad * ((-1) ** self.k) * self.sigma
        return max(0.15, min(2.8, D))
    
    def _get_rhythm_length(self) -> int:
        if self.C == "staccato":
            return random.randint(8, 25)
        else:
            return random.randint(45, 120)
    
    def _metaphor_load(self, D: float) -> int:
        if D > 1.6:
            extra = int(self.alpha * random.random())
            return self.mb + extra
        return self.mb
    
    def _register_deviation(self) -> float:
        return random.uniform(-1.4, 1.4)
    
    def _referential_weave(self) -> float:
        return random.uniform(0.4, 3.5)
    
    def _mean(self, lst: List[float]) -> float:
        return sum(lst) / len(lst) if lst else 0.0
    
    def _variance_term(self) -> float:
        if not self.history:
            return 0.0
        mean_d = self._mean(self.d_values)
        mean_m = self._mean(self.m_values)
        mean_delta = self._mean([abs(x) for x in self.delta_values])
        mean_rho = self._mean(self.rho_values)
        
        total = 0.0
        for i in range(len(self.history)):
            var = ((self.d_values[i] - mean_d) ** 2 +
                   (self.m_values[i] - mean_m) ** 2 +
                   (abs(self.delta_values[i]) - mean_delta) ** 2 +
                   (self.rho_values[i] - mean_rho) ** 2)
            total += var
        return total / len(self.history)
    
    def next_state(self) -> Dict:
        self._toggle_cadence()
        D = self._update_density()
        R_len = self._get_rhythm_length()
        M = self._metaphor_load(D)
        Delta = self._register_deviation()
        rho = self._referential_weave()
        
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
        
        # Record for uniformity penalty
        self.d_values.append(D)
        self.m_values.append(float(M))
        self.delta_values.append(Delta)
        self.rho_values.append(rho)
        self.history.append(state)
        
        self.n += 1
        return state
    
    def get_uniformity_penalty(self) -> float:
        """Approximates the Anti-Uniformity Constraint"""
        return self._variance_term()
    
    def summary(self):
        print(f"Dynamic Stylistic Operator Active — {self.n} steps")
        print(f"Uniformity Penalty: {self.get_uniformity_penalty():.4f}")
        print(f"Peak Surmounted Load: {self.surmounted_max:.3f}\n")


# =============== TEST RUN ===============
if __name__ == "__main__":
    op = DynamicStylisticOperator()
    print("Pure Python Dynamic Stylistic Variation Operator Initialized\n")
    
    for i in range(15):
        state = op.next_state()
        print(f"n={state['n']:2d} | C={state['C']:9} | D={state['D']:.2f} | "
              f"R={state['R_len']:3} | M={state['M']} | Δ={state['Δ']:+.2f} | "
              f"ρ={state['ρ']:.2f} | Peak={state['surmounted']:.2f}", end="")
        if state['negative_space']:
            print("   ← VOID")
        else:
            print()
    
    op.summary()
