from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from blocks.ElectricalPart import ElectricalPart
from blocks.PurchaseOrder import PurchaseOrder
from blocks.VendorItem import VendorItem
from optimisation_type import OptimisationType


def compute_overall_score(
    score_dict: dict[ElectricalPart, float],
    optimisation: OptimisationType = OptimisationType.COST
) -> float | int:
    if score_dict is None:
        return float('inf')

    if optimisation == OptimisationType.COST:
        return -1 * np.sum(np.array(list(score_dict.values())))
    else:
        return -1 * round(np.max(np.array(list(score_dict.values()))))


class GA(ABC):
    def __init__(
            self,
            items_vendor_map: dict[ElectricalPart, list[VendorItem]],
            population_size: int = 50,
            generations: int = 50
    ):
        self.items_vendor_map = items_vendor_map
        self.population_size = population_size
        self.generations = generations

    @abstractmethod
    def solve(
            self,
            purchase_order: PurchaseOrder,
            optimisation: OptimisationType = OptimisationType.COST
    ) -> Any:
        pass
