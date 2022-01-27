import datetime
import Betrieb
import Route
import Ausgabe
import time
start = time.time()
#######################################################################################################################
# SCHRITT 1: NAME DER SIMULATION FESTLEGEN
name_simulation = 'Test'

#######################################################################################################################
# SCHRITT 2: FESTE PARAMETER DES SIMULIERTEN FAHRZEUGS FESTLEGEN
# siehe Dateien: 'Fahrzeug', 'Elektromotor', 'Batterie', 'Nebenverbraucher', 'DWPT'

#######################################################################################################################
# SCHRITT 3: CSV MIT STRECKENCHARAKTERISTIK EINLESEN
#               1) GPS-Log im GPX-Format aufzeichnen
#               2) https://www.gpsvisualizer.com/convert_input
#                   - Output format: plain text
#                   - Plain text delimiter: comma
#                   - Add estimated fields: speed, slope(%)

strecke = 'Inputdateien/2022 Balingen/Hinweg.csv'
Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 5: BETRIEBSSTART ANGEBEN (Programm stellt Uhrzeit ein)
uhrzeit_start = '08:00'  # Format hh:mm
Betrieb.uhrzeit = datetime.datetime.strptime(uhrzeit_start, '%H:%M')

#######################################################################################################################
# SCHRITT 6: UMLÄUFE UND LADEPAUSEN ANEINANDERREIHEN
# Befehle:
# Betrieb.umlauf(fahrgaeste, aussentemperatur)
# Betrieb.pause(ende=datetime.datetime.strptime('hh:mm')) mit Angabe, wann der nächste Umlauf beginnt.

# Je nach Fahrplan können die Befehle mit Schleifen aneindergereiht werden.
# Außentemperaturen und Fahrgastzahlen können für jeden Umlauf neu festgelegt werden.

takt = 15
uhrzeit_ende = '17:00'
datetime_start = datetime.datetime.strptime(uhrzeit_start, '%H:%M')
datetime_ende = datetime.datetime.strptime(uhrzeit_ende, '%H:%M')

while Betrieb.uhrzeit < datetime_ende:
    Route.strecke_einlesen('Inputdateien/2022 Balingen/Hinweg.csv')
    Betrieb.umlauf(fahrgaeste=30, aussentemperatur=0)

    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause(ende=datetime_start, aussentemperatur=0)

    Route.strecke_einlesen('Inputdateien/2022 Balingen/Rückweg.csv')
    Betrieb.umlauf(fahrgaeste=30, aussentemperatur=0)

    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause(ende=datetime_start, aussentemperatur=0)

#######################################################################################################################
# FINALER SCHRITT: PROGRAMM AUSFÜHREN
# Die Outputdatei wird unter dem oben angegebenen Namen im Ordner Outputdateien gespeichert
ende1 = time.time()

#######################################################################################################################
# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)
ende2 = time.time()
print('{:5.3f}s'.format(ende1-start))
print('{:5.3f}s'.format(ende2-ende1))
print('{:5.3f}s'.format(ende2-start))