# 🚀 Deployment Guide

## Local Deployment

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd Movie-Recommender-System-ML-Project-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser and go to `http://localhost:8501`
   - The app will automatically open in your default browser

## Cloud Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Option 2: Heroku
1. Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
2. Deploy using Heroku CLI or GitHub integration

### Option 3: Docker
1. Create a `Dockerfile`
2. Build and run the container
3. Deploy to any cloud platform

## Requirements
- Python 3.8+
- Streamlit
- All dependencies listed in `requirements.txt`

## Notes
- The app uses TMDB API for movie posters
- Make sure all `.pkl` files are included in deployment
- Background images (`MARICINEMA.png`, `MARICINEMA_BACKGROUND.jpg`) are required for proper styling
