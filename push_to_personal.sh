#!/bin/bash

# Push to Personal GitHub Account: bathri06vishal

echo "🚀 Pushing DODO CLI to bathri06vishal GitHub account..."

# Update git config for personal account
git config user.name "bathri06vishal"
git config user.email "bathri06vishal@users.noreply.github.com"

echo ""
echo "📋 Git configuration:"
git config user.name
git config user.email

echo ""
echo "🌐 Remote origin:"
git remote -v

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository pushed successfully!"
echo "🌐 Visit: https://github.com/bathri06vishal/Dodo_CLI.V1.0"

# If repository doesn't exist, create it first:
# 1. Go to https://github.com/bathri06vishal
# 2. Click "New repository"
# 3. Name: Dodo_CLI.V1.0
# 4. Description: DODO CLI - Transform raw robotics logs into structured, ML-ready multimodal datasets
# 5. Public repository
# 6. Click "Create repository"
# 7. Then run this script again
