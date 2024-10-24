import pandas as pd
from sentence_transformers import SentenceTransformer

# Function to load the data
def load_data(file_path):
 
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None



def load_model(model_path):
    
    try:
        model = SentenceTransformer(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None