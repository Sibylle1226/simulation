import streamlit as st
import datetime

# Simuler des données (stockées dans session_state)
if "posts" not in st.session_state:
    st.session_state["posts"] = []

def add_post(author, content, reply_to=None):
    """Ajoute un nouveau post ou une réponse à un post existant."""
    timestamp = datetime.datetime.now().strftime("%H:%M")  # Heure uniquement
    post = {
        "author": author,
        "content": content,
        "likes": 0,
        "replies": [],
        "timestamp": timestamp
    }
    if reply_to is not None:
        # Ajoute la réponse au post correspondant
        st.session_state["posts"][reply_to]["replies"].append(post)
    else:
        # Ajoute un nouveau post
        st.session_state["posts"].append(post)

# Interface principale
st.title("Simulateur de Réseau Social")

# Section pour afficher les posts
st.subheader("Fil d'actualité")
for idx, post in enumerate(st.session_state["posts"]):
    st.write(f"**{post['author']}** ({post['timestamp']}) : {post['content']}")
    st.write(f"👍 {post['likes']} likes")
    
    # Boutons d'action pour chaque post
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button(f"Like {idx}", key=f"like_{idx}"):
            st.session_state["posts"][idx]["likes"] += 1
    with col2:
        if st.button(f"Répondre {idx}", key=f"reply_{idx}"):
            st.session_state[f"show_reply_{idx}"] = not st.session_state.get(f"show_reply_{idx}", False)
    with col3:
        if st.button(f"Reposter {idx}", key=f"repost_{idx}"):
            repost_author = st.text_input(f"Nom (Repost à {idx})", key=f"repost_author_{idx}")
            if st.button(f"Publier Repost {idx}", key=f"publish_repost_{idx}"):
                repost_content = f"🔁 Repost : {post['content']}"
                add_post(repost_author, repost_content)

    # Zone pour ajouter une réponse
    if st.session_state.get(f"show_reply_{idx}", False):
        st.write("**Répondre :**")
        reply_author = st.text_input(f"Nom (Réponse à {idx})", key=f"reply_author_{idx}")
        reply_content = st.text_area(f"Message (Réponse à {idx})", key=f"reply_content_{idx}")
        if st.button(f"Publier Réponse {idx}", key=f"publish_reply_{idx}"):
            add_post(reply_author, reply_content, reply_to=idx)
            st.session_state[f"show_reply_{idx}"] = False  # Ferme la zone après publication

    # Afficher les réponses
    if post["replies"]:
        st.write("**Réponses :**")
        for reply in post["replies"]:
            st.write(f"↳ **{reply['author']}** ({reply['timestamp']}) : {reply['content']}")

st.write("---")

# Section pour publier un nouveau post
st.subheader("Publier un nouveau message")
author = st.text_input("Votre nom", key="new_author")
content = st.text_area("Votre message", key="new_content")
if st.button("Publier"):
    add_post(author, content)

# Option réservée pour effacer les contenus (réservée à l'administrateur)
if st.checkbox("Effacer tous les messages (Administrateur uniquement)"):
    if st.button("Confirmer la suppression"):
        st.session_state["posts"] = []
        st.success("Tous les messages ont été supprimés.")



