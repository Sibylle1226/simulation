import streamlit as st
from datetime import datetime

# Simple password protection
def check_password():
    def password_entered():
        if st.session_state["password"] == "votre_mot_de_passe":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Ask for password
        st.text_input("Entrez le mot de passe :", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Mot de passe incorrect.")
        return False
    else:
        return True

if check_password():
    # Initialize session state for posts
    if 'posts' not in st.session_state:
        st.session_state['posts'] = []

    # Sidebar for posting a new message
    st.sidebar.title("Poster un message")
    user = st.sidebar.text_input("Votre nom")
    message = st.sidebar.text_area("Votre message")
    image = st.sidebar.file_uploader("Ajouter une image (optionnel)", type=["png", "jpg", "jpeg"])
    submit = st.sidebar.button("Poster")

    if submit and user and message:
        # Save the post
        new_post = {
            "user": user,
            "message": message,
            "image": image,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "replies": []
        }
        st.session_state['posts'].insert(0, new_post)  # Add to the top of the feed
        st.sidebar.success("Message posté!")

    # Main feed
    st.title("Fil de discussion")
    for post in st.session_state['posts']:
        st.subheader(f"{post['user']} - {post['timestamp']}")
        st.write(post['message'])
        if post['image']:
            st.image(post['image'], caption="Image ajoutée", use_column_width=True)

        # Reply functionality
        reply = st.text_input(f"Répondre à {post['user']}", key=post['timestamp'])
        if st.button("Envoyer réponse", key=f"reply_{post['timestamp']}"):
            if reply:
                post['replies'].append({"user": "Vous", "reply": reply, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                st.success("Réponse envoyée!")
        
        # Display replies
        if post['replies']:
            st.write("**Réponses :**")
            for rep in post['replies']:
                st.write(f"- {rep['user']} ({rep['timestamp']}): {rep['reply']}")

    st.write("---")
    st.caption("Application simulant un réseau social pour exercice de communication de crise.")
