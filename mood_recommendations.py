

def recommend_by_mood(df, mood):
    cols_to_see = ['tmdb_original_title', 'imdb_score_log', 'poster_path']
    mood_df = df[df['mood'] == mood][cols_to_see]
    sorted_df = mood_df.sort_values(by=['imdb_score_log'], ascending=False)
    return sorted_df.iloc[0:20]

