
from .real import Real
from .synthetic import Synthetic


# Create module-like objects to support fin.real.calculate_osp() syntax
class RealModule:
    calculate_osp = staticmethod(Real.calculate_osp)
    calculate_income = staticmethod(Real.calculate_income)

class SyntheticModule:
    calculate_osp = staticmethod(Synthetic.calculate_osp)
    calculate_income = staticmethod(Synthetic.calculate_income)

# Create instances that can be imported
real = RealModule()
synthetic = SyntheticModule()
initiation = synthetic

__all__ = ["Synthetic",
           "Real",
           "real",
           "initiation"]
