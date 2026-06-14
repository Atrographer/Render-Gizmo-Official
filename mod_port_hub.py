"""
mod_port_hub.py
Universal Porting Hub / Adapter System
Allows seamless bidirectional communication between any modules 
(WordWeaver, my_engine, style_vector, p_Tensor, actively_varying_equation, etc.)
"""

import importlib
from typing import Dict, Any, Callable, Optional

class ModPortHub:
    """
    Central porting module. You only add ports here.
    Then everything can talk to everything else.
    """
    
    def __init__(self):
        self.ports: Dict[str, Any] = {}
        self.filters: Dict[str, Callable] = {}   # modfilter system
    
    def register_port(self, name: str, instance: Any) -> None:
        """Register any object/module as a port"""
        self.ports[name] = instance
        print(f"[PortHub] Registered port: {name}")
    
    def get_port(self, name: str) -> Any:
        """Get a registered port"""
        return self.ports.get(name)
    
    def connect(self, source_port: str, target_port: str, method_map: Optional[Dict[str, str]] = None):
        """Create bidirectional bridge between two ports"""
        src = self.get_port(source_port)
        tgt = self.get_port(target_port)
        
        if not src or not tgt:
            print(f"[PortHub] Warning: Cannot connect {source_port} <-> {target_port}")
            return
        
        # Auto-connect common methods if they exist
        common_methods = ["generate", "compute", "next_state", "refine", "weave", "process"]
        
        for method in common_methods:
            if hasattr(src, method) and hasattr(tgt, method):
                setattr(src, f"to_{target_port}", lambda *a, **k: getattr(tgt, method)(*a, **k))
                setattr(tgt, f"from_{source_port}", lambda *a, **k: getattr(src, method)(*a, **k))
    
    def add_filter(self, filter_name: str, func: Callable):
        """Add to modfilter system"""
        self.filters[filter_name] = func
        print(f"[PortHub] Added modfilter: {filter_name}")
    
    def apply_filter(self, filter_name: str, data: Any, **kwargs):
        """Run data through a registered modfilter"""
        if filter_name in self.filters:
            return self.filters[filter_name](data, **kwargs)
        return data
    
    def auto_discover_and_port(self):
        """Attempt to auto-import and register common modules"""
        modules_to_try = [
            ("word_weaver", "WordWeaver"),
            ("my_engine", "StyleEngine"),
            ("style_vector", "FunctionalVector"),
            ("actively_varying_equation", "DynamicStylisticOperator"),
            ("p_Tensor", "PTensor"),
            ("max_p_mode", "MaxPMode"),
        ]
        
        for mod_name, class_name in modules_to_try:
            try:
                module = importlib.import_module(mod_name)
                if hasattr(module, class_name):
                    instance = getattr(module, class_name)()
                    self.register_port(mod_name.replace("_", "-"), instance)
                elif hasattr(module, "__name__"):
                    self.register_port(mod_name.replace("_", "-"), module)
            except Exception:
                pass  # Module not ready or doesn't have default constructor


# ====================== GLOBAL HUB INSTANCE ======================
PortHub = ModPortHub()

# Example usage when you import this mod:
if __name__ == "__main__":
    # Auto discover
    PortHub.auto_discover_and_port()
    
    # Manual registration example:
    # from word_weaver import WordWeaver
    # PortHub.register_port("weaver", WordWeaver())
    
    print("PortHub initialized. Available ports:", list(PortHub.ports.keys()))
