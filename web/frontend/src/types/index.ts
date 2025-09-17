export interface SearchRequest {
  searchterm: string;
  mode: string;
  searchnumber: number;
  sortby: string;
  email?: string;
}

export interface SearchResponse {
  success: boolean;
  mode: string;
  result: string;
  parameters: SearchRequest;
}

export interface ErrorResponse {
  error: string;
  details?: string;
}

export const OUTPUT_OPTIONS = ["overview", "emails"];
export const SORT_OPTIONS = ["relevance", "pub_date", "Author", "JournalName"];