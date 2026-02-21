import numpy as np

# comment 1
# comment 2
# Manually constructed data matrix (samples x features)
X = np.array(
    [
        [2.0, 0.0, 1.0],
        [3.0, 1.0, 2.0],
        [4.0, 0.0, 3.0],
        [5.0, 1.0, 4.0],
        [6.0, 0.0, 5.0],
    ]
)

# Mean center
mean = np.mean(X, axis=0)
X_centered = X - mean

n_samples = X_centered.shape[0]
cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)


def power_iteration(A, num_iters=1000, tol=1e-6):
    b = np.ones(A.shape[0])
    b = b / np.linalg.norm(b)

    for _ in range(num_iters):
        b_new = A @ b
        b_new_norm = np.linalg.norm(b_new)
        b_new = b_new / b_new_norm

        if np.linalg.norm(b - b_new) < tol:
            break

        b = b_new

    eigenvalue = b.T @ A @ b
    return eigenvalue, b


def eigen_decomposition_manual(A, k):
    A_copy = A.copy()
    eigenvalues = []
    eigenvectors = []

    for _ in range(k):
        val, vec = power_iteration(A_copy)
        eigenvalues.append(val)
        eigenvectors.append(vec)

        # Deflation
        A_copy = A_copy - val * np.outer(vec, vec)

    return np.array(eigenvalues), np.column_stack(eigenvectors)


# Compute eigenvalues & eigenvectors manually
k = 2
eigenvalues, eigenvectors = eigen_decomposition_manual(cov_matrix, k)

# Project data onto principal components
X_pca = X_centered @ eigenvectors

X_reconstructed = X_pca @ eigenvectors.T + mean

print("Covariance matrix:\n", cov_matrix)
print("\nEigenvalues (manual):\n", eigenvalues)
print("\nEigenvectors (manual):\n", eigenvectors)

print("\nOriginal X:\n", X)
print("\nReconstructed X:\n", np.round(X_reconstructed, 3))
