import { SearchRequest, SearchResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || '';

export class PubMedAPIService {
  static async search(searchData: SearchRequest): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE_URL}/api/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(searchData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'An error occurred during search');
    }

    return data;
  }

  static async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    
    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return await response.json();
  }
}