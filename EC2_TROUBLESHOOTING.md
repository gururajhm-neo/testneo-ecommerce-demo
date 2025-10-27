# 🔧 EC2 Troubleshooting Guide

**Error:** `ERR_CONNECTION_TIMED_OUT` when accessing http://44.202.138.57:3001

---

## ✅ Step 1: Check if Services are Running

SSH into EC2 and run these commands:

```bash
ssh ubuntu@44.202.138.57

# Check if processes are running
ps aux | grep "python main.py"
ps aux | grep "npm run dev"

# Check if ports are listening
netstat -tuln | grep -E '3001|9000'
```

**Expected output:**
- Should see processes for python main.py and npm run dev
- Should see ports 3001 and 9000 in LISTEN state

---

## ✅ Step 2: Check Logs for Errors

```bash
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Check backend logs
tail -20 backend.log

# Check frontend logs  
tail -20 frontend.log
```

**Look for:**
- Any error messages
- "Application startup complete" for backend
- "ready" message for frontend

---

## ⚠️ Step 3: Configure Security Group (MOST COMMON ISSUE)

This is usually the problem! You need to open ports in AWS Security Group.

### Go to AWS Console:
1. **AWS Console** → **EC2** → **Instances**
2. Select instance: `44.202.138.57`
3. Click **Security** tab
4. Click the **Security Group** link

### Add Inbound Rules:
1. Click **Edit inbound rules**
2. Click **Add rule**
3. Add TWO rules:

**Rule 1: Frontend**
- **Type:** Custom TCP
- **Protocol:** TCP
- **Port range:** 3001
- **Source:** 0.0.0.0/0
- **Description:** Frontend access

**Rule 2: Backend**
- **Type:** Custom TCP
- **Protocol:** TCP
- **Port range:** 9000
- **Source:** 0.0.0.0/0
- **Description:** Backend API

4. Click **Save rules**

---

## ✅ Step 4: Restart Services

After configuring security group, restart services:

```bash
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Kill existing processes
pkill -f "python main.py"
pkill -f "npm run dev"

# Wait a moment
sleep 3

# Start services
./start.sh
```

---

## 🔍 Step 5: Verify Services Started

```bash
# Check if backend is listening
curl http://localhost:9000/docs

# Check if frontend is listening
curl http://localhost:3001

# Check from outside (your local machine)
curl http://44.202.138.57:9000/docs
```

---

## 🛠️ Common Issues

### Issue 1: Port Already in Use

```bash
# Find what's using port 3001
sudo lsof -i :3001

# Kill the process
sudo kill -9 <PID>

# Find what's using port 9000
sudo lsof -i :9000

# Kill the process
sudo kill -9 <PID>
```

### Issue 2: Python Not Found

```bash
# Check Python
python3 --version
python --version

# Try with python3
python3 main.py
```

### Issue 3: npm Not Found

```bash
# Check Node
node --version
npm --version

# If not installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install node
```

---

## ✅ Step 6: Manual Start (If Script Fails)

```bash
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Start backend manually
nohup python3 main.py > backend.log 2>&1 &

# Wait and start frontend
sleep 5
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &

# Check status
sleep 10
ps aux | grep -E "python3 main.py|npm run dev"
```

---

## 🔍 Final Verification

After fixing security group and restarting services:

1. **Test from EC2:**
```bash
curl http://localhost:9000/docs
curl http://localhost:3001
```

2. **Test from your local machine:**
```bash
curl http://44.202.138.57:9000/docs
curl http://44.202.138.57:3001
```

3. **Access in browser:**
- http://44.202.138.57:3001
- http://44.202.138.57:3001/admin

---

## 📝 Quick Test Script

Create and run this test script:

```bash
# Save as test.sh
cat > test.sh << 'EOF'
#!/bin/bash
echo "=== Checking Services ==="
echo ""
echo "Backend Status:"
curl -s http://localhost:9000/docs | head -5
echo ""
echo "Frontend Status:"
curl -s http://localhost:3001 | head -5
echo ""
echo "Ports Listening:"
netstat -tuln | grep -E '3001|9000'
EOF

chmod +x test.sh
./test.sh
```

---

## 🎯 Most Likely Issue

**99% chance:** Security group doesn't have ports 3001 and 9000 open.

**Fix:** Add inbound rules as shown in Step 3 above.

**After fixing security group:**
1. Wait 30 seconds for AWS to apply rules
2. Access http://44.202.138.57:3001
3. Should work! ✅

---

## 📞 Still Not Working?

Run these diagnostic commands and share the output:

```bash
# 1. Check processes
ps aux | grep -E "python|npm" | head -20

# 2. Check ports
sudo netstat -tuln | grep -E '3001|9000'

# 3. Check logs
tail -50 backend.log
tail -50 frontend.log

# 4. Try connecting from EC2 itself
curl -v http://localhost:9000/docs
curl -v http://localhost:3001
```

Share the output and I'll help debug further!

