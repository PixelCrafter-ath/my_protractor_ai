#!/usr/bin/env python
"""
Migrate app.py from flask_mysqldb to mysql.connector
This script carefully replaces database code while preserving indentation.
"""

import re

def migrate_database():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Starting database migration...")
    
    # Step 1: Replace import statement
    content = content.replace(
        'from flask_mysqldb import MySQL',
        'import mysql.connector'
    )
    print("✓ Replaced import statement")
    
    # Step 2: Replace MySQL configuration and initialization
    old_config = """app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'Aviro@123'
app.config['MYSQL_DB'] = 'quizapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'"""
    
    new_config = """# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aviro@123",
    database="quizapp"
)
cursor = db.cursor(dictionary=True)"""
    
    content = content.replace(old_config, new_config)
    print("✓ Replaced database configuration")
    
    # Step 3: Remove mysql = MySQL(app)
    content = content.replace(
        '\nmysql = MySQL(app)\n',
        '\n'
    )
    print("✓ Removed MySQL(app) initialization")
    
    # Step 4: Replace all mysql.connection.cursor() usage patterns
    # Pattern 1: cur = mysql.connection.cursor() followed by cur.execute()
    # We'll replace these one by one to preserve indentation
    
    # Replace all instances of mysql.connection.cursor() with a comment to use global cursor
    content = re.sub(
        r'(\s+)cur = mysql\.connection\.cursor\(\)',
        r'\1# Using global cursor',
        content
    )
    print("✓ Replaced mysql.connection.cursor() calls")
    
    # Step 5: Replace all cur.execute with cursor.execute
    content = content.replace('cur.execute', 'cursor.execute')
    print("✓ Replaced cur.execute -> cursor.execute")
    
    # Step 6: Replace all cur.fetchall with cursor.fetchall
    content = content.replace('cur.fetchall', 'cursor.fetchall')
    print("✓ Replaced cur.fetchall -> cursor.fetchall")
    
    # Step 7: Replace all cur.fetchone with cursor.fetchone
    content = content.replace('cur.fetchone', 'cursor.fetchone')
    print("✓ Replaced cur.fetchone -> cursor.fetchone")
    
    # Step 8: Replace all mysql.connection.commit() with db.commit()
    content = content.replace('mysql.connection.commit()', 'db.commit()')
    print("✓ Replaced mysql.connection.commit() -> db.commit()")
    
    # Step 9: Remove all cur.close() statements
    content = re.sub(
        r'\s*cur\.close\(\)',
        '',
        content
    )
    print("✓ Removed cur.close() statements")
    
    # Step 10: Remove all cur1.close(), cur2.close(), etc.
    content = re.sub(
        r'\s*cur\d+\.close\(\)',
        '',
        content
    )
    print("✓ Removed cur1.close(), cur2.close(), etc.")
    
    # Write the migrated content
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Migration completed successfully!")
    print("Please verify the file compiles correctly.")

if __name__ == '__main__':
    migrate_database()
