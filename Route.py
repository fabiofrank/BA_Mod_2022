import numpy as np
import pandas as pd
import DWPT

strecke: pd.DataFrame

def strecke_einlesen(csv_datei):
    global strecke
    strecke = pd.read_csv(csv_datei)

# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(zeile):
    steigung_in_prozent = strecke['slope (%)'][zeile]
    return steigung_in_prozent

# Ist DWPT-Marker in Route gesetzt, so wird die feste Ladeleistung von 25 kW zurückgegeben
def dwpt_ladeleistung(distanz_in_m, dynamisch_oder_statisch):
    # if dynamisch_oder_statisch == 'dynamisch':
    #     wirkungsgrad = DWPT.wirkungsgrad_dynamisch
    # elif dynamisch_oder_statisch == 'statisch':
    #     wirkungsgrad = DWPT. wirkungsgrad_statisch
    #
    # zeile = momentane_position_strecke(distanz_in_m)
    # if strecke['DWPT-Abschnitt?'][zeile] == 1:
    #     ladeleistung = DWPT.anzahl_spulen * DWPT.ladeleistung * wirkungsgrad # Watt
    # else:
    #     ladeleistung = 0.0
    ladeleistung = 0.0
    return ladeleistung



