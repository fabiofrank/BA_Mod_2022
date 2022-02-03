import datetime
import pandas as pd
import Fahrer
import Route
import DWPT
import Ausgabe
from Fahrzeugkomponenten import Fahrzeug, Nebenverbraucher, Batterie, Elektromotor

zeit_intervall = 1  # in Sekunden

# Initialisierung: Start des Betriebstags
soc = 100.0  # SoC beträgt bei Start der Simulation 100%
daten_uebersicht = []
daten_umlaeufe = []

# Variablen während des Busbetriebs
t: int
zurueckgelegte_distanz: float
uhrzeit: datetime.datetime
uhrzeit_vor_umlauf: datetime.datetime
soc_vor_umlauf: float
temperatur: float
v_ist: float
v_soll: float
steigung: float
beschleunigung: float
ladeleistung: float
leistung_em: float
leistung_nv: float
leistung_batterie: float
energieverbrauch_im_intervall: float
kumulierter_energieverbrauch: float
liste: list

# Ladepause an Start-/Zielhaltestelle
def ladepause(ende, aussentemperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, liste, ladeleistung, leistung_nv, leistung_batterie, temperatur
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Ladepause gestartet.')
    # Initialisierung
    t = 0
    temperatur = aussentemperatur
    soc_vor_pause = soc
    uhrzeit_vor_pause = uhrzeit
    uhrzeit_nach_pause = datetime.datetime.strptime(ende, '%H:%M')
    liste = []
    kumulierter_energieverbrauch = 0.0  # in Joule
    ladeleistung = DWPT.anzahl_spulen * DWPT.ladeleistung * DWPT.wirkungsgrad_statisch  # in Watt
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    leistung_batterie = Batterie.leistung(leistung_nv - ladeleistung)
    theoretische_energieaufnahme = leistung_batterie * zeit_intervall  # in Joule

    # Sonderfall: Pause kann nicht stattfinden, da vorheriger Umlauf zu lange gebraucht hat
    if uhrzeit > uhrzeit_nach_pause:
        Ausgabe.daten_sichern_pause()
    else:
        # Pause läuft bis zu gegebener Uhrzeit (Beginn der nächsten Fahrt)
        while uhrzeit <= uhrzeit_nach_pause:
            # Der SoC von 100% nicht überschritten werden
            if (Batterie.inhalt * 3600000) - theoretische_energieaufnahme > (Batterie.kapazitaet * 3600000):
                energieaufnahme = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
            elif (Batterie.inhalt * 3600000) - theoretische_energieaufnahme < 0:
                energieaufnahme = 0.0
            else:
                energieaufnahme = theoretische_energieaufnahme

            # Energie wird "verbraucht" bzw. aufgenommen (negativ)
            kumulierter_energieverbrauch += energieaufnahme

            # Abspeichern
            Ausgabe.daten_sichern_pause()

            # Aktualisieren der Größen
            soc = Batterie.state_of_charge(energieaufnahme)
            uhrzeit += datetime.timedelta(seconds=zeit_intervall)
            t += zeit_intervall

    pause_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(pause_tabelle)

    ergebnis_pause = {'Typ': 'Ladepause',
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(uhrzeit, '%H:%M'),
                      'Außentemperatur [°C]': temperatur,
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': soc,
                      'Energieverbrauch des Intervalls [kWh]': kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)

# (Lade-)Pause an Start-/Zielhaltestelle
def pause_ohne_laden(ende, aussentemperatur):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, liste, ladeleistung, leistung_nv, leistung_batterie, temperatur
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Pause ohne Laden gestartet.')
    # Initialisierung
    t = 0
    temperatur = aussentemperatur
    soc_vor_pause = soc
    uhrzeit_vor_pause = uhrzeit
    uhrzeit_nach_pause = datetime.datetime.strptime(ende, '%H:%M')
    liste = []
    kumulierter_energieverbrauch = 0.0  # in Joule
    ladeleistung = 0.0  # in Watt
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    leistung_batterie = Batterie.leistung(leistung_nv - ladeleistung)
    theoretische_energieaufnahme = leistung_batterie * zeit_intervall  # in Joule

    # Sonderfall: Pause kann nicht stattfinden, da vorheriger Umlauf zu lange gebraucht hat
    if uhrzeit > uhrzeit_nach_pause:
        Ausgabe.daten_sichern_pause()
    else:
        # Pause läuft bis zu gegebener Uhrzeit (Beginn der nächsten Fahrt)
        while uhrzeit <= uhrzeit_nach_pause:
            # Der SoC von 100% nicht überschritten werden
            if (Batterie.inhalt * 3600000) - theoretische_energieaufnahme > (Batterie.kapazitaet * 3600000):
                energieaufnahme = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
            elif (Batterie.inhalt * 3600000) - theoretische_energieaufnahme < 0:
                energieaufnahme = 0.0
            else:
                energieaufnahme = theoretische_energieaufnahme

            # Energie wird "verbraucht" bzw. aufgenommen (negativ)
            kumulierter_energieverbrauch += energieaufnahme

            # Abspeichern
            Ausgabe.daten_sichern_pause()

            # Aktualisieren der Größen
            soc = Batterie.state_of_charge(energieaufnahme)
            uhrzeit += datetime.timedelta(seconds=zeit_intervall)
            t += zeit_intervall

    pause_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(pause_tabelle)

    ergebnis_pause = {'Typ': 'Pause ohne Laden',
                      'Uhrzeit zu Beginn': datetime.datetime.strftime(uhrzeit_vor_pause, '%H:%M'),
                      'Uhrzeit am Ende': datetime.datetime.strftime(uhrzeit, '%H:%M'),
                      'Außentemperatur [°C]': temperatur,
                      'SoC zu Beginn [%]': soc_vor_pause,
                      'SoC am Ende [%]': soc,
                      'Energieverbrauch des Intervalls [kWh]': kumulierter_energieverbrauch / 3600000}
    daten_uebersicht.append(ergebnis_pause)


# einzelner Umlauf des Busses
def umlauf(fahrgaeste, aussentemperatur, beschreibung):
    global soc, kumulierter_energieverbrauch, uhrzeit, t, zurueckgelegte_distanz, v_ist, v_soll, steigung, \
        beschleunigung, leistung_batterie, liste, ladeleistung, temperatur, soc_vor_umlauf, uhrzeit_vor_umlauf, haltezeit_ampel
    print(datetime.datetime.strftime(uhrzeit, '%H:%M'), ': Umlauf gestartet.')
    Fahrzeug.anzahl_fahrgaeste = fahrgaeste
    temperatur = aussentemperatur
    soc_vor_umlauf = soc
    uhrzeit_vor_umlauf = uhrzeit
    t_max = Route.strecke.shape[0]

    # Initialisierung der Schleife
    t = 0  # Zeit in s
    v_ist = 0.0  # Ist-Geschwindigkeit in m/s
    zurueckgelegte_distanz = 0.0  # zurückgelegte Strecke in m
    kumulierter_energieverbrauch = 0.0
    liste = []

    # Schleife, die läuft bis Umlauf beendet
    while t < t_max:
        # Geschwindigkeit im aktuellen Intervall
        v_ist = Route.strecke.loc[t, 'speed (km/h)'] / 3.6

        # Geschwindigkeit im folgenden Intervall
        if t == t_max - 1:
            v_neu = v_ist
        else:
            v_neu = Route.strecke.loc[t + 1, 'speed (km/h)'] / 3.6

        zurueckgelegte_distanz = Route.strecke.loc[t, 'distance (km)'] * 1000
        steigung = Route.steigung(t)
        beschleunigung = Fahrer.beschleunigung(v_ist, v_neu, zeit_intervall)

        # Berechnung des Energieverbrauchs
        energieverbrauch_im_intervall = energieverbrauch()

        # Aktualisieren des Gesamtenergieverbrauchs im Umlauf
        kumulierter_energieverbrauch += energieverbrauch_im_intervall

        # Gesammelte Daten abspeichern (wichtig: vor dem Aktualisieren des SoC)
        Ausgabe.daten_sichern()

        # Laden bzw. Entladen der Batterie, Berechnung des neuen SoC
        soc = Batterie.state_of_charge(energieverbrauch_im_intervall)

        # Nächste Iteration
        uhrzeit += datetime.timedelta(seconds=zeit_intervall)
        t += zeit_intervall

    # Tabelle mit allen relevanten Daten des Umlaufs wird erstellt und zurückgegeben
    umlauf_tabelle = pd.DataFrame(liste)
    daten_umlaeufe.append(umlauf_tabelle)
    Ausgabe.daten_sichern_uebersicht(beschreibung)


# Berechnung des Energieverbrauchs bei geg. Parametern Ist-Geschwindigkeit, Beschleunigung,
# Steigung, Außentemperatur, zurückgelegte Distanz
def energieverbrauch():
    global leistung_batterie, ladeleistung, leistung_em, leistung_nv

    # Ermittlung des Gesamtleistungsbedarfs
    fahrwiderstaende = Fahrzeug.fahrwiderstaende(v_ist, beschleunigung, steigung)
    leistung_em = Elektromotor.leistung(fahrwiderstaende, v_ist)
    leistung_nv = Nebenverbraucher.leistung(temperatur)
    ladeleistung = Route.dwpt_ladeleistung(t, 'dynamisch')
    benoetigte_leistung = leistung_em + leistung_nv - ladeleistung

    leistung_batterie = Batterie.leistung(benoetigte_leistung)

    # Berechnung des Energieverbrauchs während des gewählten Zeitintervalls
    theoretischer_energieverbrauch_im_intervall = leistung_batterie * zeit_intervall

    # Sonderfall: Im Falle von Energieaufnahme darf der SoC von 100% nicht überschritten werden
    if (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall > (Batterie.kapazitaet * 3600000):
        realer_energieverbrauch_im_intervall = (Batterie.inhalt - Batterie.kapazitaet) * 3600000
    elif (Batterie.inhalt * 3600000) - theoretischer_energieverbrauch_im_intervall < 0:
        realer_energieverbrauch_im_intervall = 0.0
    else:
        realer_energieverbrauch_im_intervall = theoretischer_energieverbrauch_im_intervall

    return realer_energieverbrauch_im_intervall  # in Joule



