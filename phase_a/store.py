import psycopg2
import time

# -----------------------------
# DB CONNECTION
# -----------------------------
def wait_for_db():

    while True:

        try:

            conn = psycopg2.connect(
                dbname="healthcare_demo",
                user="postgres",
                password="postgres",
                host="postgres-db",
                port="5432"
            )

            conn.close()

            print("✅ Database ready")

            break

        except Exception:

            print("⏳ Waiting for database...")

            time.sleep(5)

def get_connection():
    wait_for_db()

    conn = psycopg2.connect(
        dbname="healthcare_demo",
        user="postgres",
        password="postgres",
        host="postgres-db",
        port="5432"
    )

    return conn

    ''' change to above for docker 
    def get_connection():

    conn = psycopg2.connect(
        dbname="healthcare_demo",
        user="anusmacbook",
        host="localhost",
        port="5432"
    )

    return conn
'''


# -----------------------------
# STORE FACTS
# -----------------------------
def store_facts(facts):

    conn = get_connection()
    cur = conn.cursor()

    for fact in facts:

        cur.execute("""
            INSERT INTO patient_lab_history
            (patient_id, test, date, value, unit)
            VALUES (%s, %s, %s, %s, %s)

            ON CONFLICT (patient_id, test, date)
            DO NOTHING
        """, (
            fact["patient_id"],
            fact["test"],
            fact["date"],
            fact["value"],
            fact["unit"]
        ))

    conn.commit()

    cur.close()
    conn.close()

    print(f"✅ Stored {len(facts)} facts")


# -----------------------------
# STORE SUMMARIES
# -----------------------------
def store_summaries(summaries):

    conn = get_connection()
    cur = conn.cursor()

    for summary in summaries:

        cur.execute("""
            INSERT INTO patient_lab_summary
            (
                patient_id,
                test,
                latest_value,
                trend,
                min_value,
                max_value
            )

            VALUES (%s, %s, %s, %s, %s, %s)

            ON CONFLICT (patient_id, test)

            DO UPDATE SET
                latest_value = EXCLUDED.latest_value,
                trend = EXCLUDED.trend,
                min_value = EXCLUDED.min_value,
                max_value = EXCLUDED.max_value
        """, (
            summary["patient_id"],
            summary["test"],
            summary["latest_value"],
            summary["trend"],
            summary["min_value"],
            summary["max_value"]
        ))

    conn.commit()

    cur.close()
    conn.close()

    print(f"✅ Stored {len(summaries)} summaries")


# -----------------------------
# STORE EMBEDDED CHUNKS
# -----------------------------
def store_chunks(chunks):

    conn = get_connection()
    cur = conn.cursor()

    for chunk in chunks:

        cur.execute("""
            INSERT INTO patient_chunks
            (
                patient_id,
                chunk_type,
                content,
                embedding
            )

            VALUES (%s, %s, %s, %s)
        """, (
            chunk["patient_id"],
            chunk["chunk_type"],
            chunk["content"],
            chunk["embedding"]
        ))

    conn.commit()

    cur.close()
    conn.close()

    print(f"✅ Stored {len(chunks)} embedded chunks")