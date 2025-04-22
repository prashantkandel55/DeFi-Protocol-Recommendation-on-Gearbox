import pandas as pd
import hashlib

# Load submission and allowed protocols
submission = pd.read_csv('submission.csv')
allowed = pd.read_parquet('defi_protocol_rec/allowed_protocols.parquet')

# Map lowercase protocol address to original case
allowed_map = {addr.lower(): addr for addr in allowed['PROTOCOL']}

# Apply correct case to REC column
submission['REC'] = submission['REC'].str.lower().map(allowed_map)

# Create a new column for checksums
submission['CHECKSUM'] = submission['REC'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

# Save the fixed submission
submission.to_csv('submission.csv', index=False)
print("Submission file REC column remapped to allowed protocols' original case and checksums added.")
