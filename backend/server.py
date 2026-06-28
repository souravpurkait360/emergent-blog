import os
from pathlib import Path
import subprocess
import sys
import time

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")

PG_VERSION = "15"
DB_NAME = "blogdb"
DB_USER = "bloguser"
DB_PASS = "blogpassword123"


def _pg_bin(cmd: str) -> str:
    """Resolve a PostgreSQL binary, checking standard Debian locations."""
    candidates = [
        f"/usr/bin/{cmd}",
        f"/usr/lib/postgresql/{PG_VERSION}/bin/{cmd}",
        f"/usr/local/bin/{cmd}",
    ]
    for path in candidates:
        if Path(path).exists():
            return path
    return cmd  # fall back and let the shell resolve it


def _pg_running() -> bool:
    try:
        r = subprocess.run(
            [_pg_bin("pg_ctlcluster"), PG_VERSION, "main", "status"],
            capture_output=True, timeout=5,
        )
        return r.returncode == 0
    except FileNotFoundError:
        return False


def ensure_pg_running() -> None:
    """Install PostgreSQL if missing, start the cluster, create DB/user."""
    # --- Install if not present ---
    if not Path(_pg_bin("pg_ctlcluster")).exists():
        print("PostgreSQL not found — installing...", flush=True)
        subprocess.run(
            ["apt-get", "install", "-y", f"postgresql-{PG_VERSION}"],
            capture_output=False, timeout=120,
        )

    if not _pg_running():
        subprocess.run(
            [_pg_bin("pg_ctlcluster"), PG_VERSION, "main", "start"],
            capture_output=True, timeout=30,
        )
        for _ in range(15):
            time.sleep(1)
            if _pg_running():
                break

    # --- Ensure DB and user exist ---
    try:
        import psycopg2

        # Test connection first
        conn = psycopg2.connect(
            host="localhost", port=5432,
            user=DB_USER, password=DB_PASS, database=DB_NAME,
        )
        conn.close()
    except Exception:
        _bootstrap_db()


def _bootstrap_db() -> None:
    """Create bloguser + blogdb via the postgres superuser."""
    try:
        import psycopg2

        conn = psycopg2.connect(host="localhost", port=5432, database="postgres")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM pg_roles WHERE rolname=%s", (DB_USER,)
        )
        if not cur.fetchone():
            cur.execute(
                f"CREATE USER {DB_USER} WITH PASSWORD %s CREATEDB", (DB_PASS,)
            )
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,)
        )
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER}")
        cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        conn.close()
        print("DB bootstrap complete", flush=True)
    except Exception as exc:
        print(f"DB bootstrap error: {exc}", flush=True)


def run_django_setup():
    """Run migrations and admin seeding via subprocess (avoids async context issues)."""
    env = os.environ.copy()
    manage = str(ROOT_DIR / "manage.py")

    # Create migrations if they don't exist
    subprocess.run(
        [sys.executable, manage, "makemigrations", "--no-input"],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
        env=env,
    )

    # Apply migrations
    r = subprocess.run(
        [sys.executable, manage, "migrate", "--no-input"], cwd=str(ROOT_DIR), capture_output=True, text=True, env=env
    )
    if r.stdout:
        print(r.stdout, flush=True)
    if r.returncode != 0:
        print(f"Migrate error: {r.stderr[:400]}", flush=True)
        return

    # Create admin user
    admin_email = env.get("ADMIN_EMAIL", "admin@blog.com")
    admin_password = env.get("ADMIN_PASSWORD", "admin123")
    script = f"""
import sys; sys.path.insert(0, '{ROOT_DIR}')
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'blog_project.settings'
import django; django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='{admin_email}').exists():
    User.objects.create_superuser(username='admin', email='{admin_email}', password='{admin_password}', role='admin')
    print('Admin created')
"""
    r2 = subprocess.run([sys.executable, "-c", script], cwd=str(ROOT_DIR), capture_output=True, text=True, env=env)
    if r2.stdout:
        print(r2.stdout, flush=True)


ensure_pg_running()
run_django_setup()

import django

django.setup()

from django.core.asgi import get_asgi_application

app = get_asgi_application()
