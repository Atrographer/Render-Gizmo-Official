import hashlib
from decimal import Decimal, getcontext
from collections import defaultdict
import Levenshtein

getcontext().prec = 28

class KernelDivisionBridge:
    def __init__(self):
        self.psi = Decimal('0.1503378808')
        self.Re_tau = Decimal('1.4129651365')
        self.cos_psi_given = Decimal('0.9887205')
        self.sin_Re_tau_given = Decimal('0.98768834059')
        self.numerator = self.cos_psi_given * self.Re_tau
        self.K = self.numerator / self.sin_Re_tau_given
        self.k_norm = Decimal(1) / self.K
        print("=== JCR KERNEL DIVISION BRIDGE ACTIVATED ===")

    def scale_dot_product(self, reg_accum: int):
        accum_dec = Decimal(reg_accum)
        result = accum_dec * self.k_norm
        return int(result.quantize(Decimal('1.')))


class LocalPrngCell:
    def __init__(self, cell_id, initial_seed):
        self.REG_LOCAL_STATE = int(initial_seed)
        self.REG_LOCAL_INDEX = 0
        self.HEX_A = 0x5851F42D4C957F2D
        self.HEX_C = 0x14057B7EF767814F
        self.HEX_M_MASK = 0xFFFFFFFFFFFFFFFF

    def step_register_clock(self):
        step1 = self.REG_LOCAL_STATE * self.HEX_A
        step2 = step1 + self.HEX_C
        self.REG_LOCAL_STATE = step2 & self.HEX_M_MASK
        self.REG_LOCAL_INDEX += 1
        return self.REG_LOCAL_INDEX, self.REG_LOCAL_STATE


class GlobalPrngIndex:
    def __init__(self):
        self.GLOBAL_INDEX = 0
        self.global_cells = {0x8000: LocalPrngCell(0x8000, 0xC10C6THEE2026)}
        print("=== GLOBAL PRNG INDEX ACTIVATED ===")

    def advance_global_clock(self, steps: int = 1):
        for _ in range(steps):
            self.GLOBAL_INDEX += 1
            for cell in self.global_cells.values():
                cell.step_register_clock()
        return self.GLOBAL_INDEX


class ProofTheoreticEngine:
    def derive(self, conclusion: str):
        return {"status": "success", "chain": "⊢ ↝ ⊨_p ↝ T"}


class GizmoEngine:
    def __init__(self, db_data):
        self.global_prng = GlobalPrngIndex()
        self.proof_engine = ProofTheoreticEngine()
        self.dictionary = db_data.get("dictionary", {})
        self.thesaurus = db_data.get("thesaurus", {})
        self.bridge = KernelDivisionBridge()

    def lookup(self, word: str):
        self.global_prng.advance_global_clock(1)
        word_lower = word.lower().strip()

        # Fuzzy matching
        best_match = None
        best_score = 0
        for key in self.dictionary:
            score = Levenshtein.ratio(word_lower, key)
            if score > best_score:
                best_score = score
                best_match = key

        if best_match and best_score > 0.7:
            entry = self.dictionary[best_match]
            response = f"**{best_match.title()}** ({entry['pos']})\n\n{entry['definition']}\n\nSource: {entry['source']}"
            proof = self.proof_engine.derive(best_match)
            response += f"\n\nProof Chain: {proof.get('chain')} | Global Index: {self.global_prng.GLOBAL_INDEX}"
            return response

        if word_lower in self.thesaurus:
            return f"**{word}** (thesaurus)\n\nSynonyms: {', '.join(self.thesaurus[word_lower])}\nGlobal Index: {self.global_prng.GLOBAL_INDEX}"

        return f"No strong match for '{word}'. Global Index: {self.global_prng.GLOBAL_INDEX}"
