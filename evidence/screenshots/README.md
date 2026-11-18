# Visual Evidence Screenshots

All images in this folder are genuine captures made on 2026-11-18.

- Terminal images are full-screen captures of live PowerShell windows while the listed commands were executed against the local Docker environment.
- Web images are headless-Chromium screenshots of public GitHub and Docker Hub pages. No browser login or authentication was required.
- No placeholder, generated, or fabricated screenshots are included.

| File | Evidence | SHA-256 | Bytes | Captured (local) |
| --- | --- | --- | ---: | --- |
| `terminal/01_docker_images_tags.png` | Terminal: docker images filtered to gravity0309/frontend and gravity0309/backend, showing v1 and latest. | `8bb7edded173d4f768d77dbb12cd015994e6c8d10007494b7daa5309029d213b` | 38706 | 2026-11-18 15:23:49 |
| `terminal/02_compose_healthy_services.png` | Terminal: docker compose -f docker-compose.deploy.yml ps, all four services Up (healthy). | `e7f9b2c5bc69aee44d686d8ed085e8aff147b46bf87ac6a76c8bb8bfd02176c1` | 47772 | 2026-11-18 15:23:52 |
| `terminal/03_custom_docker_network.png` | Terminal: docker network ls/inspect for taskflow-net, bridge driver, four connected containers. | `7530b15a691e79a44650e4dde2ad8ecb650b0109b8631b6860f6c4f9c6837fd9` | 38193 | 2026-11-18 15:23:55 |
| `terminal/04_postgres_persistence_test.png` | Terminal: live marker insert, postgres container removal, recreation, and marker verification. | `d2a0b2102943660c441e8bd54d004d0b24249b478ce50c4f29c14f6a6413a309` | 86887 | 2026-11-18 15:24:06 |
| `terminal/05_redis_health_restart.png` | Terminal: Redis health/PONG before and after docker restart, plus backend /health. | `a4073fd1ee5e6f7475158f558d7e4df2d24967db5ccc590a4460f09c6fc66a9c` | 57467 | 2026-11-18 15:24:15 |
| `web/06_github_actions_success.png` | Browser: GitHub Actions run 44275529465 showing Status Success and both jobs. | `a873af06b4c8901a0c8c5140ebfe283e93a72911176567d745b92a543f1cd3c5` | 102701 | 2026-11-18 15:24:41 |
| `web/07_github_pr_20.png` | Browser: upstream Pull Request #20 with exact required title. | `19f8ee2786730d6c30b5a43e0121c447cddfba7940e6e78f616a647914dd4b0b` | 126785 | 2026-11-18 15:24:49 |
| `web/08_dockerhub_frontend_tags.png` | Browser: Docker Hub gravity0309/frontend Tags tab with latest and v1. | `912793ecd03953f857abd59061066475b4ac73b9ff46290f19ee6ade4bc5aa05` | 89831 | 2026-11-18 15:24:57 |
| `web/09_dockerhub_backend_tags.png` | Browser: Docker Hub gravity0309/backend Tags tab with latest and v1. | `6d76410c6d842300ae46c7bf8c9b8d3f8934b3c4d49705594112c171b9587447` | 89885 | 2026-11-18 15:25:05 |

These same images are embedded in `202401100400163_Sakshi_Kumari_SET2.pdf`.
