import streamlit as st
import datetime

# Initialisation des clés si elles n'existent pas dans session_state
if "new_author" not in st.session_state:
    st.session_state["new_author"] = ""
if "new_content" not in st.session_state:
    st.session_state["new_content"] = ""

# Simuler des données (stockées dans session_state)
if "posts" not in st.session_state:
    st.session_state["posts"] = []

def add_post(author, content, image=None, reply_to=None):
    """Ajoute un nouveau post ou une réponse à un post existant."""
    timestamp = datetime.datetime.now().strftime("%H:%M")  # Heure uniquement
    post = {
        "author": author,
        "content": content,
        "likes": 0,
        "replies": [],
        "image": image,
        "timestamp": timestamp
    }
    if reply_to is not None:
        # Ajoute la réponse au post correspondant
        st.session_state["posts"][reply_to]["replies"].append(post)
    else:
        # Ajoute un nouveau post
        st.session_state["posts"].append(post)

# Configuration de la mise en page
st.title("Chapitre 9 Réseau Social")

# Éditeur de texte unique
st.subheader("Créer un message ou répondre")
author = st.text_input("Votre nom", key="new_author", value=st.session_state["new_author"])
content = st.text_area("Votre message", key="new_content", value=st.session_state["new_content"])
image = st.file_uploader("Ajouter une image", type=["png", "jpg", "jpeg"], key="new_image")

# Choisir si le message est une réponse
if len(st.session_state["posts"]) > 0:
    reply_to = st.selectbox(
        "Répondre à un message existant (laisser vide pour un nouveau message)",
        options=["Nouveau message"] + [f"{i + 1}. {post['content']}" for i, post in enumerate(st.session_state["posts"])],
        key="reply_to"
    )
    if reply_to == "Nouveau message":
        reply_to = None
    else:
        reply_to = int(reply_to.split(".")[0]) - 1
else:
    reply_to = None

if st.button("Publier"):
    add_post(author, content, image=image, reply_to=reply_to)
    
    # Réinitialiser les champs après publication
    st.session_state["new_author"] = ""  # Réinitialiser le champ auteur
    st.session_state["new_content"] = ""  # Réinitialiser le champ contenu

# Option pour effacer les contenus (administrateur uniquement)
st.write("---")
if st.checkbox("Effacer tous les messages (Administrateur uniquement)"):
    if st.button("Confirmer la suppression"):
        st.session_state["posts"] = []
        st.success("Tous les messages ont été supprimés.")

# Afficher les posts avec un fond distinct
st.markdown(
    """
    <style>
        .message-container {
            background-color: #f0f8ff; /* Couleur de fond bleu clair */
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message-author {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 5px;
        }
        .message-content {
            font-size: 16px;
            margin-bottom: 10px;
        }
        .message-time {
            font-size: 12px;
            color: gray;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.subheader("Fil d'actualité")
for idx, post in enumerate(st.session_state["posts"]):
    # Conteneur avec fond de couleur
    st.markdown(f"""
        <div class="message-container">
            <div class="message-author">{post['author']} ({post['timestamp']})</div>
            <div class="message-content">{post['content']}</div>
        </div>
    """, unsafe_allow_html=True)

    # Afficher l'image du post
    if post["image"]:
        st.image(post["image"], caption=f"Image partagée par {post['author']}", use_column_width=True)

    # Boutons pour liker ou répondre
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button(f"Like {idx}", key=f"like_{idx}"):
            st.session_state["posts"][idx]["likes"] += 1
    with col2:
        st.write(f"👍 {post['likes']} likes")

    # Afficher les réponses
    if post["replies"]:
        for reply in post["replies"]:
            st.markdown(f"""
                <div style="margin-left: 20px; border-left: 2px solid #d3d3d3; padding-left: 10px;">
                    <div class="message-author">↳ {reply['author']} ({reply['timestamp']})</div>
                    <div class="message-content">{reply['content']}</div>
                </div>
            """, unsafe_allow_html=True)
            if reply["image"]:
                st.image(reply["image"], caption=f"Image partagée par {reply['author']}", use_column_width=True)
