import { useState } from 'react';
import { X } from 'lucide-react';
import newFile from '../../assets/newFile.svg'

interface FileItem {
  id: number;
  name: string;
  size: number;
  type: string;
}

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

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles.length > 0) {
      const newFiles = Array.from(droppedFiles).map((file: File) => ({
        id: Math.random(),
        name: file.name,
        size: file.size,
        type: file.type
      }));
      setFiles(prev => [...prev, ...newFiles]);
    }
  };

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const input = document.getElementById('fileInput');
    input?.click();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const newFiles = Array.from(selectedFiles).map((file: File) => ({
        id: Math.random(),
        name: file.name,
        size: file.size,
        type: file.type
      }));
      setFiles(prev => [...prev, ...newFiles]);
    }
  };

  const removeFile = (id: number) => {
    setFiles(prev => prev.filter(file => file.id !== id));
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 bg-neon-red rounded-xl">
      <h1 className="text-3xl font-bold mb-6 text-neon-dark-blue">Docs To Dark</h1>

      {/* Drop Zone */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
        className={`relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors  hover:text-neon-deep-blue ${
          dragActive
            ? 'border-neon-blue bg-neon-deep-blue'
            : 'border-neon-dark-blue bg-neon-red hover:border-neon-deep-blue'
        }`}
      >
        <input
          id="fileInput"
          type="file"
          multiple
          onChange={handleChange}
          className="hidden"
        />
        
        <img src={newFile} alt="New file" className="w-12 h-12 mx-auto mb-3" />
        <p className="text-lg font-semibold text-neon-dark-blue mb-1">
          Drag and drop files to convert to Dark Mode
        </p>
        <p className="text-sm text-neon-dark-blue">
          or click to select files
        </p>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="mt-8">
          <h2 className="text-lg font-semibold text-neon-dark-blue mb-4">
            Uploaded Files ({files.length})
          </h2>
          <div className="space-y-2">
            {files.map(file => (
              <div
                key={file.id}
                className="flex items-center justify-between bg-white border border-neon-black rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-neon-dark-blue truncate">
                    {file.name}
                  </p>
                  <p className="text-sm text-neon-dark-blue">
                    {formatFileSize(file.size)}
                  </p>
                </div>
                <button
                  onClick={() => removeFile(file.id)}
                  className="ml-4 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}