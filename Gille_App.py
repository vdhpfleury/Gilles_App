import streamlit as st
from streamlit_option_menu import option_menu
import base64
from carrousel import carrousel, preload_images
import smtplib
from email.mime.text import MIMEText
import time as time
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Gilles Gambini - Apnéiste & Biologiste Marin",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)




# Initialiser le session_state pour la navigation
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "Accueil"

if 'images_ICE' not in st.session_state:
    preload_images("Photo/ICE")
    st.session_state.images_ICE = True

if 'images_APNEE' not in st.session_state:
    preload_images("Photo/APNEE")
    st.session_state.images_APNEE = True

if 'images_ACC' not in st.session_state:
    preload_images("Photo/CARR_ACCEUIL")
    st.session_state.images_ACC = True


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

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def send_email(email_sender, email_receiver, subject, main_text, password="wycs fblq gmci ffpz"):
    try:
        msg = MIMEText(main_text)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = subject

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Email sent successfully! 🚀')
        time.sleep(2)
    except Exception as e:
        st.error(f"Erreur lors de l’envoi de l’e-mail : {e}")


@st.dialog("Me contacter")
def show_popup(Sujet_index, sub_topic, rdv=False):
    st.markdown("### 📝 Formulaire de contact")
    
    with st.form("contact_form"):
        nom = st.text_input("Nom complet *", key="fc_out_app_name")
        email = st.text_input("Email *", key="fc_out_app_mail")
        telephone = st.text_input("Téléphone", key="fc_out_app_phone")
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
            ],
            index=Sujet_index,
            key="fc_out_app_topic"
        )
        
        if rdv==True : 
            col1, col2 = st.columns(2)
            with col1:
                event_date = st.date_input("Jours souhiaté", value=None)
            with col2:
                event_time = st.time_input("A quelle heure ?")

            if event_date:
                event_datetime = datetime.combine(event_date, event_time)
                st.info(f"Rdv plannifié le: {event_datetime.strftime('%Y-%m-%d %H:%M')}")


        message = st.text_area("Votre message *", height=200, key="fc_out_app_message")
        submitted = st.form_submit_button("Envoyer", use_container_width=True)#, key="fc_out_app_submitted")
        
        if submitted:
            if nom and email and message:
                body = f" name : \t{nom} \n email : \t{email} \n tel : \t{telephone} \n sujet de la demande : {sujet} \n sous sujet : {sub_topic} \n\n ----- Message du client ----- \n {message}"
                if rdv == True : 
                    body += f"\n\n Rdv souhaité le: {event_datetime.strftime('%Y-%m-%d %H:%M')}"
                
                send_email(
                    email_sender="inconitocx@gmail.com", 
                    email_receiver="fleury.vdhp@gmail.com ",#"gilles.gambini@hotmail.fr", 
                    subject=sujet, 
                    main_text=body, 
                    password="wycs fblq gmci ffpz"
                )
                st.rerun()
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires (*)")
                st.rerun()
            


test = "wycs fblq gmci ffpz"
fb = img_to_base64("Photo/RESEAU/facebook.png")
li = img_to_base64("Photo/RESEAU/linkedIn.png")
ig = img_to_base64("Photo/RESEAU/Instagram.png")


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
        st.markdown('<p class="sub-header">Apnéiste professionnel • Instructeur • Biologiste marin • Plongeur scientifique • Scaphandrier • Photographe </p>', unsafe_allow_html=True)


        #st.markdown('<p class="sub-header"> Suivez moi sur mes réseaux </p>', unsafe_allow_html=True)
        #st.markdown(f"""
        #<div style="display: flex; justify-content: center; gap: 20px;">
        #    <p>Suivez moi sur mes réseaux</p>
        #</div>
        #""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: flex; justify-content: center; gap: 20px;">
        <a href="https://www.facebook.com/share/1BhzPeJTXS/" target="_blank">
            <img src="data:image/png;base64,{fb}" width="40">
        </a>
        <a href="https://www.linkedin.com/in/gilles-gambini-5298a287/" target="_blank">
            <img src="data:image/png;base64,{li}" width="40">
        </a>
        <a href="https://www.instagram.com/gillesgambini/" target="_blank">
            <img src="data:image/png;base64,{ig}" width="40">
        </a>
        </div>
        """, unsafe_allow_html=True)


        #st.markdown('<h1 class="main-header">📋 Services</h1>', unsafe_allow_html=True)
        st.markdown('<h1 class="main-header">Mes Services</h1>', unsafe_allow_html=True)
    
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
        #st.markdown('<p class="sub-header">le details des services est disponible plus bas sur cette page</p>', unsafe_allow_html=True)
       
       

        
    # Bio
    st.header("📋 Détails des services")


    tab_Mentoring, tab_Coaching, tab_Conferences, tab_Stages, tab_Hyperbares, tab_banque_image, tab_Cours_en_ligne = st.tabs(["Mentoring", "Coaching Apnée", "Conférences", "Stages", "Service Hyperbares", "Banque d'image", "Cours en ligne"])
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
            #st.image("Photo/APNEE/img_apnee_16.jpg", use_container_width=False)

            carrousel("Photo/APNEE", height=300, duration=3)

                    
        
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
        
        #st.markdown("---")
        
        # Formules de mentoring
        st.header("📋 Formules de Mentoring")
        
        # Formule 1
        with st.expander("🎯 Mentoring individuel « Exploration & Performance »", expanded=False):
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
                mentorin1 = st.button("Réserver un appel découverte", key="mentoring1", type="primary")
            
            if mentorin1 : 
                show_popup(Sujet_index=0, sub_topic="Mentoring individuel - Réservation d'un appel découverte", rdv=True)
                
        
        # Formule 2
        with st.expander("👥 Mentoring collectif « Ocean Skills »"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Apprenez, échangez et progressez ensemble en fonction de vos objectifs (groupes par thématiques).**
                
                ✓ Petits groupes (3 à 6 personnes)  
                ✓ 1 visio mensuel (1h30)  
                ✓ Ressources exclusives (PDF, vidéos, fiches techniques)  
                ✓ Suivi collectif + espace d'échange privé
                """)
            with col2:
                st.markdown('<p class="price-tag">60 € / mois</p>', unsafe_allow_html=True)
                mentoring2 = st.button("Rejoindre un groupe", key="mentoring2", type="primary")

            if mentoring2: 
                show_popup(Sujet_index=0, sub_topic="Mentoring collectif - Rejoindre un groupe", rdv=False)
                                    
        
        # Formule 3
        with st.expander("💼 Mentoring carrière « Carrière bleue »"):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("""
                **Pour construire un parcours professionnel aligné avec vos valeurs et votre passion pour l'océan.**
                
                Ce mentoring offre un accompagnement individuel et sur mesure de vos besoins grâce à : 

                ✓ 1 séance d'1h/mois : orientation, stratégie, CV, préparation à l'emploi ou à la mission  
                ✓ Accompagnement sur les choix de carrière, stages, formations et projets scientifiques, réseau  
                ✓ Retours d'expérience et conseils concrets issus du terrain
                
                **Idéal pour :** Étudiants, jeunes chercheurs, techniciens ou naturalistes souhaitant s'engager dans 
                une carrière marine ou scientifique.
                """)
            with col2:
                st.markdown('<p class="price-tag">100 € / mois</p>', unsafe_allow_html=True)
                mentoring3 = st.button("Me contacter", key="mentoring3", type="primary")
            
            if mentoring3: 
                show_popup(Sujet_index=0, sub_topic="Mentoring - Carrière Bleu", rdv=False)
                
        
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
                mentoring4 = st.button("Candidater", key="mentoring4", type="primary")

            if mentoring4: 
                show_popup(Sujet_index=0, sub_topic="Mentoring - Carrière Filleul", rdv=False)
     
        
        #st.markdown("---")
        
        st.markdown("### 🎯 Pourquoi ce mentoring est différent")
        col1, col2 = st.columns(2)
        with col1:
            st.write("✓ Approche croisant science, performance et exploration")
            st.write("✓ Expérience du terrain (missions, expéditions, plongées profondes)")
        with col2:
            st.write("✓ Écoute, rigueur et accompagnement humain")
            st.write("✓ Objectif : autonomie, progression, confiance")
        
        #st.info("📸 **ESPACE IMAGE** - Photo de mentorat en action ou d'expédition")

    with tab_Coaching : 
        st.title("💙 Coaching Apnée : Suivi personnalisé")
        col1, col2 = st.columns(2)
        with col1 :
            st.subheader("Progressez à votre rythme, avec un encadrement sur mesure")
                
            st.write("""
            Que vous soyez débutant, confirmé ou compétiteur, ce programme de coaching vous accompagne pas à pas vers vos 
            objectifs en apnée.
            
            Chaque mois, nous construisons ensemble une progression adaptée à votre niveau, votre environnement et vos contraintes de vie.
            
            **L'objectif : vous aider à progresser durablement, sans surentraînement ni perte de motivation.**
            """)
        with col2 : 
            st.markdown("### 🎯 Le concept")
            st.write("""
            Une approche simple, efficace et personnalisée. Une séance par mois, des exercices ciblés, et un suivi continu.
            
            **Chaque mois, vous bénéficiez de :**
            
            ✓ 1 appel de suivi (30 min à 1h) pour faire le point sur vos sensations, vos progrès et ajuster la stratégie  
            ✓ Un bloc d'exercices mensuel : préparation à sec, relaxation, renforcement, apnée, visualisation ou travail spécifique  
            ✓ Un plan de progression clair ajusté à vos capacités et à votre agenda  
            ✓ Un échange direct (mail ou message) pour toute question entre deux sessions
            """)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 👥 Pour qui ?")
            st.write("🌊 Apnéistes débutants souhaitant progresser sereinement")
            st.write("📈 Pratiquants confirmés cherchant à franchir un cap ou progresser")
            st.write("🏆 Apnéistes de haut niveau désirant préparer des compétitions")
            st.write("🧘 Sportifs voulant travailler la respiration et la gestion mentale")
            st.write("📸 Photographes sous-marins souhaitant améliorer leur aisance sous l'eau")
        with col2:
            st.markdown("### Contenue et tarifs")
            #st.markdown('<div class="service-card">', unsafe_allow_html=True)
            st.write("**Sans engagement**")
            st.write("✓ 1 visio/appel mensuel")
            st.write("✓ Bloc d'exercices personnalisé")
            st.write("✓ Suivi et adaptation mensuelle")
            st.markdown('<p class="price-tag">100 € / mois</p>', unsafe_allow_html=True)
            coaching = st.button("Réserver mon appel découverte", key="coaching", type="primary")
        
        if coaching : 
            show_popup(Sujet_index=1, sub_topic="Coacing en apnée - suivit personnalisé", rdv=True)

        st.markdown("### ⭐ Les avantages de ce coaching ")
        st.write("✓ Basé sur la physiologie et la préparation mentale du sportif de haut niveau")
        st.write("✓ Adapté à tous les niveaux et styles d'apnée")
        st.write("✓ Approche globale : physique, mental, technique et émotionnel")
        st.write("✓ Suivi par un apnéiste professionnel diplômé d'État spécialisé en physiologie hyperbare")

    with tab_Conferences : 
        st.title("🎤 Conférences - Science, Océan & Performance Humaine")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1 : 
            st.write("### 🎯 Thématiques clés")
            st.write("""
            • La physiologie de l'extrême : ce que l'apnée nous apprend sur le corps humain  
            • Explorer et préserver : science et aventure au service de la connaissance  
            • Le souffle comme outil de performance et d'équilibre  
            • Leadership et gestion de mission en milieu extrême  
            • L'océan comme source d'inspiration et d'humilité
            """)


        
        with col2 : 
            st.write("### Explorer, inspirer, reconnecter")
            st.write("""
            À travers mes expériences d'apnéiste professionnel, de biologiste marin et de plongeur scientifique, je partage 
            une vision singulière du monde : celle d'un homme qui explore les profondeurs pour mieux comprendre la vie et ses limites.
            
            Mes conférences sont une invitation à la découverte : celle de l'océan, du corps et de l'esprit humain.
            
            Entre images d'expédition, récits authentiques et apports scientifiques, elles offrent une expérience inspirante 
            et sensorielle, à la croisée de la science, du sport et de l'aventure.
            """)
        with col3 : 
            st.markdown("### Une approche unique")
            st.write("""
            Alliant rigueur scientifique, sensibilité artistique et expérience de terrain, mes interventions s'adressent à tous les publics :
            
            • Entreprises & séminaires de direction  
            • Institutions & collectivités  
            • Écoles, universités, festivals & musées
            """)

        conference = st.button("📧 Demander une conférence", key="conf", type="primary")

        if conference : 
            show_popup(Sujet_index=2, sub_topic="Conférence - Demande de réservation", rdv=True)
        
        
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
            stages = st.button("📧 Réserver un stage", key="stages", type="primary")
            if stages : 
                show_popup(Sujet_index=3, sub_topic="Demande de Stage", rdv=False)

    
    
        with col2:
            st.info("📸 **ESPACE IMAGE HEADER** - Photo de stage en action")
            st.image("https://via.placeholder.com/1200x400/0ea5e9/ffffff?text=Stages", use_container_width=True)
           
        
        # Stage 1 - Apnée sous glace
        with st.expander("❄️ Stage d'apnée sous glace : Sur mesure"):
        
            col1, col2 = st.columns(2)
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
            
                st.write("📋 **Contenu du stage**")
                st.markdown("""
                ✓ Introduction à la physiologie du froid et à la thermorégulation  
                ✓ Préparation mentale et respiratoire spécifique aux milieux extrêmes  
                ✓ Mise en place logistique (sécurité, ligne de vie, ouverture de trou, secours)  
                ✓ Immersion sous glace en apnée : exploration progressive et guidée  
                ✓ Debriefing, retour d'expérience
                """)
            with col2:
                st.info("📸 **ESPACE IMAGE HEADER** - Photo de stage en action")
                st.image("https://via.placeholder.com/1200x400/0ea5e9/ffffff?text=Stages", use_container_width=True)
           
        
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Formule individuelle**")
                st.write("• 1 à 3 jours")
                st.write("• Encadrement personnalisé")
                st.markdown('<p class="price-tag">À partir de 300 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Formule groupe (2-6 personnes)**")
                st.write("• 1 à 3 jours")
                st.write("• Gestion logistique incluse")
                st.markdown('<p class="price-tag">À partir de 120 € / personne / jour</p>', unsafe_allow_html=True)
            
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
                
                ✓ Approfondir la technique de descente et compensation  
                ✓ Optimiser la performance des techniques de déplacement  
                ✓ Explorer les réflexes physiologiques d'adaptation  
                ✓ Développer la confiance et la gestion mentale à grande profondeur
                """)

                st.write("📋 **Contenu du stage**")
                st.markdown("""
                ✓ Théorie avancée : physiologie, récupération, nutrition, sécurité profonde  
                ✓ Techniques : Mouthfill, free fall, duck dive, relaxation active, visualisation  
                ✓ Mise en pratique en milieu naturel jusqu'à 60 m (selon niveau)  
                ✓ Debriefings vidéo & plan d'entraînement personnalisé
                """)


            with col2:
                st.info("📸 **Image apnée avancée**")
                st.image("https://via.placeholder.com/400x300/1e3a8a/ffffff?text=Avancé", use_container_width=True)
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Formule individuelle**")
                st.write("• 2 jours")
                st.write("• Bilan technique + suivi à distance (1 mois inclus)")
                st.markdown('<p class="price-tag">450 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Formule de groupe (4-6 personnes)**")
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

                st.write("📋 **Contenu du stage**")
                st.markdown("""
                ✓ Cours théoriques : écologie marine, méthodologie, sécurité scientifique  
                ✓ Ateliers pratiques : transects, quadrats, inventaires, photo quadrat  
                ✓ Mise en œuvre en mer : exercices réels sur site, encadrés par un professionnel  
                ✓ Introduction à la photo scientifique sous-marine
                """)

            with col2:
                st.info("📸 **Image plongée scientifique**")
                st.image("https://via.placeholder.com/400x300/059669/ffffff?text=Scientifique", use_container_width=True)
            

            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Formule individuelle**")
                st.write("• 2 jours complets")
                st.write("• Programme intensif et personnalisé")
                st.markdown('<p class="price-tag">500 € / jour</p>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Formule de groupe (4-6 personnes)**")
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
        
        
        st.header("Tarifs")
        
        st.write("""
        Je propose des tarifs compétitifs basés sur le marché et ajustés en fonction de la complexité de la mission, 
        de la durée et des risques liés à l'intervention.
        
        **Voici un aperçu des tarifs moyens pratiqués :**
        """)
        
        tarifs_data = {
            "Type de plongée": [
                "Plongée simple (2B - 1 à 50 mètres)",
                "Plongée simple (2A - 1 à 50 mètres)",
                "Prestation moniteur apnée ou plongée",
                "Plongée technique (3B - 50 à 100 mètres)",
                "Plongée en recycleur hypoxique (>100 mètres)",
                "Forfaits missions longues (>5 jours)"
            ],
            "Tarif": [
                "À partir de 300 € / jour",
                "À partir de 600 € / jour",
                "À partir de 250 € / jour",
                "À partir de 1 000 € / jour",
                "Sur devis",
                "Sur demande"
            ]
        }
        
        import pandas as pd
        df_tarifs = pd.DataFrame(tarifs_data)
        st.table(df_tarifs)
        
        st.info("💡 Pour des devis personnalisés ou des missions urgentes, n'hésitez pas à me contacter directement.")
        
        hyperbare = st.button("📧 Demander un devis", key="hyperbare", type="primary")

        if hyperbare : 
            show_popup(Sujet_index = 4, sub_topic="Demande de devis - services hyperbare", rdv=False)

    # PAGE PRODUITS EN LIGNE
    with tab_banque_image : 
        # Banque d'images
        st.header("📸 Banque d'images et vidéos")
        
        #col1, col2 = st.columns([2, 1])
        #with col1:
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
        #with col2:
            #st.info("📸 **Aperçu galerie**")
            #st.image("https://via.placeholder.com/400x300/0ea5e9/ffffff?text=Galerie+1", use_container_width=True)
            #st.image("https://via.placeholder.com/400x300/1e3a8a/ffffff?text=Galerie+2", use_container_width=True)
        banque = st.link_button("🔍 Voir la banque d'images", "https://www.pond5.com/fr/artist/gillesgambini679", type="primary")
            
    
    with tab_Cours_en_ligne :
        st.title("Cours en ligne")
        st.write("""
        Accédez à mes ressources professionnelles pour enrichir vos projets, formations ou simplement pour approfondir 
        vos connaissances.
        """)
        st.write("Retrouver tout mes cours en ligne sur la plateforme **UDEMY**.")
        st.warning("Synchronisation des plateformes en cours")
        

    st.markdown("---")
    st.title("📧 Contact")
    
    st.write("""
    Pour toute demande d'information, réservation ou projet personnalisé, n'hésitez pas à me contacter.
    
    Je réponds généralement sous 48h.
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Formulaire de contact")
        
        with st.form("contact form"):
            nom = st.text_input("Nom complet *", key="fc_in_app_name")
            email = st.text_input("Email *", key="fc_in_app_mail")
            telephone = st.text_input("Téléphone", key="fc_in_app_phone")
            
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
                ],
                key="fc_in_app_topic"
            )
            
            message = st.text_area("Votre message *", height=200, key="fc_in_app_message")
            
            col_a, col_b = st.columns([1, 3])
            with col_a:
                submitted = st.form_submit_button("Envoyer", use_container_width=True, type="primary")
            
            if submitted:
                if nom and email and message:
                    body = f" name : \t{nom} \n email : \t{email} \n tel : \t{telephone} \n sujet de la demande : {sujet} \n\n ----- Demande ----- \n {message}"
                    send_email(
                        email_sender="inconitocx@gmail.com", 
                        email_receiver="gilles.gambini@hotmail.fr", 
                        subject=sujet, 
                        main_text=body, 
                        password="wycs fblq gmci ffpz"
                        )

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
        col1, col2 = st.columns(2)
        with col1 : st.markdown("### 🌐 Suivez-moi")
        with col2 : 
            st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 20px;">
            <a href="https://www.facebook.com/share/1BhzPeJTXS/" target="_blank">
                <img src="data:image/png;base64,{fb}" width="40">
            </a>
            <a href="https://www.linkedin.com/in/gilles-gambini-5298a287/" target="_blank">
                <img src="data:image/png;base64,{li}" width="40">
            </a>
            <a href="https://www.instagram.com/gillesgambini/" target="_blank">
                <img src="data:image/png;base64,{ig}" width="40">
            </a>
            </div>
            """, unsafe_allow_html=True)
        
        st.image("Photo/profil_02.png", use_container_width=True)
    
    st.markdown("---")

    carrousel("Photo/CARR_ACCEUIL", height=500, duration=3)

    

    st.markdown("---")

    st.header("Quelques interview")
    col1, col2, col3 = st.columns(3)

    with col1 : 
        st.video("https://www.youtube.com/watch?v=Qf6NSbwm6iw")
        st.write("*France 3*")
    with col2 :
        st.video("https://www.youtube.com/watch?v=Uz1VxVH-iyY")
        st.write("*Université Côte d'Azur*")
    with col3 :
        st.video("https://www.youtube.com/watch?v=gvhg9zYuwpc")
        st.write("*Pure Ocean*")

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
                submitted = st.form_submit_button("Envoyer", use_container_width=True, type="primary")
            
            if submitted:
                if nom and email and message:
                    st.success("✅ Message envoyé avec succès ! Je vous répondrai dans les plus brefs délais.")
                    #ajouter la logisue d'envoie de l'email
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
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1 : st.markdown("### 🌐 Suivez-moi")
        with col2 : 
            st.markdown(f"""
            <div style="display: flex; justify-content: center; gap: 20px;">
            <a href="https://www.facebook.com/share/1BhzPeJTXS/" target="_blank">
                <img src="data:image/png;base64,{fb}" width="40">
            </a>
            <a href="https://www.linkedin.com/in/gilles-gambini-5298a287/" target="_blank">
                <img src="data:image/png;base64,{li}" width="40">
            </a>
            <a href="https://www.instagram.com/gillesgambini/" target="_blank">
                <img src="data:image/png;base64,{ig}" width="40">
            </a>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("📸 **Photo profil**")
        st.image("https://via.placeholder.com/300x400/1e3a8a/ffffff?text=Photo+Profil", use_container_width=True)

elif st.session_state.menu_selection == "Qui suis-je ? +CV":
    col1, col2 = st.columns([1,3])
    with col1 : 
        st.image("Photo/profil_01.JPG", caption="Profil", use_container_width=True)

    with col2 :
        st.markdown('<h1 class="main-header">Gilles Gambini</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Apnéiste professionnel • Biologiste marin • Plongeur scientifique • Photographe</p>', unsafe_allow_html=True)

        st.markdown('<h1 class="main-header">Certifications</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">DEJEPS • Plongeur 2A, 3B • Recycleur Hypoxique</p>', unsafe_allow_html=True)

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
    #st.markdown("[Mentions légales](#) • [CGV](#)")
    st.markdown("Toute les photos sont sonmise aux droits d'auteur. Me contacter pour toute utilisation.")
