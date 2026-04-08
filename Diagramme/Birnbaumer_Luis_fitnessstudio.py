import sqlite3
from datetime import datetime


def setup_and_fill_database():
    connection = sqlite3.connect('Birnbaumer_Luis_fitnessstudio.db')
    cursor = connection.cursor()

    # Fremdschlüssel aktivieren
    cursor.execute("PRAGMA foreign_keys = ON;")

    # --- Tabellen erstellen ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mitglied (
            mitgliedID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            email VARCHAR(30),
            beitrittsDatum DATETIME
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Trainer (
            trainerID INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30) NOT NULL,
            spezialgebiet VARCHAR(30)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kurse (
            kursID INTEGER PRIMARY KEY AUTOINCREMENT,
            termin DATETIME,
            maxTeilnehmer INTEGER,
            bezeichnung VARCHAR(30),
            trainerID INTEGER,
            FOREIGN KEY (trainerID) REFERENCES Trainer(trainerID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bucht (
            buchungsID INTEGER PRIMARY KEY AUTOINCREMENT,
            mitgliedID INTEGER,
            kursID INTEGER,
            anmeldeDatum DATETIME,
            FOREIGN KEY (mitgliedID) REFERENCES mitglied(mitgliedID),
            FOREIGN KEY (kursID) REFERENCES kurse(kursID)
        )
    ''')

    # --- Beispieldaten einfügen ---

    # 1. Trainer hinzufügen
    trainer_data = [
        ('Sven Schmidt', 'Yoga & Entspannung'),
        ('Maria Müller', 'Cardio & Spinning'),
        ('Lukas Weber', 'Krafttraining & Pilates'),
        ('Elena Fischer', 'Tanz & Zumba')
    ]
    cursor.executemany('INSERT INTO Trainer (name, spezialgebiet) VALUES (?, ?)', trainer_data)

    # 2. Kurse hinzufügen (IDs sind 1, 2, 3, 4)
    kurse_data = [
        ('2024-06-01 10:00:00', 15, 'Yoga Flow', 1),
        ('2024-06-01 18:00:00', 20, 'Spinning Intense', 2),
        ('2024-06-02 09:00:00', 12, 'Pilates Core', 3),
        ('2024-06-02 17:00:00', 25, 'Zumba Party', 4)
    ]
    cursor.executemany('INSERT INTO kurse (termin, maxTeilnehmer, bezeichnung, trainerID) VALUES (?, ?, ?, ?)',
                       kurse_data)

    # 3. Mitglieder hinzufügen
    mitglieder_data = [
        ('Max Mustermann', 'max@web.de', '2023-01-15'),
        ('Erika Musterfrau', 'erika@gmx.de', '2023-03-10'),
        ('Kevin Kraft', 'kevin@fit.de', '2024-01-05')
    ]
    cursor.executemany('INSERT INTO mitglied (name, email, beitrittsDatum) VALUES (?, ?, ?)', mitglieder_data)

    # 4. Buchungen (Mitglieder melden sich für Kurse an)
    buchungen_data = [
        (1, 1, '2024-05-20'),  # Max bucht Yoga
        (1, 2, '2024-05-21'),  # Max bucht Spinning
        (2, 4, '2024-05-22'),  # Erika bucht Zumba
        (3, 3, '2024-05-23')  # Kevin bucht Pilates
    ]
    cursor.executemany('INSERT INTO Bucht (mitgliedID, kursID, anmeldeDatum) VALUES (?, ?, ?)', buchungen_data)

    connection.commit()
    print("Datenbank wurde erfolgreich erstellt und mit Beispieldaten gefüllt.")

    # Kleiner Test-Join, um zu sehen ob es klappt:
    print("\nAktuelle Buchungen:")
    cursor.execute('''
        SELECT m.name, k.bezeichnung, t.name 
        FROM Bucht b
        JOIN mitglied m ON b.mitgliedID = m.mitgliedID
        JOIN kurse k ON b.kursID = k.kursID
        JOIN Trainer t ON k.trainerID = t.trainerID
    ''')
    for row in cursor.fetchall():
        print(f"Mitglied {row[0]} besucht {row[1]} bei Trainer {row[2]}")

    connection.close()


if __name__ == "__main__":
    setup_and_fill_database()