export const config = {
  port: Number(process.env.PORT || 3000),
  databaseUrl: process.env.DATABASE_URL,
  databaseHost: process.env.PGHOST || 'localhost',
  databasePort: Number(process.env.PGPORT || 5432),
  databaseName: process.env.PGDATABASE,
  databaseUser: process.env.PGUSER,
  databasePassword: process.env.PGPASSWORD,
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  jwtSecret: process.env.JWT_SECRET || 'development_only_change_me'
};
