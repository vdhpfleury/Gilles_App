import streamlit as st
from streamlit_option_menu import option_menu
import base64
from carrousel import carrousel, preload_images

# Configuration de la page
st.set_page_config(
    page_title="Gilles Gambini - Apnéiste & Biologiste Marin",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialiser le session_state pour la navigation
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "Accueil"

if 'images_ICE' not in st.session_state:
    preload_images("Photo/ICE")
    st.session_state.images_ICE = True

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3b82f6;
        text-align: center;
        margin-bottom: 2rem;
    }
    .citation {
        font-size: 1.3rem;
        font-style: italic;
        text-align: center;
        color: #475569;
        padding: 2rem;
        background: #f1f5f9;
        border-left: 4px solid #3b82f6;
        margin: 2rem 0;
    }
    .service-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .price-tag {
        font-size: 1.5rem;
        color: #059669;
        font-weight: bold;
    }
    .contact-btn {
        background: #3b82f6;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Menu de navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Accueil", "Contact", "Qui suis-je ? +CV"],
        icons=["house", "envelope", "envelope"],
        menu_icon="cast",
        default_index=["Accueil", "Contact", "Qui suis-je ? +CV"].index(st.session_state.menu_selection),
        key="menu"
    )
    # Mettre à jour le session_state quand l'option_menu change
    st.session_state.menu_selection = selected

# PAGE ACCUEIL
if st.session_state.menu_selection == "Accueil":
    col1, col2 = st.columns([1,3])
    with col1 : 
        st.image("Photo/profil_01.JPG", caption="Profil", use_container_width=True)

    with col2 :
        st.markdown('<h1 class="main-header">Gilles Gambini</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Apnéiste professionnel • Biologiste marin • Plongeur scientifique • Photographe</p>', unsafe_allow_html=True)

        st.markdown('<h1 class="main-header">Certifications</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">DEJEPS • Plongeur 2A, 3B • Recycleur Hypoxique</p>', unsafe_allow_html=True)

        st.markdown('<h1 class="main-header">📋 Services</h1>', unsafe_allow_html=True)
    
        services_data = [
            ("Mentoring", "Accompagnement personnalisé • Carrière marine • Performance"),
            ("Coaching Apnée", "Suivi individuel • Progression technique • Préparation mentale"),
            ("Conférences", "Inspiration • Science • Aventure"),
            ("Stages", "Apnée • Plongée scientifique • Sous glace"),
            ("Services Hyperbare", "Interventions professionnelles • Tournages • Recherche"),
            ("Cours en ligne", "Formation à distance • Ressources exclusives")
        ]

        cols_per_row = 6

        for i in range(0, len(services_data), cols_per_row):
            cols = st.columns(cols_per_row)
            for col, (titre, description) in zip(cols, services_data[i:i+cols_per_row]):
                with col:
                    st.markdown(f"**{titre}**")
                    st.caption(description)

    
    col1, col2 = st.columns([1, 3])

    with col1 : 
        subcol1, subcol2  = st.columns(2)
        with subcol1 : 
            st.subheader("Contacter")
            st.write("remplir le formulaire ici")
            if st.button("Contacter"):
                st.session_state.menu_selection = "Contact"
                st.rerun()
        with subcol2 : 
            st.subheader("Suivre")
            st.write("*lien reseau*")
            
        st.subheader("Actualités")
        st.write("...")
    with col2 : 
        carrousel("Photo/ICE", height=500, duration=3)

        
    # Bio
    st.header("📋 Détails des services")


    tab_Mentoring, tab_Coaching, tab_Conferences, tab_Stages, tab_Hyperbares, tab_Cours_en_ligne = st.tabs(["Mentoring", "Coaching Apnée", "Conférences", "Stages", "Service Hyperbares", "Cours en ligne"])
    with tab_Mentoring:
        st.title("🧭 Mentoring Océan & Performance")
        st.subheader("Explorer, progresser, se dépasser")
        col1, col2 = st.columns([2,3])
        with col1 : 
            st.write("""
            Entre exploration, science et performance, je propose un accompagnement personnalisé destiné à celles et ceux qui 
            souhaitent progresser, techniquement, mentalement ou professionnellement dans l'univers du milieu marin et du sport.
            
            Que vous soyez plongeur, photographe, jeune scientifique ou apnéiste, ce mentoring est une passerelle entre la 
            connaissance, la pratique et la confiance.
            
            Chaque programme est conçu sur mesure, en fonction de votre profil, de vos objectifs et de votre expérience.
            """)

        with col2 : 
            st.info("📸 **ESPACE IMAGE HEADER** - Image inspirante de mentorat/exploration")
            st.image("https://via.placeholder.com/1200x400/1e3a8a/ffffff?text=Mentoring+Header", use_container_width=True)
                    
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🏆 Performance sportive")
            st.write("Issue de mon parcours en apnée de haut niveau, avec un travail approfondi sur la physiologie, la respiration et la gestion mentale.")
        with col2:
            st.markdown("#### 🔬 Recherche scientifique")
            st.write("Ancrée dans ma carrière d'ingénieur en écologie marine et de plongeur scientifique.")
        with col3:
            st.markdown("#### 🌍 Expérience terrain")
            st.write("Forgée lors d'expéditions, de tournages et de missions à travers le monde.")
        
        st.markdown("---")
        
        # Formules de mentoring
        st.header("📋 Formules de Mentoring")
        
        # Formule 1
        with st.expander("🎯 Mentoring individuel « Exploration & Performance »", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Pour progresser rapidement, avec un suivi entièrement personnalisé.**
                
                ✓ 1 séance de diagnostic offerte (30 min)  
                ✓ 4 à 6 séances d'1h (en visio)  
                ✓ Travail sur la technique, la stratégie de carrière, la respiration, la préparation mentale  
                ✓ Ressources et exercices personnalisés
                
                **Idéal pour :** Étudiants ou professionnels souhaitant développer de nouvelles expertises, apnéistes, 
                plongeurs, photographes sous-marins, explorateurs ou tout simplement curieux.
                """)
            with col2:
                st.markdown('<p class="price-tag">150 € / séance</p>', unsafe_allow_html=True)
                st.markdown('<p class="price-tag">ou 700 € / 5 séances</p>', unsafe_allow_html=True)
                st.button("Réserver un appel découverte", key="mentoring1")
        
        # Formule 2
        with st.expander("👥 Mentoring collectif « Ocean Skills »"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Apprenez, échangez et progressez ensemble en fonction de vos objectifs (groupes par thématiques).**
                
                ✓ Petits groupes (3 à 6 personnes)  
                ✓ 1 visio hebdomadaire (1h30)  
                ✓ Ressources exclusives (PDF, vidéos, fiches techniques)  
                ✓ Suivi collectif + espace d'échange privé
                """)
            with col2:
                st.markdown('<p class="price-tag">350 € / mois</p>', unsafe_allow_html=True)
                st.button("Rejoindre un groupe", key="mentoring2")
        
        # Formule 3
        with st.expander("💼 Mentoring carrière « Carrière bleue »"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Pour construire un parcours professionnel aligné avec vos valeurs et votre passion pour l'océan.**
                
                ✓ 1 séance d'1h/mois : orientation, stratégie, CV, préparation à l'emploi ou à la mission  
                ✓ Accompagnement sur les choix de carrière, stages, formations et projets scientifiques, réseau  
                ✓ Retours d'expérience et conseils concrets issus du terrain
                
                **Idéal pour :** Étudiants, jeunes chercheurs, techniciens ou naturalistes souhaitant s'engager dans 
                une carrière marine ou scientifique.
                """)
            with col2:
                st.markdown('<p class="price-tag">100 € / mois</p>', unsafe_allow_html=True)
                st.button("Débuter mon parcours", key="mentoring3")
        
        # Formule 4
        with st.expander("⭐ Mentoring carrière « Filleul »"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Suivi personnalisé sur long terme. Je ne prend qu'un seul filleul afin de pouvoir t'accompagner au mieux 
                dans la construction de ta carrière.**
                
                ✓ 1 séance Visio d'1h/mois : orientation, stratégie, CV, préparation à l'emploi ou à la mission  
                ✓ Opportunités de participer à des campagnes scientifiques  
                ✓ Espace d'échange privé  
                ✓ Accompagnement sur les choix de carrière, stages, formations et projets scientifiques, réseau  
                ✓ Retours d'expérience et conseils concrets issus du terrain  
                ✓ Ressources exclusives (PDF, vidéos, fiches techniques)
                
                **Idéal pour :** Étudiants souhaitant s'engager dans une carrière marine et de plongeur scientifique.
                """)
            with col2:
                st.markdown('<p class="price-tag">150 € / mois</p>', unsafe_allow_html=True)
                st.button("Candidater", key="mentoring4")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Pourquoi ce mentoring est différent")
        col1, col2 = st.columns(2)
        with col1:
            st.write("✓ Approche croisant science, performance et exploration")
            st.write("✓ Expérience du terrain (missions, expéditions, plongées profondes)")
        with col2:
            st.write("✓ Écoute, rigueur et accompagnement humain")
            st.write("✓ Objectif : autonomie, progression, confiance")
        
        st.info("📸 **ESPACE IMAGE** - Photo de mentorat en action ou d'expédition")

    with tab_Coaching : 
        st.title("💙 Coaching Apnée : Suivi personnalisé")
        col1, col2 = st.columns([2, 3])
        with col2 : 
            st.info("📸 **ESPACE IMAGE HEADER** - Image d'apnée profonde")
            st.image("https://via.placeholder.com/1200x400/0ea5e9/ffffff?text=Coaching+Apnée", use_container_width=True)
        

        with col1 :
            st.subheader("Progressez à votre rythme, avec un encadrement sur mesure")
                
            st.write("""
            Que vous soyez débutant, confirmé ou compétiteur, ce programme de coaching vous accompagne pas à pas vers vos 
            objectifs en apnée.
            
            Chaque mois, nous construisons ensemble une progression adaptée à votre niveau, votre environnement et vos contraintes de vie.
            
            **L'objectif : vous aider à progresser durablement, sans surentraînement ni perte de motivation.**
            """)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🎯 Le concept")
            st.write("""
            Une approche simple, efficace et personnalisée. Une séance par mois, des exercices ciblés, et un suivi continu.
            
            **Chaque mois, vous bénéficiez de :**
            
            ✓ 1 appel de suivi (30 min à 1h) pour faire le point sur vos sensations, vos progrès et ajuster la stratégie  
            ✓ Un bloc d'exercices mensuel : préparation à sec, relaxation, renforcement, apnée, visualisation ou travail spécifique  
            ✓ Un plan de progression clair ajusté à vos capacités et à votre agenda  
            ✓ Un échange direct (mail ou message) pour toute question entre deux sessions
            """)
        with col2:
            st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.markdown('<p class="price-tag">100 € / mois</p>', unsafe_allow_html=True)
            st.write("**Sans engagement**")
            st.write("✓ 1 visio/appel mensuel")
            st.write("✓ Bloc d'exercices personnalisé")
            st.write("✓ Suivi et adaptation mensuelle")
            st.button("Réserver mon appel découverte", key="coaching")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 👥 Pour qui ?")
        col1, col2 = st.columns(2)
        with col1:
            st.write("🌊 Apnéistes débutants souhaitant progresser sereinement")
            st.write("📈 Pratiquants confirmés cherchant à franchir un cap ou progresser")
            st.write("🏆 Apnéistes de haut niveau désirant préparer des compétitions")
        with col2:
            st.write("🧘 Sportifs voulant travailler la respiration et la gestion mentale")
            st.write("📸 Photographes sous-marins souhaitant améliorer leur aisance sous l'eau")
        
        st.markdown("---")
        
        st.markdown("### ⭐ Pourquoi ce coaching est différent")
        col1, col2 = st.columns(2)
        with col1:
            st.write("✓ Basé sur la physiologie et la préparation mentale du sportif de haut niveau")
            st.write("✓ Adapté à tous les niveaux et styles d'apnée")
        with col2:
            st.write("✓ Approche globale : physique, mental, technique et émotionnel")
            st.write("✓ Suivi par un apnéiste professionnel diplômé d'État spécialisé en physiologie hyperbare")

    with tab_Conferences : 
        st.title("🎤 Conférences - Science, Océan & Performance Humaine")
        st.subheader("Explorer, inspirer, reconnecter")

        col1, col2 = st.columns([2,3])

        with col1 : 
            st.write("""
            À travers mes expériences d'apnéiste professionnel, de biologiste marin et de plongeur scientifique, je partage 
            une vision singulière du monde : celle d'un homme qui explore les profondeurs pour mieux comprendre la vie et ses limites.
            
            Mes conférences sont une invitation à la découverte : celle de l'océan, du corps et de l'esprit humain.
            
            Entre images d'expédition, récits authentiques et apports scientifiques, elles offrent une expérience inspirante 
            et sensorielle, à la croisée de la science, du sport et de l'aventure.
            """)
        
        with col2 : 
            st.info("📸 **ESPACE IMAGE HEADER** - Photo de conférence ou d'expédition")
            st.image("https://via.placeholder.com/1200x400/1e3a8a/ffffff?text=Conférences", use_container_width=True)
        
        
        
        
        
        st.markdown("### 🎯 Une approche unique")
        st.write("""
        Alliant rigueur scientifique, sensibilité artistique et expérience de terrain, mes interventions s'adressent à tous les publics :
        
        • Entreprises & séminaires de direction  
        • Institutions & collectivités  
        • Écoles, universités, festivals & musées
        """)
        
        st.markdown("---")
        st.header("📋 Formules disponibles")
        
        # Formule 1
        with st.expander("🌊 Inspiration & Exploration", expanded=True):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Une immersion dans le monde sous-marin et la performance humaine.**
                
                ✓ 45 à 60 minutes de conférence  
                ✓ Images et vidéos exclusives d'expéditions  
                ✓ Thèmes : exploration, adaptation, dépassement, lien entre science et aventure  
                ✓ Session de questions/réponses (15-20 min)
                """)
            with col2:
                st.markdown("**Tarifs :**")
                st.markdown('<p class="price-tag">1 500 € HT</p>', unsafe_allow_html=True)
                st.write("(entreprises)")
                st.markdown('<p class="price-tag">700 € TTC</p>', unsafe_allow_html=True)
                st.write("(institutions / universités)")
        
        # Formule 2
        with st.expander("🫁 Respirer & Performer"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Une conférence interactive mêlant apnée, respiration et gestion du stress.**
                
                ✓ 30 min d'intervention + 30 min d'exercices guidés  
                ✓ Exploration des liens entre souffle, mental et performance  
                ✓ Application directe au quotidien : travail, sport, équilibre
                """)
            with col2:
                st.markdown('<p class="price-tag">1 200 € HT</p>', unsafe_allow_html=True)
        
        # Formule 3
        with st.expander("🔬 Science & Océan"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Comprendre l'océan pour mieux le préserver.**
                
                ✓ Conférence scientifique et visuelle (1h)  
                ✓ Thèmes : exploration, biodiversité, changements climatiques, missions de recherche  
                ✓ Adaptée à un public académique, institutionnel ou familial
                """)
            with col2:
                st.markdown("**Tarifs :**")
                st.markdown('<p class="price-tag">1 200 € HT</p>', unsafe_allow_html=True)
                st.write("(entreprises)")
                st.markdown('<p class="price-tag">700 € TTC</p>', unsafe_allow_html=True)
                st.write("(institutions / universités)")
        
        # Formule 4
        with st.expander("✨ Sur mesure & Partenariats"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Pour les événements, festivals ou collaborations spécifiques.**
                
                ✓ Format adaptable (15 min à 1h30)  
                ✓ Possibilité d'intégrer projection, exposition photo ou atelier respiration  
                ✓ Contenu ajusté selon le thème ou le public
                """)
            with col2:
                st.markdown('<p class="price-tag">800 à 2 500 €</p>', unsafe_allow_html=True)
                st.write("selon le format")
        
        st.markdown("---")
        
        st.markdown("### 🎨 Options complémentaires")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("🎬 Projection immersive")
            st.write("Mini-film d'expédition ou court-métrage")
        with col2:
            st.write("🫁 Atelier respiration / relaxation")
            st.write("(10-20 min)")
        with col3:
            st.write("📸 Exposition photo")
            st.write("ou installation visuelle")
        
        st.markdown("### 🎯 Thématiques clés")
        st.write("""
        • La physiologie de l'extrême : ce que l'apnée nous apprend sur le corps humain  
        • Explorer et préserver : science et aventure au service de la connaissance  
        • Le souffle comme outil de performance et d'équilibre  
        • Leadership et gestion de mission en milieu extrême  
        • L'océan comme source d'inspiration et d'humilité
        """)
        
        st.button("📧 Demander une conférence", key="conf")

    with tab_Stages : 
        st.title("🏊 Stages")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Explorez, respirez, comprenez.")
            st.write("""
            Depuis plus de 10 ans, ces stages sont une immersion complète dans mon univers : entre science, exploration et performance.
                
            Ils s'adressent à celles et ceux qui souhaitent se reconnecter à l'océan, apprendre à mieux respirer, repousser leurs 
            limites ou comprendre le milieu marin à travers une approche rigoureuse, bienveillante et passionnée.
            """)
    
    
        with col2:
            st.info("📸 **ESPACE IMAGE HEADER** - Photo de stage en action")
            st.image("https://via.placeholder.com/1200x400/0ea5e9/ffffff?text=Stages", use_container_width=True)
           
        
        # Stage 1 - Apnée sous glace
        with st.expander("❄️ Stage d'apnée sous glace : Sur mesure"):
        
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("""
                **Une expérience unique : le silence absolu, la lumière du froid, la maîtrise du souffle.**
                
                Sous la glace, chaque mouvement devient une méditation, chaque respiration une connexion profonde entre le corps, 
                l'eau et la lumière.
                
                **Objectifs :**
                
                ✓ Découvrir et pratiquer l'apnée sous glace en toute sécurité  
                ✓ Explorer la respiration, la concentration et la gestion du froid  
                ✓ Apprendre la logistique et les techniques spécifiques à la plongée sous glace  
                ✓ Développer la maîtrise mentale et physique dans un environnement extrême
                """)
            with col2:
                st.info("📸 **Image apnée sous glace**")
                st.image("https://via.placeholder.com/400x300/0ea5e9/ffffff?text=Sous+Glace", use_container_width=True)
            
            with st.expander("📋 Contenu du stage"):
                st.markdown("""
                ✓ Introduction à la physiologie du froid et à la thermorégulation  
                ✓ Préparation mentale et respiratoire spécifique aux milieux extrêmes  
                ✓ Mise en place logistique (sécurité, ligne de vie, ouverture de trou, secours)  
                ✓ Immersion sous glace en apnée : exploration progressive et guidée  
                ✓ Debriefing, retour d'expérience
                """)
        
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Formule individuelle**")
                st.write("• 1 à 3 jours")
                st.write("• Encadrement personnalisé")
                st.markdown('<p class="price-tag">À partir de 800 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Formule groupe (2-6 personnes)**")
                st.write("• 1 à 3 jours")
                st.write("• Gestion logistique incluse")
                st.markdown('<p class="price-tag">À partir de 400 € / personne / jour</p>', unsafe_allow_html=True)
            
            st.info("""
            **Période & lieu :** Décembre à avril (selon conditions) - Alpes françaises, Suisse, Norvège, Finlande, Groenland
            
            **Pré-requis :** Bonne condition physique • Certificat médical d'aptitude à la plongée en apnée
            """)
            
        
        # Stage 2 - Apnée Débutant
        with st.expander("🌊 Stage d'apnée : Niveau Débutant") : 
        
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("""
                **Découvrir le monde du silence et apprendre à respirer autrement.**
                
                **Objectifs :**
                
                ✓ Découvrir les bases de l'apnée et de la respiration consciente  
                ✓ Comprendre la physiologie de l'apnée et la sécurité  
                ✓ Apprendre les techniques de relaxation et de compensation  
                ✓ Explorer la profondeur en douceur et en confiance
                """)
            with col2:
                st.info("📸 **Image débutant apnée**")
                st.image("https://via.placeholder.com/400x300/3b82f6/ffffff?text=Débutant", use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Individuel**")
                st.write("• 1 jour (6h) ou 2 jours (12h)")
                st.write("• Coaching personnalisé, analyse vidéo")
                st.markdown('<p class="price-tag">350 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Groupe (4-6 personnes)**")
                st.write("• 2 jours complets (12h)")
                st.write("• Séances en mer + ateliers respiration")
                st.markdown('<p class="price-tag">220 € / personne</p>', unsafe_allow_html=True)
            
            st.success("✅ Aucun prérequis nécessaire — idéal pour une première approche de l'apnée")
            
        
        # Stage 3 - Apnée Avancé
        with st.expander("🏆 Stage d'apnée : Niveau Avancé"):
        
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("""
                **Repousser ses limites avec maîtrise, sécurité et conscience.**
                
                **Objectifs :**
                
                ✓ Approfondir la technique de descente et d'égalisation  
                ✓ Optimiser la performance des techniques de déplacement  
                ✓ Explorer les réflexes physiologiques d'adaptation  
                ✓ Développer la confiance et la gestion mentale à grande profondeur
                """)
            with col2:
                st.info("📸 **Image apnée avancée**")
                st.image("https://via.placeholder.com/400x300/1e3a8a/ffffff?text=Avancé", use_container_width=True)
            
            with st.expander("📋 Contenu du stage"):
                st.markdown("""
                ✓ Théorie avancée : physiologie, récupération, nutrition, sécurité profonde  
                ✓ Techniques : Mouthfill, free fall, duck dive, relaxation active, visualisation  
                ✓ Mise en pratique en milieu naturel jusqu'à 60 m (selon niveau)  
                ✓ Debriefings vidéo & plan d'entraînement personnalisé
                """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Individuel**")
                st.write("• 2 jours")
                st.write("• Bilan technique + suivi à distance (1 mois inclus)")
                st.markdown('<p class="price-tag">450 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Groupe (4-6 personnes)**")
                st.write("• 2 jours complets")
                st.write("• Immersions encadrées + ateliers")
                st.markdown('<p class="price-tag">300 € / personne</p>', unsafe_allow_html=True)
            
            st.warning("⚠️ **Pré-requis :** Bonne expérience apnée, capable de descendre à -30m, niveau équivalent AIDA 2 / SSI Level 1 minimum")
            
        
        # Stage 4 - Plongée scientifique
        with st.expander("🔬 Stage de plongée scientifique"):
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("""
                **Plonger pour observer, comprendre et protéger.**
                
                **Objectifs :**
                
                ✓ Découvrir la plongée scientifique et les protocoles d'étude marine  
                ✓ Apprendre les techniques d'échantillonnage et d'observation in situ  
                ✓ Acquérir les bases de la cartographie sous-marine et du suivi écologique  
                ✓ Se former aux gestes, méthodes et rigueurs du plongeur de recherche
                """)
            with col2:
                st.info("📸 **Image plongée scientifique**")
                st.image("https://via.placeholder.com/400x300/059669/ffffff?text=Scientifique", use_container_width=True)
            
            with st.expander("📋 Contenu du stage"):
                st.markdown("""
                ✓ Cours théoriques : écologie marine, méthodologie, sécurité scientifique  
                ✓ Ateliers pratiques : transects, quadrats, inventaires, photo quadrat  
                ✓ Mise en œuvre en mer : exercices réels sur site, encadrés par un professionnel  
                ✓ Introduction à la photo scientifique sous-marine
                """)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Individuel**")
                st.write("• 2 jours complets")
                st.write("• Programme intensif et personnalisé")
                st.markdown('<p class="price-tag">500 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Groupe (4-6 personnes)**")
                st.write("• 3 jours (théorie + terrain)")
                st.write("• Mise en pratique sur un site d'étude réel")
                st.markdown('<p class="price-tag">350 € / personne</p>', unsafe_allow_html=True)
            
            st.warning("⚠️ **Pré-requis :** Niveau minimum plongeur N2 ou équivalent. Possibilité de prêt de matériel selon disponibilité.")
            
        
            # Infos pratiques
            st.header("📍 Infos pratiques")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**📍 Lieux**")
                st.write("Nice, Côte d'Azur, Méditerranée")
                st.write("(autres destinations sur demande)")
            with col2:
                st.markdown("**⏱️ Durée**")
                st.write("1 à 3 jours selon le stage")
                st.write("Toute l'année")
            with col3:
                st.markdown("**👨‍🏫 Encadrement**")
                st.write("Diplômé d'État (DEJEPS)")
                st.write("Plongeur scientifique (3B, 2A)")
                st.write("Apnéiste de haut niveau")
            
            st.info("""
            **Matériel :** Matériel de plongée non inclus (sauf précisé) • Matériel scientifique prêté • 
            Mise à l'eau depuis embarcation de plongée
            """)
            
            st.markdown('<div class="citation">« Chaque stage est une expérience humaine et sensorielle. On apprend à mieux respirer, à mieux comprendre... et à mieux vivre. »</div>', unsafe_allow_html=True)
            
            st.button("📧 Réserver un stage", key="stages")

    with tab_Hyperbares : 
        st.title("⚙️ Services d'interventions en milieu hyperbare")

        st.header("🎓 Mes Qualifications")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🏅 Plongeur 2A")
            st.write("""
            **Classe 2A**
            
            Aptitudes à intervenir sans limites de charges ou de puissances d'outillage dans des 
            environnements sous-marins avec des risques techniques importants.
            """)
        with col2:
            st.markdown("### 🏅 Plongeur 3B")
            st.write("""
            **Classe 3B**
            
            Compétences avancées pour des plongées dans des conditions plus extrêmes et des profondeurs 
            plus importantes.
            """)
        with col3:
            st.markdown("### 🏅 Recycleur Hypoxique")
            st.write("""
            **Sans limite de profondeur**
            
            Plongées sans limite de profondeur, avec des équipements de recycleurs hypoxiques permettant 
            une plongée longue et sécurisée à de très grandes profondeurs.
            """)
        
        st.markdown("---")
        
        st.header("🔧 Types d'Interventions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ✓ Support pour les projets de recherche et études scientifiques  
            ✓ Opérateur sous-marin (tournages, publicités, clips)  
            ✓ Modèle subaquatique (marques, projets artistiques, tournages)  
            ✓ Interventions sur des infrastructures subaquatiques
            """)
        with col2:
            st.markdown("""
            ✓ Inspection et entretien des équipements immergés  
            ✓ Opérations de sauvetage et de déblaiement en milieu hyperbare  
            ✓ Interventions de recherche  
            ✓ Interventions de dépannage
            """)
        
        st.info("📸 **ESPACE GALERIE** - Photos d'interventions professionnelles")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("https://via.placeholder.com/350x250/1e3a8a/ffffff?text=Intervention+1", use_container_width=True)
        with col2:
            st.image("https://via.placeholder.com/350x250/3b82f6/ffffff?text=Intervention+2", use_container_width=True)
        with col3:
            st.image("https://via.placeholder.com/350x250/0ea5e9/ffffff?text=Intervention+3", use_container_width=True)
        
        st.markdown("---")
        
        st.header("⭐ Pourquoi me choisir ? / (remplacer par les dernière intervention réalisé)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🎯 Expertise certifiée")
            st.write("Classé 2A, 3B et plongeur recycleur hypoxique, pour des missions à toutes profondeurs avec peu de contraintes.")
        with col2:
            st.markdown("### 🛡️ Sécurité avant tout")
            st.write("Protocoles rigoureux pour chaque plongée, équipements de pointe et techniques éprouvées.")
        with col3:
            st.markdown("### ⚡ Flexibilité & réactivité")
            st.write("Disponible pour des missions urgentes ou de longue durée, adapté à vos besoins spécifiques.")
        
        st.markdown("---")
        
        st.header("💰 Tarifs")
        
        st.write("""
        Je propose des tarifs compétitifs basés sur le marché et ajustés en fonction de la complexité de la mission, 
        de la durée et des risques liés à l'intervention.
        
        **Voici un aperçu des tarifs moyens pratiqués :**
        """)
        
        tarifs_data = {
            "Type de plongée": [
                "Plongée simple (2B - 1 à 50 mètres)",
                "Plongée simple (2A - 1 à 50 mètres)",
                "Plongée technique (3B - 50 à 100 mètres)",
                "Plongée en recycleur hypoxique (>100 mètres)",
                "Interventions spécifiques (complexes)",
                "Forfaits missions longues (>5 jours)"
            ],
            "Tarif": [
                "À partir de 600 € / jour",
                "À partir de 800 € / jour",
                "À partir de 1 200 € / jour",
                "Sur devis",
                "À partir de 1 500 € / jour",
                "Sur demande (réduction possible)"
            ]
        }
        
        import pandas as pd
        df_tarifs = pd.DataFrame(tarifs_data)
        st.table(df_tarifs)
        
        st.info("💡 Pour des devis personnalisés ou des missions urgentes, n'hésitez pas à me contacter directement.")
        
        st.button("📧 Demander un devis", key="hyperbare")

    # PAGE PRODUITS EN LIGNE
    with tab_Cours_en_ligne :
        st.title("🛒 Produits en ligne")
        
        st.info("📸 **ESPACE IMAGE HEADER** - Montage de photos/vidéos produits")
        st.image("https://via.placeholder.com/1200x400/059669/ffffff?text=Produits+en+ligne", use_container_width=True)
        
        st.write("""
        Accédez à mes ressources professionnelles pour enrichir vos projets, formations ou simplement pour approfondir 
        vos connaissances.
        """)
        
        st.markdown("---")
        
        # Banque d'images
        st.header("📸 Banque d'images et vidéos")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Vidéos 4K et Photos Haute Qualité
            
            Des années d'expéditions, de plongées et d'explorations capturées en images professionnelles.
            
            **Contenu disponible :**
            
            ✓ Faune marine méditerranéenne et tropicale  
            ✓ Apnée profonde et performances sportives  
            ✓ Plongées scientifiques et missions de recherche  
            ✓ Expéditions (Groenland, fjords, récifs)  
            ✓ Apnée sous glace  
            ✓ Portraits sous-marins
            
            **Formats :**
            
            • Vidéos : 4K, 60fps, ProRes et H.264  
            • Photos : RAW et JPEG haute résolution  
            • Licences disponibles : usage personnel, commercial, éditorial
            """)
        with col2:
            st.info("📸 **Aperçu galerie**")
            st.image("https://via.placeholder.com/400x300/0ea5e9/ffffff?text=Galerie+1", use_container_width=True)
            st.image("https://via.placeholder.com/400x300/1e3a8a/ffffff?text=Galerie+2", use_container_width=True)
            st.button("🔍 Parcourir la banque d'images", key="banque")
        
        st.markdown("---")
        
        # Cours en ligne
        st.header("🎓 Cours en ligne")
        
        st.write("""
        Formez-vous à votre rythme avec des cours structurés, basés sur l'expérience terrain et la science.
        """)
        
        cours_list = [
            {
                "titre": "Physiologie de l'apnée",
                "description": "Comprendre les mécanismes physiologiques de l'apnée et optimiser vos performances",
                "duree": "4h de contenu",
                "niveau": "Tous niveaux",
                "prix": "89 €"
            },
            {
                "titre": "Respiration & Performance",
                "description": "Techniques de respiration pour le sport, la gestion du stress et le bien-être",
                "duree": "3h de contenu",
                "niveau": "Débutant",
                "prix": "69 €"
            },
            {
                "titre": "Apnée : de débutant à avancé",
                "description": "Programme complet pour progresser en apnée de manière autonome et sécurisée",
                "duree": "8h de contenu",
                "niveau": "Débutant à avancé",
                "prix": "149 €"
            },
            {
                "titre": "Plongée scientifique : méthodes et protocoles",
                "description": "Introduction aux techniques de collecte de données sous-marines",
                "duree": "5h de contenu",
                "niveau": "Plongeur N2 minimum",
                "prix": "119 €"
            },
            {
                "titre": "Photographie sous-marine",
                "description": "Techniques, réglages et composition pour des images professionnelles",
                "duree": "6h de contenu",
                "niveau": "Intermédiaire",
                "prix": "129 €"
            },
            {
                "titre": "Vidéographie sous-marine 4K",
                "description": "De la prise de vue au montage, créez des films immersifs",
                "duree": "7h de contenu",
                "niveau": "Intermédiaire à avancé",
                "prix": "159 €"
            }
        ]
        
        cols = st.columns(2)
        for idx, cours in enumerate(cours_list):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"### 📚 {cours['titre']}")
                    st.write(cours['description'])
                    st.write(f"⏱️ **Durée :** {cours['duree']}")
                    st.write(f"📊 **Niveau :** {cours['niveau']}")
                    st.markdown(f'<p class="price-tag">{cours["prix"]}</p>', unsafe_allow_html=True)
                    st.button(f"Accéder au cours", key=f"cours_{idx}")
                    st.markdown("---")
        
        st.info("""
        💡 **Tous les cours incluent :**
        
        ✓ Vidéos HD téléchargeables  
        ✓ Fiches techniques PDF  
        ✓ Exercices pratiques  
        ✓ Accès à vie  
        ✓ Mises à jour gratuites
        """)

# PAGE CONTACT
elif st.session_state.menu_selection == "Contact":
    st.title("📧 Contact")
    
    st.write("""
    Pour toute demande d'information, réservation ou projet personnalisé, n'hésitez pas à me contacter.
    
    Je réponds généralement sous 48h.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Formulaire de contact")
        
        with st.form("contact_form"):
            nom = st.text_input("Nom complet *")
            email = st.text_input("Email *")
            telephone = st.text_input("Téléphone")
            
            sujet = st.selectbox(
                "Sujet de votre demande *",
                [
                    "Mentoring",
                    "Coaching Apnée",
                    "Conférence",
                    "Stage",
                    "Services Hyperbare",
                    "Banque d'images",
                    "Cours en ligne",
                    "Autre"
                ]
            )
            
            message = st.text_area("Votre message *", height=200)
            
            col_a, col_b = st.columns([1, 3])
            with col_a:
                submitted = st.form_submit_button("Envoyer", use_container_width=True)
            
            if submitted:
                if nom and email and message:
                    st.success("✅ Message envoyé avec succès ! Je vous répondrai dans les plus brefs délais.")
                else:
                    st.error("⚠️ Veuillez remplir tous les champs obligatoires (*)")
    
    with col2:
        st.markdown("### 📞 Coordonnées")
        st.markdown("""
        **Email :**  
        gilles.gambini@hotmail.fr
        
        **Localisation :**  
        Nice, Côte d'Azur, France
        
        **Disponibilité :**  
        Interventions en France et à l'international
        """)
        
        st.markdown("---")
        
        st.markdown("### 🌐 Suivez-moi")
        st.markdown("""
        [Instagram](#) • [LinkedIn](#) • [Facebook](#)
        """)
        
        st.info("📸 **Photo profil**")
        st.image("https://via.placeholder.com/300x400/1e3a8a/ffffff?text=Photo+Profil", use_container_width=True)

elif st.session_state.menu_selection == "Qui suis-je ? +CV":
    st.write("""
    C'est ce qui guide chacun de mes coups de palme.
    
    Ingénieur en écologie marine et plongeur scientifique, je consacre ma carrière à l'étude des milieux sous-marins, 
    entre recherche scientifique, exploration et image.
    
    Sportif de haut niveau en apnée profonde, je mets à l'épreuve mes connaissances de la physiologie humaine dans des 
    environnements extrêmes que ce soit à travers mes performances, mes enseignements ou mes collaborations avec des 
    programmes de recherche, notamment auprès de l'Agence Spatiale Européenne (ESA).
    
    Cette collaboration m'a conduit à devenir astronaute analogue, participant à des simulations de missions spatiales, 
    où la maîtrise du corps et de l'esprit est mise à rude épreuve.
    
    À la suite de ces expériences, une proposition officielle de formation au programme spatial m'a été faite, un honneur 
    rare qui témoigne de la convergence entre mes travaux en milieu extrême, mes recherches scientifiques et mes aptitudes 
    physiques et mentales.
    """)

    st.write("""
    Au fil des années, j'ai réuni deux mondes : la rigueur scientifique et l'exploration humaine.
    
    Mes plongées et mes missions m'ont conduit des laboratoires aux fjords glacés du Groenland, des récifs méditerranéens 
    aux abysses caribéens, toujours animé par la même passion : découvrir, préserver, faire connaître et aimer l'océan.
    
    Aujourd'hui, je partage cette expérience à travers des cours, formations, conférences, coachings personnalisés et une 
    banque d'images dédiée à la mer et à ses habitants.
    
    Mon objectif est simple : **transmettre, inspirer et reconnecter chacun à la nature, avec respect, curiosité et émerveillement.**
    
    Les revenus issus de mes formations et de mes images servent à financer de nouvelles expéditions scientifiques, à soutenir 
    ma carrière sportive en apnée de haut niveau, et à poursuivre mes recherches sur la physiologie humaine en milieux extrêmes.
    """)
    
# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**© 2024 Gilles Gambini**")
with col2:
    st.markdown("Apnéiste professionnel • Biologiste marin")
with col3:
    st.markdown("[Mentions légales](#) • [CGV](#)")