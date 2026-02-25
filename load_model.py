import joblib

model_path = "rockfall_model_fs_reinforcement.pkl"
model = joblib.load(model_path)

print("Model loaded successfully!")
