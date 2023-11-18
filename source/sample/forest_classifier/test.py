import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pydotplus
from IPython.display import Image
import os

# Example financial features
data = {
    'PE_Ratio': np.random.uniform(5, 25, 100),  # Price-to-Earnings Ratio
    'EPS': np.random.uniform(1, 10, 100),       # Earnings Per Share
    'Beta': np.random.uniform(0.5, 2, 100),     # Stock Beta
    'ROE': np.random.uniform(10, 20, 100),      # Return on Equity
    'Debt_Equity': np.random.uniform(0.1, 1, 100), # Debt-to-Equity Ratio
    'Target': np.random.randint(0, 2, 100)      # Target Variable (0 or 1)
}

stock_data = pd.DataFrame(data)

# Data Preprocessing
stock_data.fillna(stock_data.mean(), inplace=True)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(stock_data.drop('Target', axis=1))

# PCA for Feature Reduction (Optional)
pca = PCA(n_components=3)
principal_components = pca.fit_transform(scaled_features)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(principal_components, stock_data['Target'], test_size=0.3, random_state=42)

# Model Training
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Model Evaluation
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Printing out individual predictions
for i, prediction in enumerate(predictions):
    action = 'Recommend' if prediction == 1 else 'Not Recommend'
    print(f"Data Point {i+1}: {action}")

# Visualization of the Decision Tree in the Forest
estimator = model.estimators_[0]
dot_data = export_graphviz(estimator, out_file=None, 
                           feature_names=['PCA1', 'PCA2', 'PCA3'],  
                           class_names=['Not Recommend', 'Recommend'],
                           rounded=True, proportion=False, 
                           precision=2, filled=True)

graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())

# Save the diagram
graph.write_png("decision_tree.png")
