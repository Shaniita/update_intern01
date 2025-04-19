import mysql.connector
import schedule
import time
from datetime import datetime
import os

def call_procedure():
        try : 
            connection = mysql.connector.connect(
                  host=os.environ['DB_HOST'],
                  user=os.environ['DB_USER'],
                  password=os.environ['DB_PASSWORD'],
                  database=os.environ['DB_NAME']
            )
            cursor = connection.cursor()
            cursor.execute("CALL updaterestan01(NULL, NULL);")
            connection.commit()
            print(f"[{datetime.now()}] Prosedur berhasil dijalankan.")
        except Exception as e:
            print(f"[{datetime.now()}] ERROR: {e}")
        finally:
             if connection.is.connected():
                cursor.close()
                connection.close()

schedule.every().day.at("01:00").do(call_procedure)

print("Service aktif, menunggu jadwal....")

while True:
     schedule.run_pending()
     time.sleep(60)