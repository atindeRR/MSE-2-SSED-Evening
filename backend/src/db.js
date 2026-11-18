import pg from 'pg';
import { readFile } from 'node:fs/promises';
import { config } from './config.js';

const { Pool } = pg;
const poolConfig = config.databaseUrl
  ? { connectionString: config.databaseUrl }
  : {
      host: config.databaseHost,
      port: config.databasePort,
      database: config.databaseName,
      user: config.databaseUser,
      password: config.databasePassword
    };
export const pool = new Pool(poolConfig);

pool.on('error', error => console.error('PostgreSQL idle client error:', error.message));

export async function waitForDatabase() {
  for (let attempt = 1; attempt <= 30; attempt++) {
    try {
      await pool.query('SELECT 1');
      const schema = await readFile(new URL('../db/init.sql', import.meta.url), 'utf8');
      await pool.query(schema);
      console.log('PostgreSQL connection established and schema is ready');
      return;
    } catch (error) {
      console.log(`Waiting for PostgreSQL (${attempt}/30): ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }
  throw new Error('Could not connect to PostgreSQL after 30 attempts');
}
