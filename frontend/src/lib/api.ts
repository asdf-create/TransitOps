const API_BASE_URL = 'http://localhost:8000'

export async function fetchAPI(endpoint: string, options?: RequestInit) {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Unknown error')
      throw new Error(`API error ${response.status}: ${errorText}`)
    }

    return response.json()
  } catch (err) {
    if (err instanceof TypeError && err.message.includes('fetch')) {
      throw new Error('Network error: Cannot connect to backend. Is the server running?')
    }
    throw err
  }
}

export const api = {
  get: (endpoint: string) => fetchAPI(endpoint),
  post: (endpoint: string, data: unknown) =>
    fetchAPI(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  patch: (endpoint: string, data: unknown) =>
    fetchAPI(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
  delete: (endpoint: string) =>
    fetchAPI(endpoint, {
      method: 'DELETE',
    }),
}
