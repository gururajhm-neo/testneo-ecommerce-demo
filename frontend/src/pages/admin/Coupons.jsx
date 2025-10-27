import { useState, useEffect } from 'react';
import { FiPlus, FiEdit, FiTrash2, FiSearch, FiCheck, FiX } from 'react-icons/fi';
import { useToast } from '../../components/Toast';
import Pagination from '../../components/Pagination';
import CouponModal from '../../components/admin/CouponModal';

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
    try {
      // Mock data for now - backend has coupon endpoints
      const mockCoupons = [
        {
          id: 1,
          code: 'SAVE10',
          name: 'Save 10%',
          discount_type: 'percentage',
          discount_value: 10,
          is_active: true,
          used_count: 5,
          valid_from: '2025-01-01',
          valid_until: '2025-12-31'
        },
        {
          id: 2,
          code: 'SAVE20',
          name: 'Save 20%',
          discount_type: 'percentage',
          discount_value: 20,
          is_active: true,
          used_count: 3,
          valid_from: '2025-01-01',
          valid_until: '2025-12-31'
        },
        {
          id: 3,
          code: 'FLAT50',
          name: '$50 Off',
          discount_type: 'fixed',
          discount_value: 50,
          is_active: true,
          used_count: 2,
          valid_from: '2025-01-01',
          valid_until: '2025-12-31'
        },
        {
          id: 4,
          code: 'NEWUSER',
          name: 'New User Discount',
          discount_type: 'percentage',
          discount_value: 15,
          is_active: true,
          used_count: 8,
          valid_from: '2025-01-01',
          valid_until: '2025-12-31'
        }
      ];
      setAllCoupons(mockCoupons);
      setCoupons(mockCoupons);
    } catch (error) {
      console.error('Error fetching coupons:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this coupon?')) {
      setCoupons(coupons.filter(c => c.id !== id));
      setAllCoupons(allCoupons.filter(c => c.id !== id));
      showToast('Coupon deleted successfully!', 'success');
    }
  };

  const toggleActive = async (id) => {
    setCoupons(coupons.map(c => 
      c.id === id ? { ...c, is_active: !c.is_active } : c
    ));
    setAllCoupons(allCoupons.map(c => 
      c.id === id ? { ...c, is_active: !c.is_active } : c
    ));
    showToast(`Coupon ${coupons.find(c => c.id === id).is_active ? 'deactivated' : 'activated'}`, 'success');
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

    if (searchTerm) {
      filtered = filtered.filter(coupon =>
        coupon.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
        coupon.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (statusFilter === 'active') {
      filtered = filtered.filter(coupon => coupon.is_active);
    } else if (statusFilter === 'inactive') {
      filtered = filtered.filter(coupon => !coupon.is_active);
    }

    setCoupons(filtered);
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
            {currentCoupons.map((coupon) => (
              <tr key={coupon.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="font-mono text-sm font-bold text-primary-600">{coupon.code}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{coupon.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {coupon.discount_type === 'percentage' ? 'Percentage' : 'Fixed Amount'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {coupon.discount_type === 'percentage' ? `${coupon.discount_value}%` : `$${coupon.discount_value}`}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{coupon.used_count || 0}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    coupon.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {coupon.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button 
                    onClick={() => toggleActive(coupon.id)}
                    className={coupon.is_active ? 'text-yellow-600 hover:text-yellow-900' : 'text-green-600 hover:text-green-900'}
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
                    title="Delete Coupon"
                  >
                    <FiTrash2 className="w-5 h-5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {coupons.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(coupons.length / itemsPerPage)}
          onPageChange={setCurrentPage}
          itemsPerPage={itemsPerPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}

      <CouponModal
        isOpen={modalOpen}
        onClose={handleModalClose}
        couponId={editingCouponId}
        onSuccess={handleSuccess}
      />
    </div>
  );
};

export default Coupons;

