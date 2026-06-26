import { API_BASE_URL } from './base';

export interface UploadResult {
  download_url?: string;
  error?: string;
}

export interface BatchResult {
  filename: string;
  download_url?: string;
  error?: string;
}

// Keep in sync with the server's THEMES registry (GET /themes).
export const THEMES = ['hue', 'invert', 'dim', 'sepia', 'midnight'] as const;
export type Theme = (typeof THEMES)[number];
export const DEFAULT_THEME: Theme = 'hue';

export async function uploadFile(file: File, theme: Theme = DEFAULT_THEME): Promise<UploadResult> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('theme', theme);
  const response = await fetch(`${API_BASE_URL}/upload/`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || 'Failed to upload file');
  }
  return response.json();
}

export async function uploadBatch(files: File[], theme: Theme = DEFAULT_THEME): Promise<BatchResult[]> {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  formData.append('theme', theme);
  const response = await fetch(`${API_BASE_URL}/batch/`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    throw new Error('Failed to upload batch');
  }
  const data = await response.json();
  return data.results;
}

export async function uploadFromUrl(url: string, theme: Theme = DEFAULT_THEME): Promise<UploadResult> {
  const query = `file=${encodeURIComponent(url)}&theme=${encodeURIComponent(theme)}`;
  const response = await fetch(`${API_BASE_URL}/upload-url/?${query}`, {
    method: 'POST',
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || 'Failed to convert from URL');
  }
  return response.json();
}

export function toDownloadUrl(path: string): string {
  return `${API_BASE_URL}${path}`;
}
