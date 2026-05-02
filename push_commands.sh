#!/bin/bash

# GitHub Repository Setup Commands
# Run this after creating the repository on GitHub

echo "🚀 Setting up GitHub repository..."

# Check current git status
echo "📋 Current git status:"
git status

echo ""
echo "🔧 Configuring git user..."
git config user.name "Dodo Robotics"
git config user.email "team@dodo-robotics.com"

echo ""
echo "🌐 Setting up remote origin..."
# Remove any existing remote
git remote remove origin 2>/dev/null

# Add the correct remote (update URL if needed)
git remote add origin https://github.com/dodo-robotics/Dodo_CLI.V1.0.git

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository setup complete!"
echo "🌐 Visit: https://github.com/dodo-robotics/Dodo_CLI.V1.0"

# Alternative if organization doesn't exist:
# git remote set-url origin https://github.com/YOUR_USERNAME/dodo-cli-v1.0.git
# git push -u origin main
