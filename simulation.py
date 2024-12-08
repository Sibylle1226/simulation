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

st.title("Simulateur de Réseau Social")

left_col, right_col = st.columns([1, 2])



with left_col:

    # Section pour publier un nouveau post

    st.subheader("Publier un nouveau message")

    author = st.text_input("Votre nom", key="new_author")

    content = st.text_area("Votre message", key="new_content")

    image = st.file_uploader("Ajouter une image", type=["png", "jpg", "jpeg"], key="new_image")

    if st.button("Publier"):

        add_post(author, content, image=image)



    # Option réservée pour effacer les contenus (réservée à l'administrateur)

    st.write("---")

    if st.checkbox("Effacer tous les messages (Administrateur uniquement)"):

        if st.button("Confirmer la suppression"):

            st.session_state["posts"] = []

            st.success("Tous les messages ont été supprimés.")



with right_col:

    # Section pour afficher les posts

    st.subheader("Fil d'actualité")

    

    # Affichage des posts dans l'ordre ancien -> récent

    for idx, post in enumerate(st.session_state["posts"]):

        with st.container():

            st.markdown("---")  # Séparateur visuel

            

            # Texte principal avec style agrandi

            st.markdown(

                f"""

                <div style="font-size:18px; font-weight:bold; margin-bottom:5px;">

                {post['author']} ({post['timestamp']})</div>

                <div style="font-size:16px; margin-bottom:10px;">{post['content']}</div>

                """,

                unsafe_allow_html=True

            )

            

            # Affichage de l'image (si présente)

            if post["image"]:

                st.image(post["image"], caption=f"Image partagée par {post['author']}", use_column_width=True)

            

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

                reply_image = st.file_uploader(f"Ajouter une image (Réponse à {idx})", type=["png", "jpg", "jpeg"], key=f"reply_image_{idx}")

                if st.button(f"Publier Réponse {idx}", key=f"publish_reply_{idx}"):

                    add_post(reply_author, reply_content, image=reply_image, reply_to=idx)

                    st.session_state[f"show_reply_{idx}"] = False  # Ferme la zone après publication



            # Afficher les réponses sous le post correspondant

            if post["replies"]:

                st.write("**Réponses :**")

                for reply in post["replies"]:

                    with st.container():

                        st.markdown(

                            f"""

                            <div style="font-size:16px; font-weight:bold; margin-bottom:5px;">

                            ↳ {reply['author']} ({reply['timestamp']})</div>

                            <div style="font-size:14px; margin-bottom:10px;">{reply['content']}</div>

                            """,

                            unsafe_allow_html=True

                        )

                        if reply["image"]:

                            st.image(reply["image"], caption=f"Image partagée par {reply['author']}", use_column_width=True)

