import { createContext, useContext, useState, useEffect } from 'react';

const ToastContext = createContext(null);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = (message, type = 'info') => {
    const id = Date.now();
    setToasts([...toasts, { id, message, type }]);
    return id;
  };

  const hideToast = (id) => {
    setToasts(toasts.filter(t => t.id !== id));
  };

  return (
    <ToastContext.Provider value={{ showToast, hideToast }}>
      {children}
      <div className="fixed top-4 right-4 z-50 space-y-2 pointer-events-none">
        {toasts.map(toast => (
          <div
            key={toast.id}
            className="pointer-events-auto bg-white rounded-lg shadow-lg border border-gray-200 px-4 py-3 flex items-center space-x-3 min-w-[300px] animate-slide-in"
          >
            <div className={`flex-1 ${
              toast.type === 'success' ? 'text-green-700' :
              toast.type === 'error' ? 'text-red-700' :
              toast.type === 'warning' ? 'text-yellow-700' :
              'text-blue-700'
            }`}>
              {toast.message}
            </div>
            <button
              onClick={() => hideToast(toast.id)}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

// Add to index.css
// @keyframes slide-in {
//   from {
//     transform: translateX(400px);
//     opacity: 0;
//   }
//   to {
//     transform: translateX(0);
//     opacity: 1;
//   }
// }
