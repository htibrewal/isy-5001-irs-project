from dotenv import load_dotenv

from blocks.PurchaseOrder import PurchaseOrder
from blocks.Vendor import Vendor
from load_data import load_purchase_order_data, fetch_vendors, fetch_electrical_parts, fetch_vendor_items, \
    build_line_items
from muliple_vendors import multi_genetic_algorithm, multi_fitness_score
from single_vendor import single_genetic_algorithm, single_fitness_score

load_dotenv()

def main():
    electrical_parts = fetch_electrical_parts()
    print(f"No of electrical parts = {len(electrical_parts.keys())}")

    # load purchase order data
    purchase_order_data = load_purchase_order_data()

    # build objects
    vendors: dict[str, Vendor] = fetch_vendors(purchase_order_data)
    print(f"No of vendors = {len(vendors.keys())}")

    items_vendor_map = fetch_vendor_items(purchase_order_data, electrical_parts, vendors)

    buyer_order = {'17833': 4, '17437': 10, '18087': 2, '15102': 15}
    purchase_order = PurchaseOrder(build_line_items(buyer_order, electrical_parts))

    # Trying multiple vendors solution
    multi_vendors_solution = multi_genetic_algorithm(purchase_order, items_vendor_map)

    for electrical_part, vendor_item in multi_vendors_solution.items():
        print(f"{electrical_part} -> {vendor_item.vendor}")

    cost = -1 * multi_fitness_score(purchase_order, multi_vendors_solution)
    print(f"Cost = {cost: .2f}")


    # Trying single vendor solution
    single_vendor_solution = single_genetic_algorithm(purchase_order, items_vendor_map, list(vendors.values()))
    print(single_vendor_solution)

    cost = -1 * single_fitness_score(purchase_order, single_vendor_solution, items_vendor_map)
    print(f"Cost = {cost: .2f}")


if __name__ == '__main__':
    main()