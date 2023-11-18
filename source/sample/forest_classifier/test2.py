import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.tree import export_graphviz
import pydotplus
from IPython.display import Image

# Example data generation
data = {
    'PE_Ratio': np.random.uniform(5, 25, 100),
    'EPS': np.random.uniform(1, 10, 100),
    'Beta': np.random.uniform(0.5, 2, 100),
    'ROE': np.random.uniform(10, 20, 100),
    'Debt_Equity': np.random.uniform(0.1, 1, 100)
}
stock_data = pd.DataFrame(data)

# Feature Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(stock_data)

# PCA
pca = PCA(n_components=3)
pca.fit(scaled_features)

# Create a faux decision tree for visualization
class FauxDecisionTree:
    def __init__(self, pca, feature_names):
        self.pca = pca
        self.feature_names = feature_names

    def export_graphviz(self):
        tree_dot = 'digraph Tree {\n'
        
        # Adding nodes for principal components
        for i, variance in enumerate(self.pca.explained_variance_ratio_):
            tree_dot += f'0 -> {i + 1} [label="{variance:.2%}"];\n'
            tree_dot += f'{i + 1} [label="PC{i+1}"];\n'
        
        # Adding leaves for features
        for i, feature in enumerate(self.feature_names):
            for j, loading in enumerate(self.pca.components_[:, i]):
                tree_dot += f'{j + 1} -> {len(self.feature_names) + i + 1} [label="{loading:.2f}"];\n'
            tree_dot += f'{len(self.feature_names) + i + 1} [label="{feature}", shape=box];\n'
        
        tree_dot += '}'
        return tree_dot

# Create and visualize the faux tree
faux_tree = FauxDecisionTree(pca, stock_data.columns)
dot_data = faux_tree.export_graphviz()
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())
# Save the diagram
graph.write_png("decision_tree_1.png")
