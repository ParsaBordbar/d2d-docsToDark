import { useState } from 'react';
import { X, Download, AlertCircle, CheckCircle, Loader } from 'lucide-react';
import newFile from '../../assets/newFile.svg'

interface FileItem {
  id: number;
  name: string;
  size: number;
  type: string;
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  downloadUrl?: string;
  errorMessage?: string;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:1313';

export default function DropZone() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const uploadFile = async (fileItem: FileItem) => {
    try {
      setFiles(prev => prev.map(f => f.id === fileItem.id ? { ...f, status: 'uploading' } : f));

      const formData = new FormData();
      formData.append('file', fileItem.file);

      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();

      if (data.error) {
        setFiles(prev => prev.map(f => f.id === fileItem.id ? { 
          ...f, 
          status: 'error', 
          errorMessage: data.error 
        } : f));
      } else {
        setFiles(prev => prev.map(f => f.id === fileItem.id ? { 
          ...f, 
          status: 'success', 
          downloadUrl: data.download_url 
        } : f));
      }
    } catch (error) {
      setFiles(prev => prev.map(f => f.id === fileItem.id ? { 
        ...f, 
        status: 'error', 
        errorMessage: error instanceof Error ? error.message : 'Unknown error' 
      } : f));
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      const newFileItems = Array.from(droppedFiles).map((file: File) => {
        const fileItem: FileItem = {
          id: Math.random(),
          name: file.name,
          size: file.size,
          type: file.type,
          file: file,
          status: 'pending'
        };
        // Auto-upload after adding
        setTimeout(() => uploadFile(fileItem), 100);
        return fileItem;
      });
      setFiles(prev => [...prev, ...newFileItems]);
    }
  };

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const input = document.getElementById('fileInput');
    input?.click();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const newFileItems = Array.from(selectedFiles).map((file: File) => {
        const fileItem: FileItem = {
          id: Math.random(),
          name: file.name,
          size: file.size,
          type: file.type,
          file: file,
          status: 'pending'
        };
        // Auto-upload after adding
        setTimeout(() => uploadFile(fileItem), 100);
        return fileItem;
      });
      setFiles(prev => [...prev, ...newFileItems]);
    }
  };

  const removeFile = (id: number) => {
    setFiles(prev => prev.filter(file => file.id !== id));
  };

  const downloadFile = (downloadUrl: string, fileName: string) => {
    const fullUrl = `${API_BASE_URL}${downloadUrl}`;
    const a = document.createElement('a');
    a.href = fullUrl;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="w-full min-h-screen bg-neon-dark-blue p-6 flex items-center justify-center">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-bold mb-8 text-neon-red text-center">Docs To Dark</h1>

        {/* Drop Zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleClick}
          className={`relative border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all ${
            dragActive
              ? 'border-neon-blue bg-neon-deep-blue scale-105'
              : 'border-neon-red bg-neon-red hover:border-neon-blue hover:shadow-lg'
          }`}
        >
          <input
            id="fileInput"
            type="file"
            multiple
            onChange={handleChange}
            className="hidden"
            accept=".pdf,.png,.jpg,.jpeg,.bmp"
          />
          
          <img src={newFile} alt="New file" className="w-16 h-16 mx-auto mb-4" />
          <p className="text-xl font-bold text-neon-dark-blue mb-2">
            Drag and drop files to convert to Dark Mode
          </p>
          <p className="text-sm text-neon-dark-blue">
            Supports PDF, PNG, JPG & JPEG.
          </p>
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-10">
            <h2 className="text-lg font-semibold text-neon-red mb-4">
              Files ({files.length})
            </h2>
            <div className="space-y-3">
              {files.map(file => (
                <div
                  key={file.id}
                  className="flex items-center justify-between bg-neon-black border border-neon-red rounded-lg p-5 transition-all hover:shadow-lg"
                >
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-neon-white truncate">
                      {file.name}
                    </p>
                    <p className="text-sm text-gray-400">
                      {formatFileSize(file.size)}
                    </p>
                  </div>

                  <div className="ml-4 flex items-center gap-3">
                    {file.status === 'pending' && (
                      <div className="text-gray-400 text-sm">Queued</div>
                    )}
                    {file.status === 'uploading' && (
                      <div className="flex items-center gap-2 text-neon-blue">
                        <Loader className="w-4 h-4 animate-spin" />
                        <span className="text-sm">Processing...</span>
                      </div>
                    )}
                    {file.status === 'success' && (
                      <div className="flex items-center gap-2">
                        <CheckCircle className="w-5 h-5 text-green-400" />
                        <button
                          onClick={() => downloadFile(file.downloadUrl!, file.name)}
                          className="px-3 py-1 bg-neon-blue text-neon-dark-blue font-semibold rounded hover:bg-neon-blue/80 transition-colors flex items-center gap-1"
                        >
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </div>
                    )}
                    {file.status === 'error' && (
                      <div className="flex items-center gap-2">
                        <AlertCircle className="w-5 h-5 text-red-500" />
                        <span className="text-sm text-red-500">{file.errorMessage}</span>
                      </div>
                    )}

                    {(file.status === 'pending' || file.status === 'uploading') ? (
                      <div className="w-8 h-8 flex items-center justify-center cursor-not-allowed opacity-50">
                        <X className="w-5 h-5 text-gray-500" />
                      </div>
                    ) : (
                      <button
                        onClick={() => removeFile(file.id)}
                        className="p-2 text-neon-red hover:bg-neon-red/20 rounded transition-colors"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Empty State Message */}
        {files.length === 0 && (
          <div className="mt-12 text-center text-gray-400">
            <p className="text-sm">No files yet. Drop a file or click above to start!</p>
          </div>
        )}
      </div>
    </div>
  );
}