# EC2 Master Guide - Quick Reference

**Project**: E-Commerce Testing Platform  
**Server IP**: 44.202.138.57  
**Status**: Production Ready ✅

---

## 🔗 Quick Access URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://44.202.138.57:3001 |
| **Admin Panel** | http://44.202.138.57:3001/admin |
| **API Docs (Swagger)** | http://44.202.138.57:9000/docs |
| **API Base** | http://44.202.138.57:9000 |
| **OpenAPI JSON** | http://44.202.138.57:9000/openapi.json |

---

## 🔐 Admin Credentials

```
Email: admin@ecommerce.com
Password: admin123
```

---

## 🚀 Start Services (Quick)

```bash
# SSH to server
ssh ubuntu@44.202.138.57

# Navigate to project
cd ~/ecom-app/testneo-ecommerce-demo

# Activate virtual environment
source venv/bin/activate

# Start backend (port 9000)
nohup python3 main.py > backend.log 2>&1 &

# Start frontend (port 3001)
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
```

---

## 🔧 Stop Services

```bash
# Stop all services
pkill -f "python3 main.py"
pkill -f "npm"
pkill -f "serve"
```

---

## ✅ Verify Services Running

```bash
# Check backend
ps aux | grep python3 | grep main.py
sudo lsof -i :9000

# Check frontend
ps aux | grep npm | grep -v grep
sudo lsof -i :3001
```

---

## 📊 Populate Test Data

```bash
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
python3 populate_mock_data.py
```

This creates:
- 4 Users (Admin, Customer, Moderator + 4 customers)
- 15+ Products
- 25 Orders (various statuses)
- 20 Reviews
- 4 Coupons

---

## 📋 View Logs

```bash
# Backend logs
tail -f ~/ecom-app/testneo-ecommerce-demo/backend.log

# Frontend logs
tail -f ~/ecom-app/testneo-ecommerce-demo/frontend.log

# Last 50 lines
tail -n 50 backend.log
tail -n 50 frontend.log
```

---

## 🔄 Complete Restart Procedure

```bash
# 1. Stop existing services
pkill -f "python3 main.py"
pkill -f "npm"
pkill -f "serve"
sleep 2

# 2. Navigate to project
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate

# 3. Start backend
nohup python3 main.py > backend.log 2>&1 &
sleep 5

# 4. Start frontend
cd frontend
nohup npm start > ../frontend.log 2>&1 &
cd ..
sleep 10

# 5. Verify
sudo lsof -i :9000  # Backend
sudo lsof -i :3001  # Frontend
```

---

## 🐛 Common Issues & Fixes

### Issue: Frontend not loading
**Fix**:
```bash
cd ~/ecom-app/testneo-ecommerce-demo/frontend
npm run build
cd ..
cd frontend && nohup npm start > ../frontend.log 2>&1 &
```

### Issue: Backend crashed
**Fix**:
```bash
pkill -f "python3 main.py"
sleep 2
cd ~/ecom-app/testneo-ecommerce-demo
source venv/bin/activate
nohup python3 main.py > backend.log 2>&1 &
```

### Issue: Port already in use
**Fix**:
```bash
# Find process using port 9000
sudo lsof -i :9000
# Kill it
kill -9 [PID]

# Find process using port 3001
sudo lsof -i :3001
# Kill it
kill -9 [PID]
```

### Issue: Database locked
**Fix**:
```bash
# Check for running Python processes
ps aux | grep python
# Kill hanging processes
pkill -f "python3 main.py"
# Restart
nohup python3 main.py > backend.log 2>&1 &
```

---

## 📁 Project Structure

```
/home/ubuntu/ecom-app/testneo-ecommerce-demo/
├── main.py                 # FastAPI backend
├── config.py               # Configuration
├── database.py             # Database setup
├── ecommerce.db            # SQLite database
├── requirements.txt        # Python dependencies
├── populate_mock_data.py   # Data generation script
├── backend.log             # Backend logs
├── frontend.log            # Frontend logs
└── frontend/               # React frontend
    ├── dist/              # Production build
    ├── package.json       # Node dependencies
    └── src/               # Source code
```

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Start everything
cd ~/ecom-app/testneo-ecommerce-demo && source venv/bin/activate && nohup python3 main.py > backend.log 2>&1 & cd frontend && nohup npm start > ../frontend.log 2>&1 & cd ..

# Stop everything
pkill -f "python3 main.py" && pkill -f "npm"

# Check status
ps aux | grep -E "python3 main.py|npm" | grep -v grep

# View last logs
tail -n 50 backend.log frontend.log

# Populate data
cd ~/ecom-app/testneo-ecommerce-demo && source venv/bin/activate && python3 populate_mock_data.py
```

---

## 📝 Testing Checklist

- [ ] Backend responding on port 9000
- [ ] Frontend accessible on port 3001
- [ ] Can login as admin
- [ ] Products displaying
- [ ] Orders visible in admin panel
- [ ] Dashboard statistics loading
- [ ] Search and filter working
- [ ] Pagination working
- [ ] Toast notifications appearing

---

## 📞 Support Resources

- **Full Guide**: EC2_COMPLETE_GUIDE.md
- **Troubleshooting**: EC2_TROUBLESHOOTING.md
- **BRD**: BRD_BUSINESS_REQUIREMENTS_DOCUMENT.md
- **User Stories**: JIRA_COMPLETE_USER_STORIES.md
- **Swagger UI**: http://44.202.138.57:9000/docs
- **OpenAPI Spec**: http://44.202.138.57:9000/openapi.json

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Status**: Production ✅

