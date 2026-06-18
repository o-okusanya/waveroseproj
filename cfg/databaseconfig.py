import os
import sqlite3
import logging
logger = logging.getLogger(__name__)

def database(self, df):
    db_path = r"C:\Users\ncbof\hypoxia\waveroseproj\dataOutput\wavebuoydata.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS wave_data (
                       epoch                INTEGER,
                       wave_height          REAL,
                       wave_height_qa       TEXT,
                       wave_direction       REAL,
                       wave_direction_qa    TEXT,
                       wave_period          REAL,
                       wave_period_qa       TEXT,
                       station              TEXT,
                       UNIQUE(epoch, station)
                    )
                """)

    for _, row in df.iterrows():
        cursor.execute("""
                       INSERT
                       OR IGNORE INTO wave_data
                VALUES (?,?,?,?,?,?,?,?)
                       """, (
                           row["epoch"],
                           row.get("wave_height"), row.get("wave_height_qa"),
                           row.get("wave_dir"), row.get("wave_direction_qa"),
                           row.get("wave_period"), row.get("wave_period_qa"),
                           self.station
                       ))

    conn.commit()
    conn.close()

    logger.info(f"Saved {len(df)} rows for station {self.station} to the database.")