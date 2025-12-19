# How to Access Admin Panel Locally

## 🚀 Quick Access URLs

### Admin Panel Access
1. **Login Page:** http://localhost:3001/login
2. **Admin Dashboard:** http://localhost:3001/admin
3. **Test Components:** http://localhost:3001/admin/test-components

## 📋 Step-by-Step Instructions

### Step 1: Start the Servers

**Backend Server:**
```powershell
# In project root directory
python main.py
```
Or use the restart script:
```powershell
.\restart-server.ps1
```

**Frontend Server:**
```powershell
# In frontend directory
cd frontend
npm run dev
```

### Step 2: Access Login Page

1. Open your browser
2. Go to: **http://localhost:3001/login**
3. NOT http://44.202.138.57:3001 (that's the remote server)

### Step 3: Login as Admin

**Admin Credentials:**
- **Email:** `admin@ecommerce.com`
- **Password:** `admin123`

### Step 4: After Login

You will be automatically redirected to:
- **Admin Dashboard:** http://localhost:3001/admin

## 🎯 What You'll See

### In Admin Panel:
1. **Sidebar Menu** (left side):
   - Dashboard
   - Products
   - Orders
   - Users
   - Reviews
   - Coupons
   - **Test Components** ← Should be at the bottom

2. **Top Banner** (purple):
   - "TestNeo UI Components" banner with "Open →" button
   - This appears on ALL admin pages

3. **Direct Access:**
   - http://localhost:3001/admin/test-components

## 🔍 Verify Servers Are Running

**Check Backend:**
```powershell
Invoke-WebRequest -Uri http://localhost:9000/health
```
Should return: Status 200

**Check Frontend:**
```powershell
Invoke-WebRequest -Uri http://localhost:3001
```
Should return: Status 200

## ⚠️ Common Mistakes

1. **Wrong URL:**
   - ❌ http://44.202.138.57:3001 (remote server)
   - ✅ http://localhost:3001 (local server)

2. **Wrong Port:**
   - ❌ http://localhost:9000 (backend API)
   - ✅ http://localhost:3001 (frontend)

3. **Not Logged In:**
   - Make sure you're logged in as admin
   - Check if you see "Logout" button in top right

## 🎨 Test Components Access

Once in admin panel, you can access Test Components via:

1. **Purple Banner** at top of any admin page
2. **Sidebar Menu** - "Test Components" at bottom
3. **Direct URL:** http://localhost:3001/admin/test-components

## 📝 Quick Checklist

- [ ] Backend running on http://localhost:9000
- [ ] Frontend running on http://localhost:3001
- [ ] Using http://localhost:3001 (NOT remote URL)
- [ ] Logged in as admin@ecommerce.com
- [ ] Can see admin sidebar menu
- [ ] Can see purple "Test Components" banner

