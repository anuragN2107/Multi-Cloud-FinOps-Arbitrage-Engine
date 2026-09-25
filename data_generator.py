import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# 1. Configuration
num_days = 180
start_date = datetime.today() - timedelta(days=num_days)
dates = [start_date + timedelta(days=i) for i in range(num_days)]

services = ['Compute', 'Storage', 'Database', 'Networking', 'Machine Learning']
regions = ['us-east-1', 'eu-west-1', 'ap-south-1', 'us-west-2']
environments = ['Production', 'Staging', 'Development']

print("Generating massive realistic cloud billing datasets...")

# 2. Generate AWS Data (Format A)
# AWS uses tags, specific service names (EC2, S3), and a 'BlendedCost' column
aws_rows = 120000
aws_data = pd.DataFrame({
    'UsageStartDate': np.random.choice(dates, aws_rows),
    'ProductName': np.random.choice(['AmazonEC2', 'AmazonS3', 'AmazonRDS', 'AmazonVPC', 'SageMaker'], aws_rows),
    'AvailabilityZone': np.random.choice(regions, aws_rows),
    'ResourceId': ['i-' + str(np.random.randint(100000, 999999)) for _ in range(aws_rows)],
    'UsageQuantity': np.random.uniform(1, 100, aws_rows),
    'BlendedCost': np.random.uniform(0.5, 50, aws_rows),
    'ResourceTag/Environment': np.random.choice(environments, aws_rows, p=[0.6, 0.2, 0.2])
})
aws_data.to_csv('aws_raw_billing.csv', index=False)
print(f"Generated aws_raw_billing.csv ({aws_rows} rows)")

# 3. Generate Azure Data (Format B)
# Azure uses different column names (MeterCategory, PreTaxCost) and exact datetimes
azure_rows = 110000
azure_data = pd.DataFrame({
    'Date': np.random.choice(dates, azure_rows),
    'MeterCategory': np.random.choice(['Virtual Machines', 'Storage', 'SQL Database', 'Virtual Network', 'Cognitive Services'], azure_rows),
    'ResourceLocation': np.random.choice(['East US', 'West Europe', 'Central India', 'West US'], azure_rows),
    'InstanceId': ['vm-' + str(np.random.randint(1000, 9999)) for _ in range(azure_rows)],
    'ConsumedQuantity': np.random.uniform(1, 150, azure_rows),
    'PreTaxCost': np.random.uniform(0.3, 60, azure_rows),
    'Tags': ['{"env": "' + env + '"}' for env in np.random.choice(environments, azure_rows, p=[0.5, 0.3, 0.2])]
})
azure_data.to_csv('azure_raw_billing.csv', index=False)
print(f"Generated azure_raw_billing.csv ({azure_rows} rows)")

# 4. Generate GCP Data (Format C)
# GCP uses nested JSON-like structures and different taxonomy
gcp_rows = 95000
gcp_data = pd.DataFrame({
    'usage_start_time': np.random.choice(dates, gcp_rows),
    'service.description': np.random.choice(['Compute Engine', 'Cloud Storage', 'Cloud SQL', 'Cloud DNS', 'Vertex AI'], gcp_rows),
    'location.region': np.random.choice(['us-east1', 'europe-west1', 'asia-south1', 'us-west1'], gcp_rows),
    'resource.name': ['inst-' + str(np.random.randint(10000, 99999)) for _ in range(gcp_rows)],
    'usage.amount': np.random.uniform(1, 200, gcp_rows),
    'cost': np.random.uniform(0.1, 45, gcp_rows),
    'labels.environment': np.random.choice(environments, gcp_rows, p=[0.7, 0.2, 0.1])
})
gcp_data.to_csv('gcp_raw_billing.csv', index=False)
print(f"Generated gcp_raw_billing.csv ({gcp_rows} rows)")

print("\nData generation complete! You now have over 325,000 rows of messy cloud data.")