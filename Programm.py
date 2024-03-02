import pyodbc
from datetime import datetime, timedelta
import funktionen

# Verbindungsdaten
server = 'sc-db-server.database.windows.net'
database = 'supplychain' # Setze den Namen deiner Datenbank hier ein
username = 'rse'
password = 'Pa$$w0rd'

# Verbindungsstring
conn_str = (
f'DRIVER={{ODBC Driver 18 for SQL Server}};'
f'SERVER={server};'
f'DATABASE={database};'
f'UID={username};'
f'PWD={password}'
)

while True:
    # Verbindung herstellen
    conn = pyodbc.connect(conn_str)
    # Cursor erstellen
    cursor = conn.cursor()
    
    
    # Matrix für die Daten initialisieren
    alle_daten = []
    
    alle_transport_id_liste = []
    
    transport_id_liste=[]
    
    # Abrufen der vorhandenen Transport IDs in der Datenbank
    cursor.execute('SELECT transportid FROM coolchain')
    for row in cursor:
        alle_transport_id_liste.append(row[0])
    
    for id in alle_transport_id_liste:
        if id not in transport_id_liste:
            transport_id_liste.append(id)
    
    # Benutzereingabe für die Auswahl der Transport-ID
    while True:
        eintrag = int(input("Welchen Eintrag wollen sie überprüfen? (1-" + str(len(transport_id_liste)) + ") "))
        if 1 <= eintrag <= len(transport_id_liste):
            transport_id = transport_id_liste[eintrag-1]
            break
        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine Zahl zwischen 1 und", len(transport_id_liste))
    
    # SQL-Abfrage ausführen
    cursor.execute('SELECT * FROM coolchain WHERE transportid = ?', transport_id)
    # Ergebnisse speichern
    for row in cursor:
        alle_daten.append(row)

    # Verbindung schließen
    cursor.close()
    conn.close()
    
    # Überprüfung der Kühlkettenkonsistenz
    konsistenz_ergebnis, konsistenz_fehlermeldung = funktionen.überprüfe_konsistenz(alle_daten)
    # Überprüfung der Zeitdifferenz
    zeitdifferenz_ergebnis, zeitdifferenz_fehlermeldung = funktionen.überprüfe_zeitdifferenz(alle_daten)
    # Überprüfung der Transportdauer
    transportdauer_ergebnis = funktionen.überprüfe_transportdauer(alle_daten)
   
    if konsistenz_ergebnis and zeitdifferenz_ergebnis and transportdauer_ergebnis:
        print("Die ID", transport_id, "ist korrekt.")
    else:
        # Wenn ein Fehler aufgetreten ist, Ausgabe der entsprechenden Fehlermeldungen
        if not konsistenz_ergebnis:
            print(f"Warnung: Die Kühlkette weist Konsistenzfehler auf: {konsistenz_fehlermeldung}")
        if not zeitdifferenz_ergebnis:
            print(f"Warnung: {zeitdifferenz_fehlermeldung}")
        if not transportdauer_ergebnis:
            print("Warnung: Die Transportdauer betrug länger als 48 Stunden.")

        
        
   