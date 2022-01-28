from typing import List

import numpy as np
import pandas as pd
import DWPT

strecke: pd.DataFrame

def strecke_einlesen(csv_datei):
    global strecke
    strecke = pd.read_csv(csv_datei)
    strecke['DWPT'] = [False for t in strecke.index]

def dwpt_abschnitt_hinzufügen(t_start, t_stop):
    global strecke
    dwpt_bool = []
    for t in strecke.index:
        if t >= t_start and t < t_stop:
            dwpt_bool.append(True)
        else:
            dwpt_bool.append(False)
    strecke['DWPT'] = dwpt_bool

# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(zeile):
    steigung_in_prozent = strecke['slope (%)'][zeile]
    return steigung_in_prozent

# Ist DWPT-Marker in Route gesetzt, so wird die feste Ladeleistung von 25 kW zurückgegeben
def dwpt_ladeleistung(zeile, dynamisch_oder_statisch):
    if dynamisch_oder_statisch == 'dynamisch':
         wirkungsgrad = DWPT.wirkungsgrad_dynamisch
    elif dynamisch_oder_statisch == 'statisch':
         wirkungsgrad = DWPT.wirkungsgrad_statisch

    if strecke['DWPT'][zeile] == True:
         ladeleistung = DWPT.anzahl_spulen * DWPT.ladeleistung * wirkungsgrad # Watt
    else:
         ladeleistung = 0.0
    return ladeleistung



