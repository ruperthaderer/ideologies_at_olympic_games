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

# NOC-Codes mit politischen Systemen verknüpfen
def match_period(row):
    periods = noc_periods[(noc_periods['NOC'] == row['NOC']) &
                          (noc_periods['Start_Year'] <= row['Year']) &
                          (noc_periods['End_Year'] >= row['Year'])]
    if len(periods) > 0:
        return periods.iloc[0]['System']
    return 'Unknown'

athlete_events['Political_System'] = athlete_events.apply(match_period, axis=1)

# Medaillen nach politischem System aggregieren
medal_data = athlete_events[~athlete_events['Medal'].isnull()]
medal_counts = medal_data.groupby(['Political_System', 'Year'])['Medal'].count().reset_index()
medal_totals = medal_counts.groupby('Political_System')['Medal'].sum().reset_index()

# 1. Treemap: Gesamte Medaillenanzahl pro politischem System
fig, ax = plt.subplots(figsize=(10, 6))
squarify.plot(sizes=medal_totals['Medal'], label=medal_totals['Political_System'], alpha=0.8)
plt.title('Gesamte Medaillenanzahl nach politischem System', fontsize=14)
plt.axis('off')
plt.savefig('treemap_medaillen.png')
plt.show()

# 2. Heatmap: Medaillenverteilung nach System und Jahr
heatmap_data = medal_counts.pivot_table(index='Year', columns='Political_System', values='Medal', fill_value=0)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='coolwarm', linewidths=0.5)
plt.title('Medaillenverteilung nach politischem System und Jahr', fontsize=14)
plt.xlabel('Politisches System')
plt.ylabel('Jahr')
plt.savefig('heatmap_medaillen.png')
plt.show()

# 3. Bubble Chart: Medaillenanzahl pro System und Jahr
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=medal_counts, x='Year', y='Political_System', size='Medal', hue='Political_System',
    sizes=(50, 1000), alpha=0.6, palette='tab10', legend=False
)
plt.title('Medaillenanzahl pro politischem System und Jahr', fontsize=14)
plt.xlabel('Jahr')
plt.ylabel('Politisches System')
plt.savefig('bubblechart_medaillen.png')
plt.show()

# 4. Kumulative Medaillenanzahl pro politischem System (Stacked Area Plot)
medal_counts['Cumulative_Medals'] = medal_counts.groupby('Political_System')['Medal'].cumsum()
cumulative_data = medal_counts.pivot_table(index='Year', columns='Political_System', values='Cumulative_Medals', fill_value=0)
cumulative_data.plot.area(figsize=(12, 6), alpha=0.7, colormap='viridis')
plt.title('Kumulative Medaillenanzahl nach politischem System', fontsize=14)
plt.xlabel('Jahr')
plt.ylabel('Kumulative Medaillenanzahl')
plt.legend(title='Politisches System')
plt.savefig('stackedarea_medaillen.png')
plt.show()

# Hinweis: Passen Sie die Dateipfade und Spaltennamen an, falls erforderlich.
