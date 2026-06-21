import random
from typing import List, Dict

# ── Your existing modules ─────────────────────────────────────
from actively_varying_equation import DynamicStylisticOperator
from a_z_example_word_bank import WORD_BANK
from my_engine import StyleEngine          # ← your core engine
# from run_api import run_server           # we'll expose via this file if needed


class WordWeaver:
    """
    WordWeaver — connects your DynamicStylisticOperator,
    WORD_BANK, and my_engine into one unified text generator.
    """
    
    def __init__(self):
        # Style driver from your actively-varying-equation
        self.style_operator = DynamicStylisticOperator(
            p_c=0.58,
            D0=1.15,
            Ad=0.95
        )
        
        # Your main engine (my_engine.py)
        self.engine = StyleEngine()
        
        self.word_bank = WORD_BANK
    
    def _pick_word(self, density: float) -> str:
        """Density-aware word selection using your WORD_BANK"""
        candidates = []
        
        if density > 1.8:
            keys = "ACEIMPSV"   # elevated / poetic
        elif density > 1.0:
            keys = "LMORTV"     # medium literary
        else:
            keys = "BFGKW"      # raw / visceral
        
        for k in keys:
            candidates.extend(self.word_bank.get(k, []))
        
        if not candidates:
            candidates = sum((lst for lst in self.word_bank.values()), [])
        
        return random.choice(candidates)
    
    def weave_paragraph(self, idea: str = "") -> str:
        """Generate one stylistically coherent paragraph"""
        state = self.style_operator.next_paragraph_state()
        
        target_length = state.get("rhythm_len", random.randint(8, 22))
        density = state.get("density", 1.15)
        cadence = state.get("cadence", "sinuous")
        
        words = []
        for _ in range(target_length):
            word = self._pick_word(density)
            words.append(word)
            
            # Micro rhythm breaks
            if random.random() < 0.13 * density:
                words.append(random.choice(["—", ",", ";", ":"]))
        
        paragraph = " ".join(words)
        
        # Cadence shaping
        if cadence == "staccato":
            paragraph = paragraph.replace(" ", ". ").capitalize() + "."
        else:
            paragraph = paragraph.capitalize() + "."
        
        # Let your engine post-process if desired
        paragraph = self.engine.refine(paragraph, state)
        
        if state.get("use_negative_space", False):
            paragraph = "\n\n" + paragraph + "\n"
        
        return paragraph.strip()
    
    def generate_text(self, core_idea: str = "", num_paragraphs: int = 5) -> str:
        """Generate full multi-paragraph text"""
        output = []
        for _ in range(num_paragraphs):
            para = self.weave_paragraph(core_idea)
            output.append(para)
            
            if random.random() < 0.22:
                output.append("")   # paragraph spacing
        
        return "\n\n".join(output).strip()
    
    def generate_with_vector(self, num_paragraphs: int = 5) -> Dict:
        """Return generated text + its Functional Vector"""
        try:
            from style_vector_engine_CODE import FunctionalVector
            text = self.generate_text("", num_paragraphs)
            vector = FunctionalVector().compute(text)
            return {"text": text, "vector": vector}
        except Exception as e:
            text = self.generate_text("", num_paragraphs)
            return {"text": text, "vector": f"Vector computation skipped: {e}"}


# ====================== API / RUNNER ======================
def run_weaver_api():
    """Simple entry point compatible with your run_api.py workflow"""
    weaver = WordWeaver()
    
    # Example generation
    result = weaver.generate_with_vector(num_paragraphs=6)
    
    print("\n" + "="*70)
    print(result["text"])
    print("\n" + "="*70)
    print("FUNCTIONAL VECTOR V̄ :", result["vector"])
    print("="*70)
    
    return result


if __name__ == "__main__":
    run_weaver_api()
