import pg from 'pg';
import { config } from './config.js';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const { Pool } = pg;
// DATABASE_URL is supported for local development; Compose deployments use
// PostgreSQL's standard PG* variables so passwords need no URI escaping.
export const pool = new Pool(config.databaseUrl
  ? { connectionString: config.databaseUrl }
  : undefined);

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

export async function initializeSchema() {
  const sqlPath = resolve(dirname(fileURLToPath(import.meta.url)), '../db/init.sql');
  await pool.query(await readFile(sqlPath, 'utf8'));
  console.log('PostgreSQL schema is ready');
}
