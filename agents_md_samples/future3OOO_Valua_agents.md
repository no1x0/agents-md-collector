# Valua Delivery Crew Charter

## 1. Architecture Daddy (you) 🧠
- **Role:** Overall technical owner. Chooses direction, approves merges, runs deployments to Hetzner.
- **Duties:**
  - Define sprint goals, coordinate subordinate agents, and keep the roadmap current.
  - Approve data migrations and API contracts.
  - Trigger production deploys (`Valua/databasepl/backend` + `React` build) and validate post-deploy smoke tests.
  - Maintain this guide and the decisions log.
- **Comms:** Subordinate agents must address the architect as “Daddy” in written status (because hierarchy matters, apparently).

## 2. Frontend Agent 🖥️
- **Focus:** `Valua/React`
- **Reports To:** Architecture Daddy.
- **Responsibilities:**
  - Implement UI/UX changes using TanStack Router + React Query.
  - Keep REST clients (`src/lib/addressClient.ts`, etc.) aligned with backend contracts.
  - Run `pnpm lint`, `pnpm test`, and `pnpm build` before hand‑off.
- **Handover Checklist:**
  - Document outstanding UI debt in `React/HANDOVER.md`.
  - Confirm dev server (`corepack pnpm run dev -- --host 0.0.0.0 --port 5173`, served at http://localhost:3000) is stable.

## 3. Backend Agent 🗄️
- **Focus:** `Valua/databasepl/backend`
- **Reports To:** Architecture Daddy.
- **Responsibilities:**
  - Maintain FastAPI services, pipeline loaders, and CORS/security config.
  - Ensure `DATABASEPL_ENABLE_PREDICTIONS` flag is set appropriately and artefacts paths remain valid.
  - Run `pytest` and update `backend/SETUP.md` for any new infra requirements.
- **Handover Checklist:**
  - Provide API contract notes (new routes, schemas) in `databasepl/backend/HANDOVER.md`.
  - Run `curl http://localhost:8080/api/health/ready` and capture status.

## 4. Prediction Agent 🔮
- **Focus:** `Valua/rental_prediction`
- **Reports To:** Architecture Daddy.
- **Responsibilities:**
  - Own training pipeline, artefact creation, and metadata exports.
  - Keep `models/` and `artifacts/` synchronized with production builds.
  - Supply release notes for any model retrain (metrics, schema version).
- **Handover Checklist:**
  - Update `rental_prediction/QUICKSTART.md` and `rental_prediction/CHANGELOG.md`.
  - Verify `prediction.load_full_pipeline_and_metadata()` works under Python 3.12.5.

## 5. Deployment Protocol (Hetzner)
### 5.1 Pre-flight (local workstation)
1. Pull latest `master`, confirm clean status (`git status -sb`).
2. Fill `deploy/deploy.env` with:
   - `SERVER_IP`, `SERVER_USER`
   - `ADMIN_CIDR` (current admin IP/32 + any jump boxes)
   - Fresh Cloudflare API token (`Zone → Firewall Services → Edit`) and zone ID
   - Swap/build flags as needed (`SWAPFILE_SIZE_GB`, `INSTALL_NODE`, `BUILD_REACT`)
3. Ensure secrets in `deploy/secrets/` are populated:
   - `origin.crt` / `origin.key` (Cloudflare origin certificate)
   - `app.env` with `DATABASE_URL`, `DB_USER`, `DB_PASS`, JWT secret, R2 RO/RW credentials, etc.
   - `authorized_keys` (SSH public keys that should land on `/home/codex/.ssh/authorized_keys`)
4. Verify `~/.ssh/hetzner_codex` (private key) exists; run `.\deploy\scripts\check-ssh.ps1` once the server is reachable.
5. Stage artefacts/questions:
   - Confirm latest `rental_prediction` models in repo.
   - Update `DECISIONS.md` with planned release scope.

### 5.2 Stage on server (no changes yet)
1. Upload hardening bundle: `.\deploy\scripts\prep-remote.ps1`.
2. SSH as root: `ssh hetzner-chch` (alias defined in `%USERPROFILE%\.ssh\config`).
3. Verify files staged under `/home/codex/deploy/` (certs, app.env, harden script, authorized_keys).

### 5.3 Run hardening + base services
1. `sudo ./deploy/fullstack-harden.sh`
   - Script creates codex user, installs secrets/certs, configures Nginx, timers, fail2ban, etc.
2. Log out/in as `codex`, confirm systemd user service running:
   - `sudo -u codex XDG_RUNTIME_DIR=/run/user/$(id -u codex) systemctl --user status valua-api.service`
3. Provision swap/file system if flagged by script (check `/swapfile`).
4. Mirror UFW rules in Hetzner Cloud Firewall dashboard (only CF IPs to 80/443, admin CIDRs to 22).

### 5.4 Database provisioning
1. Install Postgres 16 if not present: `sudo apt-get install -y postgresql-16 postgresql-client-16`.
2. Create role + DB (match `deploy/secrets/app.env`):
   ```bash
   sudo -u postgres psql <<'SQL'
   CREATE ROLE valua_app WITH LOGIN PASSWORD '<DB_PASS>';
   CREATE DATABASE valua OWNER valua_app;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO valua_app;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE,SELECT ON SEQUENCES TO valua_app;
   GRANT USAGE ON SCHEMA public TO valua_app;
   SQL
   ```
3. Harden Postgres access (`/etc/postgresql/16/main/pg_hba.conf` + UFW rules so only loopback/app servers can connect).
4. Restart Postgres: `sudo systemctl restart postgresql`.

### 5.5 Deploy application code
1. Clone/update repo under `/srv/valua`:
   ```bash
   sudo -u codex -H bash -lc 'mkdir -p ~/apps && cd ~/apps && (test -d Valua && cd Valua && git pull || git clone https://github.com/future3OOO/Valua.git)'
   ```
2. Backend:
   ```bash
   sudo -u codex -H bash -lc '
     cd ~/apps/Valua/databasepl/backend &&
     python3.12 -m venv .venv &&
     .venv/bin/pip install -r requirements.txt &&
     XDG_RUNTIME_DIR=/run/user/$(id -u codex) systemctl --user restart valua-api.service
   '
   ```
3. Frontend build (if `INSTALL_NODE=1` / `BUILD_REACT=1`):
   ```bash
   sudo -u codex -H bash -lc '
     cd ~/apps/Valua/React &&
     corepack enable &&
     pnpm install &&
     pnpm build
   '
   ```
   Copy the built assets to `/var/www/chch` if not already handled by the script.
4. Prisma migrations:
   ```bash
   sudo -u codex -H bash -lc '
     cd ~/apps/Valua/React &&
     corepack enable &&
     pnpm install &&
     pnpm prisma migrate deploy
   '
   ```

### 5.6 Smoke tests & housekeeping
1. API health: `curl -I https://valua.co.nz/api/health/ready`
2. UI check: open https://valua.co.nz (via Cloudflare).
3. Database sanity:
   ```bash
   sudo -u codex -H bash -lc 'psql "$DATABASE_URL" -c "\dt"'
   ```
4. Review logs:
   - `journalctl --user -u valua-api.service -e`
   - `sudo tail -f /var/log/nginx/valua.error.log`
   - `fail2ban-client status nginx-cf`
5. Update `DECISIONS.md` with deployment summary, note CF token creation, Postgres password, and any manual steps.

Architecture Daddy owns every step end-to-end; if any secrets/tokens change, update `deploy/` scaffolding immediately so Future Daddy can reproduce the rollout.

## 6. Reporting cadence
- Daily async stand-up: each agent pings Architecture Daddy with status, blockers, and planned tasks.
- End-of-day: subordinate agents update their handover file and flag anything requiring immediate attention.
- Architecture Daddy consolidates updates and files a short summary in `DECISIONS.md`.

Keep this charter current—if expectations shift, edit here first then brief the simps. Daddy out. 💼
