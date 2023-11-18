import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.tree import export_graphviz
import pydotplus
from IPython.display import Image

# Example data generation
data = {
    'PE_Ratio': np.random.uniform(5, 25, 100),
    'EPS': np.random.uniform(1, 10, 100),
    'Beta': np.random.uniform(0.5, 2, 100),
    'ROE': np.random.uniform(10, 20, 100),
    'Debt_Equity': np.random.uniform(0.1, 1, 100),
    'Target': np.random.randint(0, 2, 100)
}
stock_data = pd.DataFrame(data)

# Feature Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(stock_data.drop('Target', axis=1))

# PCA
pca = PCA(n_components=3)
principal_components = pca.fit_transform(scaled_features)

# Splitting the dataset for Model Training
X_train, X_test, y_train, y_test = train_test_split(principal_components, stock_data['Target'], test_size=0.3, random_state=42)

# Model Training
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Create a faux decision tree for visualization of PCA
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
        
        # Adding leaves for original features
        for i, feature in enumerate(self.feature_names):
            for j, loading in enumerate(self.pca.components_[:, i]):
                tree_dot += f'{j + 1} -> {len(self.feature_names) + i + 1} [label="{loading:.2f}"];\n'
            tree_dot += f'{len(self.feature_names) + i + 1} [label="{feature}", shape=box];\n'
        
        tree_dot += '}'
        return tree_dot

# Visualization of PCA as Faux Decision Tree
faux_tree = FauxDecisionTree(pca, stock_data.columns[:-1])  # Exclude 'Target'
dot_data = faux_tree.export_graphviz()
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())
graph.write_png("pca_faux_tree.png")

# Visualization of the Decision Tree in the Forest
estimator = model.estimators_[0]
dot_data = export_graphviz(estimator, out_file=None, 
                           feature_names=['PC1', 'PC2', 'PC3'],  
                           class_names=['Not Recommend', 'Recommend'],
                           rounded=True, proportion=False, 
                           precision=2, filled=True)
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())
graph.write_png("random_forest_decision_tree.png")
