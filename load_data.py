import os
import pandas as pd
from dotenv import load_dotenv

from blocks.Vendor import Vendor

load_dotenv()

def load_electrical_parts_data():
    pass

def load_purchase_order_data() -> pd.DataFrame:
    purchase_order_data = pd.read_csv(os.path.join(os.getenv('PROCESSED_DATA_FOLDER_PATH'), 'filtered_data_final.csv'))
    return purchase_order_data

# def fetch_vendors(purchase_order_data: pd.DataFrame) -> list[Vendor]:
#     vendors_info = purchase_order_data[['SUPPLIER_CODE', 'SUPPLIER_NAME']]