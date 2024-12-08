import streamlit as st
import pandas as pd
import datetime
import gdown  # Bibliothèque pour télécharger les fichiers depuis Google Drive

# Fonction pour télécharger le fichier CSV depuis Google Drive
def download_from_drive():
    """Télécharge le fichier CSV depuis Google Drive."""
    # Remplacez par votre ID de fichier Google Drive
    file_id = '1REVMIrdhkE5GLF5V9kYlhkEkN-sBACPk'  # Remplacez avec l'ID de votre fichier
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "posts.csv"
    
    # Télécharger le fichier
    gdown.download(url, output, quiet=False)
    
# Télécharger le fichier CSV depuis Google Drive
download_from_drive()

# Charger les posts depuis le fichier CSV téléchargé
def load_posts():
    try:
        # Lire le fichier CSV téléchargé
        posts = pd.read_csv("posts.csv")
        posts["timestamp"] = pd.to_datetime(posts["timestamp"], format="%H:%M")
        return posts
    except Exception as e:
        st.error(f"Erreur de chargement des messages: {e}")
        return pd.DataFrame(columns=["author", "content", "likes", "timestamp", "image", "is_reply", "parent_id"])

# Charger les messages
posts = load_posts()

# Interface utilisateur
st.title("Admin - Publier un message")

author = st.text_input("Nom de l'auteur", key="author")
content = st.text_area("Contenu du message", key="content")
image = st.file_uploader("Ajouter une image", type=["png", "jpg", "jpeg"], key="image")

if st.button("Publier"):
    add_post(author, content, image=image)
    st.success("Message publié avec succès!")
    save_to_csv()  # Sauvegarder après publication

# Affichage des posts existants
st.subheader("Fil d'actualités")
for idx, post in enumerate(st.session_state["posts"]):
    st.markdown(f"**{post['author']}** - {post['timestamp']}")
    st.markdown(post['content'])
    if post['image']:
        st.image(post['image'])
    st.markdown(f"👍 {post['likes']} likes")

    # Boutons pour ajouter des réponses ou des likes
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(f"Like {idx}", key=f"like_{idx}"):
            st.session_state["posts"][idx]["likes"] += 1
            save_to_csv()  # Sauvegarder après un like
    with col2:
        if st.button(f"Répondre {idx}", key=f"reply_{idx}"):
            st.session_state[f"show_reply_{idx}"] = not st.session_state.get(f"show_reply_{idx}", False)

    # Zone pour ajouter une réponse à un message
    if st.session_state.get(f"show_reply_{idx}", False):
        st.write("**Répondre :**")
        reply_author = st.text_input(f"Nom (Réponse à {idx})", key=f"reply_author_{idx}")
        reply_content = st.text_area(f"Message (Réponse à {idx})", key=f"reply_content_{idx}")
        reply_image = st.file_uploader(f"Ajouter une image (Réponse à {idx})", type=["png", "jpg", "jpeg"], key=f"reply_image_{idx}")
        if st.button(f"Publier Réponse {idx}", key=f"publish_reply_{idx}"):
            add_post(reply_author, reply_content, image=reply_image, reply_to=idx)
            st.session_state[f"show_reply_{idx}"] = False  # Ferme la zone après publication
            save_to_csv()  # Sauvegarder après la réponse
