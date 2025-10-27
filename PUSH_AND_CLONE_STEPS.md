# Quick Steps to Push to GitHub & Clone to testneoendtoend

## Step 1: Push Current Demo to GitHub

Open PowerShell in `testneo-ecommerce-demo` folder and run:

```powershell
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git

# Commit the setup file
git add GITHUB_SETUP.md
git commit -m "Add GitHub setup instructions"

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 2: Clone to Your New Location

After pushing, go to the parent directory and clone:

```powershell
# Go to parent directory
cd C:\Users\gururaj\Documents\

# Clone to testneoendtoend folder
git clone https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git testneoendtoend

# Enter the folder
cd testneoendtoend

# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py
```

## Important Note

**First, you need to create the GitHub repository:**
1. Go to https://github.com/new
2. Repository name: `testneo-ecommerce-demo`
3. Make it **Public** (easier for cloning)
4. **DO NOT** check "Add README" or any other options
5. Click "Create repository"

Then you can push and clone!

