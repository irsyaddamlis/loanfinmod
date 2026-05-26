from .synthetic import Synthetic
from .real import Real
from importlib.metadata import version

__version__ = version("loanfinmod")
__author__ = "Irsyad Damlis"
__email__ = "irsyad.damlis@gmail.com"
__license__ = "MIT"

# Create module-like objects to support fin.real.calculate_osp() syntax
class RealModule:
    calculate_osp = Real.calculate_osp
    calculate_income = Real.calculate_income

class SyntheticModule:
    calculate_osp = Synthetic.calculate_osp
    calculate_income = Synthetic.calculate_income

# Create instances that can be imported
real = RealModule()
synthetic = SyntheticModule()

__all__ = ["Synthetic", "Real", "real", "synthetic"]
