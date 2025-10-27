import { useState, useEffect } from 'react';
import { adminAPI } from '../../api';
import { FiPackage, FiShoppingBag, FiUsers, FiCreditCard, FiTrendingUp, FiAlertCircle, FiCheckCircle } from 'react-icons/fi';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await adminAPI.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
      setError('Failed to load dashboard statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-xl text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  const getPercentage = (current, total) => {
    if (!total || total === 0) return 0;
    return ((current / total) * 100).toFixed(1);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button 
          onClick={fetchStats}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition text-sm"
        >
          Refresh Data
        </button>
      </div>

      {/* Main Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={FiCreditCard}
          title="Total Revenue"
          value={stats?.revenue?.total ? `$${stats.revenue.total.toFixed(2)}` : '$0.00'}
          subvalue={stats?.revenue?.today ? `Today: $${stats.revenue.today.toFixed(2)}` : ''}
          color="bg-blue-500"
        />
        <StatCard
          icon={FiShoppingBag}
          title="Total Orders"
          value={stats?.orders?.total || 0}
          subvalue={`Pending: ${stats?.orders?.pending || 0}`}
          color="bg-green-500"
        />
        <StatCard
          icon={FiUsers}
          title="Total Users"
          value={stats?.users?.total || 0}
          subvalue={`Active: ${stats?.users?.active || 0}`}
          color="bg-purple-500"
        />
        <StatCard
          icon={FiPackage}
          title="Total Products"
          value={stats?.products?.total || 0}
          subvalue={`Active: ${stats?.products?.active || 0}`}
          color="bg-orange-500"
        />
      </div>

      {/* Detailed Analytics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Orders Breakdown */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <FiShoppingBag className="mr-2" />
            Order Status Breakdown
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded">
              <span className="font-medium text-yellow-800">Pending Orders</span>
              <span className="text-xl font-bold text-yellow-900">{stats?.orders?.pending || 0}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded">
              <span className="font-medium text-green-800">Completed Orders</span>
              <span className="text-xl font-bold text-green-900">{stats?.orders?.completed || 0}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-red-50 rounded">
              <span className="font-medium text-red-800">Cancelled Orders</span>
              <span className="text-xl font-bold text-red-900">{stats?.orders?.cancelled || 0}</span>
            </div>
          </div>
        </div>

        {/* Products Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <FiPackage className="mr-2" />
            Inventory Status
          </h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded">
              <span className="font-medium text-blue-800">Active Products</span>
              <span className="text-xl font-bold text-blue-900">{stats?.products?.active || 0}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded">
              <span className="font-medium text-yellow-800">Low Stock</span>
              <span className="text-xl font-bold text-yellow-900">{stats?.products?.low_stock || 0}</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-red-50 rounded">
              <span className="font-medium text-red-800">Out of Stock</span>
              <span className="text-xl font-bold text-red-900">{stats?.products?.out_of_stock || 0}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Reviews and Coupons */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <FiTrendingUp className="mr-2" />
            Reviews Status
          </h2>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Total Reviews</span>
              <span className="font-bold">{stats?.reviews?.total || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-yellow-600">Pending Approval</span>
              <span className="font-bold text-yellow-600">{stats?.reviews?.pending || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-green-600">Approved</span>
              <span className="font-bold text-green-600">{stats?.reviews?.approved || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
            <FiShoppingBag className="mr-2" />
            Coupons Status
          </h2>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-gray-600">Total Coupons</span>
              <span className="font-bold">{stats?.coupons?.total || 0}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-green-600">Active Coupons</span>
              <span className="font-bold text-green-600">{stats?.coupons?.active || 0}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Inventory Alerts */}
      {(stats?.products?.low_stock > 0 || stats?.products?.out_of_stock > 0) && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-900 mb-4 flex items-center">
            <FiAlertCircle className="mr-2" />
            Inventory Alerts
          </h2>
          <div className="grid grid-cols-2 gap-4">
            {stats?.products?.low_stock > 0 && (
              <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-300">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-yellow-800 font-semibold">Low Stock Items</p>
                    <p className="text-2xl font-bold text-yellow-900">{stats.products.low_stock}</p>
                  </div>
                  <FiAlertCircle className="text-yellow-600 text-3xl" />
                </div>
              </div>
            )}
            {stats?.products?.out_of_stock > 0 && (
              <div className="bg-red-50 p-4 rounded-lg border border-red-300">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-red-800 font-semibold">Out of Stock Items</p>
                    <p className="text-2xl font-bold text-red-900">{stats.products.out_of_stock}</p>
                  </div>
                  <FiAlertCircle className="text-red-600 text-3xl" />
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sales Charts */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Sales Overview</h2>
        <div className="grid grid-cols-2 gap-6 mb-6">
          <SimpleBarChart 
            title="Order Status Distribution"
            data={[
              { name: 'Pending', value: stats?.orders?.pending || 0, color: 'bg-yellow-500' },
              { name: 'Delivered', value: stats?.orders?.completed || 0, color: 'bg-green-500' },
              { name: 'Cancelled', value: stats?.orders?.cancelled || 0, color: 'bg-red-500' }
            ]}
          />
          <SimpleBarChart
            title="Product Inventory Status"
            data={[
              { name: 'Active', value: stats?.products?.active || 0, color: 'bg-blue-500' },
              { name: 'Low Stock', value: stats?.products?.low_stock || 0, color: 'bg-yellow-500' },
              { name: 'Out of Stock', value: stats?.products?.out_of_stock || 0, color: 'bg-red-500' }
            ]}
          />
        </div>
      </div>

      {/* Performance Indicators */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Performance Indicators</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-green-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-green-800 font-medium">Order Fulfillment Rate</span>
              <FiCheckCircle className="text-green-600" />
            </div>
            <div className="text-3xl font-bold text-green-900">
              {stats?.orders?.total ? getPercentage(stats?.orders?.completed || 0, stats?.orders?.total) : 0}%
            </div>
            <div className="text-sm text-green-600">Completed / Total Orders</div>
          </div>
          
          <div className="p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-blue-800 font-medium">Product Availability</span>
              <FiPackage className="text-blue-600" />
            </div>
            <div className="text-3xl font-bold text-blue-900">
              {stats?.products?.total ? getPercentage(stats?.products?.active || 0, stats?.products?.total) : 0}%
            </div>
            <div className="text-sm text-blue-600">Active / Total Products</div>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-purple-800 font-medium">Review Approval Rate</span>
              <FiTrendingUp className="text-purple-600" />
            </div>
            <div className="text-3xl font-bold text-purple-900">
              {stats?.reviews?.total ? getPercentage(stats?.reviews?.approved || 0, stats?.reviews?.total) : 0}%
            </div>
            <div className="text-sm text-purple-600">Approved / Total Reviews</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, subvalue, color }) => (
  <div className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition">
    <div className="flex items-center justify-between">
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        {subvalue && <p className="text-xs text-gray-500 mt-1">{subvalue}</p>}
      </div>
      <div className={`${color} p-3 rounded-full`}>
        <Icon className="w-8 h-8 text-white" />
      </div>
    </div>
  </div>
);

const SimpleBarChart = ({ title, data }) => {
  const maxValue = Math.max(...data.map(d => d.value), 1);
  
  return (
    <div>
      <h3 className="text-md font-semibold text-gray-700 mb-3">{title}</h3>
      <div className="space-y-2">
        {data.map((item, index) => (
          <div key={index}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-gray-600">{item.name}</span>
              <span className="text-sm font-semibold">{item.value}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div
                className={`${item.color} h-4 rounded-full transition-all duration-300`}
                style={{ width: `${(item.value / maxValue) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;

