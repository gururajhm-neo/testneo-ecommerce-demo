# Deploy TestNeo E‑Commerce Demo on EC2

Step-by-step guide to run this demo **beside** the main TestNeo product on the same EC2, with domain `testneo-ecom.testneo.ai`.

---

## What you get

| Item | Value |
|------|--------|
| UI | http://testneo-ecom.testneo.ai |
| Login | http://testneo-ecom.testneo.ai/login |
| Admin | http://testneo-ecom.testneo.ai/admin |
| API (via nginx) | http://testneo-ecom.testneo.ai/api/health |
| Direct UI (fallback) | http://YOUR_EC2_IP:3001 |
| Direct API (fallback) | http://YOUR_EC2_IP:9000 |

**Does not clash with main TestNeo**

| App | Frontend | Backend |
|-----|----------|---------|
| Main TestNeo | `:3000` | `:8000` / `:8001` |
| This e‑com demo | `:3001` | `:9000` |

---

## Admin login (seeded)

```
Email:    admin@ecommerce.com
Password: admin123
```

Other seeded users (optional):

- Moderator: `moderator@ecommerce.com` / `moderator123`
- Customer: `john@test.com` / `john123`

Public `/register` is **disabled**. Only admins create users (Admin → Users).

---

## Prerequisites

- EC2 Linux (Ubuntu) with main TestNeo already running
- SSH access as `ubuntu` (or your user)
- Security group inbound rules (same SG as the instance):

| Port | Purpose |
|------|---------|
| 22 | SSH |
| 80 | Domain via nginx |
| 443 | HTTPS (optional, later) |
| 3001 | Direct UI access (optional) |
| 9000 | Direct API access (optional) |

Do **not** open or reuse **8000** for this demo — that is main TestNeo.

---

## Step 1 — Get the code onto EC2

```bash
cd ~
# If cloning:
git clone <YOUR_REPO_URL> testneo-ecommerce-demo
cd testneo-ecommerce-demo

# Or upload/rsync your local copy into:
# ~/testneo-ecommerce-demo
```

---

## Step 2 — Python backend setup

```bash
cd ~/testneo-ecommerce-demo

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

SQLite DB (`ecommerce.db`) and mock data are created **automatically** when the backend starts the first time.

---

## Step 3 — Node 20 for this demo only (do not change default Node)

Vite 7 needs Node **20+**. Main TestNeo may use Node 18 — keep them separate.

```bash
cd ~/testneo-ecommerce-demo
bash upgrade_node_ec2.sh
```

This installs Node 20 via **nvm** and **does not** set it as the system default.

Verify:

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm use 20
node --version   # expect v20.x
```

Install frontend deps:

```bash
cd ~/testneo-ecommerce-demo/frontend
rm -rf node_modules
npm install
cd ..
```

---

## Step 4 — DNS for the subdomain

Where you manage `testneo.ai`, create:

| Type | Name | Value | TTL |
|------|------|--------|-----|
| A | `testneo-ecom` | `YOUR_EC2_PUBLIC_IP` (e.g. `34.229.255.219`) | `14000` or `300` while testing |

Important: apex `testneo.ai` may point elsewhere (e.g. LiteSpeed).  
**This subdomain must point at the EC2 IP**, not that other host.

Check:

```bash
dig +short testneo-ecom.testneo.ai
# should print your EC2 public IP
```

---

## Step 5 — Nginx reverse proxy

```bash
cd ~/testneo-ecommerce-demo

sudo apt update
sudo apt install -y nginx

sudo cp deploy/nginx-testneo-ecom.conf /etc/nginx/sites-available/testneo-ecom
sudo ln -sf /etc/nginx/sites-available/testneo-ecom /etc/nginx/sites-enabled/

# Avoid default site stealing the name (optional but recommended)
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl enable nginx
sudo systemctl reload nginx
```

Nginx maps:

- `/` → `127.0.0.1:3001` (UI)
- `/api/` → `127.0.0.1:9000` (FastAPI)

---

## Step 6 — Start services (critical env vars)

On a shared EC2, **main TestNeo often sets `PORT=8000`**.  
This demo must **not** use that — it must bind **9000**.

```bash
cd ~/testneo-ecommerce-demo

# Always unset these before starting the demo backend
unset PORT
unset CORS_ORIGINS
export ECOM_HOST=0.0.0.0
export ECOM_PORT=9000

# Prefer helper scripts
chmod +x start_backend.sh start_frontend.sh start_all.sh stop_all.sh ensure_services.sh upgrade_node_ec2.sh

./stop_all.sh   # only frees 3001 + 9000 (safe for main TestNeo)

# Option A — start both
./start_all.sh

# Option B — repair / ensure both are healthy
bash ensure_services.sh
```

Or start backend manually:

```bash
cd ~/testneo-ecommerce-demo
source .venv/bin/activate
unset PORT CORS_ORIGINS
export ECOM_PORT=9000
nohup python main.py > /tmp/testneo-backend.log 2>&1 &

# Frontend (Node 20 + production build)
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm use 20
nohup ./start_frontend.sh > /tmp/testneo-frontend.log 2>&1 &
```

You should see in the backend log:

```text
Starting ecommerce API on 0.0.0.0:9000
Application startup complete.
```

If you see `bind on address ('0.0.0.0', 8000)` — `PORT` was still set. `unset PORT` and restart.

---

## Step 7 — Verify

On the server:

```bash
ss -tlnp | grep -E ':9000|:3001'
curl -s http://127.0.0.1:9000/health
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:3001/
curl -s http://testneo-ecom.testneo.ai/api/health
curl -s -o /dev/null -w "%{http_code}\n" http://testneo-ecom.testneo.ai/
```

Expected: health JSON + HTTP `200` for UI.  
**Not** `502` on `/api` (502 = nginx up, backend on 9000 down).

From your laptop:

- http://testneo-ecom.testneo.ai/login  
- Login with `admin@ecommerce.com` / `admin123`

---

## Step 8 — Optional HTTPS

After HTTP works:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d testneo-ecom.testneo.ai
```

Open security group **TCP 443**. Update CORS already includes `https://testneo-ecom.testneo.ai`.

---

## Day-2 operations

### Restart demo only

```bash
cd ~/testneo-ecommerce-demo
./stop_all.sh
unset PORT CORS_ORIGINS
export ECOM_PORT=9000
./start_all.sh
# or: bash ensure_services.sh
```

### Rebuild frontend after UI changes

```bash
cd ~/testneo-ecommerce-demo
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm use 20
./stop_all.sh
./start_all.sh    # start_frontend.sh builds then serves dist
```

### Re-seed mock data (only if DB empty / &lt; 20 products)

```bash
cd ~/testneo-ecommerce-demo
source .venv/bin/activate
python populate_mock_data.py
```

### Logs

```bash
tail -f /tmp/testneo-backend.log
tail -f /tmp/testneo-frontend.log
sudo tail -f /var/log/nginx/error.log
```

---

## Security checklist (already in this repo)

- [x] Public registration disabled (`/register` → login; API register = admin only)
- [x] Create users only from Admin → Users
- [ ] Change default admin password after first login
- [ ] Prefer HTTPS (certbot)
- [ ] Rotate `secret_key` / `jwt_secret_key` in `config.py` (or env) for real use
- [ ] Never run broad kills on this host:

```bash
# DANGEROUS on shared EC2 — can kill main TestNeo
# pkill -f npm
# pkill -f vite
# pkill -f serve
```

Use only:

```bash
./stop_all.sh    # ports 3001 and 9000 only
```

---

## Troubleshooting

### 502 Bad Gateway (nginx)

| Check | Meaning |
|-------|---------|
| UI loads, login/API 502 | Backend not on **9000** |
| `curl :9000/health` fails | Start backend; check log |
| Log shows bind **8000** | `unset PORT`; use `ECOM_PORT=9000` |
| Log shows `cors_origins` JSON error | Deploy latest `config.py`; `unset CORS_ORIGINS` |

```bash
curl -s http://127.0.0.1:9000/health || tail -50 /tmp/testneo-backend.log
```

### Unable to connect to :3001

1. Security group allows 3001 (or use domain on port 80).
2. Frontend running: `ss -tlnp | grep 3001`
3. Node version: need 20+ (`nvm use 20`). Node 18 + Vite 7 → `crypto.hash is not a function`.

### Login “Network Error”

Frontend OK, API unreachable — same as 502: fix backend on 9000 / nginx `/api`.

### Domain not resolving

```bash
dig +short testneo-ecom.testneo.ai
```

Must equal EC2 public IP. Wait for TTL if you just changed DNS.

---

## Quick copy-paste (fresh box / after pull)

```bash
cd ~/testneo-ecommerce-demo

bash upgrade_node_ec2.sh
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm use 20

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd frontend && npm install && cd ..

sudo cp deploy/nginx-testneo-ecom.conf /etc/nginx/sites-available/testneo-ecom
sudo ln -sf /etc/nginx/sites-available/testneo-ecom /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

chmod +x *.sh
unset PORT CORS_ORIGINS
export ECOM_PORT=9000
./stop_all.sh
./start_all.sh
sleep 5
bash ensure_services.sh

curl -s http://127.0.0.1:9000/health
curl -s http://testneo-ecom.testneo.ai/api/health
```

Then open: **http://testneo-ecom.testneo.ai/login**

---

## File reference

| Path | Role |
|------|------|
| `start_all.sh` / `stop_all.sh` | Start/stop demo only (3001/9000) |
| `start_backend.sh` | Backend on `ECOM_PORT` (default 9000) |
| `start_frontend.sh` | Node 20 + production build + serve |
| `ensure_services.sh` | Health-check and restart if needed |
| `upgrade_node_ec2.sh` | Install Node 20 via nvm (no default change) |
| `deploy/nginx-testneo-ecom.conf` | Domain reverse proxy |
| `config.py` | CORS, safe env parsing, ignore shared `PORT` |
| `frontend/src/api.js` | IP → `:9000`; domain → `/api` via nginx |
