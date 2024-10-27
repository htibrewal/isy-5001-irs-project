import random
from blocks.ElectricalPart import ElectricalPart
from blocks.PurchaseOrder import PurchaseOrder
from blocks.Vendor import Vendor
from blocks.VendorItem import VendorItem
from genetic_algorithm import GA, compute_overall_score
from optimisation_type import OptimisationType


class SingleVendorGA(GA):
    def __init__(self, items_vendor_map: dict[ElectricalPart, list[VendorItem]], vendors: list[Vendor]):
        super().__init__(items_vendor_map)
        self.vendors = vendors


    def _initialise_population(self) -> list[Vendor]:
        population = []
        for _ in range(self.population_size):
            population.append(random.choice(self.vendors))
        return population


    def _get_fitness_score(
        self,
        purchase_order: PurchaseOrder,
        vendor: Vendor,
        optimisation: OptimisationType = OptimisationType.COST
    ) -> dict[ElectricalPart, float] | None:
        score = dict()
        for line_item in purchase_order.line_items:
            electrical_part, quantity = line_item
            vendor_items = [vendor_item for vendor_item in self.items_vendor_map[electrical_part] if
                            vendor_item.vendor == vendor]

            if vendor_items and len(vendor_items) == 1:
                score[electrical_part] = vendor_items[0].calculate_price(quantity)\
                    if optimisation == OptimisationType.COST\
                    else vendor_items[0].get_delivery_days()
            else:
                return None

        return score


    def compute_fitness_score(
        self,
        purchase_order: PurchaseOrder,
        vendor: Vendor,
        optimisation: OptimisationType = OptimisationType.COST
    ) -> float | int:
        score_dict = self._get_fitness_score(purchase_order, vendor, optimisation)
        return compute_overall_score(score_dict, optimisation)


    def solve(
        self,
        purchase_order: PurchaseOrder,
        optimisation: OptimisationType = OptimisationType.COST
    ) -> Vendor:
        population = self._initialise_population()

        for generation in range(self.generations):
            population = sorted(population, key=lambda vendor: self.compute_fitness_score(purchase_order, vendor,optimisation))

            next_population = population[:2]

            while len(next_population) < self.population_size:
                child1 = random.choice(self.vendors)
                child2 = random.choice(self.vendors)
                next_population.extend([child1, child2])

            population = next_population

        return sorted(population, key=lambda vendor: self.compute_fitness_score(purchase_order, vendor, optimisation))[0]