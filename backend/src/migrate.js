import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { pool } from './db.js';

const schemaPath = join(dirname(fileURLToPath(import.meta.url)), '..', 'db', 'init.sql');

// The schema is idempotent (CREATE TABLE IF NOT EXISTS). Running it at startup means
// an image-based deployment needs no SQL file mounted from the host/source tree.
export async function migrate() {
  const schema = await readFile(schemaPath, 'utf8');
  await pool.query(schema);
  console.log('PostgreSQL schema verified');
}
