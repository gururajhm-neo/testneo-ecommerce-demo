import { useState, useEffect } from 'react';
import { adminReviewsAPI } from '../../api';
import { FiCheck, FiX, FiTrash2 } from 'react-icons/fi';

const Reviews = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await adminReviewsAPI.getAllReviews();
      // Backend returns an array directly
      setReviews(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    } finally {
      setLoading(false);
    }
  };

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
            {reviews.slice(0, 10).map((review) => (
              <tr key={review.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  Product #{review.product_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <span className="text-yellow-500">{'★'.repeat(review.rating || 0)}</span>
                    <span className="ml-2 text-sm text-gray-600">{review.rating}/5</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                  {review.comment}
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
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Reviews;

