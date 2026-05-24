from .synthetic import Synthetic
from .real import Real

__version__ = "0.1.0"
__author__ = "Irsyad Damlis"
__email__ = "irsyad.damlis@gmail.com"
__license__ = "MIT"

# Create module-like objects to support fin.real.calculate_osp() syntax
class RealModule:
    @staticmethod
    def calculate_osp(*args, **kwargs):
        return Real.calculate_osp(*args, **kwargs)
    
    @staticmethod  
    def calculate_income(*args, **kwargs):
        return Real.calculate_income(*args, **kwargs)

class SyntheticModule:
    @staticmethod
    def calculate_osp(*args, **kwargs):
        return Synthetic.calculate_osp(*args, **kwargs)
    
    @staticmethod
    def calculate_income(*args, **kwargs):
        return Synthetic.calculate_income(*args, **kwargs)

# Create instances that can be imported
real = RealModule()
synthetic = SyntheticModule()

__all__ = ["Synthetic", "Real", "real", "synthetic"]
