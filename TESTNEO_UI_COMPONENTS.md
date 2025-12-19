# TestNeo UI Components Guide

This document describes all the complex UI components added to the e-commerce application for TestNeo web automation testing.

## 🎯 Purpose

These components are designed to provide comprehensive testing scenarios for web automation tools, including:
- Complex interactions (drag & drop, multi-step forms)
- Dynamic content (sorting, filtering, pagination)
- File operations (upload, validation)
- Data visualization (charts, tables)
- State management scenarios

## 📦 Components

### 1. Advanced DataTable (`components/DataTable.jsx`)

**Features:**
- ✅ Multi-column sorting (ascending/descending)
- ✅ Text and select-based filtering
- ✅ Pagination with customizable page size
- ✅ Bulk selection and actions
- ✅ CSV export functionality
- ✅ Row click handlers
- ✅ Loading states
- ✅ Responsive design
- ✅ Custom cell rendering

**Testing Scenarios:**
- Sort columns in different orders
- Filter data by multiple criteria
- Select multiple rows and perform bulk actions
- Export data to CSV
- Navigate through paginated data
- Handle empty states
- Test responsive behavior

**Usage:**
```jsx
<DataTable
  data={tableData}
  columns={columns}
  onRowClick={(row) => console.log(row)}
  onBulkAction={(action, ids) => console.log(action, ids)}
  onExport={(data) => console.log(data)}
  pageSize={10}
/>
```

### 2. Multi-Step Form (`components/MultiStepForm.jsx`)

**Features:**
- ✅ Step-by-step navigation
- ✅ Progress indicator
- ✅ Per-step validation
- ✅ Conditional step rendering
- ✅ Step summary/review
- ✅ Form data persistence
- ✅ Error handling per step

**Testing Scenarios:**
- Navigate forward/backward through steps
- Validate form at each step
- Skip steps conditionally
- Submit complete form
- Handle validation errors
- Test step completion states

**Usage:**
```jsx
<MultiStepForm
  steps={[
    {
      title: 'Step 1',
      component: ({ formData, updateFormData }) => <InputField />,
      validate: (data) => ({ /* errors */ })
    }
  ]}
  onSubmit={(data) => console.log(data)}
/>
```

### 3. File Upload (`components/FileUpload.jsx`)

**Features:**
- ✅ Drag and drop support
- ✅ Multiple file upload
- ✅ File type validation
- ✅ File size validation
- ✅ Upload progress tracking
- ✅ File preview (images)
- ✅ Upload queue management
- ✅ Error handling

**Testing Scenarios:**
- Drag and drop files
- Select multiple files
- Validate file types
- Validate file sizes
- Track upload progress
- Handle upload errors
- Remove files from queue
- Preview uploaded files

**Usage:**
```jsx
<FileUpload
  accept="image/*,.pdf"
  multiple={true}
  maxSize={5 * 1024 * 1024}
  maxFiles={5}
  onUpload={async (file, onProgress) => {
    // Upload logic
  }}
/>
```

### 4. Test Components Page (`pages/TestComponents.jsx`)

**Features:**
- ✅ Tabbed interface showcasing all components
- ✅ Interactive charts (bar, pie)
- ✅ Tabs and accordions
- ✅ All components in one place for easy testing

**Access:**
Navigate to `/test-components` in your application.

## 🧪 Testing Scenarios

### DataTable Testing
1. **Sorting:**
   - Click column headers to sort
   - Test ascending/descending toggle
   - Test multi-column sorting

2. **Filtering:**
   - Use text filters
   - Use select dropdowns
   - Combine multiple filters
   - Clear filters

3. **Pagination:**
   - Navigate pages
   - Change page size
   - Test edge cases (first/last page)

4. **Bulk Actions:**
   - Select individual rows
   - Select all rows
   - Perform bulk delete/edit
   - Export selected data

### Multi-Step Form Testing
1. **Navigation:**
   - Next/Previous buttons
   - Direct step selection
   - Step completion indicators

2. **Validation:**
   - Required field validation
   - Format validation (email, phone)
   - Cross-step validation

3. **Data Persistence:**
   - Data persists when navigating steps
   - Review step shows all data
   - Form submission

### File Upload Testing
1. **Drag & Drop:**
   - Drag files into drop zone
   - Visual feedback on drag
   - Multiple file drop

2. **File Selection:**
   - Click to select files
   - Multiple file selection
   - File type restrictions

3. **Validation:**
   - File size limits
   - File type restrictions
   - Error messages

4. **Upload:**
   - Progress tracking
   - Success/error states
   - Queue management

## 🚀 Future Components (Planned)

- [ ] Infinite Scroll Component
- [ ] Rich Text Editor
- [ ] Date/Time Pickers
- [ ] Image Gallery with Lightbox
- [ ] Dynamic Form Builder
- [ ] Advanced Search with Saved Searches
- [ ] Real-time Data Updates (WebSocket)
- [ ] Virtual Scrolling for Large Datasets
- [ ] Drag and Drop Reordering
- [ ] Advanced Charts (Line, Area, Scatter)

## 📝 Notes for TestNeo Automation

1. **Selectors:**
   - All components use semantic class names
   - Data attributes can be added for easier selection
   - Consistent naming conventions

2. **Interactions:**
   - All interactive elements have hover states
   - Loading states are clearly indicated
   - Error states are visually distinct

3. **Accessibility:**
   - Keyboard navigation support
   - ARIA labels where needed
   - Screen reader friendly

4. **Performance:**
   - Components handle large datasets
   - Virtual scrolling for performance
   - Optimized re-renders

## 🔗 Access

- **Test Components Page:** http://localhost:3001/test-components
- **Admin Panel:** http://localhost:3001/admin
- **Main App:** http://localhost:3001

## 📚 Component Documentation

Each component is fully documented with:
- PropTypes/TypeScript types
- Usage examples
- Props documentation
- Event handlers
- Styling customization

## 🎨 Styling

All components use Tailwind CSS for consistent styling:
- Primary color: `primary-600`
- Responsive design
- Dark mode ready (can be added)
- Customizable via className props

