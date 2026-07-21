import { useState, useEffect } from 'react';
import { FiX } from 'react-icons/fi';
import { useToast } from '../Toast';
import { adminCouponsAPI, extractErrorMessage } from '../../api';

function defaultDates() {
  const from = new Date();
  const until = new Date();
  until.setFullYear(until.getFullYear() + 1);
  const toInput = (d) => d.toISOString().slice(0, 10);
  return { valid_from: toInput(from), valid_until: toInput(until) };
}

const emptyForm = () => ({
  code: '',
  name: '',
  discount_type: 'percentage',
  discount_value: '',
  minimum_order_amount: '0',
  max_uses: '',
  is_active: true,
  ...defaultDates(),
});

const CouponModal = ({ isOpen, onClose, couponId, existingCoupon, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();
  const [formData, setFormData] = useState(emptyForm());

  useEffect(() => {
    if (!isOpen) {
      setFormData(emptyForm());
      return;
    }
    if (couponId && existingCoupon) {
      const from = existingCoupon.valid_from
        ? String(existingCoupon.valid_from).slice(0, 10)
        : defaultDates().valid_from;
      const until = existingCoupon.valid_until
        ? String(existingCoupon.valid_until).slice(0, 10)
        : defaultDates().valid_until;
      setFormData({
        code: existingCoupon.code || '',
        name: existingCoupon.name || '',
        discount_type: existingCoupon.discount_type || 'percentage',
        discount_value: existingCoupon.discount_value ?? '',
        minimum_order_amount: existingCoupon.minimum_order_amount ?? '0',
        max_uses: existingCoupon.max_uses ?? '',
        is_active: existingCoupon.is_active !== false,
        valid_from: from,
        valid_until: until,
      });
    } else {
      setFormData(emptyForm());
    }
  }, [isOpen, couponId, existingCoupon]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        code: String(formData.code || '').trim().toUpperCase(),
        name: String(formData.name || '').trim(),
        discount_type: formData.discount_type,
        discount_value: parseFloat(formData.discount_value),
        minimum_order_amount: parseFloat(formData.minimum_order_amount || '0') || 0,
        max_uses: formData.max_uses ? parseInt(formData.max_uses, 10) : null,
        valid_from: new Date(formData.valid_from).toISOString(),
        valid_until: new Date(`${formData.valid_until}T23:59:59`).toISOString(),
      };

      if (couponId) {
        await adminCouponsAPI.update(couponId, {
          name: payload.name,
          discount_value: payload.discount_value,
          minimum_order_amount: payload.minimum_order_amount,
          max_uses: payload.max_uses,
          valid_from: payload.valid_from,
          valid_until: payload.valid_until,
          is_active: !!formData.is_active,
        });
        showToast('Coupon updated successfully!', 'success');
      } else {
        await adminCouponsAPI.create(payload);
        showToast('Coupon created successfully!', 'success');
      }

      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error saving coupon:', error);
      showToast('Failed to save coupon. ' + extractErrorMessage(error), 'error');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white border-b p-4 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-900">
            {couponId ? 'Edit Coupon' : 'Add Coupon'}
          </h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <FiX className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Code *</label>
            <input
              type="text"
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              required
              disabled={!!couponId}
              minLength={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Type *</label>
              <select
                value={formData.discount_type}
                onChange={(e) => setFormData({ ...formData, discount_type: e.target.value })}
                required
                disabled={!!couponId}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 disabled:bg-gray-100"
              >
                <option value="percentage">Percentage</option>
                <option value="fixed">Fixed Amount</option>
                <option value="free_shipping">Free Shipping</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Value *</label>
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={formData.discount_value}
                onChange={(e) => setFormData({ ...formData, discount_value: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Min order amount</label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={formData.minimum_order_amount}
                onChange={(e) => setFormData({ ...formData, minimum_order_amount: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max uses</label>
              <input
                type="number"
                min="1"
                value={formData.max_uses}
                onChange={(e) => setFormData({ ...formData, max_uses: e.target.value })}
                placeholder="Unlimited"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Valid from *</label>
              <input
                type="date"
                value={formData.valid_from}
                onChange={(e) => setFormData({ ...formData, valid_from: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Valid until *</label>
              <input
                type="date"
                value={formData.valid_until}
                onChange={(e) => setFormData({ ...formData, valid_until: e.target.value })}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          {couponId && (
            <label className="flex items-center gap-2 text-sm text-gray-700">
              <input
                type="checkbox"
                checked={!!formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
              />
              Active
            </label>
          )}

          <div className="flex justify-end space-x-4 pt-4 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition disabled:opacity-50"
            >
              {loading ? 'Saving...' : couponId ? 'Update Coupon' : 'Create Coupon'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CouponModal;
