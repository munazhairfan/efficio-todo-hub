import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Get the endpoint from the query parameters
  const endpoint = req.query.endpoint as string || '';

  // Construct the backend URL - Use environment variable for flexibility
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

  // The backend has /api as a prefix for all routes (configured in main.py),
  // so we need to ensure the endpoint includes the /api prefix when forwarding
  let normalizedEndpoint = endpoint;
  if (!normalizedEndpoint.startsWith('/api/')) {
    if (normalizedEndpoint.startsWith('/')) {
      normalizedEndpoint = `/api${normalizedEndpoint}`;
    } else {
      normalizedEndpoint = `/api/${normalizedEndpoint}`;
    }
  }

  const fullBackendUrl = `${backendUrl}${normalizedEndpoint}`;

  try {
    // Determine the HTTP method from the incoming request
    const method = req.method || 'GET';

    // Prepare headers, including authorization if present
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Forward all headers except host-related headers
    Object.keys(req.headers).forEach(key => {
      if (!key.toLowerCase().startsWith('x-forwarded-') &&
          key.toLowerCase() !== 'host' &&
          key.toLowerCase() !== 'connection' &&
          key.toLowerCase() !== 'content-length') {
        const value = req.headers[key];
        if (value && typeof value === 'string') {
          headers[key] = value;
        }
      }
    });

    // Prepare the fetch options
    const fetchOptions: RequestInit = {
      method,
      headers,
    };

    // Add body for methods that can have a body
    if (method !== 'GET' && method !== 'HEAD' && method !== 'DELETE' && req.body) {
      fetchOptions.body = JSON.stringify(req.body);
    }

    console.log(`Proxying ${method} request to:`, fullBackendUrl);

    // Make the request to the backend
    const response = await fetch(fullBackendUrl, fetchOptions);

    // Get the response data
    const responseData = await response.text();

    // Forward the response status and headers
    res.status(response.status);

    // Set the content type from the backend response if available
    const contentType = response.headers.get('content-type') || 'application/json';
    res.setHeader('content-type', contentType);

    // Forward other important headers
    response.headers.forEach((value, key) => {
      if (!key.toLowerCase().startsWith('access-control-') &&
          !key.toLowerCase().match(/^(set-cookie|authorization)$/)) {
        res.setHeader(key, value);
      }
    });

    // Send the response data
    res.send(responseData);

  } catch (error: any) {
    console.error('Proxy error:', error);
    // Log more detailed error information
    if (error.cause) {
      console.error('Error cause:', error.cause);
    }
    res.status(500).json({
      error: 'Proxy error',
      details: error.message || error.toString(),
      ...(error.stack && { stack: error.stack })
    });
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