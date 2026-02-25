import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib


np.random.seed(42)
df = pd.DataFrame({
    'fs': np.random.uniform(1, 3, 500),
    'reinforcement': np.random.uniform(0, 5, 500)
})
df['rockfall_risk'] = ((df['fs'] < 1.4) | (df['reinforcement'] < 0.4)).astype(int)


X = df[['fs', 'reinforcement']]
y = df['rockfall_risk']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, 'rockfall_model_fs_reinforcement.pkl')
print(" Model trained and saved successfully.")
