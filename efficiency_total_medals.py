import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import squarify

# Daten laden
athlete_events_path = 'athlete_events.csv'
noc_periods_path = 'noc_periods_sorted.csv'

athlete_events = pd.read_csv(athlete_events_path)
noc_periods = pd.read_csv(noc_periods_path)

# Daten vorbereiten
athlete_events['Year'] = athlete_events['Year'].astype(int)

# Medaillenwertung hinzufügen (1 Punkt für Bronze, 2 für Silber, 3 für Gold)
medal_points = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
athlete_events['Medal_Points'] = athlete_events['Medal'].map(medal_points).fillna(0)

# NOC-Codes mit politischen Systemen verknüpfen
def match_period(row):
    periods = noc_periods[(noc_periods['NOC'] == row['NOC']) &
                          (noc_periods['Start_Year'] <= row['Year']) &
                          (noc_periods['End_Year'] >= row['Year'])]
    if len(periods) > 0:
        return periods.iloc[0]['System']
    return 'Unknown'

athlete_events['Political_System'] = athlete_events.apply(match_period, axis=1)

# "Unknown" aus den Daten entfernen
athlete_events = athlete_events[athlete_events['Political_System'] != 'Unknown']

# Medaillenpunkte und Teilnehmer aggregieren
medal_data = athlete_events[~athlete_events['Medal'].isnull()]
participant_counts = athlete_events.groupby(['Political_System', 'Year'])['ID'].nunique().reset_index(name='Participants')
medal_counts = medal_data.groupby(['Political_System', 'Year'])['Medal_Points'].sum().reset_index()

efficiency_data = pd.merge(medal_counts, participant_counts, on=['Political_System', 'Year'])
efficiency_data['Efficiency'] = efficiency_data['Medal_Points'] / efficiency_data['Participants']

# 1. Treemap: Gesamte Medaillenpunkte pro politischem System
fig, ax = plt.subplots(figsize=(10, 6))
squarify.plot(sizes=medal_counts.groupby('Political_System')['Medal_Points'].sum(),
              label=medal_counts['Political_System'].unique(), alpha=0.8, color=sns.color_palette("Set2"))
plt.title('Gesamte Medaillenpunkte nach politischem System', fontsize=14)
plt.axis('off')
plt.savefig('treemap_medaillenpunkte.png')
plt.show()

# 2. Heatmap: Medaillenpunkteverteilung nach System und Jahr
heatmap_data = efficiency_data.pivot_table(index='Year', columns='Political_System', values='Efficiency', fill_value=0)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='coolwarm', linewidths=0.5)
plt.title('Effizienz (Medaillenpunkte pro Teilnehmer) nach politischem System und Jahr', fontsize=14)
plt.xlabel('Politisches System')
plt.ylabel('Jahr')
plt.savefig('heatmap_effizienz.png')
plt.show()

# 3. Bubble Chart: Effizienz pro System und Jahr
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=efficiency_data, x='Year', y='Political_System', size='Efficiency', hue='Political_System',
    sizes=(50, 1000), alpha=0.6, palette='tab10', legend=False
)
plt.title('Effizienz pro politischem System und Jahr', fontsize=14)
plt.xlabel('Jahr')
plt.ylabel('Politisches System')
plt.savefig('bubblechart_effizienz.png')
plt.show()

# Hinweis: Kumulierte Effizienz-Diagramme entfernt, da sie keinen Sinn machen.
