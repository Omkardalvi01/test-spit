import numpy as np
import pandas as pd

CSV_PATH = "Sales_without_Nans_v1.3.csv"  
N_ROWS = 20                  
K_COMPONENTS = 2             


df = pd.read_csv(CSV_PATH)
df_top = df.head(N_ROWS)
X = df_top.select_dtypes(include=[np.number]).to_numpy()

mean = np.mean(X, axis=0)
X_centered = X - mean

# COVARIANCE MATRIX (MANUAL)
n_samples = X_centered.shape[0]
cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)


# POWER ITERATION
def power_iteration(A, num_iters=1000, tol=1e-6):
    b = np.ones(A.shape[0])
    b = b / np.linalg.norm(b)

    for _ in range(num_iters):
        b_new = A @ b
        b_new = b_new / np.linalg.norm(b_new)

        if np.linalg.norm(b - b_new) < tol:
            break

        b = b_new

    eigenvalue = b.T @ A @ b  # Rayleigh quotient
    return eigenvalue, b

# EIGEN DECOMPOSITION (DEFLECTION)
def eigen_decomposition_manual(A, k):
    A_work = A.copy()
    eigenvalues = []
    eigenvectors = []

    for _ in range(k):
        val, vec = power_iteration(A_work)
        eigenvalues.append(val)
        eigenvectors.append(vec)

        # Deflation
        A_work = A_work - val * np.outer(vec, vec)

    return np.array(eigenvalues), np.column_stack(eigenvectors)


# PCA COMPUTATION
k = min(K_COMPONENTS, X.shape[1])
eigenvalues, eigenvectors = eigen_decomposition_manual(cov_matrix, k)

# -----------------------------
# PROJECT INTO PCA SPACE
# Z = XW
# -----------------------------
X_pca = X_centered @ eigenvectors

# -----------------------------
# RECONSTRUCT ORIGINAL MATRIX
# X̂ = ZWᵀ + μ
# -----------------------------
X_reconstructed = X_pca @ eigenvectors.T + mean

pca_df = pd.DataFrame(
    X_pca,
    columns=[f"PC{i+1}" for i in range(k)]
)

reconstructed_df = pd.DataFrame(
    X_reconstructed,
    columns=df_top.select_dtypes(include=[np.number]).columns
)

print("===================================")
print("Manual PCA Results")
print("===================================")
print("Original shape:", X.shape)
print("PCA shape:", X_pca.shape)
print("Reconstructed shape:", X_reconstructed.shape)

print("\nEigenvalues (manual):")
print(eigenvalues)

print("\nPCA (first 5 rows):")
print(pca_df.head())

print("\nReconstructed data (first 5 rows):")
print(reconstructed_df.head())
