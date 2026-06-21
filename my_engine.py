import random
from typing import Dict, Any

class StyleEngine:
    """
    Core refinement engine expected by WordWeaver.
    Provides the .refine() method that WORD-WEAVER_CODE calls.
    """
    
    def __init__(self):
        self.refinement_intensity = 0.7
        self.variation_seed = random.randint(1000, 9999)
    
    def refine(self, text: str, state: Dict[str, Any] = None) -> str:
        """
        Post-process and polish the generated paragraph.
        This is the method WordWeaver expects.
        """
        if not text:
            return text
        
        # Basic cleanup
        text = text.strip()
        if not text.endswith(('.', '!', '?', '—')):
            text = text + "."
        
        # Light stylistic refinement based on state
        if state and random.random() < self.refinement_intensity:
            # Add subtle cadence enhancement
            if state.get("cadence") == "staccato":
                text = text.replace(", ", ". ")
            
            # Occasional elevated flourish
            if random.random() < 0.35:
                flourishes = ["", " — indeed.", " Yet it persists.", " In the fracture between."]
                text = text.rstrip(".") + random.choice(flourishes)
        
        return text
    
    def process(self, text: str) -> str:
        """Alternative entry point for broader use"""
        return self.refine(text)
    
    def __call__(self, text: str, **kwargs):
        """Make it callable for flexibility"""
        return self.refine(text, kwargs)


# ====================== QUICK TEST ======================
if __name__ == "__main__":
    engine = StyleEngine()
    sample = "Liminal vectors fracture the consensus mirror."
    print("Original:", sample)
    print("Refined: ", engine.refine(sample))
