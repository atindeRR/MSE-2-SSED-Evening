import pg from 'pg';
import { config } from './config.js';

const { Pool } = pg;
export const pool = new Pool({ connectionString: config.databaseUrl });
// Without this listener an idle client dropped by PostgreSQL (e.g. when the
// postgres container is restarted/recreated) emits an unhandled 'error' event
// and crashes the API. The pool discards the broken client and reconnects.
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
