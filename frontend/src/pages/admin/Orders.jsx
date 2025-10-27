import { useState, useEffect } from 'react';
import { adminOrdersAPI } from '../../api';
import { FiEye, FiX, FiSearch, FiEdit } from 'react-icons/fi';
import OrderModal from '../../components/admin/OrderModal';
import Pagination from '../../components/Pagination';
import { useToast } from '../../components/Toast';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [allOrders, setAllOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(25);
  
  const { showToast } = useToast();

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await adminOrdersAPI.getAllOrders();
      // Backend returns an array directly
      const ordersArray = Array.isArray(response.data) ? response.data : [];
      setAllOrders(ordersArray);
      setOrders(ordersArray);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  };

  // Filter orders based on search and status
  useEffect(() => {
    let filtered = [...allOrders];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.order_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        order.payment_method?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status === statusFilter);
    }

    setOrders(filtered);
  }, [searchTerm, statusFilter, allOrders]);

  const handleView = (id) => {
    const order = orders.find(o => o.id === id);
    setSelectedOrder(order);
    setModalOpen(true);
  };

  const handleCancel = async (id) => {
    if (window.confirm('Are you sure you want to cancel this order?')) {
      try {
        await adminOrdersAPI.cancelOrder(id);
        // Update local state immediately
        setOrders(orders.map(o => o.id === id ? { ...o, status: 'CANCELLED' } : o));
        setAllOrders(allOrders.map(o => o.id === id ? { ...o, status: 'CANCELLED' } : o));
        showToast('Order cancelled successfully!', 'success');
      } catch (error) {
        console.error('Error cancelling order:', error);
        showToast('Failed to cancel order. ' + (error.response?.data?.detail || ''), 'error');
      }
    }
  };

  const handleStatusUpdate = async (orderId, newStatus) => {
    try {
      // Convert string to proper format
      const statusUpdate = { status: newStatus };
      await adminOrdersAPI.updateOrder(orderId, statusUpdate);
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: newStatus } : o));
      setAllOrders(allOrders.map(o => o.id === orderId ? { ...o, status: newStatus } : o));
      showToast(`Order status updated to ${newStatus}`, 'success');
    } catch (error) {
      console.error('Error updating order status:', error);
      const errorMsg = error.response?.data?.detail || error.response?.data?.message || JSON.stringify(error.response?.data) || error.message;
      showToast(`Failed to update order status: ${errorMsg}`, 'error');
    }
  };

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentOrders = orders.slice(indexOfFirstItem, indexOfLastItem);

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading orders...</div>;
  }

  const getStatusColor = (status) => {
    const colors = {
      PENDING: 'bg-yellow-100 text-yellow-800',
      CONFIRMED: 'bg-blue-100 text-blue-800',
      SHIPPED: 'bg-purple-100 text-purple-800',
      DELIVERED: 'bg-green-100 text-green-800',
      CANCELLED: 'bg-red-100 text-red-800',
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Orders</h1>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search */}
          <div className="relative">
            <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search by order number..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="PENDING">Pending</option>
            <option value="CONFIRMED">Confirmed</option>
            <option value="SHIPPED">Shipped</option>
            <option value="DELIVERED">Delivered</option>
            <option value="CANCELLED">Cancelled</option>
          </select>
        </div>

        {/* Results count */}
        <div className="mt-3 text-sm text-gray-600">
          Showing {orders.length} of {allOrders.length} orders
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {currentOrders.map((order) => (
              <tr key={order.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {order.order_number}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  User #{order.user_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {new Date(order.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${(order.total_amount || 0).toFixed(2)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <select
                    value={order.status}
                    onChange={(e) => handleStatusUpdate(order.id, e.target.value)}
                    className={`px-2 py-1 text-xs font-semibold rounded-full border ${
                      order.status === 'DELIVERED' ? 'bg-green-100 text-green-800 border-green-300' :
                      order.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800 border-yellow-300' :
                      order.status === 'CANCELLED' ? 'bg-red-100 text-red-800 border-red-300' :
                      order.status === 'SHIPPED' ? 'bg-purple-100 text-purple-800 border-purple-300' :
                      'bg-blue-100 text-blue-800 border-blue-300'
                    } focus:outline-none focus:ring-2 focus:ring-primary-500`}
                  >
                    <option value="PENDING">Pending</option>
                    <option value="CONFIRMED">Confirmed</option>
                    <option value="SHIPPED">Shipped</option>
                    <option value="DELIVERED">Delivered</option>
                    <option value="CANCELLED">Cancelled</option>
                  </select>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button 
                    onClick={() => handleView(order.id)}
                    className="text-blue-600 hover:text-blue-900"
                    title="View Order Details"
                  >
                    <FiEye className="w-5 h-5" />
                  </button>
                  <button 
                    onClick={() => handleCancel(order.id)}
                    disabled={order.status === 'CANCELLED'}
                    className="text-red-600 hover:text-red-900 disabled:opacity-50"
                    title="Cancel Order"
                  >
                    <FiX className="w-5 h-5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <OrderModal
        isOpen={modalOpen}
        onClose={() => {
          setModalOpen(false);
          setSelectedOrder(null);
        }}
        order={selectedOrder}
      />

      {orders.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={Math.ceil(orders.length / itemsPerPage)}
          onPageChange={setCurrentPage}
          itemsPerPage={itemsPerPage}
          onItemsPerPageChange={setItemsPerPage}
        />
      )}
    </div>
  );
};

export default Orders;

