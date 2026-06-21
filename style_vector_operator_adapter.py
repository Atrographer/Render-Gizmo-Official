# style_vector_operator_adapter.py
# Clean port for FunctionalVector + DynamicStylisticOperator
import random
from typing import Dict, Optional, Tuple, Any

try:
    from style_vector_engine_CODE import FunctionalVector
    from actively_varying_equation import DynamicStylisticOperator
    from word_weaver_CODE import WordWeaver
except ImportError:
    # Fallback imports
    from Proper_LLM_Diction_Output.style_vector_engine_CODE import FunctionalVector
    from Proper_LLM_Diction_Output.actively_varying_equation import DynamicStylisticOperator
    from Proper_LLM_Diction_Output.word_weaver_CODE import WordWeaver


class StyleVectorOperatorAdapter:
    """
    Clean, easy-to-port adapter focused on:
    - Style Vector analysis (FunctionalVector)
    - Vector Operator dynamics (DynamicStylisticOperator)
    - Easy integration with your AI / LLM pipeline
    """
    
    def __init__(self, max_rho_mode: bool = False, seed: int = 42):
        self.vector_engine = FunctionalVector()
        self.operator = DynamicStylisticOperator()
        self.weaver = WordWeaver()  # full pipeline
        self.max_rho_mode = max_rho_mode
        random.seed(seed)
        
        # Default target vector (normalized 0-1 or appropriate ranges)
        self.target_vector = {"C": 0.6, "D": 1.8, "R": 0.65, "M": 0.8, "Delta": 0.5, "rho": 0.85}

    def analyze_vector(self, text: str) -> Dict[str, float]:
        """Compute full 6D style vector for any input text."""
        return self.vector_engine.compute(text)

    def apply_operator_step(self) -> Dict:
        """Advance the dynamic stylistic operator by one state."""
        return self.operator.next_state()

    def generate_with_vector_control(self, core_idea: str = "", num_paragraphs: int = 3) -> Tuple[str, Dict]:
        """Generate text using operator + weaver, then analyze vector."""
        if self.max_rho_mode:
            # Bias toward high impact via multiple operator steps
            for _ in range(3):
                self.operator.next_state()
        
        result = self.weaver.generate_with_vector(num_paragraphs=num_paragraphs)
        text = result["text"]
        vector = self.analyze_vector(text)
        
        return text, vector

    def enhance_text(self, original_text: str, target: Optional[Dict] = None) -> Tuple[str, Dict]:
        """Post-process any LLM output with style vector mechanics."""
        # Run operator for dynamic variation
        state = self.apply_operator_step()
        
        # Use weaver to refine / re-weave with stylistic control
        enhanced = self.weaver.generate_text(core_idea=original_text, num_paragraphs=2)
        
        vector = self.analyze_vector(enhanced)
        
        return enhanced, vector

    def prompt_with_style_vector(self, base_prompt: str, vector: Optional[Dict] = None) -> str:
        """Inject vector-aware instructions into a prompt."""
        v = vector or self.target_vector
        instr = (
            f"Respond using high-ρ stylistic vector control: "
            f"Cadence \~{v.get('C',0.6):.1f} (mix sinuous/staccato), "
            f"Density \~{v.get('D',1.8):.1f}, Metaphor load \~{v.get('M',0.8):.1f}, "
            f"with rhythmic variation, register shifts (Δ), and negative space. "
            f"Maximize surmounted diction impact while avoiding uniformity."
        )
        return f"{base_prompt}\n\n{instr}"

    def get_operator_summary(self):
        """Print current operator state and uniformity penalty."""
        self.operator.summary()
