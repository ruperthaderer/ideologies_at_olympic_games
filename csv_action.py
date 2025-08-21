import pandas as pd

# CSV-Dateien laden
athlete_events_path = 'athlete_events.csv'
noc_regions_path = 'noc_regions.csv'

# Daten laden
athlete_events = pd.read_csv(athlete_events_path)
noc_regions = pd.read_csv(noc_regions_path)

# Verknüpfe NOC-Regionen mit den Olympischen Daten
athlete_events = athlete_events.merge(noc_regions, on='NOC', how='left')


# Perioden extrahieren basierend auf Teilnahme an Olympischen Spielen
def extract_periods_by_participation(df):
    periods = []
    grouped = df.groupby('NOC')
    for noc, group in grouped:
        group = group.sort_values('Year')  # Nach Jahr sortieren
        current_start = group['Year'].iloc[0]
        current_end = group['Year'].iloc[0]

        # Gehe die Jahre der Teilnahme durch und beende die Periode, wenn Lücken gefunden werden
        for i in range(1, len(group)):
            if group['Year'].iloc[i] - current_end > 4:  # Lücke von mehr als einem olympischen Zyklus
                periods.append([noc, group['region'].iloc[0], current_start, current_end])
                current_start = group['Year'].iloc[i]
            current_end = group['Year'].iloc[i]

        # Letzte Periode hinzufügen
        periods.append([noc, group['region'].iloc[0], current_start, current_end])
    return periods


# Perioden berechnen
period_data = extract_periods_by_participation(athlete_events)
period_df = pd.DataFrame(period_data, columns=['NOC', 'Country', 'Start_Year', 'End_Year'])

# Nach Land sortieren
period_df = period_df.sort_values(by=['Country', 'Start_Year']).reset_index(drop=True)

# Ergebnis speichern oder anzeigen
print(period_df)

# Optional: In eine CSV speichern
period_df.to_csv('noc_periods_sorted.csv', index=False)
