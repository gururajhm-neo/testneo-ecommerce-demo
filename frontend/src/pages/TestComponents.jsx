import { useState } from 'react';
import DataTable from '../components/DataTable';
import MultiStepForm from '../components/MultiStepForm';
import FileUpload from '../components/FileUpload';
import IframeContainer from '../components/IframeContainer';
import ComplexDOM from '../components/ComplexDOM';
import { useToast } from '../components/Toast';

/**
 * Test Components Page for TestNeo Automation Testing
 * Showcases all complex UI components for testing scenarios
 */
const TestComponents = () => {
  const { showToast } = useToast();
  const [activeTab, setActiveTab] = useState('datatable');

  // Sample data for DataTable
  const tableData = [
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin', status: 'Active', created: '2024-01-15' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'User', status: 'Active', created: '2024-01-20' },
    { id: 3, name: 'Bob Wilson', email: 'bob@example.com', role: 'User', status: 'Inactive', created: '2024-02-01' },
    { id: 4, name: 'Alice Brown', email: 'alice@example.com', role: 'Moderator', status: 'Active', created: '2024-02-10' },
  ];

  const tableColumns = [
    { key: 'name', header: 'Name', sortable: true, filterable: true },
    { key: 'email', header: 'Email', sortable: true, filterable: true },
    { 
      key: 'role', 
      header: 'Role', 
      sortable: true, 
      filterable: true,
      filterType: 'select',
      filterOptions: [
        { value: 'Admin', label: 'Admin' },
        { value: 'User', label: 'User' },
        { value: 'Moderator', label: 'Moderator' }
      ]
    },
    { 
      key: 'status', 
      header: 'Status', 
      sortable: true,
      filterType: 'select',
      filterOptions: [
        { value: 'Active', label: 'Active' },
        { value: 'Inactive', label: 'Inactive' }
      ],
      render: (row) => (
        <span className={`px-2 py-1 rounded text-xs font-semibold ${
          row.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}>
          {row.status}
        </span>
      )
    },
    { key: 'created', header: 'Created', sortable: true }
  ];

  // Multi-step form steps
  const formSteps = [
    {
      title: 'Personal Info',
      component: ({ formData, updateFormData, errors }) => (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            <input
              type="text"
              value={formData.firstName || ''}
              onChange={(e) => updateFormData({ firstName: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            {errors.firstName && <p className="text-red-500 text-sm mt-1">{errors.firstName}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            <input
              type="text"
              value={formData.lastName || ''}
              onChange={(e) => updateFormData({ lastName: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            {errors.lastName && <p className="text-red-500 text-sm mt-1">{errors.lastName}</p>}
          </div>
        </div>
      ),
      validate: (data) => {
        const errors = {};
        if (!data.firstName) errors.firstName = 'First name is required';
        if (!data.lastName) errors.lastName = 'Last name is required';
        return errors;
      }
    },
    {
      title: 'Contact',
      component: ({ formData, updateFormData, errors }) => (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              value={formData.email || ''}
              onChange={(e) => updateFormData({ email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            <input
              type="tel"
              value={formData.phone || ''}
              onChange={(e) => updateFormData({ phone: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
      ),
      validate: (data) => {
        const errors = {};
        if (!data.email) errors.email = 'Email is required';
        else if (!/\S+@\S+\.\S+/.test(data.email)) errors.email = 'Email is invalid';
        return errors;
      }
    },
    {
      title: 'Review',
      component: ({ formData }) => (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold mb-4">Review Your Information</h3>
          <div className="bg-gray-50 p-4 rounded-lg space-y-2">
            <p><strong>Name:</strong> {formData.firstName} {formData.lastName}</p>
            <p><strong>Email:</strong> {formData.email}</p>
            <p><strong>Phone:</strong> {formData.phone || 'Not provided'}</p>
          </div>
        </div>
      ),
      validate: () => ({})
    }
  ];

  const tabs = [
    { id: 'datatable', label: 'Data Table', icon: '📊' },
    { id: 'multistep', label: 'Multi-Step Form', icon: '📝' },
    { id: 'fileupload', label: 'File Upload', icon: '📁' },
    { id: 'iframes', label: 'Iframes', icon: '🖼️' },
    { id: 'complexdom', label: 'Complex DOM', icon: '🌳' },
    { id: 'charts', label: 'Charts', icon: '📈' },
    { id: 'tabs', label: 'Tabs & Accordions', icon: '📑' },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">TestNeo UI Components Testing</h1>
      
      {/* Tabs Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="mt-6">
        {activeTab === 'datatable' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">Advanced Data Table</h2>
            <DataTable
              data={tableData}
              columns={tableColumns}
              onRowClick={(row) => showToast(`Clicked on ${row.name}`, 'info')}
              onBulkAction={(action, ids) => showToast(`Bulk action: ${action} on ${ids.length} items`, 'info')}
              onExport={(data) => showToast(`Exported ${data.length} rows`, 'success')}
              pageSize={5}
            />
          </div>
        )}

        {activeTab === 'multistep' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">Multi-Step Form Wizard</h2>
            <MultiStepForm
              steps={formSteps}
              onSubmit={(data) => {
                showToast('Form submitted successfully!', 'success');
                console.log('Form data:', data);
              }}
              onStepChange={(step, data) => {
                console.log(`Step ${step} changed`, data);
              }}
            />
          </div>
        )}

        {activeTab === 'fileupload' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">File Upload with Drag & Drop</h2>
            <FileUpload
              accept="image/*,.pdf,.doc,.docx"
              multiple={true}
              maxSize={5 * 1024 * 1024}
              maxFiles={5}
              onUpload={async (file, onProgress) => {
                // Simulate upload
                for (let i = 0; i <= 100; i += 10) {
                  await new Promise(resolve => setTimeout(resolve, 100));
                  onProgress(i);
                }
                showToast(`${file.name} uploaded successfully!`, 'success');
              }}
            />
          </div>
        )}

        {activeTab === 'iframes' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">Iframe Testing</h2>
            <p className="text-gray-600 mb-4">
              Test iframe interactions, nested iframes, and iframe communication scenarios.
            </p>
            <IframeContainer 
              defaultUrl="https://example.com"
              title="Main Iframe Container"
            />
          </div>
        )}

        {activeTab === 'complexdom' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold mb-4">Complex DOM Structures</h2>
            <ComplexDOM />
          </div>
        )}

        {activeTab === 'charts' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold mb-4">Interactive Charts</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold mb-4">Sales Chart</h3>
                <div className="h-64 flex items-end justify-around gap-2">
                  {[65, 80, 45, 90, 70, 85, 60].map((height, idx) => (
                    <div key={idx} className="flex-1 flex flex-col items-center">
                      <div
                        className="w-full bg-primary-600 rounded-t hover:bg-primary-700 transition-all cursor-pointer"
                        style={{ height: `${height}%` }}
                        title={`Value: ${height}`}
                      />
                      <span className="text-xs text-gray-600 mt-2">Day {idx + 1}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold mb-4">Pie Chart</h3>
                <div className="h-64 flex items-center justify-center">
                  <div className="relative w-48 h-48">
                    <svg viewBox="0 0 100 100" className="transform -rotate-90">
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke="#e5e7eb"
                        strokeWidth="20"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke="#3b82f6"
                        strokeWidth="20"
                        strokeDasharray={`${40 * 2 * Math.PI * 0.4} ${40 * 2 * Math.PI}`}
                        strokeDashoffset="0"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-2xl font-bold">40%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'tabs' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold mb-4">Tabs & Accordions</h2>
            
            {/* Nested Tabs Example */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold mb-4">Nested Tabs</h3>
              <div className="border-b mb-4">
                <div className="flex space-x-4">
                  {['Tab 1', 'Tab 2', 'Tab 3'].map((tab, idx) => (
                    <button
                      key={idx}
                      className={`py-2 px-4 border-b-2 ${
                        idx === 0 ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500'
                      }`}
                    >
                      {tab}
                    </button>
                  ))}
                </div>
              </div>
              <p className="text-gray-600">Content for selected tab...</p>
            </div>

            {/* Accordion Example */}
            <div className="bg-white rounded-lg shadow-md">
              {[
                { title: 'Accordion Item 1', content: 'This is the content for the first accordion item.' },
                { title: 'Accordion Item 2', content: 'This is the content for the second accordion item.' },
                { title: 'Accordion Item 3', content: 'This is the content for the third accordion item.' },
              ].map((item, idx) => (
                <div key={idx} className="border-b last:border-b-0">
                  <button className="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50">
                    <span className="font-semibold">{item.title}</span>
                    <span className="text-gray-400">+</span>
                  </button>
                  {idx === 0 && (
                    <div className="px-6 py-4 bg-gray-50">
                      <p className="text-gray-600">{item.content}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TestComponents;

