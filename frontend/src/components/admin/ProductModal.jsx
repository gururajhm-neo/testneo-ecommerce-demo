import { useState, useEffect } from 'react';
import { adminProductsAPI, productsAPI, extractErrorMessage } from '../../api';
import { FiX, FiLoader } from 'react-icons/fi';
import { useToast } from '../Toast';

const CATEGORIES = [
  { value: 'electronics',  label: 'Electronics' },
  { value: 'clothing',     label: 'Clothing' },
  { value: 'books',        label: 'Books' },
  { value: 'home_garden',  label: 'Home & Garden' },
  { value: 'sports',       label: 'Sports' },
  { value: 'beauty',       label: 'Beauty' },
  { value: 'toys',         label: 'Toys' },
  { value: 'automotive',   label: 'Automotive' },
  { value: 'health',       label: 'Health' },
  { value: 'food',         label: 'Food' },
  { value: 'jewelry',      label: 'Jewelry' },
  { value: 'furniture',    label: 'Furniture' },
  { value: 'music',        label: 'Music' },
  { value: 'movies',       label: 'Movies' },
  { value: 'gardening',    label: 'Gardening' },
];

const EMPTY_FORM = {
  name: '',
  description: '',
  price: '',
  sale_price: '',
  stock_quantity: '',
  category: 'electronics',
  brand: '',
  sku: '',
};

const ProductModal = ({ isOpen, onClose, productId, onSuccess }) => {
  const [loading, setLoading]   = useState(false);
  const [fetching, setFetching] = useState(false);
  const [formData, setFormData] = useState(EMPTY_FORM);
  const { showToast } = useToast();

  useEffect(() => {
    if (!isOpen) return;
    if (productId) {
      fetchProduct();
    } else {
      setFormData(EMPTY_FORM);
    }
  }, [productId, isOpen]);

  const fetchProduct = async () => {
    setFetching(true);
    try {
      const response = await productsAPI.getById(productId);
      const p = response.data;
      setFormData({
        name:           p.name           || '',
        description:    p.description    || '',
        price:          p.price          || '',
        sale_price:     p.sale_price     || '',
        stock_quantity: p.stock_quantity || '',
        category:       p.category       || 'electronics',
        brand:          p.brand          || '',
        sku:            p.sku            || '',
      });
    } catch (error) {
      showToast('Failed to load product details', 'error');
      onClose();
    } finally {
      setFetching(false);
    }
  };

  const set = (field) => (e) => setFormData((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = {
        name:           formData.name,
        description:    formData.description,
        price:          parseFloat(formData.price),
        sale_price:     formData.sale_price ? parseFloat(formData.sale_price) : null,
        stock_quantity: parseInt(formData.stock_quantity),
        category:       formData.category,
        brand:          formData.brand || '',
        sku:            formData.sku,
      };

      if (productId) {
        await adminProductsAPI.updateProduct(productId, data);
        showToast('Product updated successfully!', 'success');
      } else {
        await adminProductsAPI.createProduct(data);
        showToast('Product created successfully!', 'success');
      }

      onSuccess();
      onClose();
    } catch (error) {
      showToast('Failed to save product. ' + extractErrorMessage(error), 'error');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const isEdit = Boolean(productId);

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: 'rgba(0,0,0,0.55)' }}
      onClick={(e) => { if (e.target === e.currentTarget && !loading) onClose(); }}
    >
      {/* Panel */}
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[92vh] flex flex-col animate-modal-in">

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              {isEdit ? 'Edit Product' : 'Add New Product'}
            </h2>
            <p className="text-sm text-gray-500 mt-0.5">
              {isEdit ? 'Update the product details below' : 'Fill in the details to create a new product'}
            </p>
          </div>
          <button
            onClick={onClose}
            disabled={loading}
            className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition disabled:opacity-40"
            aria-label="Close"
          >
            <FiX className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        {fetching ? (
          <div className="flex-1 flex items-center justify-center py-20 text-gray-400">
            <FiLoader className="w-8 h-8 animate-spin" />
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto px-6 py-5 space-y-5">

            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Product Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={set('name')}
                required
                placeholder="e.g. Wireless Headphones Pro"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description <span className="text-red-500">*</span>
              </label>
              <textarea
                value={formData.description}
                onChange={set('description')}
                required
                rows={3}
                placeholder="Brief description of the product..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition resize-none"
              />
            </div>

            {/* Price row */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Price ($) <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  value={formData.price}
                  onChange={set('price')}
                  required
                  placeholder="0.00"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Sale Price ($)
                  <span className="ml-1 text-xs text-gray-400 font-normal">optional</span>
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  value={formData.sale_price}
                  onChange={set('sale_price')}
                  placeholder="0.00"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
                />
              </div>
            </div>

            {/* Stock + Category */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Stock Quantity <span className="text-red-500">*</span>
                </label>
                <input
                  type="number"
                  min="0"
                  value={formData.stock_quantity}
                  onChange={set('stock_quantity')}
                  required
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category <span className="text-red-500">*</span>
                </label>
                <select
                  value={formData.category}
                  onChange={set('category')}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition bg-white"
                >
                  {CATEGORIES.map((c) => (
                    <option key={c.value} value={c.value}>{c.label}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Brand + SKU */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Brand
                  <span className="ml-1 text-xs text-gray-400 font-normal">optional</span>
                </label>
                <input
                  type="text"
                  value={formData.brand}
                  onChange={set('brand')}
                  placeholder="e.g. Sony"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  SKU <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formData.sku}
                  onChange={set('sku')}
                  required
                  placeholder="e.g. WH-PRO-001"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent transition"
                />
              </div>
            </div>

            {/* Footer */}
            <div className="flex justify-end items-center gap-3 pt-2 border-t border-gray-100">
              <button
                type="button"
                onClick={onClose}
                disabled={loading}
                className="px-5 py-2 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition disabled:opacity-40"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-2 px-5 py-2 text-sm font-medium bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition disabled:opacity-60"
              >
                {loading && <FiLoader className="w-4 h-4 animate-spin" />}
                {loading ? 'Saving…' : isEdit ? 'Update Product' : 'Create Product'}
              </button>
            </div>

          </form>
        )}
      </div>
    </div>
  );
};

export default ProductModal;
