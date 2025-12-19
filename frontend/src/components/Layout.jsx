import { Link } from 'react-router-dom';
import { FiShoppingCart, FiUser, FiShield } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const Layout = ({ children }) => {
  const { isAuthenticated, user, logout, isAdmin } = useAuth();
  const { getCartCount } = useCart();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-primary-600">Ecom</span>
            </Link>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center space-x-6">
              <Link to="/products" className="text-gray-700 hover:text-primary-600 transition">
                Products
              </Link>
              <Link to="/test-components" className="text-gray-700 hover:text-primary-600 transition">
                Test Components
              </Link>
              {isAdmin && (
                <Link to="/admin" className="flex items-center space-x-1 text-purple-600 hover:text-purple-700 transition">
                  <FiShield className="w-5 h-5" />
                  <span>Admin</span>
                </Link>
              )}
            </div>

            {/* Right Side */}
            <div className="flex items-center space-x-4">
              <Link to="/cart" className="relative">
                <FiShoppingCart className="w-6 h-6 text-gray-700" />
                {getCartCount() > 0 && (
                  <span className="absolute -top-2 -right-2 bg-primary-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                    {getCartCount()}
                  </span>
                )}
              </Link>
              
              {isAuthenticated ? (
                <div className="flex items-center space-x-2">
                  <FiUser className="w-6 h-6 text-gray-700" />
                  <span className="text-sm text-gray-700">{user?.email}</span>
                  <button
                    onClick={logout}
                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <Link to="/login" className="px-4 py-2 text-gray-700 hover:text-primary-600 transition">
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 transition"
                  >
                    Register
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <p>&copy; 2025 Ecom. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;

