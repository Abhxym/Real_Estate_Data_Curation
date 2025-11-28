#!/bin/bash

echo "=========================================="
echo "Real Estate Dashboard Deployment Script"
echo "=========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists git; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Menu
echo "Select deployment option:"
echo "1) Local deployment (test)"
echo "2) Docker deployment"
echo "3) Prepare for Streamlit Cloud"
echo "4) Prepare for Heroku"
echo "5) Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting local deployment..."
        python3 -m pip install -r requirements.txt
        echo ""
        echo "Testing models..."
        python3 test_models.py
        echo ""
        echo "Starting dashboard..."
        python3 -m streamlit run dashboard.py
        ;;
    
    2)
        echo ""
        echo "Docker deployment..."
        if ! command_exists docker; then
            echo "❌ Docker is not installed. Please install Docker first."
            exit 1
        fi
        
        echo "Building Docker image..."
        docker build -t real-estate-dashboard .
        
        echo ""
        echo "Starting container..."
        docker run -p 8503:8503 real-estate-dashboard
        ;;
    
    3)
        echo ""
        echo "Preparing for Streamlit Cloud deployment..."
        
        # Check if git repo exists
        if [ ! -d ".git" ]; then
            echo "Initializing git repository..."
            git init
        fi
        
        echo "Adding files..."
        git add .
        
        echo ""
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
        
        echo ""
        echo "✅ Repository prepared!"
        echo ""
        echo "Next steps:"
        echo "1. Create a GitHub repository"
        echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
        echo "3. Run: git push -u origin main"
        echo "4. Go to https://share.streamlit.io/"
        echo "5. Click 'New app' and select your repository"
        echo "6. Set main file: dashboard.py"
        echo "7. Click 'Deploy'"
        ;;
    
    4)
        echo ""
        echo "Preparing for Heroku deployment..."
        
        if ! command_exists heroku; then
            echo "❌ Heroku CLI is not installed."
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo "Logging into Heroku..."
        heroku login
        
        echo ""
        read -p "Enter app name: " app_name
        
        echo "Creating Heroku app..."
        heroku create $app_name
        
        echo ""
        echo "Deploying to Heroku..."
        git push heroku main
        
        echo ""
        echo "Opening app..."
        heroku open
        ;;
    
    5)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac
