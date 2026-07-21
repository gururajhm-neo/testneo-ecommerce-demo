import { useState, useEffect } from 'react';
import { productsAPI, adminProductsAPI } from '../../api';
import { FiEdit, FiTrash2, FiPlus, FiSearch, FiDownload } from 'react-icons/fi';
import ProductModal from '../../components/admin/ProductModal';
import DeleteConfirmModal from '../../components/admin/DeleteConfirmModal';
import Pagination from '../../components/Pagination';
import { useToast } from '../../components/Toast';

const CATEGORIES = [
  { value: 'electronics', label: 'Electronics' },
  { value: 'clothing',    label: 'Clothing' },
  { value: 'books',       label: 'Books' },
  { value: 'home_garden', label: 'Home & Garden' },
  { value: 'sports',      label: 'Sports' },
  { value: 'beauty',      label: 'Beauty' },
  { value: 'toys',        label: 'Toys' },
  { value: 'automotive',  label: 'Automotive' },
  { value: 'health',      label: 'Health' },
  { value: 'food',        label: 'Food' },
  { value: 'jewelry',     label: 'Jewelry' },
  { value: 'furniture',   label: 'Furniture' },
  { value: 'music',       label: 'Music' },
  { value: 'movies',      label: 'Movies' },
  { value: 'gardening',   label: 'Gardening' },
];

const Products = () => {
  const [products, setProducts]             = useState([]);
  const [allProducts, setAllProducts]       = useState([]);
  const [loading, setLoading]               = useState(true);

  // Add / edit modal
  const [modalOpen, setModalOpen]           = useState(false);
  const [editingProductId, setEditingProductId] = useState(null);

  // Delete confirm modal
  const [deleteModal, setDeleteModal] = useState({ open: false, product: null, loading: false });

  // Filters
  const [searchTerm, setSearchTerm]         = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [statusFilter, setStatusFilter]     = useState('all');

  // Pagination
  const [currentPage, setCurrentPage]       = useState(1);
  const [itemsPerPage, setItemsPerPage]     = useState(25);

  const { showToast } = useToast();

  useEffect(() => { fetchProducts(); }, []);

  const fetchProducts = async () => {
    try {
      const response = await productsAPI.getAll();
      const raw = response.data.products || response.data;
      const arr = Array.isArray(raw) ? raw : [];
      setAllProducts(arr);
      setProducts(arr);
    } catch (error) {
      console.error('Error fetching products:', error);
      showToast('Failed to load products', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Client-side filter
  useEffect(() => {
    let filtered = [...allProducts];
    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.sku?.toLowerCase().includes(q) ||
        p.brand?.toLowerCase().includes(q)
      );
    }
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(p => p.category === selectedCategory);
    }
    if (statusFilter === 'active')   filtered = filtered.filter(p => p.is_active);
    if (statusFilter === 'inactive') filtered = filtered.filter(p => !p.is_active);
    setProducts(filtered);
    setCurrentPage(1);
  }, [searchTerm, selectedCategory, statusFilter, allProducts]);

  // ── Delete handlers ──────────────────────────────────────────────────────
  const openDeleteModal  = (product) => setDeleteModal({ open: true, product, loading: false });
  const closeDeleteModal = () => setDeleteModal({ open: false, product: null, loading: false });

  const handleDeleteConfirm = async () => {
    const { product } = deleteModal;
    setDeleteModal((prev) => ({ ...prev, loading: true }));
    try {
      await adminProductsAPI.deleteProduct(product.id);
      setAllProducts((prev) => prev.filter(p => p.id !== product.id));
      showToast(`"${product.name}" deleted successfully`, 'success');
      closeDeleteModal();
    } catch (error) {
      console.error('Error deleting product:', error);
      showToast('Failed to delete product', 'error');
      setDeleteModal((prev) => ({ ...prev, loading: false }));
    }
  };

  // ── Add / edit handlers ──────────────────────────────────────────────────
  const handleEdit  = (id)  => { setEditingProductId(id);   setModalOpen(true); };
  const handleAdd   = ()    => { setEditingProductId(null);  setModalOpen(true); };
  const handleClose = ()    => { setModalOpen(false); setEditingProductId(null); };

  // ── Export ───────────────────────────────────────────────────────────────
  const handleExport = () => {
    const rows = products.map(p => ({
      id: p.id, name: p.name, description: p.description,
      price: p.price, stock_quantity: p.stock_quantity,
      category: p.category, brand: p.brand, sku: p.sku, is_active: p.is_active,
    }));
    const headers = Object.keys(rows[0]);
    const csv = [headers.join(','), ...rows.map(r => Object.values(r).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url  = window.URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url;
    a.download = `products_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    showToast('Products exported successfully!', 'success');
  };

  // ── Pagination ───────────────────────────────────────────────────────────
  const indexOfLast    = currentPage * itemsPerPage;
  const indexOfFirst   = indexOfLast - itemsPerPage;
  const currentProducts = products.slice(indexOfFirst, indexOfLast);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        Loading products…
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* Page header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Products</h1>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleExport}
            disabled={products.length === 0}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition disabled:opacity-50"
          >
            <FiDownload className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={handleAdd}
            className="flex items-center space-x-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
          >
            <FiPlus className="w-5 h-5" />
            <span>Add Product</span>
          </button>
        </div>
      </div>

      {/* Add / edit modal */}
      <ProductModal
        isOpen={modalOpen}
        onClose={handleClose}
        productId={editingProductId}
        onSuccess={fetchProducts}
      />

      {/* Delete confirm modal */}
      <DeleteConfirmModal
        isOpen={deleteModal.open}
        onClose={closeDeleteModal}
        onConfirm={handleDeleteConfirm}
        loading={deleteModal.loading}
        title="Delete Product"
        itemName={deleteModal.product?.name}
      />

      {/* Search + filters */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="relative">
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by name, SKU or brand…"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Categories</option>
            {CATEGORIES.map((c) => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="active">Active Only</option>
            <option value="inactive">Inactive Only</option>
          </select>
        </div>

        <div className="mt-3 text-sm text-gray-500">
          Showing {currentProducts.length > 0 ? indexOfFirst + 1 : 0}–{Math.min(indexOfLast, products.length)} of {products.length} products
          {products.length !== allProducts.length && ` (filtered from ${allProducts.length})`}
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {currentProducts.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-12 text-center text-sm text-gray-400">
                  No products found
                </td>
              </tr>
            ) : currentProducts.map((product) => (
              <tr key={product.id} className="hover:bg-gray-50 transition">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10">
                      <img
                        className="h-10 w-10 rounded-lg object-cover bg-gray-100"
                        src={product.thumbnail || 'https://placehold.co/40x40?text=?'}
                        alt={product.name}
                        onError={(e) => { e.target.src = 'https://placehold.co/40x40?text=?'; }}
                      />
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">{product.name}</div>
                      <div className="text-xs text-gray-400">{product.sku}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${(product.current_price || product.price || 0).toFixed(2)}
                  {product.sale_price && (
                    <span className="ml-2 text-xs text-gray-400 line-through">
                      ${product.price.toFixed(2)}
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`text-sm font-medium ${
                    product.stock_quantity === 0 ? 'text-red-600' :
                    product.stock_quantity <= 5  ? 'text-yellow-600' : 'text-gray-900'
                  }`}>
                    {product.stock_quantity ?? 0}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    product.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {product.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleEdit(product.id)}
                      className="p-1.5 rounded-lg text-blue-600 hover:bg-blue-50 transition"
                      title="Edit product"
                    >
                      <FiEdit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => openDeleteModal(product)}
                      className="p-1.5 rounded-lg text-red-500 hover:bg-red-50 transition"
                      title="Delete product"
                    >
                      <FiTrash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {products.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(products.length / itemsPerPage)}
          onPageChange={setCurrentPage}
          itemsPerPage={itemsPerPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}
    </div>
  );
};

export default Products;
