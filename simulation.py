import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Application Administrateur", layout="wide")

# Initialisation de la session pour stocker les messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Fonction pour afficher les messages
def display_messages():
    for msg in reversed(st.session_state["messages"]):  # Affiche les messages les plus anciens en haut
        st.markdown(f"**{msg['name']}** ({msg['time']}): {msg['text']}")
        if msg["photo"]:
            st.image(msg["photo"], use_column_width=True)
        st.markdown("---")

# Colonne gauche : zone d'entrée des messages
st.sidebar.header("Zone d'administration")
with st.sidebar.form("new_message_form"):
    name = st.text_input("Nom", placeholder="Votre nom")
    text = st.text_area("Message", placeholder="Tapez votre message ici")
    photo = st.file_uploader("Ajouter une photo (facultatif)", type=["jpg", "png", "jpeg"])
    submit = st.form_submit_button("Publier")
    if submit and text:
        st.session_state["messages"].append({
            "name": name or "Anonyme",
            "text": text,
            "photo": photo,
            "time": datetime.now().strftime("%H:%M")
        })
        st.success("Message publié !")

# Colonne droite : affichage des messages
st.title("Flux de messages")
display_messages()
