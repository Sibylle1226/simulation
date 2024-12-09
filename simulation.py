import streamlit as st
import datetime
import sqlite3

# Configuration de la base de données SQLite
DB_FILE = "social_network.db"

def init_db():
    """Initialise la base de données SQLite avec la table des posts."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            image BLOB,
            likes INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL
        )
        """)
        conn.commit()

def add_post_to_db(author, content, image=None):
    """Ajoute un nouveau post à la base de données."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO posts (author, content, image, likes, timestamp)
        VALUES (?, ?, ?, 0, ?)
        """, (author, content, image, timestamp))
        conn.commit()

def get_posts_from_db():
    """Récupère tous les posts depuis la base de données."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, author, content, image, likes, timestamp FROM posts ORDER BY id ASC")
        return cursor.fetchall()

def update_likes_in_db(post_id, new_likes):
    """Met à jour le nombre de likes d'un post."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET likes = ? WHERE id = ?", (new_likes, post_id))
        conn.commit()

def reset_posts_in_db():
    """Efface tous les posts de la base de données."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts")
        conn.commit()

# Initialisation de la base de données
init_db()

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
        if author and content:  # Vérifie que le nom et le contenu ne sont pas vides
            image_data = image.read() if image else None
            add_post_to_db(author, content, image=image_data)
            st.success("Votre message a été publié !")
        else:
            st.error("Veuillez remplir votre nom et votre message.")

    # Option réservée pour effacer les contenus (réservée à l'administrateur)
    st.write("---")
    if st.checkbox("Effacer tous les messages (Administrateur uniquement)"):
        if st.button("Confirmer la suppression"):
            reset_posts_in_db()
            st.success("Tous les messages ont été supprimés.")

with right_col:
    # Section pour afficher les posts
    st.subheader("Fil d'actualité")
    
    posts = get_posts_from_db()
    
    for post in posts:
        post_id, author, content, image, likes, timestamp = post
        with st.container():
            st.markdown("---")  # Séparateur visuel
            
            # Texte principal avec police agrandie
            st.markdown(
                f"""
                <div style="font-size:24px; font-weight:bold; margin-bottom:10px; color: #333;">
                {author} ({timestamp})</div>
                <div style="font-size:20px; margin-bottom:15px; line-height:1.5; color: #000;">
                {content}</div>
                """,
                unsafe_allow_html=True
            )
            
            # Affichage de l'image (si présente)
            if image:
                st.image(image, caption=f"Image partagée par {author}", use_column_width=True)
            
            st.write(f"👍 {likes} likes")

            # Boutons d'action pour chaque post
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button(f"Like {post_id}", key=f"like_{post_id}"):
                    update_likes_in_db(post_id, likes + 1)
                    st.experimental_rerun()  # Recharge l'application pour afficher le changement
            with col2:
                st.write("")  # Espace pour équilibrer les colonnes
