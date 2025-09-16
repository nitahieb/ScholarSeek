import type { SearchRequest, SearchResponse } from '../types';
import api from '../api';
const API_BASE_URL = import.meta.env.VITE_API_URL;

export class PubMedAPIService {
  static async search(searchData: SearchRequest): Promise<SearchResponse> {
    const response = await api.post(`/api/pubmed-search/`, searchData);

    const data = response.data;

    if (response.status !== 200) {
      throw new Error(data.error || 'An error occurred during search');
    }

    return data;
  }

  static async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await api.get('/api/health');
    if (response.status !== 200) {
      throw new Error('Health check failed');
    }
    return response.data;
  }
}