import streamlit as st
from datetime import datetime

# Initialize session state for posts
if 'posts' not in st.session_state:
    st.session_state['posts'] = []

# Sidebar for posting a new message
st.sidebar.title("Poster un message")
user = st.sidebar.text_input("Votre nom", key="new_post_user")
message = st.sidebar.text_area("Votre message (emojis acceptés)", key="new_post_message")
image = st.sidebar.file_uploader("Ajouter une image (optionnel)", type=["png", "jpg", "jpeg"], key="new_post_image")
submit = st.sidebar.button("Poster", key="submit_post")

if submit and user and message:
    # Save the post
    new_post = {
        "user": user,
        "message": message,
        "image": image,
        "timestamp": datetime.now().strftime("%H:%M:%S"),  # Only time
        "likes": 0,
        "replies": []
    }
    st.session_state['posts'].insert(0, new_post)  # Add to the top of the feed
    st.sidebar.success("Message posté!")

# Admin-only reset functionality
st.sidebar.markdown("---")
admin_password = st.sidebar.text_input("Mot de passe admin", type="password", key="admin_password")
if st.sidebar.button("Effacer tous les contenus") and admin_password == "votre_mot_de_passe":
    st.session_state['posts'] = []
    st.sidebar.success("Tous les contenus ont été effacés.")
elif admin_password and admin_password != "votre_mot_de_passe":
    st.sidebar.error("Mot de passe incorrect.")

# Main feed
st.title("Fil de discussion")
for post_index, post in enumerate(st.session_state['posts']):
    # Display the post
    st.subheader(f"{post['user']} - {post['timestamp']}")
    st.write(post['message'])
    if post['image']:
        st.image(post['image'], caption="Image ajoutée", use_column_width=True)
    
    # Like button
    if st.button(f"👍 Like ({post['likes']})", key=f"like_post_{post_index}"):
        post['likes'] += 1
        st.experimental_rerun()  # Refresh the app to update like count
    
    # Repost functionality
    if st.button("🔁 Reposter", key=f"repost_post_{post_index}"):
        repost = {
            "user": post['user'],
            "message": f"Repost : {post['message']}",
            "image": post['image'],
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "likes": 0,
            "replies": []
        }
        st.session_state['posts'].insert(0, repost)
        st.success("Message reposté!")
        st.experimental_rerun()

    # Reply functionality
    st.write("**Répondre :**")
    reply_user = st.text_input(f"Votre nom (réponse à {post['user']})", key=f"reply_user_{post_index}")
    reply = st.text_area(f"Votre réponse (à {post['user']} - emojis acceptés)", key=f"reply_message_{post_index}")
    if st.button("Envoyer réponse", key=f"send_reply_{post_index}"):
        if reply_user and reply:
            post['replies'].append({
                "user": reply_user,
                "reply": reply,
                "timestamp": datetime.now().strftime("%H:%M:%S"),  # Only time
                "likes": 0
            })
            st.success("Réponse envoyée!")
            st.experimental_rerun()
        else:
            st.error("Veuillez indiquer votre nom et un message pour répondre.")

    # Display replies
    if post['replies']:
        st.write("**Réponses :**")
        for reply_index, rep in enumerate(post['replies']):
            st.write(f"- {rep['user']} ({rep['timestamp']}): {rep['reply']}")
            # Like button for replies
            if st.button(f"👍 Like ({rep['likes']})", key=f"like_reply_{post_index}_{reply_index}"):
                rep['likes'] += 1
                st.experimental_rerun()

st.write("---")
st.caption("Application simulant un réseau social pour exercice de communication de crise.")

