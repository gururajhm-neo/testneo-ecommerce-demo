import { useState, useRef, useEffect } from 'react';
import { FiExternalLink, FiRefreshCw, FiX, FiMaximize2, FiMinimize2 } from 'react-icons/fi';

/**
 * Iframe Container Component for TestNeo Automation Testing
 * Features:
 * - Multiple iframes
 * - Nested iframes
 * - Dynamic iframe loading
 * - Iframe communication (postMessage)
 * - Iframe resizing
 * - Iframe sandbox attributes
 */
const IframeContainer = ({ defaultUrl = 'https://example.com', title = 'Iframe Container' }) => {
  const [url, setUrl] = useState(defaultUrl);
  const [iframes, setIframes] = useState([
    { id: 1, url: 'https://example.com', title: 'Iframe 1', sandbox: 'allow-same-origin allow-scripts' },
    { id: 2, url: 'https://www.w3.org', title: 'Iframe 2', sandbox: 'allow-same-origin allow-scripts allow-forms' },
  ]);
  const [nestedIframe, setNestedIframe] = useState(false);
  const [messages, setMessages] = useState([]);
  const iframeRefs = useRef({});

  const addIframe = () => {
    const newId = Math.max(...iframes.map(i => i.id), 0) + 1;
    setIframes([...iframes, {
      id: newId,
      url: url,
      title: `Iframe ${newId}`,
      sandbox: 'allow-same-origin allow-scripts'
    }]);
  };

  const removeIframe = (id) => {
    setIframes(iframes.filter(i => i.id !== id));
  };

  const updateIframeUrl = (id, newUrl) => {
    setIframes(iframes.map(i => i.id === id ? { ...i, url: newUrl } : i));
  };

  const sendMessageToIframe = (id, message) => {
    const iframe = iframeRefs.current[id];
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage(message, '*');
      setMessages(prev => [...prev, { type: 'sent', to: id, message }]);
    }
  };

  const handleIframeMessage = (event) => {
    setMessages(prev => [...prev, { type: 'received', from: 'iframe', message: event.data }]);
  };

  // Listen for messages from iframes
  useEffect(() => {
    window.addEventListener('message', handleIframeMessage);
    return () => window.removeEventListener('message', handleIframeMessage);
  }, []);

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <div className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-sm font-medium text-gray-700 mb-2">Iframe URL</label>
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <button
            onClick={addIframe}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Add Iframe
          </button>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={nestedIframe}
              onChange={(e) => setNestedIframe(e.target.checked)}
              className="rounded"
            />
            <span className="text-sm">Nested Iframe</span>
          </label>
        </div>
      </div>

      {/* Iframes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {iframes.map((iframe) => (
          <div key={iframe.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-gray-100 px-4 py-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-semibold">{iframe.title}</span>
                <a
                  href={iframe.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700"
                >
                  <FiExternalLink className="w-4 h-4" />
                </a>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => sendMessageToIframe(iframe.id, { type: 'ping', timestamp: Date.now() })}
                  className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Send Message
                </button>
                <button
                  onClick={() => removeIframe(iframe.id)}
                  className="p-1 text-red-600 hover:bg-red-50 rounded"
                >
                  <FiX />
                </button>
              </div>
            </div>
            <div className="relative" style={{ height: '400px' }}>
              <iframe
                ref={(el) => (iframeRefs.current[iframe.id] = el)}
                src={iframe.url}
                title={iframe.title}
                sandbox={iframe.sandbox}
                className="w-full h-full border-0"
                allow="camera; microphone; geolocation"
              />
              {nestedIframe && iframe.id === 1 && (
                <div className="absolute inset-4 bg-white border-2 border-dashed border-gray-300 rounded">
                  <div className="p-2 bg-gray-100 text-xs font-semibold">Nested Iframe</div>
                  <iframe
                    src="https://www.example.com"
                    className="w-full h-full border-0"
                    style={{ height: 'calc(100% - 32px)' }}
                  />
                </div>
              )}
            </div>
            <div className="p-2 bg-gray-50 text-xs text-gray-600">
              Sandbox: {iframe.sandbox || 'none'}
            </div>
          </div>
        ))}
      </div>

      {/* Messages Log */}
      {messages.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-4">
          <h3 className="font-semibold mb-2">Message Log</h3>
          <div className="max-h-40 overflow-y-auto space-y-1">
            {messages.slice(-10).map((msg, idx) => (
              <div key={idx} className="text-xs p-2 bg-gray-50 rounded">
                <span className={`font-semibold ${msg.type === 'sent' ? 'text-blue-600' : 'text-green-600'}`}>
                  {msg.type === 'sent' ? '→' : '←'}
                </span>
                {' '}
                {JSON.stringify(msg.message)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Iframe Testing Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-semibold text-blue-900 mb-2">Iframe Testing Scenarios</h3>
        <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
          <li>Test iframe loading and content access</li>
          <li>Test postMessage communication</li>
          <li>Test sandbox attribute restrictions</li>
          <li>Test nested iframe structures</li>
          <li>Test iframe resizing and responsive behavior</li>
          <li>Test cross-origin iframe interactions</li>
        </ul>
      </div>
    </div>
  );
};

export default IframeContainer;
