import psycopg2


# -----------------------------------
# DB CONNECTION
# -----------------------------------

def get_connection():

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


# -----------------------------------
# GET LATEST TEST VALUE
# -----------------------------------

def get_latest_test(patient_id, test_name):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            test,
            latest_value,
            trend

        FROM patient_lab_summary

        WHERE patient_id = %s
        AND LOWER(test) = LOWER(%s)

    """, (patient_id, test_name))

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:

        return {
            "test": result[0],
            "latest_value": result[1],
            "trend": result[2]
        }

    return None


# -----------------------------------
# GET FULL HISTORY
# -----------------------------------

def get_test_history(patient_id, test_name):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            date,
            value,
            unit

        FROM patient_lab_history

        WHERE patient_id = %s
        AND LOWER(test) = LOWER(%s)

        ORDER BY date ASC

    """, (patient_id, test_name))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    history = []

    for row in rows:

        history.append({
            "date": str(row[0]),
            "value": row[1],
            "unit": row[2]
        })

    return history


# -----------------------------------
# TEST
# -----------------------------------

if __name__ == "__main__":

    latest = get_latest_test(
        "P001",
        "CRP"
    )

    print("\n--- LATEST ---")
    print(latest)

    history = get_test_history(
        "P001",
        "CRP"
    )

    print("\n--- HISTORY ---")

    for h in history:
        print(h)