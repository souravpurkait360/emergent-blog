import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')


def ensure_pg_running():
    try:
        result = subprocess.run(['pg_isready', '-q'], capture_output=True, timeout=5)
        if result.returncode != 0:
            subprocess.run(['service', 'postgresql', 'start'], capture_output=True, timeout=15)
            for _ in range(15):
                time.sleep(1)
                r = subprocess.run(['pg_isready', '-q'], capture_output=True, timeout=5)
                if r.returncode == 0:
                    return
    except Exception as e:
        print(f"PG startup: {e}", flush=True)


def run_django_setup():
    """Run migrations and admin seeding via subprocess (avoids async context issues)."""
    env = os.environ.copy()
    manage = str(ROOT_DIR / 'manage.py')

    # Create migrations if they don't exist
    subprocess.run(
        [sys.executable, manage, 'makemigrations', '--no-input'],
        cwd=str(ROOT_DIR), capture_output=True, text=True, env=env
    )

    # Apply migrations
    r = subprocess.run(
        [sys.executable, manage, 'migrate', '--no-input'],
        cwd=str(ROOT_DIR), capture_output=True, text=True, env=env
    )
    if r.stdout:
        print(r.stdout, flush=True)
    if r.returncode != 0:
        print(f"Migrate error: {r.stderr[:400]}", flush=True)
        return

    # Create admin user
    admin_email = env.get('ADMIN_EMAIL', 'admin@blog.com')
    admin_password = env.get('ADMIN_PASSWORD', 'admin123')
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
    r2 = subprocess.run([sys.executable, '-c', script],
                        cwd=str(ROOT_DIR), capture_output=True, text=True, env=env)
    if r2.stdout:
        print(r2.stdout, flush=True)


ensure_pg_running()
run_django_setup()

import django
django.setup()

from django.core.asgi import get_asgi_application
app = get_asgi_application()
