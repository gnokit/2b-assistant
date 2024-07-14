import sqlite3
import os
from config import Config

import sqlite3
import os

def create_fts5_table(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Step 1: Check if FTS5 is supported
        cursor.execute("SELECT sqlite_version()")
        version = cursor.fetchone()[0]
        print(f"SQLite version: {version}")

        cursor.execute("SELECT * FROM pragma_compile_options WHERE compile_options LIKE 'ENABLE_FTS5'")
        if not cursor.fetchone():
            raise Exception("FTS5 is not enabled in this SQLite installation")

        # Step 2: Drop the existing FTS5 table if it exists
        cursor.execute("DROP TABLE IF EXISTS qa_pairs_fts")
        print("Dropped existing qa_pairs_fts table (if it existed)")

        # Step 3: Create the new FTS5 virtual table
        cursor.execute("""
        CREATE VIRTUAL TABLE qa_pairs_fts USING fts5(
            qa_id UNINDEXED,
            page_num UNINDEXED,
            question,
            answer
        )
        """)

        print("FTS5 table 'qa_pairs_fts' created successfully")
        
         # Step 4: Copy data from the existing table to the FTS5 table
        cursor.execute("""
        INSERT INTO qa_pairs_fts (qa_id, page_num, question, answer)
        SELECT qa_id, page_num, question, answer FROM qa_pairs
        """)        

        # Commit the changes
        conn.commit()        

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()

    finally:
        # Close the connection
        conn.close()

def test(db_path, sql):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()    
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            print(row)
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close the connection
        conn.close()    

if __name__ == "__main__":
    db_path = Config['qa_db']  # Replace with your actual database path
    if os.path.exists(db_path):
        sql = "select * from qa_pairs_fts where qa_pairs_fts match 'fish' order by rank"
        #create_fts5_table(db_path)        
        test(db_path, sql)  # Test the search functionality with a predefined query
    else:
        print(f"Database file not found: {db_path}")