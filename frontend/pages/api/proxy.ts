import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Get the endpoint from the query parameters
  const endpoint = req.query.endpoint as string || '';

  // Construct the backend URL
  const backendUrl = `http://munazha-efficio-todo-hub.hf.space/api/${endpoint}`;

  try {
    // Determine the HTTP method from the incoming request
    const method = req.method || 'GET';

    // Prepare headers, including authorization if present
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (req.headers.authorization) {
      headers['Authorization'] = req.headers.authorization;
    }

    // Prepare the fetch options
    const fetchOptions: RequestInit = {
      method,
      headers,
    };

    // Add body for methods that can have a body
    if (method !== 'GET' && method !== 'HEAD' && req.body) {
      fetchOptions.body = JSON.stringify(req.body);
    }

    // Make the request to the backend
    const response = await fetch(backendUrl, fetchOptions);

    // Get the response data
    const responseData = await response.text();

    // Forward the response status and headers
    res.status(response.status);

    // Set the content type from the backend response if available
    const contentType = response.headers.get('content-type') || 'application/json';
    res.setHeader('content-type', contentType);

    // Send the response data
    res.send(responseData);

  } catch (error) {
    console.error('Proxy error:', error);
    res.status(500).json({ error: 'Proxy error', details: (error as Error).message });
  }
}

// Export config to handle all HTTP methods
export const config = {
  api: {
    bodyParser: {
      sizeLimit: '10mb',
    },
  },
};