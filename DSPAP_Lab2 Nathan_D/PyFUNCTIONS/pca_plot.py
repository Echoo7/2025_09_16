
def plot_correlation_circle_file(study_df, interest_cols, first_axis=1, second_axis=2):
    """
    Plot the PCA correlation circle for any pair of principal axes.

    WARNING /!\ This function needs the following libraries to be imported beforehand :
        _ pandas as pd
        _ matplotlib.pyplot as plt
        _ StandardScaler from sklearn.preprocessing
        _ PCA from sklearn.decomposition

    Parameters
    ----------
    study_df : pd.DataFrame
        The original dataframe containing the data.
    
    interest_cols : list of str
        List of column names to include in the PCA.

    first_axis : int, optional (default=1)
        The first principal component axis to plot.
    
    second_axis : int, optional (default=2)
        The second principal component axis to plot.

    Returns
    -------
    None. Displays the correlation circle plot.
    """
    
    # Check for required imports
    import sys
    if 'pd' not in globals():
        raise ImportError("pandas must be imported as 'pd'")
    if 'plt' not in globals():
        raise ImportError("matplotlib.pyplot must be imported as 'plt'")
    if 'StandardScaler' not in globals():
        raise ImportError("StandardScaler must be imported from sklearn.preprocessing")
    if 'PCA' not in globals():
        raise ImportError("PCA must be imported from sklearn.decomposition")
    
    # We select the interesting columns in the original dataframe
    df_notna = study_df[interest_cols].dropna().copy()
    X = df_notna.values

    # We standardize the data in case they are not on the same scale or units
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # We fit the PCA on the standardized data
    pca = PCA().fit(Xs)
    evr = pca.explained_variance_ratio_

    # We plot the PCA circle for the given axes
    loadings = pd.DataFrame(pca.components_.T, index=feats, columns=[f"PC{i+1}" for i in range(pca.components_.shape[0])])
    eigvals = pca.explained_variance_
    coords = loadings[[f"PC{first_axis}",f"PC{second_axis}"]].values * np.sqrt(eigvals[:2])
    fig, ax = plt.subplots(figsize=(6,6))
    circ = plt.Circle((0,0), 1.0, fill=False, linewidth=1.0); ax.add_artist(circ)
    ax.axhline(0, linewidth=0.5); ax.axvline(0, linewidth=0.5)
    for (x,y), name in zip(coords, feats):
        ax.arrow(0,0,x,y, head_width=0.03, head_length=0.04, length_includes_head=True, linewidth=0.8)
        ax.text(x*1.08, y*1.08, name, fontsize=9)
    ax.set_xlabel(f"PC{first_axis}"); ax.set_ylabel(f"PC{second_axis}"); ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1); ax.set_title(f"PCA Correlation Circle (PC{first_axis}–PC{second_axis})")
    
    plt.tight_layout(); plt.show()