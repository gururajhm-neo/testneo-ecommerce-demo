import { useState } from 'react';
import { FiChevronDown, FiChevronUp, FiPlus, FiMinus } from 'react-icons/fi';

/**
 * Complex DOM Structure Component for TestNeo Automation Testing
 * Features:
 * - Deeply nested elements (10+ levels)
 * - Dynamic DOM manipulation
 * - Shadow DOM elements
 * - Complex selectors
 * - Nested tables
 * - Dynamic IDs and classes
 * - Multiple data attributes
 */
const ComplexDOM = () => {
  const [expandedSections, setExpandedSections] = useState(new Set());
  const [dynamicContent, setDynamicContent] = useState([]);

  const toggleSection = (id) => {
    setExpandedSections(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const addDynamicContent = () => {
    const id = Date.now();
    setDynamicContent([...dynamicContent, {
      id,
      type: 'item',
      level: Math.floor(Math.random() * 5) + 1,
      data: `Dynamic Item ${dynamicContent.length + 1}`
    }]);
  };

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="bg-white p-4 rounded-lg shadow-md">
        <button
          onClick={addDynamicContent}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center gap-2"
        >
          <FiPlus /> Add Dynamic Content
        </button>
      </div>

      {/* Deeply Nested Structure */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Deeply Nested DOM Structure (10+ levels)</h3>
        <div className="space-y-2">
          <div data-testid="level-1" className="p-4 bg-gray-50 rounded border-l-4 border-blue-500">
            <div data-testid="level-2" className="p-3 bg-white rounded border-l-4 border-green-500">
              <div data-testid="level-3" className="p-3 bg-gray-50 rounded border-l-4 border-yellow-500">
                <div data-testid="level-4" className="p-2 bg-white rounded">
                  <div data-testid="level-5" className="p-2 bg-gray-50 rounded">
                    <div data-testid="level-6" className="p-2 bg-white rounded">
                      <div data-testid="level-7" className="p-2 bg-gray-50 rounded">
                        <div data-testid="level-8" className="p-2 bg-white rounded">
                          <div data-testid="level-9" className="p-2 bg-gray-50 rounded">
                            <div data-testid="level-10" className="p-2 bg-blue-100 rounded">
                              <p className="font-semibold">Level 10 - Deeply Nested Content</p>
                              <p className="text-sm text-gray-600">This is a test for deep DOM traversal</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Nested Tables */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Nested Tables</h3>
        <table className="w-full border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border border-gray-300 p-2">Category</th>
              <th className="border border-gray-300 p-2">Items</th>
              <th className="border border-gray-300 p-2">Details</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-gray-300 p-2" rowSpan="2">Electronics</td>
              <td className="border border-gray-300 p-2">Phones</td>
              <td className="border border-gray-300 p-2">
                <table className="w-full border-collapse">
                  <tr>
                    <td className="border border-gray-200 p-1 text-xs">iPhone</td>
                    <td className="border border-gray-200 p-1 text-xs">$999</td>
                  </tr>
                  <tr>
                    <td className="border border-gray-200 p-1 text-xs">Samsung</td>
                    <td className="border border-gray-200 p-1 text-xs">$899</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td className="border border-gray-300 p-2">Laptops</td>
              <td className="border border-gray-300 p-2">
                <table className="w-full border-collapse">
                  <tr>
                    <td className="border border-gray-200 p-1 text-xs">MacBook</td>
                    <td className="border border-gray-200 p-1 text-xs">$2499</td>
                  </tr>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Complex Selectors */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Complex Selectors (data attributes, classes, IDs)</h3>
        <div className="space-y-4">
          <div
            id="complex-element-1"
            className="complex-wrapper active-item primary-section"
            data-testid="complex-1"
            data-type="container"
            data-status="active"
            data-index="0"
            aria-label="Complex Element 1"
          >
            <div className="nested-content">
              <span className="label-text" data-label="name">Element 1</span>
              <button
                className="action-btn primary-btn"
                data-action="click"
                data-target="element-1"
                onClick={() => alert('Clicked Element 1')}
              >
                Click Me
              </button>
            </div>
          </div>

          <div
            id="complex-element-2"
            className="complex-wrapper inactive-item secondary-section"
            data-testid="complex-2"
            data-type="container"
            data-status="inactive"
            data-index="1"
            aria-label="Complex Element 2"
          >
            <div className="nested-content">
              <span className="label-text" data-label="name">Element 2</span>
              <button
                className="action-btn secondary-btn"
                data-action="click"
                data-target="element-2"
                onClick={() => alert('Clicked Element 2')}
              >
                Click Me
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Dynamic Content */}
      {dynamicContent.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Dynamically Generated Content</h3>
          <div className="space-y-2">
            {dynamicContent.map((item) => (
              <div
                key={item.id}
                data-dynamic-id={item.id}
                data-dynamic-type={item.type}
                data-dynamic-level={item.level}
                className={`p-3 rounded border-l-4 ${
                  item.level === 1 ? 'border-red-500 bg-red-50' :
                  item.level === 2 ? 'border-orange-500 bg-orange-50' :
                  item.level === 3 ? 'border-yellow-500 bg-yellow-50' :
                  item.level === 4 ? 'border-green-500 bg-green-50' :
                  'border-blue-500 bg-blue-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>{item.data} (Level {item.level})</span>
                  <button
                    onClick={() => setDynamicContent(dynamicContent.filter(i => i.id !== item.id))}
                    className="text-red-600 hover:text-red-700"
                  >
                    <FiMinus />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Collapsible Nested Sections */}
      <div className="bg-white rounded-lg shadow-md">
        <h3 className="text-lg font-semibold p-6 pb-4">Collapsible Nested Sections</h3>
        {[1, 2, 3].map((sectionId) => (
          <div key={sectionId} className="border-b last:border-b-0">
            <button
              onClick={() => toggleSection(sectionId)}
              className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50"
              data-section-id={sectionId}
            >
              <span className="font-semibold">Section {sectionId}</span>
              {expandedSections.has(sectionId) ? <FiChevronUp /> : <FiChevronDown />}
            </button>
            {expandedSections.has(sectionId) && (
              <div className="px-6 py-4 bg-gray-50">
                <div className="space-y-2">
                  <div className="p-3 bg-white rounded">
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="p-2 bg-white rounded">
                        <p className="text-sm">Nested content level 3 in Section {sectionId}</p>
                        <div className="mt-2 space-x-2">
                          <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm">Action 1</button>
                          <button className="px-3 py-1 bg-green-600 text-white rounded text-sm">Action 2</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Shadow DOM Simulation */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Shadow DOM-like Structure</h3>
        <div className="relative">
          <div className="p-4 bg-gray-100 rounded border-2 border-dashed border-gray-300">
            <div className="text-xs text-gray-500 mb-2">Shadow Root (simulated)</div>
            <div className="p-3 bg-white rounded">
              <div className="p-2 bg-gray-50 rounded">
                <p className="text-sm">Content inside shadow boundary</p>
                <input
                  type="text"
                  placeholder="Input in shadow DOM"
                  className="mt-2 w-full px-3 py-2 border border-gray-300 rounded"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Multiple Data Attributes */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Multiple Data Attributes</h3>
        <div className="grid grid-cols-2 gap-4">
          {[1, 2, 3, 4].map((idx) => (
            <div
              key={idx}
              data-component="card"
              data-id={`card-${idx}`}
              data-index={idx}
              data-type="interactive"
              data-visible="true"
              data-loaded="true"
              data-test-scenario={`scenario-${idx}`}
              className="p-4 border-2 border-gray-300 rounded-lg hover:border-primary-500 cursor-pointer"
            >
              <h4 className="font-semibold">Card {idx}</h4>
              <p className="text-sm text-gray-600">Multiple data attributes for testing</p>
              <div className="mt-2 text-xs text-gray-500">
                data-component, data-id, data-index, data-type, data-visible, data-loaded, data-test-scenario
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ComplexDOM;
