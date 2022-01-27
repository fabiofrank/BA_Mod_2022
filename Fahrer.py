# geschwindigkeitsabhängige Wahl der Beschleunigung
def beschleunigung(v_alt, v_neu, t):
    a = (v_neu - v_alt) / t
    return a  # in m/s²
