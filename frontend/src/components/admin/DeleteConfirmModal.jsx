import { FiAlertTriangle, FiTrash2, FiLoader } from 'react-icons/fi';

/**
 * Reusable delete-confirmation modal.
 *
 * Props:
 *   isOpen      - boolean
 *   onClose     - () => void
 *   onConfirm   - () => void
 *   loading     - boolean
 *   title       - string  (default: "Delete item")
 *   description - string  (default: generic warning)
 *   itemName    - string  (shown in bold inside the description)
 */
const DeleteConfirmModal = ({
  isOpen,
  onClose,
  onConfirm,
  loading = false,
  title = 'Delete item',
  description,
  itemName,
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: 'rgba(0,0,0,0.55)' }}
      onClick={(e) => { if (e.target === e.currentTarget && !loading) onClose(); }}
    >
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md animate-modal-in">

        {/* Icon + Title */}
        <div className="px-6 pt-6 pb-4 flex flex-col items-center text-center">
          <div className="w-14 h-14 rounded-full bg-red-50 flex items-center justify-center mb-4">
            <FiAlertTriangle className="w-7 h-7 text-red-500" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <p className="mt-2 text-sm text-gray-500 leading-relaxed">
            {description || (
              <>
                Are you sure you want to delete
                {itemName ? <> <span className="font-medium text-gray-700">"{itemName}"</span></> : ' this item'}?
                <br />
                This action <span className="font-medium text-red-600">cannot be undone</span>.
              </>
            )}
          </p>
        </div>

        {/* Actions */}
        <div className="flex gap-3 px-6 pb-6">
          <button
            onClick={onClose}
            disabled={loading}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition disabled:opacity-40"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={loading}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-60"
          >
            {loading ? (
              <FiLoader className="w-4 h-4 animate-spin" />
            ) : (
              <FiTrash2 className="w-4 h-4" />
            )}
            {loading ? 'Deleting…' : 'Yes, delete'}
          </button>
        </div>

      </div>
    </div>
  );
};

export default DeleteConfirmModal;
