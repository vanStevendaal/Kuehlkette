import pyodbc
from datetime import datetime, timedelta

# Abfrage welche ID aus der Liste abgefragt werden soll
id = int(input("Welchen Eintrag wollen sie überprüfen (1-20) " )) -1
id_liste= ['72359278599178561029675',
           '15668407856331648336231',
           '73491878556297128760578',
           '99346757838434834886542',
           '46204863139457546291334',
           '77631003455214677542311',
           '34778534098134729847267',
           '64296734612883933474299',
           '84356113249506843372979',
           '23964376768701928340034',
           '55638471099438572108556',
           '84552276793340958450995',
           '96853785349211053482893',
           '68345254400506854834562',
           '67424886737245693583645',
           '85746762813849598680239',
           '56993454245564893300000',
           '95662334024905944384522',
           '13456783852887496020345',
           '76381745965049879836902'
           ]

transport_id = id_liste[id] 

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

# Initialisierung einer Matrix für die Funktionen
alle_daten=[]

# Verbindung herstellen
conn = pyodbc.connect(conn_str)
# Cursor erstellen
cursor = conn.cursor()
# SQL-Statement ausführen
cursor.execute('SELECT * FROM coolchain WHERE transportid = ?', transport_id)
# Ergebnisse ausgeben
for row in cursor:
    alle_daten.append(row)

#---------------------------------------------FUNKTIONEN-----------------------------------------------------------------#

#Funktion zur Überprüfung der Konsistenz = (Folgt In auf Out und Ist der erste Eintrag ein In)
def überprüfe_konsistenz(matrix):
    for i in range(len(matrix) - 1):
        if matrix[i][-2] == "'in'" and matrix[i+1][-2] != "'out'":
            return False, "In folgt nicht auf Out"
        if matrix[i][-2] == matrix[i+1][-2]:
            return False, f"Eintrag {i} und Eintrag {i+1} sind beide '{matrix[i][-2]}'"
        
    if matrix[0][-2] != "'in'":
        return False, "Erster Eintrag ist kein In"
    return True, ""

ergebnis, fehlermeldung = überprüfe_konsistenz(alle_daten)

if ergebnis:
    print("Die Kühlkettenkosistenz weist keine Fehler auf")
else:
    print(f"WARNUNG: Die Kühlkette weist konsistenz fehler auf: {fehlermeldung}")
    
#-------------------------------------------------------------------------------------------------------------------------#
    
#Funktion zur Überprüfung der Zeistempel (Ist die zeitliche Abfolge sinnvoll und wurden die 10 Minuten eingehalten)   
def überprüfe_zeitdifferenz(matrix): 
    for i in range(len(matrix) - 1):
        if matrix[i][-2] == "'in'" and matrix[i+1][-2] == "'out'":
            zeit_in = matrix[i][-1]
            zeit_out = matrix[i+1][-1]
            if zeit_out < zeit_in:
                return False, f"Der Zeitstempel für 'out' ({zeit_out}) ist kleiner als der Zeitstempel für 'in' ({zeit_in})"  
            
        elif matrix[i][-2] == "'out'" and matrix[i+1][-2] == "'in'":
            zeit_out = matrix[i][-1]
            zeit_in = matrix[i+1][-1]
            zeitdifferenz = zeit_in - zeit_out
            if zeitdifferenz > timedelta(minutes=10):
                return False, "Die Zeitdifferenz zwischen 'out' und 'in' beträgt mehr als 10 Minuten."
    return True, ""

ergebnis, fehlermeldung = überprüfe_zeitdifferenz(alle_daten)

if ergebnis:
    print("Die Kühlkette wurde nicht für mehr als 10 Minuten unterbrochen")
else:
    print(f"WARNUNG: {fehlermeldung}")
    
#--------------------------------------------------------------------------------------------------------------------------#

#Funktion zur Überprüfung ob die Transportdauer von 48 Stunden eingehalten worden ist
def überprüfe_transportdauer(matrix):
    erste_zeit = matrix[0][-1]
    letzte_zeit = matrix[-1][-1]
    gesamte_transportdauert = letzte_zeit - erste_zeit
    if gesamte_transportdauert > timedelta(hours=48):
        return False
    return True

if überprüfe_transportdauer(alle_daten):
    print("Die Transportdauert betrug nicht länger als 48 Stunden")
else:
    print("WARNUNG: Die Transportdauert betrug länger als 48 Stunden")

#--------------------------------------------------------------------------------------------------------------------------#

# Verbindung schließen
cursor.close()
conn.close()