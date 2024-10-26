import random
from blocks.ElectricalPart import ElectricalPart
from blocks.PurchaseOrder import PurchaseOrder
from blocks.VendorItem import VendorItem
from genetic_algorithm import GA, compute_overall_score
from optimisation_type import OptimisationType


class MultiVendorGA(GA):
    def __init__(self, items_vendor_map: dict[ElectricalPart, list[VendorItem]]):
        super().__init__(items_vendor_map)


    def _initialise_population(self, purchase_order: PurchaseOrder) -> list[dict[ElectricalPart, VendorItem]]:
        population = []
        for _ in range(self.population_size):
            chromosome: dict[ElectricalPart, VendorItem] = {}
            for line_item in purchase_order.line_items:
                electrical_part, _ = line_item
                chromosome[electrical_part] = random.choice(self.items_vendor_map[electrical_part])

            population.append(chromosome)
        return population


    def _get_fitness_score(
        self,
        purchase_order: PurchaseOrder,
        chromosome: dict[ElectricalPart, VendorItem],
        optimisation: OptimisationType = OptimisationType.COST
    ) -> dict[ElectricalPart, float]:
        score = dict()
        for line_item in purchase_order.line_items:
            electrical_part, quantity = line_item
            vendor_item = chromosome[electrical_part]

            score[electrical_part] = vendor_item.calculate_price(quantity)\
                if optimisation == OptimisationType.COST\
                else vendor_item.get_delivery_days()

        return score


    def compute_fitness_score(
        self,
        purchase_order: PurchaseOrder,
        chromosome: dict[ElectricalPart, VendorItem],
        optimisation: OptimisationType = OptimisationType.COST
    ) -> float:
        score_dict = self._get_fitness_score(purchase_order, chromosome, optimisation)
        return compute_overall_score(score_dict, optimisation)


    def _crossover(
        self,
        parent1: dict[ElectricalPart, VendorItem],
        parent2: dict[ElectricalPart, VendorItem]
    ):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1, child2 = {}, {}

        electrical_parts = list(parent1.keys())
        for i, electrical_part in enumerate(electrical_parts):
            if i < crossover_point:
                child1[electrical_part] = parent1[electrical_part]
                child2[electrical_part] = parent2[electrical_part]
            else:
                child1[electrical_part] = parent2[electrical_part]
                child2[electrical_part] = parent1[electrical_part]

        return child1, child2


    def _mutate(self, chromosome: dict[ElectricalPart, VendorItem]):
        mutation_point = random.randint(0, len(chromosome) - 1)
        electrical_part = list(chromosome.keys())[mutation_point]

        chromosome[electrical_part] = random.choice(self.items_vendor_map[electrical_part])


    def solve(
        self,
        purchase_order: PurchaseOrder,
        optimisation: OptimisationType = OptimisationType.COST
    ) -> dict[ElectricalPart, VendorItem]:
        population = self._initialise_population(purchase_order)

        for generation in range(self.generations):
            population = sorted(population, key=lambda chromo: self.compute_fitness_score(purchase_order, chromo, optimisation))

            # Selecting the top 2 chromosomes (Can be changed)
            next_population = population[:2]

            while len(next_population) < self.population_size:
                parent1, parent2 = random.sample(population[:10], 2)
                child1, child2 = self._crossover(parent1, parent2)

                self._mutate(child1)
                self._mutate(child2)

                next_population.extend([child1, child2])

            population = next_population

        # return the top solution with the best fitness score
        return sorted(population, key=lambda chromo: self.compute_fitness_score(purchase_order, chromo, optimisation))[0]
