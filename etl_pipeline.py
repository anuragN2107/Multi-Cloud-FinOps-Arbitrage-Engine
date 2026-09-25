import pandas as pd
import numpy as np

print("Starting Cloud FinOps ETL Pipeline...")

# 1. Master Taxonomy Mapping
service_mapping = {
    # AWS mappings
    'AmazonEC2': 'Compute', 'AmazonS3': 'Storage', 'AmazonRDS': 'Database', 
    'AmazonVPC': 'Networking', 'SageMaker': 'Machine Learning',
    # Azure mappings
    'Virtual Machines': 'Compute', 'Storage': 'Storage', 'SQL Database': 'Database', 
    'Virtual Network': 'Networking', 'Cognitive Services': 'Machine Learning',
    # GCP mappings
    'Compute Engine': 'Compute', 'Cloud Storage': 'Storage', 'Cloud SQL': 'Database', 
    'Cloud DNS': 'Networking', 'Vertex AI': 'Machine Learning'
}
# 2. Extract & Transform AWS
print("Processing AWS data...")
df_aws = pd.read_csv('aws_raw_billing.csv')
df_aws = df_aws.rename(columns={
    'UsageStartDate': 'Date',
    'ProductName': 'RawService',
    'AvailabilityZone': 'Region',
    'ResourceId': 'ResourceID',
    'UsageQuantity': 'UsageAmount',
    'BlendedCost': 'Cost',
    'ResourceTag/Environment': 'Environment'
})
df_aws['Provider'] = 'AWS'

# 3. Extract & Transform Azure
print("Processing Azure data...")
df_azure = pd.read_csv('azure_raw_billing.csv')
df_azure = df_azure.rename(columns={
    'Date': 'Date',
    'MeterCategory': 'RawService',
    'ResourceLocation': 'Region',
    'InstanceId': 'ResourceID',
    'ConsumedQuantity': 'UsageAmount',
    'PreTaxCost': 'Cost'
})
# Fast regex extraction to parse the JSON-like 'Tags' string
df_azure['Environment'] = df_azure['Tags'].str.extract(r'"env":\s*"([^"]+)"')
df_azure = df_azure.drop(columns=['Tags'])
df_azure['Provider'] = 'Azure'

# 4. Extract & Transform GCP
print("Processing GCP data...")
df_gcp = pd.read_csv('gcp_raw_billing.csv')
df_gcp = df_gcp.rename(columns={
    'usage_start_time': 'Date',
    'service.description': 'RawService',
    'location.region': 'Region',
    'resource.name': 'ResourceID',
    'usage.amount': 'UsageAmount',
    'cost': 'Cost',
    'labels.environment': 'Environment'
})
df_gcp['Provider'] = 'GCP'
# 5. Merge and Normalize
print("Merging datasets into the Single Source of Truth...")
df_master = pd.concat([df_aws, df_azure, df_gcp], ignore_index=True)

# Standardize data types
df_master['Date'] = pd.to_datetime(df_master['Date']).dt.date
df_master['ServiceCategory'] = df_master['RawService'].map(service_mapping)
df_master['Environment'] = df_master['Environment'].fillna('Unknown')

# 6. Feature Engineering: Calculate Cost Per Unit
# np.where prevents division by zero errors
df_master['CostPerUnit'] = np.where(
    df_master['UsageAmount'] > 0, 
    df_master['Cost'] / df_master['UsageAmount'], 
    0
)

# Reorder columns for the target SQL warehouse
final_columns = [
    'Date', 'Provider', 'ServiceCategory', 'RawService', 'Region', 
    'Environment', 'ResourceID', 'UsageAmount', 'Cost', 'CostPerUnit'
]
df_master = df_master[final_columns]

# 7. Export the clean data
output_file = 'normalized_cloud_spend.csv'
df_master.to_csv(output_file, index=False)
print(f"ETL Complete! Unified dataset saved to {output_file} with {len(df_master):,} rows.")