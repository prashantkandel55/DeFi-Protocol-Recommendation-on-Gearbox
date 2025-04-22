import pandas as pd
import os

def precision_at_k_from_files(submission_file, ground_truth_file, k=5):
    """
    Computes Precision@k given a submission file and ground truth file.
    submission_file: Path to CSV with columns WALLET, REC
    ground_truth_file: Path to Parquet/CSV with columns ADDRESS, ACTUAL
    k: Number of recommendations per user
    Returns: Average Precision@k across all users
    """
    def load_file(path):
        if path.endswith('.csv'):
            return pd.read_csv(path)
        elif path.endswith('.parquet'):
            return pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported file type: {path}")

    submission = load_file(submission_file)
    ground_truth = load_file(ground_truth_file)

    # Use ADDRESS for grouping (update if your ground truth uses WALLET)
    gt = ground_truth.groupby('ADDRESS')['ACTUAL'].apply(set).to_dict()
    recs = submission.groupby('WALLET')['REC'].apply(list).to_dict()

    precisions = []
    for address, recommended in recs.items():
        relevant = gt.get(address, set())
        recommended_set = set(recommended[:k])
        num_relevant = len(recommended_set & relevant)
        precisions.append(num_relevant / k)

    return sum(precisions) / len(precisions)

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), 'defi_protocol_rec')
    submission_file = os.path.join(os.path.dirname(__file__), 'submission.csv')
    ground_truth_file = os.path.join(data_dir, "ground_truth.parquet")
    k = 5
    precision = precision_at_k_from_files(submission_file, ground_truth_file, k)
    print(f"Precision@{k}: {precision:.4f}")
