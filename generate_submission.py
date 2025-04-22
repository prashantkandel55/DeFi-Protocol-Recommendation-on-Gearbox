import pandas as pd
import os

# Set up file paths
data_dir = os.path.join(os.path.dirname(__file__), 'defi_protocol_rec')
account_ops_path = os.path.join(data_dir, 'account_operations.parquet')
allowed_protocols_path = os.path.join(data_dir, 'allowed_protocols.parquet')
test_addresses_path = os.path.join(data_dir, 'test_addresses.parquet')
submission_csv_path = os.path.join(os.path.dirname(__file__), 'submission.csv')

# Load data files
account_ops = pd.read_parquet(account_ops_path)
allowed_protocols = pd.read_parquet(allowed_protocols_path)
test_addresses = pd.read_parquet(test_addresses_path)

# Standardize all addresses to lowercase for processing
account_ops['DAPP'] = account_ops['DAPP'].str.lower()
account_ops['BORROWER'] = account_ops['BORROWER'].str.lower()
allowed_protocols['PROTOCOL'] = allowed_protocols['PROTOCOL'].str.lower()
test_addresses['ADDRESS'] = test_addresses['ADDRESS'].str.lower()

# Only consider allowed protocols
allowed_set = set(allowed_protocols['PROTOCOL'])
user_protocols = account_ops[account_ops['DAPP'].isin(allowed_set)]

# For each test wallet, recommend up to 5 most frequent protocols
rows = []
for wallet in test_addresses['ADDRESS']:
    # Protocols used by this wallet, most frequent first
    protos = user_protocols[user_protocols['BORROWER'] == wallet]['DAPP'].value_counts().index.tolist()
    # Fill up to 5 with globally popular protocols
    if len(protos) < 5:
        global_top = user_protocols['DAPP'].value_counts().index.tolist()
        protos += [p for p in global_top if p not in protos]
    # Fill up with any remaining allowed protocols if needed
    if len(protos) < 5:
        protos += [p for p in allowed_protocols['PROTOCOL'] if p not in protos]
    for rec in protos[:5]:
        rows.append({'WALLET': wallet, 'REC': rec})

submission = pd.DataFrame(rows)
submission.to_csv(submission_csv_path, index=False)
print(f"Submission file generated at {submission_csv_path}")
