import { Pool } from 'pg';

// Create a connection pool to Neon PostgreSQL database
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false // For Neon
  }
});

export { pool };