# 🚀 Deploy to EC2 - Quick Start

Your code is already on EC2 at **44.202.138.57**

---

## ✅ Steps to Start Services

### 1. SSH into EC2

```bash
ssh ec2-user@44.202.138.57
```

### 2. Navigate to project

```bash
cd ~/testneoendtoend
```

### 3. Make script executable

```bash
chmod +x start.sh
```

### 4. Start services

```bash
./start.sh
```

---

## 🌐 Access Your App

After starting services:

- **Frontend:** http://44.202.138.57:3000
- **Backend API:** http://44.202.138.57:9000
- **Admin Panel:** http://44.202.138.57:3000/admin

**Login:** admin@ecommerce.com / admin123

---

## ⚠️ Open Security Group Ports

Go to AWS Console → EC2 → Security Groups

Add inbound rules:
- **Port 3000** (Frontend)
- **Port 9000** (Backend API)

Source: **0.0.0.0/0**

---

## 📝 Common Commands

```bash
# Start services
./start.sh

# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# Stop services
pkill -f "python main.py"
pkill -f "npm run dev"
```

---

## 🎉 Done!

Your e-commerce application is now running on EC2!

**Public URL:** http://44.202.138.57:3000

