# carrousel.py - Version optimisée
import os
import base64
from functools import lru_cache
from PIL import Image
from io import BytesIO
import streamlit as st

# ---- CONFIGURATION ----
MAX_IMAGE_SIZE = (1200, 800)  # Redimensionner si plus grand
JPEG_QUALITY = 95  # Qualité de compression

# ---- UTILITAIRES ----
@lru_cache(maxsize=1)
def list_files_cached(folder):
    """Liste les fichiers d'un dossier (mise en cache)."""
    return tuple(
        os.path.join(folder, f) 
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
    )

@lru_cache(maxsize=32)
def img_to_base64_optimized(path: str):
    """Convertit et optimise une image en base64."""
    try:
        img = Image.open(path)
        
        # Convertir en RGB si nécessaire
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Redimensionner si trop grande
        if img.size[0] > MAX_IMAGE_SIZE[0] or img.size[1] > MAX_IMAGE_SIZE[1]:
            img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # Compresser en JPEG
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=True)
        return base64.b64encode(buffer.getvalue()).decode()
    except Exception as e:
        st.error(f"Erreur lors du chargement de {path}: {e}")
        return None

@lru_cache(maxsize=1)
def load_folder_base64(folder: str):
    """Charge toutes les images d'un dossier de manière optimisée."""
    files = list_files_cached(folder)
    images = []
    
    for f in files:
        img_b64 = img_to_base64_optimized(f)
        if img_b64:
            images.append(img_b64)
    
    return tuple(images)

# ---- COMPOSANT CARROUSEL ----
def carrousel(folder: str, height=400, duration=4, lazy_load=True):
    """
    Affiche un carrousel HTML/CSS optimisé.
    
    Args:
        folder: chemin du dossier contenant les images
        height: hauteur du carrousel en pixels
        duration: durée entre les transitions en secondes
        lazy_load: activer le lazy loading (True par défaut)
    """
    # Vérifier l'existence du dossier
    if not os.path.exists(folder):
        st.error(f"Dossier introuvable : {folder}")
        return
    
    # Charger les images (utilise le cache)
    images_base64 = load_folder_base64(folder)
    
    if len(images_base64) == 0:
        st.warning(f"Aucune image trouvée dans : {folder}")
        return
    
    # Limiter le nombre d'images pour performance
    max_images = 10
    if len(images_base64) > max_images:
        #st.info(f"Affichage limité à {max_images} images sur {len(images_base64)}")
        images_base64 = images_base64[:max_images]
    
    # CSS optimisé avec GPU acceleration
    animations = "\n".join([
        f".slider img:nth-child({i+1}) {{ animation-delay: {i * duration}s; }}"
        for i in range(len(images_base64))
    ])
    
    total_duration = len(images_base64) * duration
    
    # HTML avec lazy loading optionnel
    loading_attr = 'loading="lazy"' if lazy_load else ''
    
    html = f"""
    <div class="slider">
        {
            ''.join([
                f'<img src="data:image/jpeg;base64,{img}" {loading_attr} alt="Image {i+1}"/>' 
                for i, img in enumerate(images_base64)
            ])
        }
    </div>
    <style>
    .slider {{
        width: 100%;
        height: {height}px;
        overflow: hidden;
        position: relative;
        background-color: #000;
    }}
    .slider img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        position: absolute;
        animation: slide {total_duration}s infinite;
        opacity: 0;
        will-change: opacity;
        transform: translateZ(0);
    }}
    {animations}
    @keyframes slide {{
        0% {{ opacity: 0; }}
        8% {{ opacity: 1; }}
        25% {{ opacity: 1; }}
        33% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}
    </style>
    """
    
    st.components.v1.html(html, height=height + 50, scrolling=False)

# ---- FONCTION DE PRÉCHARGEMENT (optionnel) ----
def preload_images(folder: str):
    """Précharge les images au démarrage de l'app (à appeler dans le main)."""
    load_folder_base64(folder)