from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# Load and prepare data - keeping it simple to avoid errors
print("Loading movie data...")
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on='title')

# Select relevant columns
movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.rename(columns={'id': 'movie_id'}, inplace=True)

# Drop rows with missing values
movies.dropna(inplace=True)

# Helper functions to parse JSON strings
def get_genres(obj):
    try:
        return ' '.join([i['name'] for i in ast.literal_eval(obj)])
    except:
        return ''

def get_keywords(obj):
    try:
        return ' '.join([i['name'] for i in ast.literal_eval(obj)])
    except:
        return ''

def get_cast(obj):
    try:
        cast = ast.literal_eval(obj)
        return ' '.join([cast[i]['name'] for i in range(min(3, len(cast)))])
    except:
        return ''

def get_director(obj):
    try:
        crew = ast.literal_eval(obj)
        for person in crew:
            if person['job'] == 'Director':
                return person['name']
        return ''
    except:
        return ''

# Process columns
print("Processing data columns...")
movies['genres_str'] = movies['genres'].apply(get_genres)
movies['keywords_str'] = movies['keywords'].apply(get_keywords)
movies['cast_str'] = movies['cast'].apply(get_cast)
movies['director'] = movies['crew'].apply(get_director)

# Create tags string directly (avoiding list joining issues)
movies['tags'] = (
    movies['overview'].fillna('') + ' ' + 
    movies['genres_str'] + ' ' + 
    movies['keywords_str'] + ' ' + 
    movies['cast_str'] + ' ' + 
    movies['director']
).str.lower()

# Filter out entries with empty tags
movies = movies[movies['tags'].str.strip() != '']

print(f"Processed {len(movies)} movies")
print("Sample tags:", movies['tags'].iloc[0][:100] + "...")

# Create count vectorizer
print("Creating vectors...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Calculate similarity matrix
print("Calculating similarity matrix...")
similarity = cosine_similarity(vectors)
print("Similarity matrix shape:", similarity.shape)

# Function to get recommendations
def get_recommendations(movie_title, similarity=similarity):
    try:
        # Get the index of the movie
        movie_indices = movies.index[movies['title'] == movie_title].tolist()
        if not movie_indices:
            return []
            
        idx = movie_indices[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(similarity[idx]))
        
        # Sort movies based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top 10 similar movies (excluding the movie itself)
        sim_scores = sim_scores[1:11]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return recommendations with similarity scores
        recommendations = []
        for i, movie_idx in enumerate(movie_indices):
            recommendations.append({
                'title': movies['title'].iloc[movie_idx],
                'similarity': f"{sim_scores[i][1]:.2f}"
            })
        
        return recommendations
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []

@app.route('/')
def home():
    all_movies = sorted(movies['title'].tolist())[:1000]  
    return render_template('index.html', movies=all_movies)


@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie']
    recommendations = get_recommendations(movie_title)
    return jsonify({"recommendations": recommendations})

@app.route('/movies', methods=['GET'])
def get_movies():
    movie_list = sorted(movies['title'].unique().tolist())[:1000]
    return jsonify({"movies": movie_list})

os.makedirs('templates', exist_ok=True)


if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True)