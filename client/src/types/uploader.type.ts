export type UploadStatus = 'pending' | 'uploading' | 'success' | 'error';

export interface FileItem {
  id: number;
  name: string;
  size: number;
  type: string;
  file?: File;
  status: UploadStatus;
  downloadUrl?: string;
  errorMessage?: string;
}
