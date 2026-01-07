# API Contracts: Frontend UI Reimplementation

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Create a new user account
**Request**:
- Content-Type: application/json
- Body:
  ```json
  {
    "email": "string (valid email format)",
    "password": "string (min 8 characters)",
    "name": "string (1-100 characters)"
  }
  ```

**Response**:
- 201 Created
- Body:
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string"
    },
    "token": "string (JWT token)"
  }
  ```

### POST /api/auth/signin
**Description**: Authenticate an existing user
**Request**:
- Content-Type: application/json
- Body:
  ```json
  {
    "email": "string (valid email)",
    "password": "string"
  }
  ```

**Response**:
- 200 OK
- Body:
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string"
    },
    "token": "string (JWT token)"
  }
  ```

### GET /api/auth/me
**Description**: Get current authenticated user info
**Request**:
- Headers:
  - Authorization: Bearer {token}

**Response**:
- 200 OK
- Body:
  ```json
  {
    "id": "string",
    "email": "string",
    "name": "string"
  }
  ```

## Todo Endpoints

### GET /api/todos
**Description**: Get all todos for the authenticated user
**Request**:
- Headers:
  - Authorization: Bearer {token}

**Response**:
- 200 OK
- Body:
  ```json
  {
    "todos": [
      {
        "id": "string",
        "title": "string",
        "description": "string (optional)",
        "completed": "boolean",
        "userId": "string",
        "createdAt": "string (ISO date)",
        "updatedAt": "string (ISO date)"
      }
    ]
  }
  ```

### POST /api/todos
**Description**: Create a new todo for the authenticated user
**Request**:
- Headers:
  - Authorization: Bearer {token}
- Content-Type: application/json
- Body:
  ```json
  {
    "title": "string (1-255 characters)",
    "description": "string (optional)",
    "completed": "boolean (default: false)"
  }
  ```

**Response**:
- 201 Created
- Body:
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string (optional)",
    "completed": "boolean",
    "userId": "string",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
  ```

### PUT /api/todos/{id}
**Description**: Update an existing todo
**Request**:
- Headers:
  - Authorization: Bearer {token}
- Content-Type: application/json
- Body:
  ```json
  {
    "title": "string (1-255 characters) (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```

**Response**:
- 200 OK
- Body:
  ```json
  {
    "id": "string",
    "title": "string",
    "description": "string (optional)",
    "completed": "boolean",
    "userId": "string",
    "createdAt": "string (ISO date)",
    "updatedAt": "string (ISO date)"
  }
  ```

### DELETE /api/todos/{id}
**Description**: Delete an existing todo
**Request**:
- Headers:
  - Authorization: Bearer {token}

**Response**:
- 204 No Content