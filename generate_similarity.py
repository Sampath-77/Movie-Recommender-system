#!/usr/bin/env python3
"""
Script to generate similarity.pkl file for the Movie Recommender System.
Run this script after cloning the repository to generate the required similarity matrix.
"""

import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer
import re

def generate_similarity_matrix():
    """Generate and save the similarity matrix for movie recommendations."""
    
    print("🎬 Generating similarity matrix for Movie Recommender System...")
    print("=" * 60)
    
    try:
        # Load the movie data
        print("📁 Loading movie data...")
        movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        movies = pd.DataFrame(movie_dict)
        print(f"✅ Loaded {len(movies)} movies")
        
        # Download required NLTK data
        print("📚 Downloading NLTK data...")
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Initialize stemmer
        ps = PorterStemmer()
        
        def stem(text):
            """Stem the text using Porter Stemmer."""
            y = []
            for i in text.split():
                y.append(ps.stem(i))
            return " ".join(y)
        
        # Process the data
        print("🔧 Processing movie data...")
        movies['tags'] = movies['overview'] + ' ' + movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['cast'] + ' ' + movies['crew']
        movies['tags'] = movies['tags'].fillna('')
        movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
        movies['tags'] = movies['tags'].apply(lambda x: x.lower())
        movies['tags'] = movies['tags'].apply(stem)
        
        # Vectorize the tags
        print("🔢 Vectorizing movie tags...")
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vectors = cv.fit_transform(movies['tags']).toarray()
        
        # Calculate cosine similarity
        print("📐 Calculating cosine similarity matrix...")
        similarity = cosine_similarity(vectors)
        
        # Save the similarity matrix
        print("💾 Saving similarity matrix...")
        pickle.dump(similarity, open('similarity.pkl', 'wb'))
        
        print("✅ Successfully generated similarity.pkl!")
        print(f"📊 Similarity matrix shape: {similarity.shape}")
        print("🎉 You can now run the Streamlit app!")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure movie_dict.pkl exists in the current directory.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your data and try again.")

if __name__ == "__main__":
    generate_similarity_matrix()
