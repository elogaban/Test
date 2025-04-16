import pandas as pd
import streamlit as st
import altair as alt

# URL du dataset
DATA_URL = "https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt"

# Fonction pour charger les données depuis l'URL
@st.cache_data
def load_data(url):
    """
    Charge les données depuis l'URL spécifiée, en gérant les particularités du fichier.

    Args:
        url (str): L'URL du fichier CSV.

    Returns:
        pd.DataFrame: Le DataFrame contenant les données.
    """
    df = pd.read_csv(url, skiprows=2, delim_whitespace=True)
    df = df.dropna()
    df['Year'] = df['Year'].astype(int)
    return df

# Charger les données
df = load_data(DATA_URL)

# Créer le graphique combiné avec Altair
def create_combined_temperature_chart(df):
    """
    Crée un graphique combiné montrant à la fois les données annuelles et la tendance lissée.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        alt.Chart: Le graphique Altair combiné.
    """

    # Graphique pour les données annuelles (points gris)
    annual_mean = alt.Chart(df).mark_circle(color='grey', size=20).encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Année')),  #  <--  CORRECTION ICI : Year:O
        y=alt.Y('No_Smoothing', axis=alt.Axis(title='Anomalie de Température (°C)')),
        tooltip=['Year', 'No_Smoothing']
    )

    # Graphique pour la tendance lissée (ligne noire)
    lowess_smoothing = alt.Chart(df).mark_line(color='black').encode(
        x=alt.X('Year:O'),  #  <--  CORRECTION ICI : Year:O
        y='Lowess(5)',
        tooltip=['Year', 'Lowess(5)']
    )

    # Combiner les deux graphiques
    combined_chart = (annual_mean + lowess_smoothing).properties(
        title='Indice Global de Température Terre-Océan'
    ).interactive()

    return combined_chart

# Afficher dans Streamlit
st.title("INDICE MONDIAL DE TEMPÉRATURE TERRESTRE ET OCÉANIQUE\nSource des données : Institut Goddard d'études spatiales (GISS) de la NASA. Crédit : NASA/GISS")

# Afficher le graphique combiné
combined_temperature_chart = create_combined_temperature_chart(df)
st.altair_chart(combined_temperature_chart, use_container_width=True)

# Ajouter une explication
st.write(
    """
    Ce graphique montre l'évolution de la température de surface mondiale par rapport à la moyenne à long terme de 1951 à 1980. 
    Il combine les données annuelles de l'anomalie de température (points gris) 
    avec une tendance lissée sur 5 ans (ligne noire) pour mieux visualiser les variations à court 
    terme et les tendances à long terme. Globalement, la Terre était environ 1,47 °C plus chaude en 2024 que la moyenne 
    préindustrielle de la fin du XIXe siècle (1850-1900). Les dix années les plus récentes sont les plus chaudes jamais enregistrées. Les données proviennent de la NASA/GISS.
    """
)