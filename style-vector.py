import re
import numpy as np
from typing import List, Dict
import statistics

class FunctionalVector:
    """
    Computes V_bar = [C, D, R, M, Δ, ρ] for stylistic functional commentary.
    Fully implements your defined framework.
    """
    
    def compute(self, text: str) -> Dict[str, float]:
        """Main entry point: returns the 6D style vector"""
        if not text or not text.strip():
            return {'C': 0.0, 'D': 0.0, 'R': 0.0, 'M': 0.0, 'Delta': 0.0, 'rho': 0.0}
        
        sentences = self._split_sentences(text)
        words = self._tokenize(text)
        
        vector = {
            'C':     self._cadence(sentences),           # Staccato vs Sinuous
            'D':     self._diction_density(words),       # Diction density
            'R':     self._rhythm(sentences),            # Average rhythm/length
            'M':     self._metaphor_load(text, words),   # Metaphor load
            'Delta': self._register_deviation(sentences, words),  # Register deviation
            'rho':   self._surmounted_diction(words)     # Surmounted diction density
        }
        return {k: round(v, 4) for k, v in vector.items()}
    
    def _split_sentences(self, text: str) -> List[str]:
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text.lower())
    
    # ── Component Implementations ─────────────────────────────────────
    
    def _cadence(self, sentences: List[str]) -> float:
        """Average cadence: proportion of staccato (short) vs sinuous (flowing)"""
        if not sentences:
            return 0.5
        lengths = [len(s.split()) for s in sentences]
        staccato_ratio = sum(1 for l in lengths if l < 9) / len(sentences)
        return round(staccato_ratio, 4)
    
    def _diction_density(self, words: List[str]) -> float:
        """Lexical density: unique words / total words"""
        if not words:
            return 0.0
        return len(set(words)) / len(words)
    
    def _rhythm(self, sentences: List[str]) -> float:
        """Average sentence rhythm/length (normalized)"""
        if not sentences:
            return 0.0
        lengths = [len(s.split()) for s in sentences]
        avg = statistics.mean(lengths)
        return min(max((avg - 4) / 28, 0.0), 1.0)  # scales roughly 4–32 words
    
    def _metaphor_load(self, text: str, words: List[str]) -> float:
        """Metaphor/simile density heuristic"""
        if not words:
            return 0.0
        simile_markers = len(re.findall(r'\b(like|as|seems?|appears?|metaphor|symbol|echoes?)\b', text.lower()))
        return min(simile_markers * 3.0 / len(words), 1.0)
    
    def _register_deviation(self, sentences: List[str], words: List[str]) -> float:
        """Variance in sentence length + word complexity"""
        if not sentences or not words:
            return 0.0
        sent_var = np.var([len(s.split()) for s in sentences]) if len(sentences) > 1 else 0
        word_var = np.var([len(w) for w in words]) if len(words) > 1 else 0
        combined = (sent_var + word_var * 2) / 40
        return min(combined, 1.0)
    
    def _surmounted_diction(self, words: List[str]) -> float:
        """Density of complex / elevated vocabulary"""
        if not words:
            return 0.0
        complex_words = sum(1 for w in words if len(w) > 8 or bool(re.search(r'[xqz]', w)))
        return complex_words / len(words)
