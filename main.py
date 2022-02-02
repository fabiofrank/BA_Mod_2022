import datetime
import Betrieb
import Route
import Ausgabe
import time
start = time.time()
#######################################################################################################################
# SCHRITT 1: NAME DER SIMULATION FESTLEGEN
name_simulation = 'GoodCase_Süd'

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

# strecke = 'Inputdateien/2022 Balingen/Hinweg.csv'
# Route.strecke_einlesen(strecke)

#######################################################################################################################
# SCHRITT 4: DWPT-ABSCHNITTE HINZUFÜGEN
# Jeder Abschnitt wird durch das Zeitintervall definiert, in welchem der Bus die elektrifizierte Strecke passiert
# Route.dwpt_abschnitt_hinzufügen(t_start, t_stop)
# Route.dwpt_abschnitt_hinzufügen(t_start, t_stop)

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
uhrzeit_ende = '20:00'
datetime_start = datetime.datetime.strptime(uhrzeit_start, '%H:%M')
datetime_ende = datetime.datetime.strptime(uhrzeit_ende, '%H:%M')
anzahl_fahrgaeste = 20
temperatur = 20
ladezeit = 8

while Betrieb.uhrzeit < datetime_ende:
    Route.strecke_einlesen('Inputdateien/2022 Balingen/Hinweg.csv')
    Route.dwpt_abschnitt_hinzufügen(t_start=104, t_stop=144) # DWPT-Abschnitt Süd
    #Route.dwpt_abschnitt_hinzufügen(t_start=144, t_stop=161) # DWPT-Abschnitt Mitte
    #Route.dwpt_abschnitt_hinzufügen(t_start=217, t_stop=280) # DWPT-Abschnitt Nord
    Betrieb.umlauf(fahrgaeste=anzahl_fahrgaeste, aussentemperatur=temperatur, beschreibung='Hinweg Messe-Stadthalle')

    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause_ohne_laden(ende=datetime_start - datetime.timedelta(minutes=ladezeit), aussentemperatur=temperatur)
    Betrieb.ladepause(ende=datetime_start, aussentemperatur=temperatur)

    Route.strecke_einlesen('Inputdateien/2022 Balingen/Rückweg.csv')
    #Route.dwpt_abschnitt_hinzufügen(t_start=95, t_stop=142) # Nord
    #Route.dwpt_abschnitt_hinzufügen(t_start=202, t_stop=213) # Mitte
    Route.dwpt_abschnitt_hinzufügen(t_start=213, t_stop=245) # Süd
    Betrieb.umlauf(fahrgaeste=anzahl_fahrgaeste, aussentemperatur=temperatur, beschreibung='Rückweg Stadthalle-Messe')

    datetime_start += datetime.timedelta(minutes=takt)
    Betrieb.pause_ohne_laden(ende=datetime_start - datetime.timedelta(minutes=ladezeit), aussentemperatur=temperatur)
    Betrieb.ladepause(ende=datetime_start, aussentemperatur=temperatur)

#Betrieb.ladepause(ende=datetime.datetime.strptime('1900-01-02 01:00:00', '%Y-%m-%d %H:%M:%S'), aussentemperatur=temperatur)
#######################################################################################################################
# FINALER SCHRITT: PROGRAMM AUSFÜHREN
# Die Outputdatei wird unter dem oben angegebenen Namen im Ordner Outputdateien gespeichert
ende1 = time.time()

#######################################################################################################################
# Output als formatierte Tabelle in Excel-Dokument
Ausgabe.formatierung(name_simulation, Betrieb.daten_uebersicht, Betrieb.daten_umlaeufe)
ende2 = time.time()
print('Rechenzeit: {:5.3f}s'.format(ende1-start))
print('Erstellen der Outputdatei: {:5.3f}s'.format(ende2-ende1))
print('Total: {:5.3f}s'.format(ende2-start))