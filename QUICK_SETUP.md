# Quick Setup for gururajhm-neo GitHub Account

## Your GitHub Profile
https://github.com/gururajhm-neo

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `testneo-ecommerce-demo`
3. Make it **Public**
4. DO NOT check "Add README"
5. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in PowerShell (in the testneo-ecommerce-demo folder):

```powershell
# Navigate to the demo folder
cd C:\Users\gururaj\Documents\testneo-api\testneo-ecommerce-demo

# Add the new files
git add GITHUB_SETUP.md PUSH_AND_CLONE_STEPS.md PUSH_AND_CLONE_STEPS.md

# Commit
git commit -m "Add setup documentation"

# Add remote
git remote add origin https://github.com/gururajhm-neo/testneo-ecommerce-demo.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Clone to C:\Users\gururaj\Documents\testneoendtoend

After pushing, run these commands:

```powershell
# Go to Documents folder
cd C:\Users\gururaj\Documents\

# Clone to testneoendtoend folder
git clone https://github.com/gururajhm-neo/testneo-ecommerce-demo.git testneoendtoend

# Enter the folder
cd testneoendtoend

# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py
```

## Done!

Your demo will be at:
- GitHub: https://github.com/gururajhm-neo/testneo-ecommerce-demo
- Local: `C:\Users\gururaj\Documents\testneoendtoend`

