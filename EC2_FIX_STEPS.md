# 🔧 Quick Fix Steps for EC2

**Problem:** Can't access http://44.202.138.57:3001 even though ports are open

---

## ✅ Run These Commands on EC2

```bash
# SSH into EC2
ssh ubuntu@44.202.138.57

# Navigate to project
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Make scripts executable
chmod +x fix_and_start.sh
chmod +x check_services.sh

# Run diagnostics first
./check_services.sh

# Then fix and start
./fix_and_start.sh
```

---

## 🔍 Most Common Issues

### Issue 1: UFW Firewall Blocking
```bash
# Check UFW status
sudo ufw status

# If active, allow ports
sudo ufw allow 9000/tcp
sudo ufw allow 3001/tcp

# Or disable UFW temporarily
sudo ufw disable
```

### Issue 2: Services Not Running
```bash
# Check if services are actually running
ps aux | grep -E "python.*main.py|npm.*dev"

# If not running, check logs
tail -50 backend.log
tail -50 frontend.log
```

### Issue 3: Services Running on Wrong Port
```bash
# Check what ports are actually listening
sudo netstat -tuln | grep LISTEN
```

---

## ✅ Expected Output from check_services.sh

**If working correctly, you should see:**

```
1. Checking if processes are running...
   ubuntu    750026  ... python main.py
   ubuntu    750500  ... npm run dev

2. Checking if ports are listening...
   tcp6  0  0  :::9000  :::*  LISTEN
   tcp6  0  0  :::3001  :::*  LISTEN

3. Testing backend from localhost...
   HTTP Status: 200

4. Testing frontend from localhost...
   HTTP Status: 200
```

---

## 🎯 Quick Fix Commands

If services aren't running:

```bash
# Navigate to project
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo

# Allow firewall ports
sudo ufw allow 9000/tcp
sudo ufw allow 3001/tcp

# Kill existing processes
pkill -9 -f "python"
pkill -9 -f "npm"

# Start backend
nohup python3 main.py > backend.log 2>&1 &
sleep 5

# Start frontend
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
cd ..
sleep 5

# Check status
ps aux | grep -E "python|npm"
curl http://localhost:9000/docs
curl http://localhost:3001
```

---

## 📤 Share the Diagnostic Output

Run this and share the output:

```bash
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
chmod +x check_services.sh
./check_services.sh > diagnostic.txt 2>&1
cat diagnostic.txt
```

This will help identify the exact issue!

