import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def handle_user_input(input_text, df, model, movie_embeddings):
    # Encode the user input text using the model
    embedded_input_text = model.encode([input_text])
    
    # Calculate cosine similarities between the input embedding and movie embeddings
    similarities = cosine_similarity(embedded_input_text, movie_embeddings)[0]
    
    # Get the indices of the top 10 most similar movies
    top_10_indices = np.argsort(similarities)[::-1][:10]
    
    # Retrieve the top 10 movies from the dataframe
    top_10_movies = df.iloc[top_10_indices]
    
    # Return the titles of the top 10 similar movies
    return top_10_movies[['tmdb_original_title', 'poster_path']]