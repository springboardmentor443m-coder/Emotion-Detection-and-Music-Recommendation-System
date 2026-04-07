"""
MoodMate - Database Setup Script (Python version, no psql needed)
Run: py setup_db.py
"""
import subprocess, sys, os, getpass

print("=" * 52)
print("   MoodMate - PostgreSQL Setup (Python version)")
print("=" * 52)

# ── Step 1: Install psycopg2 if needed ───────────────
try:
    import psycopg2
except ImportError:
    print("\n📦 Installing psycopg2 for setup...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary", "-q"])
    import psycopg2

# ── Step 2: Ask for postgres password ────────────────
print("\nEnter the password you set for PostgreSQL during install.")
pg_password = getpass.getpass("postgres password: ")

# ── Step 3: Connect as superuser and create DB + user ─
print("\nConnecting to PostgreSQL...")
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",      # connect to default db first
        user="postgres",
        password=pg_password
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create user if not exists
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname='moodmate_user'")
    if not cur.fetchone():
        cur.execute("CREATE USER moodmate_user WITH PASSWORD 'moodmate_pass'")
        print("✅ Created user: moodmate_user")
    else:
        print("✅ User moodmate_user already exists")

    # Create database if not exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname='moodmate_db'")
    if not cur.fetchone():
        cur.execute("CREATE DATABASE moodmate_db OWNER moodmate_user")
        print("✅ Created database: moodmate_db")
    else:
        print("✅ Database moodmate_db already exists")

    # Grant privileges
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE moodmate_db TO moodmate_user")
    print("✅ Privileges granted")

    cur.close()
    conn.close()

    print("\n" + "=" * 52)
    print("   Setup complete! ✅")
    print("=" * 52)
    print("   DB Host:     localhost:5432")
    print("   Database:    moodmate_db")
    print("   User:        moodmate_user")
    print("   Password:    moodmate_pass")
    print("\nNext step — install Python packages:")
    print("   pip install asyncpg bcrypt python-jose[cryptography]")
    print("\nThen start the server:")
    print("   py -m uvicorn main:app --reload")
    print("=" * 52)

except psycopg2.OperationalError as e:
    err = str(e)
    print(f"\n❌ Connection failed: {err}")
    if "password" in err.lower():
        print("\n→ Wrong password. Try running setup_db.py again with the correct postgres password.")
    elif "could not connect" in err.lower() or "refused" in err.lower():
        print("\n→ PostgreSQL is not running!")
        print("  Fix: Press Windows key → search 'Services'")
        print("  Find 'postgresql-x64-16' (or similar) → right-click → Start")
    else:
        print("\n→ Check that PostgreSQL is installed and running.")
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")

input("\nPress Enter to close...")