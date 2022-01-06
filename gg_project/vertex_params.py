""" Contains types used to store vertex parameters
"""

from dataclasses import dataclass
from enum import Enum


class VertexType(str, Enum):
    """Describes the type of a vertex"""

    START = "S"
    START_USED = "s"
    EXTERIOR = "E"
    INTERIOR = "I"
    INTERIOR_USED = "i"


@dataclass(eq=True)
class VertexParams:
    """Contains internal parameters of a vertex"""

    vertex_type: VertexType
    position: tuple[float, float]
    level: int
