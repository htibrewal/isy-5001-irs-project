import random

from blocks.ElectricalPart import ElectricalPart
from blocks.PurchaseOrder import PurchaseOrder
from blocks.Vendor import Vendor
from blocks.VendorItem import VendorItem


def initialise_population(vendors: list[Vendor], population_size: int):
    population = []
    for _ in range(population_size):
        population.append(random.choice(vendors))
    return population


def single_fitness_score(purchase_order: PurchaseOrder, vendor: Vendor, items_vendor_map: dict[ElectricalPart, list[VendorItem]]):
    total_cost = 0
    for line_item in purchase_order.line_items:
        electrical_part, quantity = line_item
        vendor_items = [vendor_item for vendor_item in items_vendor_map[electrical_part] if vendor_item.vendor == vendor]

        if vendor_items and len(vendor_items) == 1:
            total_cost += vendor_items[0].calculate_price(quantity)
        else:
            return float('inf')

    return -total_cost


def single_genetic_algorithm(purchase_order: PurchaseOrder, items_vendor_map: dict[ElectricalPart, list[VendorItem]], vendors: list[Vendor], population_size: int = 50, generations: int = 20) -> Vendor:
    population = initialise_population(vendors, population_size)

    for generation in range(generations):
        population = sorted(population, key=lambda vendor: single_fitness_score(purchase_order, vendor, items_vendor_map))

        next_population = population[:2]

        while len(next_population) < population_size:
            child1 = random.choice(vendors)
            child2 = random.choice(vendors)
            next_population.extend([child1, child2])

        population = next_population

    return sorted(population, key=lambda vendor: single_fitness_score(purchase_order, vendor, items_vendor_map))[0]

