import { useState } from 'react';
import { X, Download, AlertCircle, CheckCircle, Loader, Link as LinkIcon, Github, Palette } from 'lucide-react';
import newFile from '../../assets/newFile.svg';
import { useUpload } from '../../hooks/useUpload';
import { THEMES, type Theme } from '../../api/upload';

const THEME_LABELS: Record<Theme, string> = {
  hue: 'Hue-preserving',
  invert: 'Pure invert',
  dim: 'Dim (easy on eyes)',
  sepia: 'Sepia',
  midnight: 'Midnight blue',
};

// Representative swatches per theme — swatches[0] doubles as the accent color.
const THEME_PALETTES: Record<Theme, string[]> = {
  hue: ['#e43f5a', '#f6c90e', '#1eae98', '#1b1b2f'],
  invert: ['#9ca3af', '#ffffff', '#3a3a3a', '#000000'],
  dim: ['#7b8794', '#cbd2d9', '#3e4c59', '#1f2933'],
  sepia: ['#a98467', '#e6ccb2', '#5c4a32', '#2a2118'],
  midnight: ['#3a86ff', '#5bc0be', '#1c2541', '#0a1128'],
};

function formatFileSize(bytes: number) {
  if (bytes === 0) return '';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

export default function DropZone() {
  const { files, addFiles, addUrl, removeFile, downloadFile, theme, setTheme } = useUpload();
  const [dragActive, setDragActive] = useState(false);
  const [url, setUrl] = useState('');
  const [showPalettes, setShowPalettes] = useState(false);

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
    if (e.dataTransfer.files?.length) {
      addFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleClick = () => {
    document.getElementById('fileInput')?.click();
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      addFiles(Array.from(e.target.files));
      e.target.value = '';
    }
  };

  const handleUrlSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = url.trim();
    if (trimmed) {
      addUrl(trimmed);
      setUrl('');
    }
  };

  return (
    <div className="w-full min-h-screen bg-neon-dark-blue p-4 sm:p-6 flex items-center justify-center">
      <div className="w-full max-w-2xl">
        <h1 className="text-3xl sm:text-4xl font-bold mb-6 sm:mb-8 text-neon-red text-center">
          Docs To Dark <span className="text-neon-white">(D2D)</span>
        </h1>

        {/* Theme Selector — opens palette modal */}
        <div className="mb-5">
          <button
            type="button"
            onClick={() => setShowPalettes(true)}
            className="glass-dark w-full flex items-center gap-3 rounded-2xl px-4 py-3 text-left"
          >
            <Palette className="w-5 h-5 text-neon-white/70 shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-xs text-neon-white/50">Theme</p>
              <p className="text-sm font-semibold text-neon-white truncate">
                {THEME_LABELS[theme]}
              </p>
            </div>
            <div className="flex shrink-0">
              {THEME_PALETTES[theme].map((c, i) => (
                <span
                  key={i}
                  className="w-5 h-5 rounded-full border border-white/20"
                  style={{ backgroundColor: c, marginLeft: i === 0 ? 0 : -8 }}
                />
              ))}
            </div>
          </button>
        </div>

        {/* Drop Zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleClick}
          className={`relative border-2 border-dashed rounded-lg p-6 sm:p-12 text-center cursor-pointer transition-all ${
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
            accept=".pdf,.png,.jpg,.jpeg,.bmp,.webp,.tiff,.gif"
          />

          <img src={newFile} alt="New file" className="w-16 h-16 mx-auto mb-4" />
          <p className="text-lg sm:text-xl font-bold text-neon-dark-blue mb-2">
            Drag and drop files to convert to Dark Mode
          </p>
          <p className="text-xs sm:text-sm text-neon-dark-blue">
            Supports PDF, PNG, JPG, JPEG, BMP, WEBP, TIFF & GIF.
          </p>
        </div>

        {/* URL Upload */}
        <form onSubmit={handleUrlSubmit} className="mt-4 flex flex-col sm:flex-row gap-2">
          <div className="flex-1 flex items-center gap-2 glass rounded-lg px-3">
            <LinkIcon className="w-4 h-4 text-neon-red shrink-0" />
            <input
              type="url"
              value={url}
              onChange={e => setUrl(e.target.value)}
              placeholder="...or paste a PDF / image URL"
              className="flex-1 bg-transparent py-3 text-neon-white placeholder-gray-500 outline-none"
            />
          </div>
          <button
            type="submit"
            className="glass-dark px-5 text-neon-white font-semibold rounded-lg"
          >
            Convert
          </button>
        </form>

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-10">
            <h2 className="text-lg font-semibold text-neon-red mb-4">Files ({files.length})</h2>
            <div className="space-y-3">
              {files.map(file => (
                <div
                  key={file.id}
                  className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 glass rounded-lg p-4 sm:p-5 transition-all hover:shadow-lg"
                >
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-neon-white truncate">{file.name}</p>
                    {file.size > 0 && (
                      <p className="text-sm text-gray-400">{formatFileSize(file.size)}</p>
                    )}
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    {file.status === 'pending' && <div className="text-gray-400 text-sm">Queued</div>}
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
                          className="glass-dark px-3 py-1.5 text-neon-white font-semibold rounded-lg flex items-center gap-1.5"
                        >
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </div>
                    )}
                    {file.status === 'error' && (
                      <div className="flex items-center gap-2 min-w-0">
                        <AlertCircle className="w-5 h-5 text-red-500 shrink-0" />
                        <span className="text-sm text-red-500 break-words">{file.errorMessage}</span>
                      </div>
                    )}

                    {file.status === 'pending' || file.status === 'uploading' ? (
                      <div className="mac-icon-btn cursor-not-allowed opacity-40">
                        <X className="w-4 h-4" />
                      </div>
                    ) : (
                      <button
                        onClick={() => removeFile(file.id)}
                        className="mac-icon-btn"
                        aria-label="Remove file"
                      >
                        <X className="w-4 h-4" />
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
            <p className="text-sm">No files yet. Drag &amp; Drop files or click above to start!</p>
          </div>
        )}
        <a
          href="https://github.com/ParsaBordbar/d2d-docsToDark"
          target="_blank"
          rel="noreferrer"
          className="mt-8 flex items-center justify-center gap-2 text-neon-red hover:text-neon-red/80 transition-colors"
        >
          <Github className="w-4 h-4" />
          Github Repository
        </a>
      </div>

      {/* Palette Preview Modal */}
      {showPalettes && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
          onClick={() => setShowPalettes(false)}
        >
          <div
            onClick={e => e.stopPropagation()}
            className="glass w-full max-w-lg rounded-3xl p-6 sm:p-7 max-h-[85vh] overflow-y-auto"
          >
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="text-xl font-semibold text-neon-white">Choose a theme</h3>
                <p className="text-xs text-neon-white/50 mt-0.5">Tap a palette to apply it.</p>
              </div>
              <button onClick={() => setShowPalettes(false)} className="mac-icon-btn" aria-label="Close">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3">
              {THEMES.map(t => {
                const active = theme === t;
                return (
                  <button
                    key={t}
                    type="button"
                    onClick={() => {
                      setTheme(t);
                      setShowPalettes(false);
                    }}
                    className={`w-full flex items-center gap-4 rounded-2xl p-4 text-left transition-all ${
                      active ? 'glass ring-2 ring-neon-blue scale-[1.01]' : 'glass-dark'
                    }`}
                  >
                    <div className="flex shrink-0">
                      {THEME_PALETTES[t].map((c, i) => (
                        <span
                          key={i}
                          className="w-8 h-8 rounded-full border-2 border-white/20"
                          style={{ backgroundColor: c, marginLeft: i === 0 ? 0 : -10 }}
                        />
                      ))}
                    </div>
                    <span className="flex-1 text-base font-medium text-neon-white">
                      {THEME_LABELS[t]}
                    </span>
                    {active && <CheckCircle className="w-5 h-5 text-neon-blue shrink-0" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
