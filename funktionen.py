from datetime import timedelta, datetime

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

#Funktion zur Überprüfung ob die Transportdauer von 48 Stunden eingehalten worden ist
def überprüfe_transportdauer(matrix):
    erste_zeit = matrix[0][-1]
    letzte_zeit = matrix[-1][-1]
    gesamte_transportdauert = letzte_zeit - erste_zeit
    if gesamte_transportdauert > timedelta(hours=48):
        return False
    return True