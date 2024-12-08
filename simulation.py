import streamlit as st
import pandas as pd
import time

# Initialiser les messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "paused" not in st.session_state:
    st.session_state["paused"] = False

# Fonction pour charger les messages
@st.cache_data
def load_messages(file_path):
    return pd.read_csv(file_path)

# Afficher le flux de messages
def display_messages():
    for message in sorted(st.session_state["messages"], key=lambda x: x["timestamp"]):
        st.write(f"**{message['name']}** ({message['timestamp']} minutes après le début):")
        st.write(message["text"])
        if message["photo"]:
            st.image(message["photo"], width=300)
        for response in message["responses"]:
            st.write(f"↳ **{response['name']}**: {response['text']}")
        st.divider()

# Ajouter un nouveau message au flux
def add_message(name, text, photo, timestamp, responses):
    st.session_state["messages"].append({
        "name": name,
        "text": text,
        "photo": photo,
        "timestamp": timestamp,
        "responses": responses
    })

# Charger les données du fichier CSV
file_path = "https://drive.google.com/uc?id=1ddjTlbN8rBYY5jbsLx1Ph40kmZNV8irr&export=download"
data = load_messages(file_path)

# Interface administrateur
st.sidebar.title("Administration")
password = st.sidebar.text_input("Mot de passe", type="password")

if password == "admin123":  # Mot de passe administrateur
    if st.sidebar.button("Start"):
        st.session_state["start_time"] = time.time()
        st.session_state["paused"] = False
    if st.sidebar.button("Pause"):
        st.session_state["paused"] = True
    if st.sidebar.button("Stop"):
        st.session_state["start_time"] = None
        st.session_state["messages"] = []
        st.session_state["paused"] = False

    # Lecture et ajout de messages basés sur le timing
    if st.session_state["start_time"] and not st.session_state["paused"]:
        elapsed_minutes = (time.time() - st.session_state["start_time"]) / 60
        for _, row in data.iterrows():
            if row["Timing (minutes)"] <= elapsed_minutes and not any(m["text"] == row["Texte"] for m in st.session_state["messages"]):
                responses = []
                if pd.notna(row["Reponses"]):
                    responses.append({"name": row["Nom Réponse"], "text": row["Reponses"]})
                add_message(row["Nom"], row["Texte"], row["Photo URL"], row["Timing (minutes)"], responses)

    # Afficher les messages dans le flux
    st.title("Flux de messages")
    display_messages()
else:
    st.sidebar.error("Accès refusé. Veuillez entrer le mot de passe correct.")
