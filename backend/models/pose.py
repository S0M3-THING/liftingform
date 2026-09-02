from dataclasses import dataclass


@dataclass
class Landmark:
    x: float
    y: float
    z: float
    visibility: float