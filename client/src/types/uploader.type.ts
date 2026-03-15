export interface FileItem {
  id: number;
  name: string;
  size: number;
  type: string;
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  downloadUrl?: string;
  errorMessage?: string;
}