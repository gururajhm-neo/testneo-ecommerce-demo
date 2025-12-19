# Components Location Guide

## 📁 Component Files Location

### Main Components (Reusable)
Located in: `frontend/src/components/`

1. **DataTable.jsx** - Advanced data table with sorting, filtering, pagination
   - Path: `frontend/src/components/DataTable.jsx`

2. **MultiStepForm.jsx** - Multi-step form wizard component
   - Path: `frontend/src/components/MultiStepForm.jsx`

3. **FileUpload.jsx** - File upload with drag & drop
   - Path: `frontend/src/components/FileUpload.jsx`

### Test Components Page
Located in: `frontend/src/pages/`

- **TestComponents.jsx** - Showcase page for all test components
  - Path: `frontend/src/pages/TestComponents.jsx`

## 🔗 How to Access

### Option 1: From Admin Panel (Recommended)
1. Login as admin: `http://localhost:3001/login`
   - Email: `admin@ecommerce.com`
   - Password: `admin123`

2. In the Admin Panel sidebar, click **"Test Components"** (with code icon 📝)

3. Or navigate directly to: `http://localhost:3001/admin/test-components`

### Option 2: From Main Navigation
1. Go to: `http://localhost:3001/test-components`
2. Or click "Test Components" in the main navigation menu

## 📂 File Structure

```
frontend/src/
├── components/
│   ├── DataTable.jsx          ← Advanced data table
│   ├── MultiStepForm.jsx      ← Multi-step form wizard
│   ├── FileUpload.jsx          ← File upload component
│   ├── Toast.jsx              ← Toast notifications
│   ├── Pagination.jsx         ← Pagination component
│   └── admin/
│       ├── AdminLayout.jsx    ← Admin layout (sidebar navigation)
│       ├── ProductModal.jsx
│       ├── UserModal.jsx
│       └── ...
├── pages/
│   ├── TestComponents.jsx     ← Test components showcase page
│   ├── Home.jsx
│   ├── Products.jsx
│   └── admin/
│       ├── Dashboard.jsx
│       ├── Products.jsx
│       └── ...
└── App.jsx                     ← Routes configuration
```

## 🎯 Quick Access URLs

- **Admin Panel:** http://localhost:3001/admin
- **Test Components (Admin):** http://localhost:3001/admin/test-components
- **Test Components (Public):** http://localhost:3001/test-components

## 💡 Usage in Your Code

### Import Components

```jsx
// In any component file
import DataTable from '../components/DataTable';
import MultiStepForm from '../components/MultiStepForm';
import FileUpload from '../components/FileUpload';
```

### Use in Admin Pages

You can use these components in any admin page:

```jsx
// Example: In admin/Products.jsx
import DataTable from '../../components/DataTable';

const AdminProducts = () => {
  return (
    <DataTable
      data={products}
      columns={productColumns}
      // ... other props
    />
  );
};
```

## 🔍 Finding Components

### Search in VS Code/Cursor
- Press `Ctrl+P` (or `Cmd+P` on Mac)
- Type: `DataTable.jsx` or `MultiStepForm.jsx` or `FileUpload.jsx`

### File Explorer
Navigate to: `frontend/src/components/`

## ✅ Verification

To verify components are accessible:
1. Start the frontend: `cd frontend && npm run dev`
2. Login to admin panel
3. Check sidebar for "Test Components" menu item
4. Click it to see all components

