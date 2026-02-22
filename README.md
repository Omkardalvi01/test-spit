# Python Lab

This repository contains two independent sets of Python scripts: a GitHub webhook receiver, and a custom implementation of Principal Component Analysis (PCA) built from scratch.

## 1. GitHub Webhook Receiver (`main.py`)

A simple [FastAPI](https://fastapi.tiangolo.com/) application designed to receive and verify webhook payloads from GitHub. 

### Features
- Listens for POST requests on the root (`/`) endpoint.
- Validates the `x-hub-signature-256` header using HMAC-SHA256 to ensure the webhook legitimately originated from GitHub.
- Extracts and logs repository branch names and commit messages.

### Requirements
- FastAPI
- python-dotenv
- Uvicorn (for running the server)

To use it, ensure your `.env` file or environment has the appropriate `GITHUB_SECRET` configured (currently hardcoded as a fallback in the script), and run it using Uvicorn.

## 2. Manual PCA Implementation (`test.py` & `test_csv.py`)

These scripts demonstrate how to perform Principal Component Analysis (PCA) from scratch using NumPy and Pandas, without relying on machine learning libraries like scikit-learn.

### Methodology
The PCA is implemented using the following linear algebra steps:
1. Mean-centering the data.
2. Computing the Covariance Matrix manually.
3. Using the **Power Iteration** algorithm to find the dominant eigenvalue and eigenvector.
4. Using **Deflation** to iteratively extract the top $k$ principal components.
5. Projecting the data into the PCA space and reconstructing the original matrix.

### Files
- **`test.py`**: Runs the PCA algorithm on a small, manually constructed 5x3 data matrix. Useful for understanding the math behind the algorithm.
- **`test_csv.py`**: Runs the same PCA algorithm on the first 20 rows of the `Sales_without_Nans_v1.3.csv` dataset. It compares the shape of the original data, the projected data, and the reconstructed data.

### Requirements
- NumPy
- Pandas

### Datasets Included
- `Sales_with_NaNs_v1.3.csv`
- `Sales_without_NaNs_v1.3.csv`

## 3. Running with Docker

A `Dockerfile` is included in this repository to run the GitHub Webhook Receiver in an isolated container instance.

**To build and run the container:**

```bash
docker build -t webhook-receiver .
docker run -p 8000:8000 webhook-receiver
```

Once running, the application will be listening for POST webhook events on `http://127.0.0.1:8000/`.
## 3. Testing the Webhook

You can test the GitHub webhook receiver locally by running this Python snippet:

```python
import hmac
import hashlib
import requests
import json

# Your secret from .env or main.py
secret = "ASjhjaskGIrewuPheOTg"
url = "http://127.0.0.1:8000/"

payload = {
    "ref": "refs/heads/main",
    "commits": [
        {"id": "12345abcde", "message": "Test commit"}
    ],
    "head_commit": {"id": "12345abcde", "message": "Test commit"}
}

payload_bytes = json.dumps(payload).encode('utf-8')
mac = hmac.new(secret.encode(), msg=payload_bytes, digestmod=hashlib.sha256)
signature = f"sha256={mac.hexdigest()}"

headers = {"x-hub-signature-256": signature, "Content-Type": "application/json"}
response = requests.post(url, data=payload_bytes, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```
