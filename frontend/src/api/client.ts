export interface ApiClient {
  get: <T>(path: string, init?: RequestInit) => Promise<T>;
  post: <T>(path: string, body?: unknown, init?: RequestInit) => Promise<T>;
}

export const createApiClient = (
  getAccessToken: () => Promise<string | undefined>,
  baseUrl: string = import.meta.env.VITE_API_BASE_URL ?? ''
): ApiClient => {
  const request = async <T>(path: string, init: RequestInit = {}) => {
    const token = await getAccessToken();
    const response = await fetch(`${baseUrl}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...init.headers,
      },
    });

    if (!response.ok) {
      const message = await response.text();
      throw new Error(message || `Request failed: ${response.status}`);
    }

    return response.json() as Promise<T>;
  };

  return {
    get: (path, init) => request(path, { ...init, method: 'GET' }),
    post: (path, body, init) =>
      request(path, {
        ...init,
        method: 'POST',
        body: body ? JSON.stringify(body) : undefined,
      }),
  };
};
