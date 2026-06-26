import { useCallback, useState } from 'react';
import type { FileItem } from '../types/uploader.type';
import { toDownloadUrl, uploadFile, uploadFromUrl, DEFAULT_THEME } from '../api/upload';
import type { Theme } from '../api/upload';

export function useUpload() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [theme, setTheme] = useState<Theme>(DEFAULT_THEME);

  const patch = useCallback((id: number, changes: Partial<FileItem>) => {
    setFiles(prev => prev.map(f => (f.id === id ? { ...f, ...changes } : f)));
  }, []);

  const runUpload = useCallback(
    async (item: FileItem, send: () => Promise<{ download_url?: string; error?: string }>) => {
      patch(item.id, { status: 'uploading' });
      try {
        const data = await send();
        if (data.error || !data.download_url) {
          patch(item.id, { status: 'error', errorMessage: data.error || 'Conversion failed' });
        } else {
          patch(item.id, { status: 'success', downloadUrl: data.download_url });
        }
      } catch (error) {
        patch(item.id, {
          status: 'error',
          errorMessage: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    },
    [patch],
  );

  const addFiles = useCallback(
    (selected: File[]) => {
      const items: FileItem[] = selected.map(file => ({
        id: Math.random(),
        name: file.name,
        size: file.size,
        type: file.type,
        file,
        status: 'pending',
      }));
      setFiles(prev => [...prev, ...items]);
      items.forEach(item => runUpload(item, () => uploadFile(item.file!, theme)));
    },
    [runUpload, theme],
  );

  const addUrl = useCallback(
    (url: string) => {
      const name = url.split('/').pop() || url;
      const item: FileItem = {
        id: Math.random(),
        name,
        size: 0,
        type: 'url',
        status: 'pending',
      };
      setFiles(prev => [...prev, item]);
      runUpload(item, () => uploadFromUrl(url, theme));
    },
    [runUpload, theme],
  );

  const removeFile = useCallback((id: number) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  }, []);

  const downloadFile = useCallback((path: string, fileName: string) => {
    const a = document.createElement('a');
    a.href = toDownloadUrl(path);
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }, []);

  return { files, addFiles, addUrl, removeFile, downloadFile, theme, setTheme };
}

export default useUpload;
