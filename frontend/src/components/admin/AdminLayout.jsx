import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  FiLayout,
  FiPackage,
  FiShoppingBag,
  FiUsers,
  FiMessageSquare,
  FiLogOut,
  FiMenu,
  FiX,
  FiTag,
  FiCode,
} from 'react-icons/fi';

const AdminLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { icon: FiLayout, label: 'Dashboard', path: '/admin' },
    { icon: FiPackage, label: 'Products', path: '/admin/products' },
    { icon: FiShoppingBag, label: 'Orders', path: '/admin/orders' },
    { icon: FiUsers, label: 'Users', path: '/admin/users' },
    { icon: FiMessageSquare, label: 'Reviews', path: '/admin/reviews' },
    { icon: FiTag, label: 'Coupons', path: '/admin/coupons' },
    { icon: FiCode, label: 'Test Components', path: '/admin/test-components' },
  ];

  // Debug: Log menu items
  console.log('AdminLayout menuItems:', menuItems);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Top Navigation */}
      <nav className="bg-white shadow-md fixed w-full top-0 z-50">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden p-2 rounded-md text-gray-600 hover:bg-gray-100"
              >
                {sidebarOpen ? <FiX className="w-6 h-6" /> : <FiMenu className="w-6 h-6" />}
              </button>
              <h1 className="text-xl font-bold text-primary-600">Admin Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user?.email}</span>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
              >
                <FiLogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex pt-16">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
          } fixed inset-y-0 left-0 w-64 bg-white shadow-lg transform transition-transform duration-200 ease-in-out z-40 pt-16`}
        >
          <div className="h-full overflow-y-auto">
            <nav className="mt-5 px-2 space-y-1">
              {menuItems.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className="flex items-center space-x-3 px-4 py-3 text-gray-700 hover:bg-primary-50 hover:text-primary-600 rounded-md transition"
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                );
              })}
            </nav>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 ml-0 md:ml-64 p-8">
          {/* Test Components Banner - Always Visible */}
          <div className="mb-6 bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg shadow-lg p-4 text-white">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FiCode className="w-6 h-6" />
                <div>
                  <h3 className="text-lg font-bold">TestNeo UI Components</h3>
                  <p className="text-sm text-purple-100">Test complex UI components for automation</p>
                </div>
              </div>
              <Link
                to="/admin/test-components"
                className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-purple-50 transition font-semibold"
              >
                Open →
              </Link>
            </div>
          </div>
          {children}
        </main>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </div>
  );
};

export default AdminLayout;

