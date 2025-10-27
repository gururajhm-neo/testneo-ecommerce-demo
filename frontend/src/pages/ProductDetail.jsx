import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { FiShoppingCart } from 'react-icons/fi';
import { productsAPI } from '../api';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const { isAuthenticated } = useAuth();
  const { addToCart: addToCartContext } = useCart();

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await productsAPI.getById(id);
      setProduct(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching product:', error);
      setLoading(false);
    }
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      alert('Please login to add items to cart');
      return;
    }

    try {
      await addToCartContext(parseInt(id), quantity);
      alert('Product added to cart!');
    } catch (error) {
      alert('Failed to add product to cart');
      console.error(error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-2xl text-gray-600">Loading...</div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-12 text-center">
        <p className="text-xl text-gray-600">Product not found</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          {/* Product Images */}
          <div>
            <div className="aspect-square bg-gray-200 rounded-lg overflow-hidden mb-4">
              {product.thumbnail ? (
                <img
                  src={product.thumbnail}
                  alt={product.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  No Image
                </div>
              )}
            </div>
            {product.images && product.images.length > 0 && (
              <div className="grid grid-cols-4 gap-4">
                {product.images.slice(0, 4).map((image, index) => (
                  <img
                    key={index}
                    src={image}
                    alt={`${product.name} ${index + 1}`}
                    className="w-full h-24 object-cover rounded border border-gray-200 cursor-pointer hover:border-primary-500"
                  />
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-4">{product.name}</h1>
            
            {/* Price */}
            <div className="mb-6">
              {product.sale_price ? (
                <div className="flex items-center space-x-4">
                  <span className="text-4xl font-bold text-primary-600">
                    ${product.sale_price}
                  </span>
                  <span className="text-2xl text-gray-500 line-through">
                    ${product.price}
                  </span>
                  <span className="px-3 py-1 bg-red-100 text-red-600 rounded-full text-sm font-semibold">
                    Sale!
                  </span>
                </div>
              ) : (
                <span className="text-4xl font-bold text-primary-600">
                  ${product.price}
                </span>
              )}
            </div>

            {/* Description */}
            <div className="mb-6">
              <h2 className="text-xl font-semibold mb-2">Description</h2>
              <p className="text-gray-700 leading-relaxed">{product.description}</p>
            </div>

            {/* Product Details */}
            <div className="mb-6 space-y-2">
              {product.brand && (
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Brand:</span> {product.brand}
                </p>
              )}
              {product.category && (
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Category:</span> {product.category}
                </p>
              )}
              {product.sku && (
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">SKU:</span> {product.sku}
                </p>
              )}
              <p className="text-sm">
                <span className="font-semibold text-gray-600">Stock:</span>{' '}
                <span className={product.stock_quantity > 0 ? 'text-green-600' : 'text-red-600'}>
                  {product.stock_quantity > 0 ? `${product.stock_quantity} available` : 'Out of Stock'}
                </span>
              </p>
            </div>

            {/* Quantity & Add to Cart */}
            {product.stock_quantity > 0 ? (
              <div className="mb-6">
                <label htmlFor="quantity" className="block text-sm font-medium text-gray-700 mb-2">
                  Quantity
                </label>
                <div className="flex items-center space-x-4 mb-4">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-10 h-10 bg-gray-200 rounded hover:bg-gray-300 transition"
                  >
                    -
                  </button>
                  <input
                    id="quantity"
                    type="number"
                    min="1"
                    max={product.stock_quantity}
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, Math.min(product.stock_quantity, parseInt(e.target.value) || 1)))}
                    className="w-20 px-3 py-2 border border-gray-300 rounded text-center"
                  />
                  <button
                    onClick={() => setQuantity(Math.min(product.stock_quantity, quantity + 1))}
                    className="w-10 h-10 bg-gray-200 rounded hover:bg-gray-300 transition"
                  >
                    +
                  </button>
                </div>
                <button
                  onClick={handleAddToCart}
                  className="w-full py-4 px-6 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition font-semibold flex items-center justify-center space-x-2"
                >
                  <FiShoppingCart className="w-5 h-5" />
                  <span>Add to Cart</span>
                </button>
              </div>
            ) : (
              <button
                disabled
                className="w-full py-4 px-6 bg-gray-400 text-white rounded-lg font-semibold cursor-not-allowed"
              >
                Out of Stock
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;

