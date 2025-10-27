import { useState, useEffect } from 'react';
import { adminAPI } from '../../api';
import { FiPackage, FiShoppingBag, FiUsers, FiCreditCard } from 'react-icons/fi';

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

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={FiCreditCard}
          title="Total Revenue"
          value={stats?.revenue?.total ? `$${stats.revenue.total.toFixed(2)}` : '$0.00'}
          color="bg-blue-500"
        />
        <StatCard
          icon={FiShoppingBag}
          title="Total Orders"
          value={stats?.orders?.total || 0}
          color="bg-green-500"
        />
        <StatCard
          icon={FiUsers}
          title="Total Users"
          value={stats?.users?.total || 0}
          color="bg-purple-500"
        />
        <StatCard
          icon={FiPackage}
          title="Total Products"
          value={stats?.products?.total || 0}
          color="bg-orange-500"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Recent Activity</h2>
        <p className="text-gray-600">Dashboard analytics will appear here.</p>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, title, value, color }) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
      </div>
      <div className={`${color} p-3 rounded-full`}>
        <Icon className="w-8 h-8 text-white" />
      </div>
    </div>
  </div>
);

export default Dashboard;

