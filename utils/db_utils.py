import sqlite3
from datetime import datetime
import streamlit as st
import sqlite3
import pandas as pd
from typing import List, NamedTuple

# Initialize database and create a table
def init_db():
    conn = sqlite3.connect("local.db")  # Creates a local SQLite database file
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records_V1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uniqueid TEXT UNIQUE NOT NULL,
            asana TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            remarks TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to write a record to the database
def write_to_db(uniqueid, asana, status,neg_status=['Match Not Found'],pos_status=['Match Found']):
    conn = sqlite3.connect("local.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Check if the unique ID exists
        cursor.execute("SELECT status FROM records_V1 WHERE uniqueid = ? AND asana = ?", (uniqueid,asana))
        db_status = cursor.fetchone()
        if db_status:
            print(f"Current status : {cursor.fetchone()[0]}")
            if db_status[0] in neg_status:
                if status in neg_status:
                    pass
                else:
                    cursor.execute("""
                    UPDATE records_V1
                    SET  timestamp = ?, status = ?
                    WHERE uniqueid = ?, asana = ?
                """, (timestamp, status, uniqueid, asana))
                print(f"Record updated successfully. {uniqueid} {asana} {status}")
            else:
                    # Update the existing record
                if status in pos_status:
                    pass
                else:
                    cursor.execute("""
                        UPDATE records_V1
                        SET  timestamp = ?, status = ?
                        WHERE uniqueid = ?, asana = ?
                    """, (timestamp, status, uniqueid, asana))
                    print(f"Record updated successfully. {uniqueid} {asana} {status}")
        else:
            # Insert a new record
            cursor.execute("""
                INSERT INTO records_V1 (uniqueid, asana, timestamp, status)
                VALUES (?, ?, ?, ?)
            """, (uniqueid, asana, timestamp, status))
            print(f"Record added successfully.  {uniqueid} {asana} {status}")

            conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


# Initialize the database and table
init_db()

def clear_table():
    conn = sqlite3.connect("local.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM records_V1")
        conn.commit()
        print("Table cleared successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# Function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect("local.db")
    query = "SELECT * FROM records_V1"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

class MatchResult(NamedTuple):
    uid:int
    asana: int
    status: str
# Example usage
#write_to_db("UID123", "Active", "Initial entry")
#write_to_db("UID124", "Inactive", "Test entry")
