import numpy as np
import pandas as pd
from plotting import plot_scree

def portfolio_analysis(big_df):
    
    # Get Correlation
    corr_matrix = big_df.corr().to_numpy()

    # Get Eigenvalues and Eigenvectors
    w, v = np.linalg.eig(corr_matrix)

    eigen_pairs = []
    for i in range(len(w)):
        eigen_pairs.append([w[i], v[:,i]])

    # Sort Eigen pairs form largest of smallest
    eigen_pairs.sort(key=lambda x: x[0], reverse=True)

    total_variance = sum(w)

    explained_variance = [i / total_variance for i, j in eigen_pairs]

    plot_scree(explained_variance)





