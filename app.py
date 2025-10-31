import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

#st.title("Population en BZH",)

# Pour afficher le titre centré !
st.markdown("<h1 style='text-align: center;'>Population en BZH</h1>", unsafe_allow_html=True)

# Image
st.image("Data/images/Belle-ile.jpg")
st.logo("Data/images/Bretagne-logo.png", size = "large")

# Sidebar controls
#st.sidebar.header("Data source")
#uploaded = st.sidebar.file_uploader("Upload a CSV", type=["csv"])
#use_demo = st.sidebar.checkbox("Use demo data", value=not uploaded)

# choix
choix = st.radio("Vous préférez visualiser par :", ["Départements", "Villes"])
#st.selectbox("Pick one", ["cats", "dogs"])
choix_val = 0
valid = st.button("Validez")

if valid:
    choix_val = choix   



#   1
if choix_val == "Départements":
    st.header("1. Par département")

    try:
        pop_dep = pd.read_csv("Data/CSV/population.csv", sep=";")
        st.dataframe(pop_dep)

    except FileNotFoundError:
        st.error("Fichier introuvable. Vérifie le chemin : 'Data/CSV/population.csv'")
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()


    # Créer un diagramme circulaire
    fig, ax = plt.subplots()

#    fig.patch.set_facecolor('#D6D0D0')  # Fond global
    #ax.set_facecolor('#262730')  # Fond derrière le graphique

    colors = plt.cm.Paired(np.arange(len(pop_dep)))
    ax.pie(pop_dep['Population'], labels=pop_dep['Département'], autopct='%1.1f%%', colors =colors)
    st.pyplot(fig)

# 2
elif choix_val == "Villes":

    st.header("2. Par villes")

#     # Charger le fichier GeoJSON 
#     import geopandas as gpd
#     import json

#     url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions/bretagne/departements-bretagne.geojson"
#     gdf = gpd.read_file(url)

# #   Convertir en format utilisable par Altair
#     geojson_data = json.loads(gdf.to_json())

#     # Créer la carte avec Altair
#     import altair as alt
#     import pandas as pd

#     chart = alt.Chart(alt.Data(values=geojson_data['features'])).mark_geoshape(
#         stroke='black'
#     ).encode(
# #        color='properties.ton_champ_de_couleur:N'  # adapte selon ton champ
#     ).properties(
#         width=600,
#         height=400
#     )

#     st.altair_chart(chart)

    

# # Exemple villes bretonnes avec affichage points simples
#     data = pd.DataFrame({
#         'lat': [48.1173, 48.3904, 47.9959],  # Rennes, Brest, Quimper
#         'lon': [-1.6778, -4.4861, -4.1025]
#     })

#     st.title("villes BZH")
#     st.map(data[['lat', 'lon']])



# Avec Pydeck pour une carte avec grosseur des points en fonction de la population
    import pydeck as pdk
    pop_villes = pd.read_csv("Data/CSV/bretagne_communes.csv", sep=",")
    st.dataframe(pop_villes)

    pop_villes["radius"]= pop_villes["pop"] / 10  # Ajuster le facteur de division selon les besoins

    # Créer une carte avec Pydeck
    st.title("Villes en BZH par population")

    # Définir la vue initiale de la carte
    view_state = pdk.ViewState(
        latitude=48.2020,
        longitude=-2.9326,
        zoom=7,
        pitch=0
    )

    # Créer une couche de points
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=pop_villes,
        get_position=["long", "lat"],
        get_fill_color=[200, 30, 0, 160],
        get_radius="pop / 10",  # Ajuster la taille en fonction de la population
#        get_radius="radius",
        pickable=True
    )

    # Créer la carte
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="light", # style
        tooltip={"text": "Ville: {Nom}\nPopulation: {pop}"}
    )

    st.pydeck_chart(r)

    st.write("Source des données : https://france.comersis.com/listes-des-villes-de-bretagne-105.html")

# Logo Python en bas
st.image("https://www.python.org/static/community_logos/python-powered-w-200x80.png", width=150)
