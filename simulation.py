import streamlit as st
import pandas as pd
import datetime

# Initialisation de la liste des posts dans session_state si elle n'existe pas encore
if "posts" not in st.session_state:
    st.session_state["posts"] = []

# Fonction pour ajouter un nouveau message
def add_post(author, content, image=None, reply_to=None):
    """Ajoute un nouveau message ou une réponse à un message existant."""
    timestamp = datetime.datetime.now().strftime("%H:%M")
    post = {
        "author": author,
        "content": content,
        "likes": 0,
        "replies": [],
        "image": image,
        "timestamp": timestamp
    }
    if reply_to is not None:
        # Ajouter la réponse au post existant
        st.session_state["posts"][reply_to]["replies"].append(post)
    else:
        # Ajouter un nouveau message principal
        st.session_state["posts"].append(post)

# Fonction pour sauvegarder les messages dans un fichier CSV
def save_to_csv():
    """Sauvegarde les messages et réponses dans un fichier CSV."""
    flat_posts = []
    for post in st.session_state["posts"]:
        flat_posts.append({
            "author": post["author"],
            "content": post["content"],
            "likes": post["likes"],
            "timestamp": post["timestamp"],
            "image": post["image"],  # Vous pouvez stocker un chemin ou laisser vide
            "is_reply": False,
            "parent_id": None
        })
        for reply in post["replies"]:
            flat_posts.append({
                "author": reply["author"],
                "content": reply["content"],
                "likes": 0,
                "timestamp": reply["timestamp"],
                "image": reply["image"],  # Vous pouvez stocker un chemin ou laisser vide
                "is_reply": True,
                "parent_id": post["content"]
            })
    
    df = pd.DataFrame(flat_posts)
    df.to_csv("posts.csv", index=False)  # Sauvegarde les posts dans un fichier CSV

# Interface pour publier un message
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
