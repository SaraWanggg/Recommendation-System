# Movie Recommendation System

A content-based movie recommendation system built with Flask, scikit-learn, and modern web technologies. This application analyzes movie features like plot, genres, cast, and keywords to recommend similar movies based on content similarity.

## Features

- **Content-Based Filtering**: Recommends movies based on content similarity
- **Beautiful Pink UI**: Modern, responsive interface with a pink color scheme
- **Real-Time Search**: Autocomplete and instant recommendations
- **Similarity Scoring**: Shows how closely each recommendation matches the selected movie
- **Fast Processing**: Efficient vector calculations for quick recommendations

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- pandas
- NumPy
- scikit-learn
- Internet connection (for CSS libraries)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SaraWanggg/Recommendation-System
   cd movie-recommender
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the data:
   - Place your movie data files in the `data/` directory:
     - `tmdb_5000_movies.csv`
     - `tmdb_5000_credits.csv`

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## How It Works

### Content-Based Filtering

The recommendation system follows these steps:

1. **Data Processing**:
   - Extracts features from movie data (genres, keywords, cast, crew)
   - Combines them into a unified "tag" for each movie

2. **Feature Extraction**:
   - Uses CountVectorizer to convert text data into feature vectors
   - Applies stop-word removal and term frequency analysis

3. **Similarity Calculation**:
   - Computes cosine similarity between movie feature vectors
   - Creates a similarity matrix for quick lookups

4. **Recommendation**:
   - When a user selects a movie, finds the top 10 most similar movies
   - Returns results sorted by similarity score

## Project Structure

```
movie-recommender/
├── app.py                  # Main Flask application
├── data/                   # Data directory
│   ├── tmdb_5000_movies.csv  # Movie data
│   └── tmdb_5000_credits.csv # Cast and crew data
├── models/                 # Generated models directory
│   ├── movies_processed.pkl  # Processed movie dataframe
│   └── similarity_matrix.pkl # Similarity matrix
├── templates/              # HTML templates
│   └── index.html          # Main interface
├── README.md               # This documentation
└── requirements.txt        # Python dependencies
```

## Customization

### Modifying the Recommendation Algorithm

To adjust how recommendations are generated, edit the `get_recommendations` function in `app.py`. You can:

- Change the number of recommendations
- Adjust feature weights
- Modify similarity thresholds

### Changing the UI Theme

The UI uses a pink theme by default. To change this:

1. Open `templates/index.html`
2. Modify the CSS variables for colors, such as:
   - `#e75480` (hot pink)
   - `#ffb6c1` (light pink)
   - `#fff0f5` (pink background)

## Future Improvements

- Add user accounts for personalized recommendations
- Implement collaborative filtering for hybrid recommendations
- Add movie posters and additional details
- Create a watchlist feature
- Add movie genre filtering options

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- TMDb for the movie dataset
- scikit-learn for machine learning tools
- Flask for the web framework

---

Created with ❤️ by Sara Wang
