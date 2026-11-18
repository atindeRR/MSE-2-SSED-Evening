# Run Steps (PowerShell) — har step ke baad screenshot lo 📸

> `rohansharma152` ki jagah apna Docker Hub username daalo (agar alag hai).

## 0. Setup
```powershell
cd "$HOME\Desktop\MSE-2-SSED-Evening"
@"
POSTGRES_DB=taskflow
POSTGRES_USER=taskflow_user
POSTGRES_PASSWORD=localpass123
JWT_SECRET=local_secret_123
DOCKERHUB_USERNAME=rohansharma152
"@ | Out-File -Encoding ascii .env
```
`.env` git mein commit NAHI hota (.gitignore mein hai) → password hardcode nahi hua.

## 1–2. Images build  📸 (Screenshot 1, 2)
```powershell
docker build -t rohansharma152/frontend:v1 ./frontend
docker build -t rohansharma152/backend:v1  ./backend
docker images | Select-String rohansharma152
```

## 3. Compose up  📸 (Screenshot 3)
```powershell
docker compose up -d --build
docker compose ps          # sab "healthy" dikhna chahiye
```
Browser: http://localhost:8080 (frontend) aur http://localhost:3000/health  📸 (Screenshot 9)

## 4. Network  📸 (Screenshot 4)
```powershell
docker network ls
docker network inspect mse-2-ssed-evening_taskflow-net
```

## 5. Health checks  📸 (Screenshot 5)
```powershell
docker inspect --format "{{.Name}} {{.State.Health.Status}}" taskflow-postgres taskflow-redis taskflow-backend
```

## Task 5 verification
```powershell
# Frontend -> backend (nginx proxy)
docker exec taskflow-frontend wget -qO- http://backend:3000/health
# Backend -> postgres / redis by service name
docker exec taskflow-backend nslookup postgres
docker exec taskflow-backend nslookup redis
docker exec taskflow-postgres pg_isready -U taskflow_user
docker exec taskflow-redis redis-cli ping
# Redis restart
docker compose restart redis
docker compose ps
```

## 6. Persistence  📸 (Screenshot 6)
```powershell
docker exec taskflow-postgres psql -U taskflow_user -d taskflow -c "INSERT INTO users(name,email,password_hash) VALUES('Rohan','rohan@test.com','x');"
docker compose rm -sf postgres          # container delete
docker compose up -d postgres           # naya container, same volume
Start-Sleep 8
docker exec taskflow-postgres psql -U taskflow_user -d taskflow -c "SELECT * FROM users;"   # Rohan abhi bhi hai ✅
docker volume ls
```

## 7. Docker Hub push  📸 (Screenshot 7 — hub.docker.com par tags)
```powershell
docker login
docker tag rohansharma152/frontend:v1 rohansharma152/frontend:latest
docker tag rohansharma152/backend:v1  rohansharma152/backend:latest
docker push rohansharma152/frontend:v1
docker push rohansharma152/frontend:latest
docker push rohansharma152/backend:v1
docker push rohansharma152/backend:latest
```

## 8. Image-based deploy  📸 (Screenshot 8)
```powershell
docker compose down
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
docker compose -f docker-compose.deploy.yml ps
curl.exe http://localhost:3000/health
```

## 10. GitHub Actions  📸 (Screenshot 10)
1. Fork repo → apne fork mein ye files push karo.
2. Settings → Secrets → Actions: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (hub.docker.com → Account Settings → Personal access tokens), `POSTGRES_PASSWORD`.
3. Push to main → Actions tab mein green ✅.
```powershell
git add .
git commit -m "Docker setup: Dockerfiles, compose, deploy, CD"
git push origin main
```
4. PR banao original repo par — title: `DOCKER-SET-2 | ROLL | Rohan Sharma | SECTION`

---
## Viva cheat-sheet
- **Multi-stage build**: Node stage React ko build karta hai, final image sirf Nginx + `dist/` → image ~50MB, source/node_modules nahi.
- **`npm install --omit=dev`**: sirf production deps. **`USER node`**: root se nahi chalta (security).
- **Layer caching**: pehle `package.json` copy → code change par npm install dobara nahi chalta.
- **Custom network**: containers ek-dusre ko service name se dhoondhte hain (Docker ka internal DNS) — `postgres`, `redis`, `backend`.
- **Ports**: sirf frontend (8080) aur backend (3000) host par; postgres/redis bahar expose nahi → secure.
- **Named volume** `postgres_data`: data container ke bahar rehta hai → container delete ho jaaye to bhi data safe. `down -v` se hi volume delete hota hai.
- **Healthcheck**: `pg_isready`, `redis-cli ping`, backend `/health`. **`depends_on: condition: service_healthy`** → backend tab start hoga jab DB ready ho.
- **init.sql** `/docker-entrypoint-initdb.d/` mein mount → pehli baar tables ban jaati hain.
- **deploy.yml**: `build:` nahi, `image: user/backend:latest` → deploy machine par source code ki zarurat nahi.
- **Secrets**: `${{ secrets.X }}` — token workflow file mein kabhi nahi likhte.
