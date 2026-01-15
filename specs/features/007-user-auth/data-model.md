# Data Model: User Authentication

## Key Entities

### User
- **Fields**:
  - id: string (unique identifier)
  - email: string (unique, required, valid email format)
  - password_hash: string (hashed password, required)
  - created_at: datetime (timestamp of account creation)
  - updated_at: datetime (timestamp of last update)
  - is_active: boolean (account status, default: true)

- **Validation Rules**:
  - Email must be unique and follow valid email format
  - Password must meet minimum security requirements (handled by Better Auth)
  - User ID must be unique across system

- **State Transitions**:
  - Inactive → Active (on account verification/creation)
  - Active → Inactive (on account deactivation)

### JWT Token
- **Claims**:
  - sub: string (subject - user identifier)
  - exp: number (expiration timestamp)
  - iat: number (issued at timestamp)
  - jti: string (JWT ID for potential revocation, optional)

- **Validation Rules**:
  - Must be signed with shared secret
  - Must not be expired at time of verification
  - Signature must be valid

### Authentication Context
- **Fields**:
  - user_id: string (extracted from JWT token)
  - is_authenticated: boolean (whether token is valid)
  - token_expiry: datetime (when token expires)

## Relationships
- User → JWT Token (one-to-many, via user_id claim)
- JWT Token → Authentication Context (one-to-one, during request processing)

## API Endpoints

### Authentication Endpoints
1. `POST /api/auth/signup`
   - Input: { email: string, password: string }
   - Output: { token: string, user: { id, email } }
   - Error: 400 for validation errors, 409 for duplicate email

2. `POST /api/auth/signin`
   - Input: { email: string, password: string }
   - Output: { token: string, user: { id, email } }
   - Error: 400 for validation errors, 401 for invalid credentials

3. `POST /api/auth/verify`
   - Input: Authorization: Bearer {token}
   - Output: { user: { id, email }, is_valid: boolean }
   - Error: 401 for invalid/missing token

### Protected Endpoints
- All endpoints under `/api/*` except auth endpoints
- Require valid JWT token in Authorization header
- Return 401 for invalid/missing tokens