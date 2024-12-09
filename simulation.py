import streamlit as st
import datetime
import sqlite3

# Initialisation de la base de données SQLite
conn = sqlite3.connect('messages.db', check_same_thread=False)
c = conn.cursor()

# Création de la table pour stocker les messages
c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        likes INTEGER DEFAULT 0,
        timestamp TEXT NOT NULL,
        image BLOB
    )
''')
conn.commit()

# Fonction pour ajouter un post dans la base de données
def add_post(author, content, image=None):
    timestamp = datetime.datetime.now().strftime("%H:%M")
    c.execute('INSERT INTO posts (author, content, likes, timestamp, image) VALUES (?, ?, ?, ?, ?)',
              (author, content, 0, timestamp, image))
    conn.commit()

# Fonction pour récupérer les posts depuis la base de données
def get_posts():
    c.execute('SELECT id, author, content, likes, timestamp, image FROM posts ORDER BY id ASC')
    return c.fetchall()

# Fonction pour mettre à jour les likes d'un post
def like_post(post_id):
    c.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
    conn.commit()

# Effacer tous les messages (administrateur uniquement)
def delete_all_posts():
    c.execute('DELETE FROM posts')
    conn.commit()

# Titre de l'application
st.title("Simulateur de Réseau Social")

# Mise en page avec deux colonnes
left_col, right_col = st.columns([1, 2])

with left_col:
    # Section pour publier un nouveau message
    st.subheader("Publier un nouveau message")
    author = st.text_input("Votre nom")
    content = st.text_area("Votre message")
    image = st.file_uploader("Ajouter une image", type=["png", "jpg", "jpeg"])
    if st.button("Publier"):
        image_data = image.read() if image else None
        add_post(author, content, image=image_data)
        st.success("Message publié avec succès !")

    # Option pour effacer tous les messages
    st.write("---")
    if st.checkbox("Effacer tous les messages (Administrateur uniquement)"):
        if st.button("Confirmer la suppression"):
            delete_all_posts()
            st.success("Tous les messages ont été supprimés.")

with right_col:
    # Section pour afficher les messages
    st.subheader("Fil d'actualité")
    posts = get_posts()

    # Affichage des posts
    for post in posts:
        post_id, author, content, likes, timestamp, image = post

        with st.container():
            st.markdown("---")  # Séparateur visuel

            # Texte principal avec style agrandi
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

            # Affichage du nombre de likes
            st.write(f"👍 {likes} likes")

            # Boutons d'interaction
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button(f"Like {post_id}", key=f"like_{post_id}"):
                    like_post(post_id)
                    st.experimental_rerun()  # Rafraîchir pour afficher les likes mis à jour

---

### **Explications des modifications :**
1. **Base de données SQLite** :
   - Une base de données `messages.db` est créée (ou réutilisée si elle existe déjà).
   - La table `posts` stocke les messages, leurs auteurs, les likes, l'heure de publication, et une éventuelle image.

2. **Fonctions pour interagir avec la base** :
   - `add_post`: Ajoute un nouveau post dans la base.
   - `get_posts`: Récupère tous les posts pour affichage.
   - `like_post`: Met à jour les likes pour un post donné.
   - `delete_all_posts`: Supprime tous les messages.

3. **Affichage des messages** :
   - Les messages sont récupérés depuis SQLite et affichés dans une boucle.
   - Les images sont gérées et affichées si elles sont présentes.

4. **Boutons d'interaction** :
   - Le bouton "Like" augmente le compteur de likes et force un rafraîchissement de la page avec `st.experimental_rerun`.

---

### **Déploiement :**
Une fois ce code intégré dans votre application Streamlit, déployez-le sur Streamlit Cloud. Tous les utilisateurs verront les mêmes messages et pourront interagir en temps réel.

---

Si vous avez besoin d'aide supplémentaire, faites-le moi savoir ! 😊
