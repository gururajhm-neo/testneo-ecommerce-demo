# EC2 Frontend Fix - Node.js Version Issue

## Problem
```
TypeError: crypto.hash is not a function
```

This error occurs because Vite requires **Node.js 18+**, but your EC2 instance likely has an older version.

## Solution Options

### Option 1: Upgrade Node.js (Recommended for Development)

**Quick Fix:**
```bash
cd ~/ecom-app/testneo-ecommerce-demo

# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js 18
nvm install 18
nvm use 18
nvm alias default 18

# Verify
node --version  # Should show v18.x.x or higher

# Reinstall frontend dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# Start frontend
npm run dev
```

**Or use the script:**
```bash
cd ~/ecom-app/testneo-ecommerce-demo
chmod +x upgrade_node_ec2.sh
./upgrade_node_ec2.sh
```

### Option 2: Build for Production (Recommended for Production)

Instead of running the dev server, build static files:

```bash
cd ~/ecom-app/testneo-ecommerce-demo/frontend

# Install dependencies (if not done)
npm install

# Build for production
npm run build

# The built files will be in: frontend/dist
```

Then serve with nginx or a simple HTTP server:

**Option A: Python HTTP Server**
```bash
cd ~/ecom-app/testneo-ecommerce-demo/frontend/dist
python3 -m http.server 3001
```

**Option B: Nginx (Better for Production)**
```bash
# Install nginx
sudo apt-get update
sudo apt-get install -y nginx

# Configure nginx
sudo nano /etc/nginx/sites-available/frontend
```

Add this configuration:
```nginx
server {
    listen 3001;
    server_name _;
    root /home/ubuntu/ecom-app/testneo-ecommerce-demo/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Enable and start:
```bash
sudo ln -s /etc/nginx/sites-available/frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Use PM2 with Production Build

```bash
# Install PM2
npm install -g pm2

# Build frontend
cd ~/ecom-app/testneo-ecommerce-demo/frontend
npm run build

# Serve with PM2
cd dist
pm2 serve . 3001 --name frontend
pm2 save
```

## Check Current Node Version

```bash
node --version
```

If it shows v16.x or lower, you need to upgrade.

## Quick Test After Fix

After upgrading Node.js or building:

```bash
# Test Node.js version
node --version  # Should be 18+

# Test frontend
cd ~/ecom-app/testneo-ecommerce-demo/frontend
npm run dev
```

## Recommended for Production

For production on EC2, I recommend:
1. **Build the frontend** (`npm run build`)
2. **Serve with nginx** (more stable, better performance)
3. **Keep backend running** with your current setup

This avoids Node.js version issues and is more production-ready.

