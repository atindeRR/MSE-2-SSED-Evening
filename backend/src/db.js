import pg from 'pg';
import { readFile } from 'node:fs/promises';
import { config } from './config.js';

const { Pool } = pg;
export const pool = config.databaseUrl
  ? new Pool({ connectionString: config.databaseUrl })
  : new Pool({
      host: process.env.PGHOST || 'localhost',
      port: Number(process.env.PGPORT || 5432),
      database: process.env.PGDATABASE,
      user: process.env.PGUSER,
      password: process.env.PGPASSWORD
    });

pool.on('error', error => console.error('PostgreSQL pool error:', error.message));

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
  await pool.query(schema);
  console.log('Database schema is ready');
}
