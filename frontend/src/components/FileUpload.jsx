import { useState, useRef } from 'react';
import { FiUpload, FiX, FiCheck, FiFile, FiImage } from 'react-icons/fi';

/**
 * Advanced File Upload Component for TestNeo Automation Testing
 * Features:
 * - Drag and drop
 * - Multiple file support
 * - Progress tracking
 * - File preview
 * - File validation
 * - Upload queue management
 */
const FileUpload = ({
  onUpload,
  accept = '*/*',
  multiple = false,
  maxSize = 10 * 1024 * 1024, // 10MB
  maxFiles = 5,
  showPreview = true,
  className = ''
}) => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (file) => {
    const errors = [];
    
    if (file.size > maxSize) {
      errors.push(`File size exceeds ${(maxSize / 1024 / 1024).toFixed(2)}MB`);
    }
    
    if (accept !== '*/*') {
      const acceptedTypes = accept.split(',').map(t => t.trim());
      const fileType = file.type || '';
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      const isAccepted = acceptedTypes.some(type => {
        if (type.startsWith('.')) {
          return type.toLowerCase() === fileExtension;
        }
        return fileType.match(type.replace('*', '.*'));
      });
      
      if (!isAccepted) {
        errors.push(`File type not accepted. Accepted: ${accept}`);
      }
    }
    
    return errors;
  };

  const handleFiles = (newFiles) => {
    const fileArray = Array.from(newFiles);
    const validFiles = [];
    const invalidFiles = [];

    fileArray.forEach(file => {
      const errors = validateFile(file);
      if (errors.length === 0) {
        validFiles.push({
          file,
          id: Date.now() + Math.random(),
          name: file.name,
          size: file.size,
          type: file.type,
          progress: 0,
          status: 'pending',
          preview: file.type.startsWith('image/') ? URL.createObjectURL(file) : null
        });
      } else {
        invalidFiles.push({ file, errors });
      }
    });

    if (invalidFiles.length > 0) {
      alert(`Some files were rejected:\n${invalidFiles.map(f => `${f.file.name}: ${f.errors.join(', ')}`).join('\n')}`);
    }

    if (validFiles.length > 0) {
      setFiles(prev => {
        const updated = multiple ? [...prev, ...validFiles] : [validFiles[0]];
        return updated.slice(0, maxFiles);
      });
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files);
    }
  };

  const removeFile = (fileId) => {
    setFiles(prev => {
      const updated = prev.filter(f => f.id !== fileId);
      updated.forEach(f => {
        if (f.preview) URL.revokeObjectURL(f.preview);
      });
      return updated;
    });
  };

  const uploadFiles = async () => {
    if (files.length === 0) return;

    setUploading(true);
    const uploadPromises = files.map(async (fileObj, index) => {
      try {
        // Simulate upload progress
        const progressInterval = setInterval(() => {
          setFiles(prev => prev.map(f => 
            f.id === fileObj.id 
              ? { ...f, progress: Math.min(f.progress + 10, 90) }
              : f
          ));
        }, 200);

        // Call actual upload function
        if (onUpload) {
          await onUpload(fileObj.file, (progress) => {
            setFiles(prev => prev.map(f => 
              f.id === fileObj.id ? { ...f, progress } : f
            ));
          });
        } else {
          // Simulate upload
          await new Promise(resolve => setTimeout(resolve, 2000));
        }

        clearInterval(progressInterval);
        
        setFiles(prev => prev.map(f => 
          f.id === fileObj.id 
            ? { ...f, progress: 100, status: 'completed' }
            : f
        ));
      } catch (error) {
        setFiles(prev => prev.map(f => 
          f.id === fileObj.id 
            ? { ...f, status: 'error', error: error.message }
            : f
        ));
      }
    });

    await Promise.all(uploadPromises);
    setUploading(false);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className={className}>
      {/* Drop Zone */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all ${
          dragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          multiple={multiple}
          onChange={handleFileInput}
          className="hidden"
        />
        <FiUpload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-lg font-semibold text-gray-700 mb-2">
          Drag and drop files here, or click to select
        </p>
        <p className="text-sm text-gray-500">
          {accept !== '*/*' && `Accepted: ${accept}`}
          {maxSize && ` • Max size: ${(maxSize / 1024 / 1024).toFixed(2)}MB`}
          {multiple && ` • Max files: ${maxFiles}`}
        </p>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map(fileObj => (
            <div
              key={fileObj.id}
              className="border rounded-lg p-4 flex items-center gap-4"
            >
              {/* Preview/Icon */}
              <div className="flex-shrink-0">
                {fileObj.preview ? (
                  <img
                    src={fileObj.preview}
                    alt={fileObj.name}
                    className="w-16 h-16 object-cover rounded"
                  />
                ) : (
                  <div className="w-16 h-16 bg-gray-100 rounded flex items-center justify-center">
                    {fileObj.type?.startsWith('image/') ? (
                      <FiImage className="w-8 h-8 text-gray-400" />
                    ) : (
                      <FiFile className="w-8 h-8 text-gray-400" />
                    )}
                  </div>
                )}
              </div>

              {/* File Info */}
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">{fileObj.name}</p>
                <p className="text-sm text-gray-500">{formatFileSize(fileObj.size)}</p>
                
                {/* Progress Bar */}
                {fileObj.status === 'uploading' && (
                  <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${fileObj.progress}%` }}
                    />
                  </div>
                )}
                
                {/* Status */}
                {fileObj.status === 'completed' && (
                  <p className="text-sm text-green-600 flex items-center gap-1 mt-1">
                    <FiCheck /> Uploaded
                  </p>
                )}
                {fileObj.status === 'error' && (
                  <p className="text-sm text-red-600 mt-1">{fileObj.error}</p>
                )}
              </div>

              {/* Remove Button */}
              <button
                onClick={() => removeFile(fileObj.id)}
                className="flex-shrink-0 p-2 text-red-600 hover:bg-red-50 rounded"
              >
                <FiX />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Upload Button */}
      {files.length > 0 && (
        <button
          onClick={uploadFiles}
          disabled={uploading || files.every(f => f.status === 'completed')}
          className="mt-4 w-full px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {uploading ? 'Uploading...' : 'Upload Files'}
        </button>
      )}
    </div>
  );
};

export default FileUpload;

