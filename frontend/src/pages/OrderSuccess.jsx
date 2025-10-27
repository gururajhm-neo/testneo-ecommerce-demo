import { Link } from 'react-router-dom';
import { FiCheckCircle, FiPackage, FiHome } from 'react-icons/fi';

const OrderSuccess = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-2xl mx-auto text-center px-4">
        <div className="bg-white rounded-lg shadow-lg p-12">
          <div className="mb-6">
            <FiCheckCircle className="w-24 h-24 text-green-500 mx-auto" />
          </div>

          <h1 className="text-3xl font-bold text-gray-800 mb-4">
            Order Placed Successfully!
          </h1>

          <p className="text-gray-600 mb-8">
            Thank you for your purchase. Your order has been received and is being processed.
            You will receive a confirmation email shortly.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/orders"
              className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition gap-2"
            >
              <FiPackage className="w-5 h-5" />
              View Orders
            </Link>

            <Link
              to="/products"
              className="inline-flex items-center justify-center px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition gap-2"
            >
              <FiHome className="w-5 h-5" />
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderSuccess;

