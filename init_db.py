import psycopg2
import os

conn = psycopg2.connect(
    dbname=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.environ['PGPASSWORD'],
    host=os.environ['PGHOST'],
    port=os.environ['PGPORT']
)

cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# Create goals table
cur.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    activity TEXT NOT NULL,
    objective TEXT,
    frequency TEXT,
    notes TEXT,
    rating INTEGER,
    last_updated TIMESTAMP
);
""")

# Insert default admin user (password: admin123)
from werkzeug.security import generate_password_hash
admin_pw = generate_password_hash("admin123")
cur.execute("""
INSERT INTO users (username, password)
VALUES (%s, %s)
ON CONFLICT (username) DO NOTHING;
""", ("admin", admin_pw))

# Optional: Prepopulate goals table (can be removed later)
goals = [
    ('Health Improvement', 'Gym', 'Build Muscle Mass, Reduce Body Fat to 15%', '3x/week, 60 min'),
    ('Health Improvement', 'Core', 'Strengthen core to support body', '15 min/day'),
    ('Health Improvement', 'Yoga', 'Enhance flexibility', '1x/week'),
    ('Sports', 'Padel', 'Compete in 3 competitions', 'Max 2 sessions/week'),
    ('Skill Improvement', 'AI Courses', 'Learn AI applications post-retirement', 'Online learning'),
    ('Travel', 'Taiwan Trip', 'Complete trip by Oct', '1x Oct')
]

for g in goals:
    cur.execute("""
        INSERT INTO goals (category, activity, objective, frequency)
        VALUES (%s, %s, %s, %s)
    """, g)

conn.commit()
cur.close()
conn.close()
print("✅ Database initialized.")
