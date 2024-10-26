from dotenv import load_dotenv

from blocks.PurchaseOrder import PurchaseOrder
from blocks.Vendor import Vendor
from load_data import load_purchase_order_data, fetch_vendors, fetch_electrical_parts, fetch_vendor_items, \
    build_line_items
from multi_vendor_ga import MultiVendorGA
from single_vendor_ga import SingleVendorGA
from optimisation_type import OptimisationType

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

    # create objects for SingleVendorGA and MultiVendorGA
    single_vendor_ga = SingleVendorGA(items_vendor_map, list(vendors.values()))
    multiple_vendor_ga = MultiVendorGA(items_vendor_map)

    # create PurchaseOrder object
    buyer_order = {'17833': 4, '17437': 10, '18087': 2, '15102': 15}
    purchase_order = PurchaseOrder(build_line_items(buyer_order, electrical_parts))


    ## Cost
    print("\n------------Cost Optimisation-----------")
    print("\nSingle Vendor")
    single_vendor = single_vendor_ga.solve(purchase_order)
    print(single_vendor)

    cost = -1 * single_vendor_ga.compute_fitness_score(purchase_order, single_vendor)
    print(f"Cost = {cost: .2f}")


    print("\nMultiple Vendor")
    multiple_vendors = multiple_vendor_ga.solve(purchase_order)
    for electrical_part, vendor_item in multiple_vendors.items():
        print(f"{electrical_part} -> {vendor_item.vendor}")

    print(multiple_vendor_ga.print_fitness_score(purchase_order, multiple_vendors))


    ## Delivery Days
    print("\n-----------Delivery Optimisation-----------")
    optimisation = OptimisationType.DELIVERY

    print("\nSingle Vendor")
    single_vendor = single_vendor_ga.solve(purchase_order, optimisation=optimisation)
    print(single_vendor)

    days = -1 * single_vendor_ga.compute_fitness_score(purchase_order, single_vendor, optimisation=optimisation)
    print(f"Delivery in Days = {days}")


    print("\nMultiple Vendor")
    multiple_vendors = multiple_vendor_ga.solve(purchase_order, optimisation=optimisation)
    for electrical_part, vendor_item in multiple_vendors.items():
        print(f"{electrical_part} -> {vendor_item.vendor}")

    print(multiple_vendor_ga.print_fitness_score(purchase_order, multiple_vendors, optimisation=optimisation))


if __name__ == '__main__':
    main()