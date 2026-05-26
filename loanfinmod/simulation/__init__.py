from .synthetic import Synthetic
from .real import Real
from importlib.metadata import version, author, email, license

__version__ = version("loanfinmod")
__author__ = author("loanfinmod")
__email__ = email("loanfinmod")
__license__ = license("loanfinmod")

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
