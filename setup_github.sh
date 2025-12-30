#!/bin/bash

# Quick setup script for GitHub repository

echo "🚀 Setting up GitHub repository for Review Analyser"
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Show status
echo ""
echo "📊 Git status:"
git status --short

# Commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: Groww App Review Analyzer with GitHub Actions"
fi

git commit -m "$commit_msg"
echo "✅ Committed changes"

# Ask for remote URL
echo ""
echo "📡 Setting up remote repository..."
echo "Create a new repository on GitHub, then enter the URL below:"
echo "Example: https://github.com/YOUR_USERNAME/Review-Analyser.git"
echo ""
read -p "GitHub repository URL: " repo_url

if [ ! -z "$repo_url" ]; then
    # Check if remote already exists
    if git remote | grep -q "origin"; then
        echo "⚠️  Remote 'origin' already exists. Updating..."
        git remote set-url origin "$repo_url"
    else
        git remote add origin "$repo_url"
    fi
    
    echo "✅ Remote added"
    
    # Push to GitHub
    echo ""
    read -p "Push to GitHub now? (y/n): " push_now
    if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
        git branch -M main
        git push -u origin main
        echo "✅ Pushed to GitHub"
    else
        echo "ℹ️  Skipped push. Run 'git push -u origin main' when ready."
    fi
else
    echo "⚠️  No repository URL provided. Skipping remote setup."
fi

echo ""
echo "="*70
echo "✅ Setup complete!"
echo "="*70
echo ""
echo "📋 Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to Settings → Secrets and variables → Actions"
echo "3. Add these secrets:"
echo "   - GEMINI_API_KEY"
echo "   - GMAIL_ADDRESS"
echo "   - GMAIL_APP_PASSWORD"
echo ""
echo "4. Test the workflow:"
echo "   - Go to Actions tab"
echo "   - Click 'Weekly Review Analysis'"
echo "   - Click 'Run workflow'"
echo ""
echo "📖 See GITHUB_ACTIONS_SETUP.md for detailed instructions"
echo ""
