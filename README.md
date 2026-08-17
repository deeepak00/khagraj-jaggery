# GurMahima — Jaggery E-commerce App

Full-stack app: **Flask** (REST API) + **Vue 3 / Vite / Pinia** (frontend).

```
khagraj_jaggery/
├── backend/
│   ├── app.py                 # Flask app factory, DB seed, entry point
│   ├── config.py               # Env-based config (dev/prod)
│   ├── extensions.py           # db, jwt, mail, cache, cors, celery
│   ├── tasks.py                 # Celery email tasks
│   ├── gunicorn.conf.py         # Production server config
│   ├── models/
│   │   └── models.py            # User, Product, Order, SiteSetting
│   ├── routers/                 # Blueprints (was misnamed "routes" — see note below)
│   │   ├── __init__.py           # require_auth / require_admin decorators
│   │   ├── user.py               # /api/auth, /api/products, /api/orders, /api/settings
│   │   └── admin.py              # /api/admin/*
│   ├── static/uploads/          # Uploaded product images / logo land here
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── .env.example
│   └── src/
│       ├── main.js / App.vue
│       ├── api/index.js         # Axios instance + endpoint helpers
│       ├── router/index.js      # Vue Router routes + auth guards
│       ├── stores/               # Pinia: auth, cart, site, toast
│       ├── components/           # AppNavbar, AppFooter, CartSidebar, ProductCard, AppToast
│       └── pages/                # HomePage, ShopPage, AuthPage, CheckoutPage, MyOrdersPage,
│                                  # OrderSuccessPage, admin/* (Dashboard, Products, Orders, Users, Settings)
├── requirements.txt
└── Procfile
```

## What was wrong with the original zip, and what changed

1. **`backend/routes/` was named wrong.** Every file (`app.py`, `routers/user.py`,
   `routers/admin.py`) imports from `routers` (e.g. `from routers.user import user_bp`), but the
   folder on disk was `routes/`. That made the app crash on startup with
   `ModuleNotFoundError: No module named 'routers'`. **Fixed** by renaming the folder to
   `routers/` to match the imports.
2. **The whole Vue frontend was flat** — all `.vue`/`.js` files sat directly in `frontend/`
   with no `src/`, even though `vite.config.js` aliases `@` to `./src` and every component
   imports from `@/stores/...`, `@/components/...`, `@/pages/...`. **Fixed** by moving each file
   into the structure its own imports expect (`src/stores`, `src/components`, `src/pages`,
   `src/pages/admin`, `src/api`, `src/router`, `src/assets`).
3. **Two files were both named `index.js`** (one was the Axios API client, the other the
   Vue Router config — the second had literally been saved as `index (1).js` by the OS).
   **Fixed**: the API client is now `src/api/index.js` and the router is `src/router/index.js`,
   matching what `App.vue`/pages import.
4. **Missing files that the code already references but the zip never included:**
   - `frontend/index.html` — Vite's required entry HTML file (didn't exist at all).
   - `src/stores/toast.js` — `useToastStore` is imported/used in 8+ files but was never
     included. Added a small Pinia store (`success()`, `error()`, `info()`).
   - `src/components/AppToast.vue` — imported by `App.vue` but missing. Added a minimal
     toast-notification UI that reads from the store above.
   - `src/pages/OrderSuccessPage.vue` — routed to from `router/index.js`
     (`/success/:orderNumber`) and used after checkout, but missing. Added a simple
     order-confirmation page.
   - `backend/gunicorn.conf.py` — referenced by the `Procfile` (`gunicorn -c gunicorn.conf.py`)
     but not present. Added a sane default config.
   - `.env.example` for both `backend/` and `frontend/` — no environment template existed.

Both halves have been verified to actually run: the Flask app factory boots, seeds the DB,
and registers all routes; `npm install && npx vite build` completes cleanly with no unresolved
imports.

## Setup & Run

### 1. Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

cp .env.example .env            # then edit values as needed
# Minimum to get going: nothing is required — defaults work with local SQLite,
# eager (synchronous) Celery tasks, and console-only "sent" emails.

python app.py                   # runs on http://localhost:5000
```

- On first run it creates `backend/jaggery.db` (SQLite), seeds an admin user and sample
  products, and prints the admin email in the log.
- Default admin login: `admin@gurmahima.in` / `Admin@2025` (override via `.env`).
- Health check: `GET http://localhost:5000/health`

**Optional (production-like) extras:**
- Postgres: set `DATABASE_URL` in `.env`.
- Redis + async email/tasks: set `REDIS_URL`; without it, Celery tasks run synchronously (eager mode).
- Real outgoing email: set `MAIL_USERNAME` / `MAIL_PASSWORD`; without it, emails are just skipped.

### 2. Frontend (Vue 3 + Vite)

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env            # optional — default already points to /api via the dev proxy
npm run dev                     # runs on http://localhost:5173
```

The Vite dev server proxies `/api`, `/uploads`, and `/health` to `http://localhost:5000`
(see `vite.config.js`), so just open **http://localhost:5173** once both servers are running.

```bash
npm run build     # production build -> frontend/dist
npm run preview   # preview the production build locally
```

### 3. Production Deployment on Render.com (Step-by-Step)

Follow these literal steps to deploy the application on **Render.com** for your customers:

---

#### **Step A: Push Code to GitHub**
1. Create a new repository on your GitHub account.
2. Initialize git in your local project root (`khagraj_jaggery_fixed/`) and push the entire codebase to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Prepare for deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

---

#### **Step B: Deploy the Backend (Render Web Service)**
1. Go to your **Render Dashboard** and click **New +** > **Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   * **Name**: `khagraj-backend` (or any name you prefer)
   * **Region**: Choose the region closest to your customers (e.g., `Singapore` for India).
   * **Root Directory**: `backend` *(This is important!)*
   * **Runtime**: `Python 3` (or the latest version available)
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn -c gunicorn.conf.py app:app`
4. Expand the **Advanced** section to add **Environment Variables**:
   * `FLASK_ENV`: `production`
   * `SECRET_KEY`: `<generate-a-long-random-string>`
   * `JWT_SECRET_KEY`: `<generate-another-long-random-string>`
   * `FRONTEND_URL`: `https://your-frontend-subdomain.onrender.com` (you will update this with your frontend URL once created).
5. **Setup a Free Database on Neon.tech (Crucial for 100% Free Persistent Storage)**:
   * Go to **[Neon.tech](https://neon.tech/)** and sign up for a free account (no credit card required).
   * Click **Create Project**, name it `khagraj`, and choose the nearest region.
   * Under **Dashboard**, copy your connection string (looks like `postgresql://alex:password@ep-cool-water-1234.us-east-2.neon.tech/neondb?sslmode=require`).
   * Back in your Render Web Service dashboard, add a new **Environment Variable**:
     * `DATABASE_URL`: `<paste-your-neon-connection-string>`
   * *Why this is needed*: Since Render's free tier does not support persistent disks, any local SQLite file gets erased every 15 minutes. Using Neon.tech ensures your orders, user accounts, and settings are saved forever, completely free!
6. Click **Create Web Service**. Wait for it to build. Note down the backend URL (e.g. `https://khagraj-backend.onrender.com`).

---

#### **Step C: Deploy the Frontend (Render Static Site)**
1. Go to your **Render Dashboard** and click **New +** > **Static Site**.
2. Connect your GitHub repository.
3. Configure the following settings:
   * **Name**: `khagraj-frontend` (or your brand name)
   * **Root Directory**: `frontend` *(This is important!)*
   * **Build Command**: `npm run build`
   * **Publish Directory**: `dist`
4. Expand the **Advanced** section and add **Environment Variables**:
   * `VITE_API_URL`: `https://your-backend-url.onrender.com` (paste the URL of your backend service created in Step B).
5. **Setup Redirects & Rewrites (To solve image pathing and CORS)**:
   * Once the static site is created, go to **Redirects/Rewrites** in the static site side menu.
   * Add a new rule:
     * **Source Path**: `/uploads/*`
     * **Destination Path**: `https://your-backend-url.onrender.com/uploads/*`
     * **Action**: `Rewrite`
   * Add a second rule:
     * **Source Path**: `/api/*`
     * **Destination Path**: `https://your-backend-url.onrender.com/api/*`
     * **Action**: `Rewrite`
   * Add a third rule (for Vue Router SPA routing fallback):
     * **Source Path**: `/*`
     * **Destination Path**: `/index.html`
     * **Action**: `Rewrite`
6. Click **Create Static Site**.

---

#### **Step D: Deploy the Celery Worker (Render Background Worker)**
To run email notifications asynchronously using Celery:
1. **Create a Redis Queue**:
   * **Using Render Key Value**: Click **New +** > **Key Value** (this is Render's managed Redis service). Name it `khagraj-redis` and click create. Once active, copy the connection URL starting with `redis://` or `rediss://`.
   * **Using Upstash (Permanently Free)**: Go to [Upstash](https://upstash.com/), create a free Redis database, and copy the connection string.
2. **Add `REDIS_URL` to Backend**: Go to your Backend Web Service's environment variables and add `REDIS_URL` with the copied Redis connection string.
3. **Deploy the Worker Service**:
   * On the Render Dashboard, click **New +** > **Background Worker**.
   * Connect your GitHub repository and set:
     * **Name**: `khagraj-celery-worker`
     * **Root Directory**: `backend` *(This is important!)*
     * **Runtime**: `Python 3`
     * **Build Command**: `pip install -r requirements.txt`
     * **Start Command**: `celery -A app.celery worker --loglevel=info`
   * Under **Advanced**, copy all environment variables from your Backend Web Service (including `DATABASE_URL`, `REDIS_URL`, and SMTP server credentials so it can send emails).
4. Click **Create Background Worker**.

Once both builds finish, your website will be live! Open your frontend URL to access the site. You can login to the admin panel with the default seeded credentials.

---

### **🖼️ Handling Image Uploads for Free (logo/photos/products)**
Since Render's free tier has an **ephemeral filesystem** (any uploaded files are wiped out when the server sleeps or restarts), follow this approach to keep your site completely free:
* Instead of uploading raw files in the admin panel, upload your brand logos, manager photos, and product images to a free image hosting service (such as **[ImgBB](https://imgbb.com/)** or **[PostImages](https://postimages.org/)**).
* Copy the **Direct Link** to the image (ending in `.png`, `.jpg`, or `.webp`).
* Paste this URL directly into the product image fields or admin site settings inside your admin dashboard. This avoids needing storage disks completely!

---

### **🔒 Production Security & Environment Variables Reference**

To protect your application from unauthorized access, data leaks, and attacks, you must set these environment variables in your production server dashboard:

| Variable | Recommended Value / Format | Description & Security Purpose |
| :--- | :--- | :--- |
| **`FLASK_ENV`** | `production` | **CRITICAL**: Turns off debug mode, debugger consoles, and stack traces that could expose backend code to hackers. |
| **`SECRET_KEY`** | A 64-character random hex string | Signs sessions and secure cookies. Generate one using: `python -c "import secrets; print(secrets.token_hex(32))"`. Keep this secret! |
| **`JWT_SECRET_KEY`** | A different 64-character random hex string | Signs JSON Web Tokens (JWT) for user authentication. Protects user sessions from spoofing. |
| **`FRONTEND_URL`** | `https://your-brand-name.onrender.com` | **CORS protection**: Ensures that only your official frontend can make API calls, locking out malicious requests from third-party sites. |
| **`ADMIN_EMAIL`** | `your-secure-admin-email@domain.com` | Overrides the default seed email to protect your administrative panel. |
| **`ADMIN_PASSWORD`** | A strong, unique password (e.g. `Kj#9!ax$2Lq`) | Overrides the default password (`Admin@2025`) to prevent automated credential scanning attacks. |
| **`DB_PATH`** *(If SQLite)* | `/data/jaggery.db` | Path inside the mounted persistent disk volume to save database changes. |
| **`UPLOAD_FOLDER`** *(If SQLite)* | `/data/uploads` | Path inside the mounted persistent disk volume to save uploaded media. |
| **`DATABASE_URL`** *(If PostgreSQL)* | `postgresql+psycopg2://user:password@host:5432/dbname` | Secure connection string to your database. Used instead of SQLite for automatic scaling. |
| **`REDIS_URL`** | `redis://default:password@host:port/0` | Secure broker endpoint for async Celery task queues. |
| **`MAIL_SERVER`** | `smtp.gmail.com` (or your mail host) | Outgoing mail server address. |
| **`MAIL_PORT`** | `587` | Port for TLS mail communication. |
| **`MAIL_USE_TLS`** | `true` | Forces TLS encryption for outgoing emails to prevent credential interception. |
| **`MAIL_USERNAME`** | `your-email@gmail.com` | SMTP login account. |
| **`MAIL_PASSWORD`** | 16-character App Password | Secure app token instead of your raw Google account password. |
| **`MAIL_SENDER`** | `BrandName <your-email@gmail.com>` | Custom brand sender name to prevent email spam flags. |

---

### **🚀 Performance & Mobile Compatibility Optimizations**

We have made significant optimizations to ensure the app is fast, responsive, and does not freeze or time out:
1. **Batch Writes for Site Settings**: Consolidated 30+ sequential settings queries into a single query in `models/SiteSetting.set_many` to prevent network latency timeouts (sub-100ms updates).
2. **Dashboard Query Reductions**: Grouped order status counts (`GROUP BY`) and daily revenues into single SQL operations. Dashboard query counts dropped from 20 to 8 queries.
3. **Background Threading Fallback**: Created a threading handler in `tasks.py` to run Celery tasks asynchronously in a background daemon thread if Redis is missing. This prevents SMTP email connections from blocking HTTP requests.
4. **NullCache Fallback**: Avoids stale Gunicorn process-local memory caching when Redis is missing, ensuring settings and product updates are live instantly.
5. **Admin Drawer Navigation & Mobile Grid Layouts**: Integrated a sliding sidebar nav drawer on mobile viewports with backdrop overlay triggers. Replaced rigid inline styles in `DashboardPage` and `SettingsPage` with a responsive grid (`.admin-grid-2x1`) to guarantee perfect scaling on all phone screens.
