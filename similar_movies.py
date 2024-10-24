

def find_similar_movies(movie_title, df, top_10_similar, top_n=10):
    try:
        # Get the index of the selected movie
        movie_idx = df[df['tmdb_original_title'] == movie_title].index[0]
    except IndexError:
        print("Movie title not found in the dataset.")
        return []

    # Get the indices and scores of the top 10 similar movies for the selected movie
    similar_indices, similar_scores = top_10_similar[str(movie_idx)]

    # Create a list of tuples (movie title, poster path, similarity score)
    similar_movies = [(df.iloc[idx]['tmdb_original_title'], df.iloc[idx]['poster_path'], score) 
                      for idx, score in zip(similar_indices, similar_scores)]

    # Return the top N similar movies
    return similar_movies[:top_n]


