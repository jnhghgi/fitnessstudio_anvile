import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3


@anvil.server.callable
def get_buchungs_liste():
  conn = sqlite3.connect('Birnbaumer_Luis_fitnessstudio.db')
  cursor = conn.cursor()

  query = '''
    SELECT 
    k.bezeichnung AS bezeichnung, 
    k.termin AS termin,
    t.name AS name,
    k.maxTeilnehmer AS maxTeilnehmer,
    COUNT(b.mitgliedID) AS aktuelleTeilnehmer
    FROM kurse k
    JOIN Trainer t ON k.trainerID = t.trainerID
    LEFT JOIN Bucht b ON k.kursID = b.kursID
    GROUP BY k.kursID
    '''
  cursor.execute(query)
  rows = cursor.fetchall()

  ergebnis = []
  for row in rows:
    belegungs_string = f"{row['aktuelle_anzahl']} / {row['maxTeilnehmer']}"
    ergebnis.append({
      'kurs': row['bezeichnung'],
      'name': row['name'],
      'termin':row['termin'],
      'belegung': belegungs_string,
    })
  return ergebnis





@anvil.server.callable
def get_mitglieder(kurs):
  conn = sqlite3.connect('Birnbaumer_Luis_fitnessstudio.db')
  cursor = conn.cursor()

  query = '''
SELECT 
    k.bezeichnung AS bezeichnung, 
    k.termin AS termin,
    t.name AS name,
    k.maxTeilnehmer AS maxTeilnehmer,
    COUNT(b.mitgliedID) AS aktuelleTeilnehmer
FROM kurse k
JOIN Trainer t ON k.trainerID = t.trainerID
LEFT JOIN Bucht b ON k.kursID = b.kursID
Where 
    '''
  cursor.execute(query)
  rows = cursor.fetchall()

  ergebnis = []
  for row in rows:
    belegungs_string = f"{row['aktuelle_anzahl']} / {row['maxTeilnehmer']}"
    ergebnis.append({
      'kurs': row['bezeichnung'],
      'name': row['name'],
      'termin':row['termin'],
      'belegung': belegungs_string,
    })
  return ergebnis



