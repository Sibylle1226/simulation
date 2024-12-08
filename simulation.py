import streamlit as st
import datetime

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

# Créer deux colonnes : une pour l'éditeur de texte et une pour le flux
left_col, right_col = st.columns([1, 3])

# Section pour publier un nouveau message dans la colonne de gauche
with left_col:
    st.subheader("Publier un nouveau message")
    author = st.text_input("Votre nom", key="new_author")
    content = st.text_area("Votre message", key="new_content")
    image = st.file_uploader("Ajouter une image", type=["png", "jpg", "jpeg"], key="new_image")
    
    # Bouton "Publier" qui ajoute le message ou la réponse
    if st.button("Publier"):
        add_post(author, content, image=image)
        
        # Réinitialiser les champs après publication
        st.session_state["new_author"] = ""
        st.session_state["new_content"] = ""

# Section pour afficher les posts dans la colonne de droite avec un fond de couleur
with right_col:
    st.subheader("Fil d'actualité")

    # Appliquer un fond de couleur pour le flux des messages
    st.markdown(
        """
        <style>
            .message-container {
                background-color: #f0f8ff; /* Fond bleu clair */
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

    # Afficher les posts et leurs réponses
    for idx, post in enumerate(st.session_state["posts"]):
        with st.container():
            # Affichage principal du message
            st.markdown(f"""
                <div class="message-container">
                    <div class="message-author">{post['author']} ({post['timestamp']})</div>
                    <div class="message-content">{post['content']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Affichage de l'image (si présente)
            if post["image"]:
                st.image(post["image"], caption=f"Image partagée par {post['author']}", use_column_width=True)

            # Boutons d'action : like et répondre
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(f"Like {idx}", key=f"like_{idx}"):
                    st.session_state["posts"][idx]["likes"] += 1
            with col2:
                st.write(f"👍 {post['likes']} likes")

            # Bouton pour répondre
            if st.button(f"Répondre {idx}", key=f"reply_{idx}"):
                # Afficher la zone de réponse
                reply_author = st.text_input(f"Votre nom (Réponse à {idx})", key=f"reply_author_{idx}")
                reply_content = st.text_area(f"Message (Réponse à {idx})", key=f"reply_content_{idx}")
                reply_image = st.file_uploader(f"Ajouter une image (Réponse à {idx})", type=["png", "jpg", "jpeg"], key=f"reply_image_{idx}")
                
                # Bouton de publication de la réponse
                if st.button(f"Publier Réponse {idx}", key=f"publish_reply_{idx}"):
                    add_post(reply_author, reply_content, image=reply_image, reply_to=idx)
                    
                    # Fermer la zone de réponse après publication
                    st.session_state[f"show_reply_{idx}"] = False

            # Afficher les réponses sous le post correspondant
            if post["replies"]:
                st.write("**Réponses :**")
                for reply in post["replies"]:
                    with st.container():
                        st.markdown(f"""
                            <div style="margin-left: 20px; border-left: 2px solid #d3d3d3; padding-left: 10px;">
                                <div class="message-author">↳ {reply['author']} ({reply['timestamp']})</div>
                                <div class="message-content">{reply['content']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if reply["image"]:
                            st.image(reply["image"], caption=f"Image partagée par {reply['author']}", use_column_width=True)

