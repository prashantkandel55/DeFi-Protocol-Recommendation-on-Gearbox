# DeFi Protocol Recommendation on Gearbox

This project is a solution for the CryptoPond Model Factory challenge: recommending DeFi protocols to users based on their historical activity within the Gearbox protocol. The goal is to generate personalized protocol recommendations for each wallet, evaluated using Precision@5.

## Overview
This project builds a recommendation system for DeFi protocols based on user activity on the Gearbox protocol. It leverages on-chain user actions to suggest the top 5 protocols each user is likely to interact with next, enhancing user experience and capital efficiency.

## Dataset
- **Account Operations**: User actions on Gearbox.
- **Allowed Protocols**: Whitelisted protocols for recommendations.
- **Ethereum Transactions**: User transactions on Ethereum mainnet.
- **DEX Swaps**: User swaps on decentralized exchanges.
- **Test Addresses**: Wallets for which recommendations are generated.

**Download the dataset here:**
[Gearbox DeFi Protocol Recommendation Dataset](https://www.kaggle.com/datasets/gearboxprotocol/defi-protocol-recommendation)

> **Note:** The dataset files are large and are not included in this repository. Please download them using the above link and place them in the `defi_protocol_rec` folder as described below.

## Project Structure

- `defi_protocol_rec/` — Contains all dataset files (not tracked in git)
- `generate_submission.py` — Main script to generate the submission file
- `fix_submission_checksum.py` — Ensures protocol addresses are checksummed to match allowed protocols
- `evaluate_precision.py` — Script to evaluate your submission using Precision@5
- `submission.csv` — Output file for submission (WALLET, REC columns)

## How It Works

1. **Data Processing:**
   - Loads user activity, allowed protocols, and test wallet addresses.
   - Standardizes all addresses to lowercase for internal processing.
   - Filters only allowed protocols for recommendations.

2. **Recommendation Logic:**
   - For each test wallet, recommends up to 5 protocols:
     - First, protocols the wallet interacted with, ordered by frequency.
     - Fills remaining slots with globally popular allowed protocols.
     - Ensures all recommendations are from the allowed list.

3. **Checksumming:**
   - Uses `fix_submission_checksum.py` to remap protocol addresses in the submission to the original (checksummed) case required by the evaluation system.

4. **Evaluation:**
   - `evaluate_precision.py` computes Precision@5 by comparing your recommendations to the ground truth.

## Usage Guide

1. **Prepare Data**
   - Place all dataset files in the `defi_protocol_rec/` directory.

2. **Generate Submission File**
   ```bash
   python generate_submission.py
   ```
   This creates `submission.csv` with lowercase addresses.

3. **Fix Protocol Address Checksums**
   ```bash
   python fix_submission_checksum.py
   ```
   This updates `submission.csv` so protocol addresses match the case in `allowed_protocols.parquet`.

4. **Evaluate Precision@5**
   ```bash
   python evaluate_precision.py
   ```
   Prints your Precision@5 score.

## Submission Format
- `submission.csv` must have columns:
  - `WALLET`: Wallet address (string)
  - `REC`: Recommended protocol address (string, checksummed)
- Each wallet should have 5 recommendations.

## Model Factory Reference

For more details, benchmarks, or to submit your model, visit the official challenge page:
[CryptoPond Model Factory - DeFi Protocol Recommendation Challenge](https://cryptopond.xyz/modelfactory/detail/33?tab=1)

## License
MIT
