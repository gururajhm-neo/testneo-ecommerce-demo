# 🚀 EC2 Deployment Guide

Complete guide to deploy your e-commerce application to EC2 and make it always running.

---

## 📋 Prerequisites

Your code is already on EC2 at IP: **44.202.138.57**

Make sure you have on EC2:
- ✅ Python 3.x
- ✅ Node.js and npm
- ✅ The project code in `/home/ec2-user/testneoendtoend` or `~/testneoendtoend`

---

## 🚀 Quick Start

### Step 1: SSH into EC2

```bash
ssh -i your-key.pem ec2-user@44.202.138.57
```

### Step 2: Navigate to project directory

```bash
cd ~/testneoendtoend
# or
cd /home/ec2-user/testneoendtoend
```

### Step 3: Make scripts executable

```bash
chmod +x start_services.sh
chmod +x stop_services.sh
```

### Step 4: Start the services

```bash
./start_services.sh
```

This will:
- Start backend on port 9000
- Start frontend on port 3000
- Show you the URLs to access

---

## 🌐 Access Your Application

### Public URLs (after security group setup):
- **Frontend:** http://44.202.138.57:3000
- **Backend API:** http://44.202.138.57:9000
- **Admin Panel:** http://44.202.138.57:3000/admin

### Login Credentials:
- **Email:** admin@ecommerce.com
- **Password:** admin123

---

## 🔧 EC2 Security Group Configuration

You need to open these ports in your EC2 security group:

1. Go to AWS Console → EC2 → Security Groups
2. Select your security group
3. Add inbound rules:

| Type | Protocol | Port Range | Source |
|------|----------|------------|--------|
| Custom TCP | TCP | 3000 | 0.0.0.0/0 |
| Custom TCP | TCP | 9000 | 0.0.0.0/0 |
| SSH | TCP | 22 | Your IP (for security) |

---

## 📝 Script Usage

### Start Services
```bash
./start_services.sh
```

### Stop Services
```bash
./stop_services.sh
```

### View Logs
```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
```

### Check if services are running
```bash
# Check backend
ps aux | grep "python main.py"

# Check frontend
ps aux | grep "npm run dev"

# Check ports
netstat -tuln | grep -E '3000|9000'
```

---

## 🔄 Make Services Run Automatically (Optional)

To make services start automatically on EC2 reboot, create a systemd service:

### Create Backend Service:

```bash
sudo nano /etc/systemd/system/ecommerce-backend.service
```

Paste this content:

```ini
[Unit]
Description=E-commerce Backend Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/testneoendtoend
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /home/ec2-user/testneoendtoend/main.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ec2-user/testneoendtoend/backend.log
StandardError=append:/home/ec2-user/testneoendtoend/backend.log

[Install]
WantedBy=multi-user.target
```

### Create Frontend Service:

```bash
sudo nano /etc/systemd/system/ecommerce-frontend.service
```

Paste this content:

```ini
[Unit]
Description=E-commerce Frontend Service
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/testneoendtoend/frontend
Environment="PATH=/usr/bin:/usr/local/bin:/home/ec2-user/.nvm/versions/node/v18.9.0/bin"
ExecStart=/usr/bin/npm run dev
Restart=always
RestartSec=10
StandardOutput=append:/home/ec2-user/testneoendtoend/frontend.log
StandardError=append:/home/ec2-user/testneoendtoend/frontend.log

[Install]
WantedBy=multi-user.target
```

### Enable and Start Services:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable ecommerce-backend.service
sudo systemctl enable ecommerce-frontend.service

# Start services
sudo systemctl start ecommerce-backend.service
sudo systemctl start ecommerce-frontend.service

# Check status
sudo systemctl status ecommerce-backend.service
sudo systemctl status ecommerce-frontend.service
```

---

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 9000
sudo lsof -ti:9000 | xargs kill -9

# Kill process on port 3000
sudo lsof -ti:3000 | xargs kill -9
```

### Check what's running
```bash
netstat -tuln | grep LISTEN
```

### View application logs
```bash
tail -f backend.log
tail -f frontend.log
```

### Restart Services
```bash
./stop_services.sh
./start_services.sh
```

---

## 📊 Verification

### Test if services are running:

```bash
# Test backend
curl http://localhost:9000/admin/stats

# Test frontend
curl http://localhost:3000
```

### From outside (after opening ports):
```bash
curl http://44.202.138.57:9000/admin/stats
```

---

## 🎯 Quick Commands Reference

```bash
# SSH into EC2
ssh -i key.pem ec2-user@44.202.138.57

# Navigate to project
cd ~/testneoendtoend

# Start services
./start_services.sh

# Stop services
./stop_services.sh

# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# Check if services are running
ps aux | grep -E "python main.py|npm run dev"
```

---

## ✅ Success Indicators

When everything is working:
- ✅ `./start_services.sh` completes without errors
- ✅ Backend responds at http://44.202.138.57:9000/docs
- ✅ Frontend loads at http://44.202.138.57:3000
- ✅ Admin login works at http://44.202.138.57:3000/admin
- ✅ All admin features work (users, products, orders, etc.)

---

## 📞 Next Steps

1. Run `./start_services.sh` on EC2
2. Open ports 3000 and 9000 in security group
3. Access your application via http://44.202.138.57:3000
4. (Optional) Set up systemd services for auto-start on reboot

**Your application is now deployed and running on EC2!** 🎉

