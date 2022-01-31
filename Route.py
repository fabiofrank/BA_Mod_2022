import datetime
from typing import List

import numpy as np
import pandas as pd
import DWPT

strecke: pd.DataFrame

def strecke_einlesen(csv_datei):
    global strecke
    strecke_raw = pd.read_csv(csv_datei)
    uhrzeit_start = datetime.datetime.strptime(strecke_raw['time'][0], '%Y-%m-%d %H:%M:%S')
    uhrzeit_ende = datetime.datetime.strptime(strecke_raw.iloc[-1,:]['time'], '%Y-%m-%d %H:%M:%S')

    # Fehlende Zeilen (Stillstand ergänzen)
    liste = []
    uhrzeit = uhrzeit_start
    while uhrzeit < uhrzeit_ende:
        uhrzeit_str = datetime.datetime.strftime(uhrzeit, '%Y-%m-%d %H:%M:%S')
        if uhrzeit_str in strecke_raw.values:
            df_zeile = strecke_raw[strecke_raw['time'] == uhrzeit_str].iloc[0]
            zeile = {'time': uhrzeit_str, 'speed (km/h)': df_zeile['speed (km/h)'], 'slope (%)': df_zeile['slope (%)'], 'distance (km)': df_zeile['distance (km)']}
            liste.append(zeile)
        else:
            zeile = {'time': uhrzeit_str, 'speed (km/h)': df_zeile['speed (km/h)'], 'slope (%)': df_zeile['slope (%)'],
                     'distance (km)': df_zeile['distance (km)']}
            liste.append(zeile)

        uhrzeit += datetime.timedelta(seconds=1)

    strecke = pd.DataFrame(liste)
    strecke['DWPT'] = [False for t in strecke.index]
    strecke.to_csv('strecke_test.csv')

def dwpt_abschnitt_hinzufügen(t_start, t_stop):
    global strecke
    for t in strecke.index:
        if t >= t_start and t < t_stop:
            strecke.loc[t, 'DWPT'] = True

# Funktion gibt die Steigung in Prozent zurück, die auf einem bestimmten Streckenabschnitt auf der Route vorliegt
def steigung(zeile):
    steigung_in_prozent = strecke['slope (%)'][zeile]
    return steigung_in_prozent

# Ist DWPT-Marker in Route gesetzt, so wird die DWPT-Ladeleistung zurückgegeben
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



