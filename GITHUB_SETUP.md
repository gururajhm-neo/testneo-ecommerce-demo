# How to Push to GitHub & Clone

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named: `testneo-ecommerce-demo`
3. **DO NOT** initialize with README (we already have files)
4. Click "Create repository"

## Step 2: Push to GitHub

Run these commands:

```bash
cd testneo-ecommerce-demo
git remote add origin https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git
git push -u origin master
```

Replace `YOUR_USERNAME` with your GitHub username!

## Step 3: Verify

Visit: `https://github.com/YOUR_USERNAME/testneo-ecommerce-demo`

## Step 4: Clone Anywhere

Once pushed, you can clone it anywhere:

```bash
git clone https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git
cd testneo-ecommerce-demo
pip install -r requirements.txt
python main.py
```

## Quick Commands

```bash
# To push (after creating repo on GitHub)
git remote add origin https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git
git branch -M main  # Rename master to main
git push -u origin main

# To clone after pushing
git clone https://github.com/YOUR_USERNAME/testneo-ecommerce-demo.git

# To test locally
cd testneo-ecommerce-demo
python main.py
```

