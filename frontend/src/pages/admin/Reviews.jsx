import { useState, useEffect } from 'react';
import { adminReviewsAPI } from '../../api';
import { FiCheck, FiX, FiTrash2, FiSearch } from 'react-icons/fi';

const Reviews = () => {
  const [reviews, setReviews] = useState([]);
  const [allReviews, setAllReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [approvalFilter, setApprovalFilter] = useState('all');

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await adminReviewsAPI.getAllReviews({ limit: 100 });
      // Backend returns data in different formats
      const reviewsData = response.data.reviews || response.data || [];
      const reviewsArray = Array.isArray(reviewsData) ? reviewsData : [];
      setAllReviews(reviewsArray);
      setReviews(reviewsArray);
      console.log('Reviews fetched:', reviewsArray.length);
      console.log('Sample review:', reviewsArray[0]);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setReviews([]);
      setAllReviews([]);
    } finally {
      setLoading(false);
    }
  };

  // Filter reviews based on search and approval status
  useEffect(() => {
    let filtered = [...allReviews];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(review =>
        review.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        review.comment?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        review.product_name?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Approval filter
    if (approvalFilter === 'approved') {
      filtered = filtered.filter(review => review.is_approved);
    } else if (approvalFilter === 'pending') {
      filtered = filtered.filter(review => !review.is_approved);
    }

    setReviews(filtered);
  }, [searchTerm, approvalFilter, allReviews]);

  const handleApprove = async (id) => {
    try {
      await adminReviewsAPI.approveReview(id);
      fetchReviews();
    } catch (error) {
      console.error('Error approving review:', error);
      alert('Failed to approve review.');
    }
  };

  const handleReject = async (id) => {
    try {
      await adminReviewsAPI.rejectReview(id);
      fetchReviews();
    } catch (error) {
      console.error('Error rejecting review:', error);
      alert('Failed to reject review.');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this review?')) {
      try {
        await adminReviewsAPI.deleteReview(id);
        fetchReviews();
      } catch (error) {
        console.error('Error deleting review:', error);
        alert('Failed to delete review.');
      }
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading reviews...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Reviews</h1>

      {/* Search and Filter Bar */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search */}
          <div className="relative">
            <FiSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search reviews..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Approval Status Filter */}
          <select
            value={approvalFilter}
            onChange={(e) => setApprovalFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="all">All Reviews</option>
            <option value="approved">Approved Only</option>
            <option value="pending">Pending Only</option>
          </select>
        </div>

        {/* Results count */}
        <div className="mt-3 text-sm text-gray-600">
          Showing {reviews.length} of {allReviews.length} reviews
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rating</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comment</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {reviews.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-6 py-8 text-center text-gray-500">
                  No reviews found. Reviews will appear here after customers leave feedback on products.
                </td>
              </tr>
            ) : (
              reviews.map((review) => (
                <tr key={review.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {review.product_name || `Product #${review.product_id}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <span className="text-yellow-500">{'★'.repeat(review.rating || 0)}</span>
                      <span className="ml-2 text-sm text-gray-600">{review.rating}/5</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900 max-w-xs">
                    <div className="font-medium">{review.title || 'No title'}</div>
                    <div className="text-gray-500 text-xs truncate">{review.comment || 'No comment'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        review.is_approved
                          ? 'bg-green-100 text-green-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {review.is_approved ? 'Approved' : 'Pending'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    {!review.is_approved && (
                      <>
                        <button 
                          onClick={() => handleApprove(review.id)}
                          className="text-green-600 hover:text-green-900"
                          title="Approve Review"
                        >
                          <FiCheck className="w-5 h-5" />
                        </button>
                        <button 
                          onClick={() => handleReject(review.id)}
                          className="text-yellow-600 hover:text-yellow-900"
                          title="Reject Review"
                        >
                          <FiX className="w-5 h-5" />
                        </button>
                      </>
                    )}
                    <button 
                      onClick={() => handleDelete(review.id)}
                      className="text-red-600 hover:text-red-900"
                      title="Delete Review"
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
    </div>
  );
};

export default Reviews;

