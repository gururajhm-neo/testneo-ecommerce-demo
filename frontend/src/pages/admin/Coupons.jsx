import { useState, useEffect } from 'react';
import { FiPlus, FiEdit, FiTrash2, FiSearch, FiCheck, FiX } from 'react-icons/fi';
import { useToast } from '../../components/Toast';
import Pagination from '../../components/Pagination';
import CouponModal from '../../components/admin/CouponModal';
import { adminCouponsAPI, extractErrorMessage } from '../../api';

const Coupons = () => {
  const [coupons, setCoupons] = useState([]);
  const [allCoupons, setAllCoupons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCouponId, setEditingCouponId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(25);

  const { showToast } = useToast();

  useEffect(() => {
    fetchCoupons();
  }, []);

  const fetchCoupons = async () => {
    setLoading(true);
    try {
      const { data } = await adminCouponsAPI.list({ skip: 0, limit: 100 });
      const rows = Array.isArray(data) ? data : data?.coupons || [];
      // Normalize for UI (API uses current_uses)
      const normalized = rows.map((c) => ({
        ...c,
        used_count: c.used_count ?? c.current_uses ?? 0,
        name: c.name || '',
        code: c.code || '',
      }));
      setAllCoupons(normalized);
      setCoupons(normalized);
    } catch (error) {
      console.error('Error fetching coupons:', error);
      showToast('Failed to load coupons. ' + extractErrorMessage(error), 'error');
      setAllCoupons([]);
      setCoupons([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Deactivate this coupon? (soft-delete via inactive status)')) {
      return;
    }
    try {
      await adminCouponsAPI.update(id, { is_active: false });
      showToast('Coupon deactivated', 'success');
      await fetchCoupons();
    } catch (error) {
      showToast('Failed to deactivate coupon. ' + extractErrorMessage(error), 'error');
    }
  };

  const toggleActive = async (id) => {
    const current = allCoupons.find((c) => c.id === id);
    if (!current) return;
    try {
      await adminCouponsAPI.update(id, { is_active: !current.is_active });
      showToast(`Coupon ${current.is_active ? 'deactivated' : 'activated'}`, 'success');
      await fetchCoupons();
    } catch (error) {
      showToast('Failed to update coupon. ' + extractErrorMessage(error), 'error');
    }
  };

  const handleEdit = (id) => {
    setEditingCouponId(id);
    setModalOpen(true);
  };

  const handleAdd = () => {
    setEditingCouponId(null);
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setEditingCouponId(null);
  };

  const handleSuccess = () => {
    fetchCoupons();
  };

  // Filter logic
  useEffect(() => {
    let filtered = [...allCoupons];
    const q = (searchTerm || '').trim().toLowerCase();

    if (q) {
      filtered = filtered.filter((coupon) => {
        const code = String(coupon.code || '').toLowerCase();
        const name = String(coupon.name || '').toLowerCase();
        return code.includes(q) || name.includes(q);
      });
    }

    if (statusFilter === 'active') {
      filtered = filtered.filter((coupon) => !!coupon.is_active);
    } else if (statusFilter === 'inactive') {
      filtered = filtered.filter((coupon) => !coupon.is_active);
    }

    setCoupons(filtered);
    setCurrentPage(1);
  }, [searchTerm, statusFilter, allCoupons]);

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentCoupons = coupons.slice(indexOfFirstItem, indexOfLastItem);

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading coupons...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Coupons</h1>
        <button
          onClick={handleAdd}
          className="flex items-center space-x-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
        >
          <FiPlus className="w-5 h-5" />
          <span>Add Coupon</span>
        </button>
      </div>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="relative">
            <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search coupons..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
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
        <div className="mt-3 text-sm text-gray-600">
          Showing {currentCoupons.length} of {coupons.length} coupons
          {searchTerm || statusFilter !== 'all' ? ' (filtered)' : ''}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Used</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {currentCoupons.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-6 py-10 text-center text-sm text-gray-500">
                  No coupons match this filter. Clear search or set status to All.
                </td>
              </tr>
            ) : (
              currentCoupons.map((coupon) => (
                <tr key={coupon.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="font-mono text-sm font-bold text-primary-600">{coupon.code}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{coupon.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {coupon.discount_type === 'percentage'
                      ? 'Percentage'
                      : coupon.discount_type === 'free_shipping'
                        ? 'Free Shipping'
                        : 'Fixed Amount'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {coupon.discount_type === 'percentage'
                      ? `${coupon.discount_value}%`
                      : coupon.discount_type === 'free_shipping'
                        ? '—'
                        : `$${coupon.discount_value}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {coupon.used_count ?? coupon.current_uses ?? 0}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        coupon.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {coupon.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      onClick={() => toggleActive(coupon.id)}
                      className={
                        coupon.is_active
                          ? 'text-yellow-600 hover:text-yellow-900'
                          : 'text-green-600 hover:text-green-900'
                      }
                      title={coupon.is_active ? 'Deactivate' : 'Activate'}
                    >
                      {coupon.is_active ? <FiX className="w-5 h-5" /> : <FiCheck className="w-5 h-5" />}
                    </button>
                    <button
                      onClick={() => handleEdit(coupon.id)}
                      className="text-blue-600 hover:text-blue-900"
                      title="Edit Coupon"
                    >
                      <FiEdit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(coupon.id)}
                      className="text-red-600 hover:text-red-900"
                      title="Deactivate Coupon"
                    >
                      <FiTrash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {coupons.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={Math.max(1, Math.ceil(coupons.length / itemsPerPage))}
          onPageChange={setCurrentPage}
          itemsPerPage={itemsPerPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}

      <CouponModal
        isOpen={modalOpen}
        onClose={handleModalClose}
        couponId={editingCouponId}
        existingCoupon={allCoupons.find((c) => c.id === editingCouponId) || null}
        onSuccess={handleSuccess}
      />
    </div>
  );
};

export default Coupons;
