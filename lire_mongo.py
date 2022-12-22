import streamlit as st
import pymongo

# dans le requirements.txt
# ne pas installer time (ou autre module)
# qui est un module standard à Python

# local run
# streamlit run lire_mongo.py

st.title ("Dashboard pour tester pymongo")

# MongoDB account OK
# Atlas cluster OK
# username, passwork OK
# IP OK
# connection string OK

# Interact with cluster...
# ...with JS GUI 
# ...**connect app with drivers**
# ...connect with Compass

# https://www.mongodb.com/docs/guides/crud/install/
# https://www.mongodb.com/docs/guides/atlas/connection-string/

# pip install pymongo[srv]


st.header("URI, Open Client")

# Replace the uri string with your
# MongoDB deployment's connection string
uri = "mongodb+srv://toucanfortune:4Yiv7jZl6H1knJ0U@toucanfortune.gzo0glz.mongodb.net/?retryWrites=true&writeConcern=majority"
#uri_local = "mongodb://localhost:27017"

st.write("uri: ")
st.write(uri)

client = pymongo.MongoClient(uri)
#client = pymongo.MongoClient(uri_local) 
st.write("open client")


st.header("DBS, Collections")

db = client.toucan_test

st.write("db: ")
st.write(db)

st.write("collections: ")
st.write(db.list_collection_names())

coll = db.test_premier

st.write("collection: ")
st.write(coll)


st.header("CRUD")

st.write("attributes: ")
st.write(dir(coll))

# find code
cursor = coll.find()
# iterate code
liste_account_id = []
st.write("documents (boucle for): ")
for doc in cursor:
    st.write(doc)
    st.write("keys: ")
    st.write(doc.keys())
    st.write("account_id: ")
    st.write(doc["account_id"])
    liste_account_id.append(doc["account_id"])

st.write("liste account_id: ")
st.write(liste_account_id)
st.write("extraction de liste account_id: ")
st.write(liste_account_id[1])
#st.write(type(liste_account_id))

st.write("metrics: ")
st.metric(label="Account ID",
          value=liste_account_id[1],
          delta=None,
          delta_color="normal",
          label_visibility="visible")


cursor = coll.find({"limit": 9000})
st.write("liste de documents avec .find({\"limit\": 9000}: ")
cursor_l = list(cursor)
st.write("extraction de liste: ")
st.write(cursor_l[0])
st.write("extraction de liste, puis extraction de account_id: ")
st.write(cursor_l[0]["account_id"])

st.write("metrics: ")
st.metric(label="Account ID",
          value=cursor_l[0]["account_id"],
          delta=None,
          delta_color="normal",
          label_visibility="visible")


cursor = coll.find({"limit": 9000})
st.write("documents avec .find({\"limit\": 9000}: ")
st.write("dans chaque document, avec la clé .limit")
#for doc in cursor:
    #print(doc)
#    st.write(doc)






st.header("Close Client")

client.close()
st.write("close client")


# https://www.pubnub.com/blog/realtime-mongodb-to-fetch-and-stream-report-data/
# https://www.pubnub.com/docs
# https://www.pubnub.com/docs/sdks/python