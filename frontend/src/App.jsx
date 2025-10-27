import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { ToastProvider } from './components/Toast';
import Layout from './components/Layout';
import AdminLayout from './components/admin/AdminLayout';
import Home from './pages/Home';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import OrderSuccess from './pages/OrderSuccess';
import Login from './pages/Login';
import Register from './pages/Register';
import AdminDashboard from './pages/admin/Dashboard';
import AdminProducts from './pages/admin/Products';
import AdminOrders from './pages/admin/Orders';
import AdminUsers from './pages/admin/Users';
import AdminReviews from './pages/admin/Reviews';
import AdminCoupons from './pages/admin/Coupons';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();
  
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  if (!isAdmin) {
    return <Navigate to="/" />;
  }
  
  return <AdminLayout>{children}</AdminLayout>;
};

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <ToastProvider>
        <Router>
          <Routes>
            {/* Customer Routes */}
            <Route path="/" element={<Layout><Home /></Layout>} />
            <Route path="/products" element={<Layout><Products /></Layout>} />
            <Route path="/products/:id" element={<Layout><ProductDetail /></Layout>} />
            <Route path="/cart" element={<Layout><PrivateRoute><Cart /></PrivateRoute></Layout>} />
            <Route path="/checkout" element={<Layout><PrivateRoute><Checkout /></PrivateRoute></Layout>} />
            <Route path="/order-success/:id" element={<Layout><PrivateRoute><OrderSuccess /></PrivateRoute></Layout>} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
                   {/* Admin Routes */}
                   <Route path="/admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
                   <Route path="/admin/products" element={<AdminRoute><AdminProducts /></AdminRoute>} />
                   <Route path="/admin/orders" element={<AdminRoute><AdminOrders /></AdminRoute>} />
                   <Route path="/admin/users" element={<AdminRoute><AdminUsers /></AdminRoute>} />
                   <Route path="/admin/reviews" element={<AdminRoute><AdminReviews /></AdminRoute>} />
                   <Route path="/admin/coupons" element={<AdminRoute><AdminCoupons /></AdminRoute>} />
            
            <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
      </ToastProvider>
    </CartProvider>
  </AuthProvider>
  );
}

export default App;
