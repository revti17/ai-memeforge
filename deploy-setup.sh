#!/bin/bash

# AI MemeForge - Quick Deploy Script
# This script helps you prepare your project for deployment

echo "🚀 AI MemeForge - Deployment Setup"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized!"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "📝 Adding files to Git..."
git add .

echo ""
echo "💾 Creating commit..."
git commit -m "Initial commit: AI MemeForge v1.0 - Ready for deployment"

echo ""
echo "✅ Your code is ready for GitHub!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "2. Copy your repository URL"
echo "3. Run these commands:"
echo ""
echo "   git remote add origin YOUR_GITHUB_URL"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Then follow DEPLOYMENT_GUIDE.md for Railway and Vercel setup"
echo ""
echo "🎉 Good luck with your deployment!"
