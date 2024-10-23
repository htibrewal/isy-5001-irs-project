import os

import pandas as pd
from dotenv import load_dotenv
from sdmetrics.reports.single_table import QualityReport
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

load_dotenv()

# Function to generate synthetic data using CTGAN
def generate_synthetic_data(
        real_data_df,
        categorical_columns,
        num_synthetic_samples=5000,
        epochs=100
):
    # Create metadata object
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(data=real_data_df)

    # Set categorical columns in metadata
    for col in categorical_columns:
        metadata.update_column(
            column_name=col,
            sdtype='categorical'
        )

    # Initialize and train CTGAN
    synthesizer = CTGANSynthesizer(
        metadata,
        epochs=epochs
    )

    synthesizer.fit(real_data_df)

    # Generate synthetic data
    synthetic_data = synthesizer.sample(num_synthetic_samples)

    report = QualityReport()
    print(report.generate(real_data_df, synthetic_data, metadata))

    return synthetic_data


processed_po_data = pd.read_csv(os.path.join(os.getenv('PROCESSED_DATA_FOLDER_PATH'), 'filtered_data_final_2.csv'), index_col=0)
print(processed_po_data.shape)

# prepare unique list of vendor codes and purchase order numbers
# vendor_codes = processed_po_data['SUPPLIER_CODE'].unique()
# po_nums = processed_po_data['PO_NUM'].unique()

# fetch ID of unused parts
# unused_electrical_parts = pd.read_csv(os.path.join(os.getenv('PROCESSED_DATA_FOLDER_PATH'), 'electrical_parts_not_used.csv'))
# unused_part_ids = unused_electrical_parts['PART_ID_CLEANED'].unique()

processed_po_data = processed_po_data.iloc[:, :18]
processed_po_data['ITEM_CODE_CLEANED'] = processed_po_data['ITEM_CODE_CLEANED'].astype(int)
print(processed_po_data.shape)

synthetic_data = generate_synthetic_data(processed_po_data, ['PO_NUM', 'DOCCUR', 'SUPPLIER_CODE', 'ITEM_CODE_CLEANED'], num_synthetic_samples=50000)
print(synthetic_data.shape)

# save the synthetic_data to a csv
synthetic_data.to_csv('synthetic_data.csv')
