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
from sklearn.preprocessing import LabelEncoder


# Combine Basic Features:
# 1. Financial Ratios (P/E, D/E, ROE).
# 2. Growth Indicators (Revenue Growth, EPS Growth).
# 3. Market Trends (Moving Averages, RSI).
# 4. Volatility Measures (Beta, Standard Deviation).
# 5. Macro-economic Indicators (Interest Rates, Inflation, GDP Growth).

# Technical Indicators (Bollinger Bands, MACD).
# 1. Fundamental Analysis Metrics (Dividend Yield, Book Value).
# 2. Analyst Recommendations, Google Trends.
# 3. Alternative Data (Supply Chain, Patent Filings).
# 4. Corporate Governance (Management Changes, ESG Scores).
# 5. Economic Indicators (Consumer Confidence, Unemployment Rates).
# 6. Behavioral Factors (Trading Volume Trends, Investor Holdings).

# Get data and convert to Pandas
data = {
    'P/E': np.random.uniform(5, 25, 100),
    'D/E': np.random.uniform(0.1, 1, 100),
    'ROE': np.random.uniform(10, 20, 100),
    'Revenue Growth': np.random.uniform(0, 20, 100),
    'EPS Growth': np.random.uniform(0, 15, 100),
    'Moving Average': np.random.uniform(30, 200, 100),
    'RSI': np.random.uniform(30, 70, 100),
    'Beta': np.random.uniform(0.5, 2, 100),
    'Standard Deviation': np.random.uniform(1, 5, 100),
    'Interest Rate': np.random.uniform(0.5, 5, 100),
    'Inflation': np.random.uniform(1, 5, 100),
    'GDP Growth': np.random.uniform(1, 5, 100),
    'Dividend Yield': np.random.uniform(0, 5, 100),
    'Book Value': np.random.uniform(10, 100, 100),
    'ESG Score': np.random.uniform(0, 100, 100),
    'Consumer Confidence': np.random.uniform(0, 100, 100),
    'Unemployment Rate': np.random.uniform(0, 10, 100),
    'Trading Volume Trend': np.random.uniform(1000, 100000, 100),
    'Investor Holdings': np.random.uniform(1000, 1000000, 100),
    'Target': np.random.randint(0, 2, 100)
}
stock_data = pd.DataFrame(data)

# Ensure proper data types (especially for categorical data like 'Sector' and 'Global Events')

# Feature Scaling
# Exclude the target since it is using for evaluation
scaled_features = StandardScaler().fit_transform(stock_data.drop('Target', axis=1))

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
