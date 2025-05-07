import os
import subprocess
import psycopg2

DB = {
    'host': os.getenv("DB_HOST", "localhost"),
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': os.getenv("DB_PORT", "5432"),
}

def get_git_log(repo_path, repo_name):
    log_format = '--pretty=format:%H|%an|%ae|%ad|%s'
    try:
        output = subprocess.check_output(
            ['git', '-C', repo_path, 'log', log_format],
            text=True
        )
        for line in output.splitlines():
            parts = line.strip().split('|')
            if len(parts) == 5:
                yield [repo_name] + parts
    except subprocess.CalledProcessError:
        print(f"Skipping {repo_path} (git error)")

def get_submodule_paths():
    try:
        output = subprocess.check_output(
            ['git', 'submodule', 'foreach', '--quiet', 'echo $path'],
            text=True
        )
        return [line.strip() for line in output.splitlines()]
    except subprocess.CalledProcessError:
        return []

def main():
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    # Log from main repo
    for commit in get_git_log('.', 'main'):
        cur.execute("""
            INSERT INTO commits (repo, commit_hash, author_name, author_email, commit_date, message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, commit)

    # Logs from submodules
    for sub_path in get_submodule_paths():
        for commit in get_git_log(sub_path, sub_path):
            cur.execute("""
                INSERT INTO commits (repo, commit_hash, author_name, author_email, commit_date, message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, commit)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All commit logs inserted successfully.")

if __name__ == "__main__":
    main()
