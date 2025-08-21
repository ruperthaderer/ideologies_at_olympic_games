import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import squarify
from math import pi
import numpy as np

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

# Medaillenpunkte nach politischem System aggregieren
medal_data = athlete_events[~athlete_events['Medal'].isnull()]
medal_counts = medal_data.groupby(['Political_System', 'Year'])['Medal_Points'].sum().reset_index()
medal_totals = medal_counts.groupby('Political_System')['Medal_Points'].sum().reset_index()

# Teilnehmeranzahl pro politischem System berechnen
participant_counts = athlete_events.groupby('Political_System').size().reset_index(name='Participants')

# Effizienz berechnen (Medaillenpunkte pro Teilnehmer)
efficiency_data = medal_totals.merge(participant_counts, on='Political_System')
efficiency_data['Efficiency'] = efficiency_data['Medal_Points'] / efficiency_data['Participants']

# "Unknown" entfernen
efficiency_data = efficiency_data[efficiency_data['Political_System'] != 'Unknown']

# Einheitliches Farbschema definieren
ideology_colors = {
    'Capitalism': 'blue',
    'Communism': 'red',
    'Fascism': 'brown',
    'Monarchism': 'purple',
    'Theocracy': 'green'
}

participant_counts = athlete_events.groupby(['Political_System', 'Year']).size().reset_index(name='Participants')

# Effizienz pro Jahr und politischem System berechnen
efficiency_by_year = medal_counts.merge(participant_counts, on=['Political_System', 'Year'])
efficiency_by_year = efficiency_by_year[efficiency_by_year['Political_System'] != 'Unknown']
efficiency_by_year['Efficiency'] = efficiency_by_year['Medal_Points'] / efficiency_by_year['Participants']

# 1. Streamgraph (ungestackt, separate Linien)
fig, ax = plt.subplots(figsize=(12, 6))
for system, color in ideology_colors.items():
    if system in efficiency_by_year['Political_System'].unique():
        system_data = efficiency_by_year[efficiency_by_year['Political_System'] == system]
        ax.plot(system_data['Year'], system_data['Efficiency'], label=system, color=color, linewidth=2)
plt.title('Effizienz (Medaillenpunkte pro Teilnehmer) nach politischem System', fontsize=14, fontweight='bold')
plt.xlabel('Jahr')
plt.ylabel('Effizienz')
plt.legend(title='Politisches System', bbox_to_anchor=(1.05, 1), loc='upper right')
plt.tight_layout()
plt.savefig('streamgraph_efficiency_unstacked.png', bbox_inches='tight')
plt.show()

# 2. Circular Barplot
circular_data = efficiency_data.copy()
circular_data['Angle'] = np.linspace(0, 2 * np.pi, len(circular_data), endpoint=False)
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
for i, row in circular_data.iterrows():
    ax.bar(row['Angle'], row['Efficiency'], color=ideology_colors[row['Political_System']], width=0.4, edgecolor='black', alpha=0.7)
ax.set_xticks(circular_data['Angle'])
ax.set_xticklabels(circular_data['Political_System'], fontsize=12)
plt.title('Circular Barplot: Durchschnittliche Effizienz nach politischem System', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('circular_barplot_efficiency.png', bbox_inches='tight')
plt.show()

# Filter 'Unknown' aus medal_totals
medal_totals = medal_totals[medal_totals['Political_System'] != 'Unknown']

# Treemap: Gesamte Medaillenpunkte pro politischem System
fig, ax = plt.subplots(figsize=(10, 6))

# Farbliste basierend auf gefilterten Political_System
treemap_colors = [ideology_colors[system] for system in medal_totals['Political_System']]

squarify.plot(sizes=medal_totals['Medal_Points'], label=medal_totals['Political_System'], alpha=0.8, color=treemap_colors)
plt.title('Gesamte Medaillenpunkte nach politischem System', fontsize=14)
plt.axis('off')
plt.savefig('treemap_medaillenpunkte.png')
plt.show()



# Tabelle erstellen: Teilnehmeranzahl, Medaillenpunkte und Effizienz pro Ideologie
table_data = efficiency_data[['Political_System', 'Participants', 'Medal_Points', 'Efficiency']]

# "Unknown" herausfiltern
table_data = table_data[table_data['Political_System'] != 'Unknown']

# Tabelle als CSV speichern
table_data.to_csv('efficiency_table.csv', index=False)

# Tabelle als Excel speichern
table_data.to_excel('efficiency_table.xlsx', index=False)

# Optional: Tabelle anzeigen
print(table_data)

# Violinplot: Effizienzverteilung pro politischem System
plt.figure(figsize=(10, 6))
sns.violinplot(data=efficiency_by_year, x="Political_System", y="Efficiency", palette=ideology_colors)

plt.title("Violinplot: Effizienzverteilung nach politischem System", fontsize=14)
plt.xlabel("Politisches System")
plt.ylabel("Effizienz (Medaillenpunkte pro Teilnehmer)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("violinplot_effizienz.png", bbox_inches='tight')
plt.show()




