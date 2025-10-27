import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FiShoppingCart, FiSearch } from 'react-icons/fi';
import { productsAPI, cartAPI } from '../api';
import { useAuth } from '../context/AuthContext';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const { isAuthenticated } = useAuth();

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await productsAPI.getAll();
      setProducts(response.data.products || response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching products:', error);
      setLoading(false);
    }
  };

  const addToCart = async (productId) => {
    if (!isAuthenticated) {
      alert('Please login to add items to cart');
      return;
    }

    try {
      await cartAPI.addToCart({ product_id: productId, quantity: 1 });
      alert('Product added to cart!');
    } catch (error) {
      alert('Failed to add product to cart');
      console.error(error);
    }
  };

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading products...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Our Products</h1>
        
        {/* Search Bar */}
        <div className="max-w-md">
          <div className="relative">
            <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredProducts.map((product) => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow"
          >
            {/* Product Image */}
            <div className="h-48 bg-gray-200 flex items-center justify-center overflow-hidden">
              {product.thumbnail ? (
                <img
                  src={product.thumbnail}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/300x200?text=No+Image';
                  }}
                />
              ) : (
                <span className="text-gray-400">No Image</span>
              )}
            </div>

            {/* Product Info */}
            <div className="p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                {product.name}
              </h3>
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {product.description}
              </p>
              
              {/* Price */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  {product.sale_price ? (
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl font-bold text-primary-600">
                        ${product.sale_price}
                      </span>
                      <span className="text-sm text-gray-500 line-through">
                        ${product.price}
                      </span>
                    </div>
                  ) : (
                    <span className="text-2xl font-bold text-primary-600">
                      ${product.price}
                    </span>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-2">
                <Link
                  to={`/products/${product.id}`}
                  className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition text-center"
                >
                  View Details
                </Link>
                <button
                  onClick={() => addToCart(product.id)}
                  className="flex items-center justify-center px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 transition"
                  disabled={product.stock_quantity === 0}
                >
                  <FiShoppingCart className="w-5 h-5" />
                </button>
              </div>

              {/* Stock Status */}
              {product.stock_quantity === 0 && (
                <p className="text-sm text-red-600 mt-2">Out of Stock</p>
              )}
            </div>
          </div>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <p className="text-xl text-gray-600">No products found</p>
        </div>
      )}
    </div>
  );
};

export default Products;

