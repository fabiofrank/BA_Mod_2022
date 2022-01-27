import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'text.usetex': True,
    'pgf.rcfonts': False,
    'pgf.preamble': [
        #r"\usepackage[latin1]{inputenc}",    # use utf8 fonts
        #r"\usepackage[T1]{fontenc}",        # plots will be generated
        r"\usepackage[detect-all,locale=DE]{siunitx}",
        ]
})

def uhrzeit_soc_array(datei):
    daten_dict = pd.read_excel(datei, sheet_name=None)
    del daten_dict['Übersicht Betriebstag']
    del daten_dict['Parameter']

    liste = []
    soc_array = np.array(liste)
    uhrzeit_array = np.array([])

    for tabellenblatt in daten_dict:
        umlauf_dataframe = daten_dict[tabellenblatt]
        uhrzeit_umlauf = umlauf_dataframe['Uhrzeit']
        uhrzeit_array = np.append(uhrzeit_array, uhrzeit_umlauf)
        uhrzeit_format = mdates.DateFormatter('%H:%M')

        if 'Umlauf' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC zum Zeitpunkt t \n[%]'].to_numpy()
        elif 'Pause' in tabellenblatt:
            soc_umlauf = umlauf_dataframe['SoC [%]'].to_numpy()
        soc_array = np.append(soc_array, soc_umlauf)

    datetimes_liste = []
    for i in range(0, len(uhrzeit_array)):
        datetimes_liste.append(datetime.strptime(uhrzeit_array[i], '%H:%M:%S'))
    datetimes_array = np.array(datetimes_liste)
    return (datetimes_array, soc_array)

################################################################################################################################
fig, ax = plt.subplots(1, 1)

datei1 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\Basisszenario\Basisszenario_Linie24_inklMittagspause.xlsx'
datei2 = r'C:\Users\fabio\PycharmProjects\Bachelorarbeit_Git\Outputdateien\Balingen\Linie 24\HVZ und NVZ\Linie24_HVZ_NVZ.xlsx'

(x1, y1) = uhrzeit_soc_array(datei1)
(x2, y2) = uhrzeit_soc_array(datei2)

plt.plot_date(x1, y1, '-', label='Basis')
plt.plot_date(x2, y2, '-', label='Berücksichtigung der Hauptverkehrszeiten')

ax.axvspan(datetime.strptime('07:18:00', '%H:%M:%S'), datetime.strptime('09:17:50', '%H:%M:%S'), facecolor='0.9')
ax.axvspan(datetime.strptime('11:48:00', '%H:%M:%S'), datetime.strptime('13:47:50', '%H:%M:%S'), facecolor='0.9')
ax.axvspan(datetime.strptime('15:48:00', '%H:%M:%S'), datetime.strptime('17:47:50', '%H:%M:%S'), facecolor='0.9')

ax.text(datetime.strptime('08:30:00', '%H:%M:%S'), 50, 'HVZ', color='0.5', ha='center', va='center')
ax.text(datetime.strptime('12:48:00', '%H:%M:%S'), 50, 'HVZ', color='0.5', ha='center', va='center')
ax.text(datetime.strptime('16:48:00', '%H:%M:%S'), 70, 'HVZ', color='0.5', ha='center', va='center')

fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)
plt.ylim(bottom=0)
#plt.xticks(fontsize=12)
#plt.yticks(fontsize=12)
ax.set_xlabel(r'$Uhrzeit\ \longrightarrow$', color='black')
ax.set_ylabel(r'$SoC$ / % $\longrightarrow$')
plt.legend(borderpad=1.3)
#plt.title(r'$\bf{Linie\ 24\ -\ Basisszenario}$' + '\n10,5 km Umlauf, davon 2,4 km DWPT-unterstützt / 4 DWPT-Receiver / 174-kWh-Batterie (netto) / 15 Fahrgäste / 20 °C Außentemperatur', fontsize=15)
plt.grid()
fig.set_size_inches(7, 4)
fig.savefig(r'C:\Users\fabio\Studium\Bachelorarbeit\BA Latex\Latex_Bachelorarbeit\Bilder\HVZ_NVZ.pgf')
#plt.show()