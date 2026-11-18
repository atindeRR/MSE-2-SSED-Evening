export const config = {
  port: Number(process.env.PORT || 3000),
  databaseUrl: process.env.DATABASE_URL,
  databaseHost: process.env.POSTGRES_HOST || 'localhost',
  databasePort: Number(process.env.POSTGRES_PORT || 5432),
  databaseName: process.env.POSTGRES_DB || 'taskflow',
  databaseUser: process.env.POSTGRES_USER || 'taskflow_user',
  databasePassword: process.env.POSTGRES_PASSWORD,
  redisUrl: process.env.REDIS_URL || 'redis://localhost:6379',
  jwtSecret: process.env.JWT_SECRET || 'development_only_change_me'
};
