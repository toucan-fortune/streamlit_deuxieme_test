import streamlit as st
import pymongo
import numpy as np
import pandas as pd
import time
import random
import plotly.express as px

# dans le requirements.txt
# ne pas installer time (ou autre module)
# qui est un module standard à Python

# local run
# streamlit run lire_mongo.py

##################################################
st.title ("Tableau pour lire pymongo")

st.header("URI, Open Client")

# Exécuter 1 seule fois...
# https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
# https://docs.streamlit.io/library/api-reference/performance/st.experimental_singleton
# https://docs.streamlit.io/library/api-reference/performance/st.experimental_singleton.clear
@st.experimental_singleton
def init_connection():
    # Chercher les données dans le fichier secrets.toml
    URI = "mongodb+srv://st.secrets['db_username']:st.secrets['db_pw']@toucanfortune.gzo0glz.mongodb.net/?retryWrites=true&writeConcern=majority"
    return pymongo.MongoClient(URI)

client = init_connection()

db = client.toucan
#st.write(db)

#coll = db.test_premier
#st.write(coll)

#items = db.test_premier.find()
#st.write(items)
#liste_items = list(items)

#for item in items:
#    st.write(item)

# 1 sort ascending, oldest to newest
items = db.messages.find().sort("heure", 1).limit(1)
liste_items = list(items)

for item in liste_items:
    st.write(item)

# -1 sort descending, newest to oldest
items = db.messages.find().sort("heure", -1).limit(1)
liste_items = list(items)

for item in liste_items:
    st.write(item)

st.write("---")


# Importer les données de la collection
# https://docs.streamlit.io/library/api-reference/performance/st.experimental_memo
@st.experimental_memo
def get_data():
    db = client.toucan
    items = db.messages.find()
    liste_items = list(items)
    return liste_items

liste_items = get_data()

st.write(liste_items[0:2])

#for item in items:
#    st.write(item['valeur'])

st.write("---")


df = pd.DataFrame(liste_items)
st.write(df)

st.write("---")


# ttl: la mémorisation est gardée en mémoire un certain temps (secondes)
# Persistent memo caches
# Durant ce temps, la même requête ne donne rien, car la fonction
# a mémorisé le résultat
# Après ce temps, la même requête donne une nouvelle exécution
@st.experimental_memo(ttl=3)
def load_data(rows):
    chart_data = pd.DataFrame(
        np.random.randn(rows, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )
    # Contains a static element st.area_chart
    st.line_chart(chart_data) # This will be recorded and displayed even when the function is skipped
    return chart_data

df = load_data(20)

st.dataframe(df)

st.write("---")

# https://towardsdatascience.com/creating-dynamic-dashboards-with-streamlit-747b98a68ab5
placeholder = st.empty()
start_button = st.empty()


def radar_chart():  
    df = pd.DataFrame(dict(r=[random.randint(0,22),
                              random.randint(0,22),
                              random.randint(0,22),
                              random.randint(0,22),
                              random.randint(0,22)],
                           theta=['processing cost',
                                  'mechanical properties',
                                  'chemical stability',
                                  'thermal stability',
                                  'device integration']))
    
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    placeholder.write(fig)

# Affiche le bouton et si le bouton est pressé
if start_button.button('Start', key='start'):
    # Cache le bouton
    start_button.empty()
    # Affiche le bouton et...
    if st.button('Stop', key='stop'):
        pass
    # ...exécute la boucle tant que le bouton n'est pas pressé
    while True:
        # Exécute la fonction à intervalles
        radar_chart()
        time.sleep(0.5)

# bouton start, end
# bouton fetch
# sélection de périodes de temps
# sélection du temps pour le sleep
# sélection graphique: line, bar

st.write("---")



st.write("---")

# show dbs
# use database
# show collections
# show users
# show roles
# client.close()
# db.collection.count()
# db.collection.findOne()
# db.collection.find(). prettyPrint()
# db.collection.find({"field": "value"})
# db.collection.find({"field": "value"}).count()
# db.collection.find({"student_id": 151, "class_id": 339})
# db.collection.find({"pop": {$lt: 1000}})
# $lt, $lte, $gt, $gte, $ne, $eq, $in, $nin
# $or, $and, $not, $nor
# $exists, $type, $regex
# $expr, look at the value of that field rather than the field name
# $all, $size, $in, $elemMatch
# projections

# json to dataframe
