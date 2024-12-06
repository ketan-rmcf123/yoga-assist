import sqlite3
from datetime import datetime
import streamlit as st
import sqlite3
import pandas as pd
from typing import List, NamedTuple
import logging
import os

import streamlit as st
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)

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

def get_ice_servers():
    """Use Twilio's TURN server because Streamlit Community Cloud has changed
    its infrastructure and WebRTC connection cannot be established without TURN server now.  # noqa: E501
    We considered Open Relay Project (https://www.metered.ca/tools/openrelay/) too,
    but it is not stable and hardly works as some people reported like https://github.com/aiortc/aiortc/issues/832#issuecomment-1482420656  # noqa: E501
    See https://github.com/whitphx/streamlit-webrtc/issues/1213
    """

    # Ref: https://www.twilio.com/docs/stun-turn/api
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        token = client.tokens.create()
    except TwilioRestException as e:
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    return token.ice_servers
# Example usage
#write_to_db("UID123", "Active", "Initial entry")
#write_to_db("UID124", "Inactive", "Test entry")
