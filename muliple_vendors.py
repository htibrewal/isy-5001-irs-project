import random

from blocks.ElectricalPart import ElectricalPart
from blocks.PurchaseOrder import PurchaseOrder
from blocks.VendorItem import VendorItem


def initialise_population(purchase_order: PurchaseOrder, items_vendor_map: dict[ElectricalPart, list[VendorItem]], population_size: int):
    population = []
    for _ in range(population_size):
        chromosome: dict[ElectricalPart, VendorItem] = {}
        for line_item in purchase_order.line_items:
            electrical_part, _ = line_item
            chromosome[electrical_part] = random.choice(items_vendor_map[electrical_part])

        population.append(chromosome)
    return population


def multi_fitness_score(purchase_order: PurchaseOrder, chromosome: dict[ElectricalPart, VendorItem]):
    total_cost = 0
    for line_item in purchase_order.line_items:
        electrical_part, quantity = line_item
        vendor_item = chromosome[electrical_part]

        total_cost += vendor_item.calculate_price(quantity)

    return -total_cost


def crossover(parent1: dict[ElectricalPart, VendorItem], parent2: dict[ElectricalPart, VendorItem]):
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


def mutate(chromosome: dict[ElectricalPart, VendorItem], items_vendor_map: dict[ElectricalPart, list[VendorItem]]):
    mutation_point = random.randint(0, len(chromosome) - 1)
    electrical_part = list(chromosome.keys())[mutation_point]

    chromosome[electrical_part] = random.choice(items_vendor_map[electrical_part])


def multi_genetic_algorithm(purchase_order: PurchaseOrder, items_vendor_map: dict[ElectricalPart, list[VendorItem]], population_size: int = 50, generations: int = 20) -> dict[ElectricalPart, VendorItem]:
    population = initialise_population(purchase_order, items_vendor_map, population_size)

    for generation in range(generations):
        population = sorted(population, key=lambda chromo: multi_fitness_score(purchase_order, chromo))

        # Selecting the top 2 chromosomes (Can be changed)
        next_population = population[:2]

        while len(next_population) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)
            child1, child2 = crossover(parent1, parent2)

            mutate(child1, items_vendor_map)
            mutate(child2, items_vendor_map)

            next_population.extend([child1, child2])

        population = next_population

    # return the top solution with the best fitness score
    return sorted(population, key=lambda chromo: multi_fitness_score(purchase_order, chromo))[0]

