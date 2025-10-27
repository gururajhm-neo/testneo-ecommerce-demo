# 🚀 Quick Start for EC2 Deployment

Your application path: `/home/ubuntu/ecom-app/testneo-ecommerce-demo`

---

## ✅ Run This on EC2

```bash
cd /home/ubuntu/ecom-app/testneo-ecommerce-demo
chmod +x start.sh
./start.sh
```

---

## 🌐 Access URLs

**After starting services:**

- **Frontend:** http://44.202.138.57:3001
- **Backend API:** http://44.202.138.57:9000  
- **Admin Panel:** http://44.202.138.57:3001/admin

**Login:** admin@ecommerce.com / admin123

---

## ⚠️ Security Group - Open These Ports

In AWS Console → EC2 → Security Groups → Inbound Rules:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| Custom TCP | TCP | 3001 | 0.0.0.0/0 |
| Custom TCP | TCP | 9000 | 0.0.0.0/0 |

---

## 📝 View Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
```

---

## 🛑 Stop Services

```bash
pkill -f "python main.py"
pkill -f "npm run dev"
```

---

## 🎉 Done!

Your e-commerce application will be live at **http://44.202.138.57:3001**

