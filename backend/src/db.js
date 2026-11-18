import pg from 'pg';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { config } from './config.js';

const { Pool } = pg;
export const pool = new Pool({ connectionString: config.databaseUrl });

// Keep the process alive if a connection breaks (e.g. while the database
// container is recreated during the persistence test); /health reports 503
// until PostgreSQL is reachable again.
pool.on('error', error => console.error('PostgreSQL pool error:', error.message));

// The schema is bundled into the image so a deployment started with an empty
// PostgreSQL volume is usable without mounting any application source files.
const schemaFile = fileURLToPath(new URL('../db/init.sql', import.meta.url));

export async function ensureSchema() {
  const schema = await readFile(schemaFile, 'utf8');
  await pool.query(schema);
  console.log('Database schema verified');
}

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
