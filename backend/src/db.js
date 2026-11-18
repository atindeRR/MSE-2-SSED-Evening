import { readFile } from 'node:fs/promises';
import pg from 'pg';
import { config } from './config.js';

const { Pool } = pg;
export const pool = new Pool({
  connectionString: config.databaseUrl,
  connectionTimeoutMillis: 5000
});

pool.on('error', error => console.error('PostgreSQL idle connection error:', error.message));

export async function waitForDatabase() {
  for (let attempt = 1; attempt <= 30; attempt++) {
    try {
      await pool.query('SELECT 1');
      console.log('PostgreSQL connection established');
      return;
    } catch (error) {
      console.log(`Waiting for PostgreSQL (${attempt}/30): ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  throw new Error('Could not connect to PostgreSQL after 30 attempts');
}

export async function initializeDatabase() {
  const schema = await readFile(new URL('../db/init.sql', import.meta.url), 'utf8');
  const client = await pool.connect();

  try {
    await client.query('BEGIN');
    // Serialize schema changes when more than one backend starts together.
    await client.query("SELECT pg_advisory_xact_lock(hashtext('taskflow_schema'))");
    await client.query(schema);
    await client.query('COMMIT');
    client.release();
  } catch (error) {
    // Discarding the connection rolls back any open transaction.
    client.release(error);
    throw error;
  }
}
