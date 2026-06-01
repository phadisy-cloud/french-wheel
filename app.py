import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration de la page en mode large
st.set_page_config(page_title="Roue Sensorielle des Rillettes", layout="wide")

# ============================================================
# 1. CONSTANTES & CONFIGURATION DU SYSTÈME
# ============================================================
CAT_APPEARANCE = "<b>Aspect</b>"
CAT_AROMA = "<b>Arôme</b>"
CAT_TASTE = "<b>Goût</b>"
CAT_TEXTURE = "<b>Texture</b>"
CAT_OVERALL = "<b>Global</b>"

R_BASE = "Recette de Base"
R_1 = "Recette 1"
R_2 = "Recette 2"
R_3 = "Recette 3"
R_4 = "Recette 4"

# Codes couleur pour la couronne extérieure (Recettes)
RECIPE_COLORS = {
    R_BASE: "#A6A6A6",  # Gris
    R_1: "#F4B6ED",     # Rose clair
    R_2: "#D633B0",     # Magenta
    R_3: "#94C4EB",     # Bleu clair
    R_4: "#4A004A"      # Violet foncé
}

# Les 5 nuances de jaune/doré pour les catégories internes
FAMILY_TRACK_COLORS = {
    CAT_APPEARANCE: "#FFD966",   # Groupe 1 : Or brillant / Jaune
    CAT_AROMA:      "#F4C430",   # Groupe 2 : Jaune safran
    CAT_TASTE:      "#FFEAA7",   # Groupe 3 : Jaune pastel doux
    CAT_TEXTURE:    "#C29200",   # Groupe 4 : Or ambré foncé
    CAT_OVERALL:    "#FFF0C2"    # Groupe 5 : Crème ivoire clair
}

# Matrice restrictive des attributs autorisés (en français)
ALLOWED_ATTRIBUTES = {
    CAT_APPEARANCE: ["Pâle", "Coloré", "Épais", "Particules", "Huileux"],
    CAT_AROMA: ["Poisson", "Échalote", "Végétal", "Poivron", "Soufré", "Arôme faible", "Arôme fort"],
    CAT_TASTE: ["Poisson", "Frais", "Épicé", "Salé"],
    CAT_TEXTURE: ["Lisse", "Liquide", "Granuleux", "Grumeleux", "Collant", "Facile à avaler", "Difficile à avaler"],
    CAT_OVERALL: ["Peu appétissant", "Texture moyenne"]
}

# ============================================================
# 2. JEU DE DONNÉES TRADUIT ET NETTOYÉ
# ============================================================
RAW_DATA = [
    # --- RECETTE DE BASE ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Pâle", "Recipe": R_BASE, "Value": 2, "Verbatim": "pale color; too pale"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_BASE, "Value": 2, "Verbatim": "liquid-like; un peu liquide"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_BASE, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_BASE, "Value": 1, "Verbatim": "petites particules"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Huileux", "Recipe": R_BASE, "Value": 2, "Verbatim": "brillant; huileux, gras"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_BASE, "Value": 1, "Verbatim": "échalotte"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_BASE, "Value": 2, "Verbatim": "très peu d’odeur; odeur équilibrée"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_BASE, "Value": 2, "Verbatim": "goût de poisson pas très prononcé"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_BASE, "Value": 2, "Verbatim": "humide; frais; léger"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_BASE, "Value": 1, "Verbatim": "fondant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "texture un peu grumeleuse / collante"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "peu granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_BASE, "Value": 1, "Verbatim": "dommage que la couleur soit peu attractive"},

    # --- RECETTE 1 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_1, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_1, "Value": 1, "Verbatim": "particule végétale agréable"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme fort", "Recipe": R_1, "Value": 1, "Verbatim": "plus forte à l'ouverture"},
    {"Category": CAT_AROMA, "Descriptor": "Soufré", "Recipe": R_1, "Value": 1, "Verbatim": "légère odeur fromagère; note soufrée"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_1, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_1, "Value": 2, "Verbatim": "Peu d’odeur; Pas de véritable odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_1, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_1, "Value": 2, "Verbatim": "épicé avec ail un peu prononcé; poivré"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_1, "Value": 1, "Verbatim": "Bon goût de poisson"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_1, "Value": 2, "Verbatim": "un peu plus granuleux; plus granuleux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_1, "Value": 1, "Verbatim": "plus grumelux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_1, "Value": 1, "Verbatim": "moins crémeux / plus pâteux"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture moyenne", "Recipe": R_1, "Value": 1, "Verbatim": "texture pas super"},

    # --- RECETTE 2 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_2, "Value": 1, "Verbatim": "Fait un peu bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_2, "Value": 2, "Verbatim": "Plus coloré (poireaux); belles couleurs"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_2, "Value": 1, "Verbatim": "particules végétales appréciées"},
    {"Category": CAT_AROMA, "Descriptor": "Poivron", "Recipe": R_2, "Value": 2, "Verbatim": "odeur de poivron de moyenne à forte"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_2, "Value": 1, "Verbatim": "Bonne odeur d’aromates"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_2, "Value": 2, "Verbatim": "très faible; Je ne perçois pas d’odeur"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_2, "Value": 1, "Verbatim": "poisson très présent"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_2, "Value": 1, "Verbatim": "on ne sent pas le goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_2, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_2, "Value": 1, "Verbatim": "Goût frais"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_2, "Value": 1, "Verbatim": "piquant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_2, "Value": 1, "Verbatim": "aspect un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_2, "Value": 1, "Verbatim": "collant aux dents"},
    {"Category": CAT_TEXTURE, "Descriptor": "Difficile à avaler", "Recipe": R_2, "Value": 1, "Verbatim": "moyen car beaucoup de grains"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_2, "Value": 1, "Verbatim": "plus granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture moyenne", "Recipe": R_2, "Value": 1, "Verbatim": "la texture pourrait être améliorée"},

    # --- RECETTE 3 ---
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 1, "Verbatim": "bien lisse mais pas liquide"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_3, "Value": 1, "Verbatim": "white and liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Pâle", "Recipe": R_3, "Value": 2, "Verbatim": "un peu pâle; pâle"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_3, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_3, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_3, "Value": 1, "Verbatim": "arôme de poisson dominant"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_3, "Value": 2, "Verbatim": "odeur assez faible; aucune odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_3, "Value": 1, "Verbatim": "goût de poisson plus prononcé"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_3, "Value": 2, "Verbatim": "humide; frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_3, "Value": 1, "Verbatim": "très salé"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 2, "Verbatim": "très crémeux; on sent comme de la crème"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_3, "Value": 1, "Verbatim": "fondant en bouche"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_3, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_3, "Value": 1, "Verbatim": "not appealing"},

    # --- RECETTE 4 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_4, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "aspect granuleux"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_4, "Value": 1, "Verbatim": "de la couleur, particules vertes et rouges"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_4, "Value": 1, "Verbatim": "could be stronger"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_4, "Value": 1, "Verbatim": "odeur de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_4, "Value": 1, "Verbatim": "odeur végétale appréciée"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_4, "Value": 1, "Verbatim": "Bon parfum gustatif de poisson"},
    {"Category": CAT_TASTE, "Recipe": R_4, "Descriptor": "Frais", "Value": 1, "Verbatim": "plus frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_4, "Value": 1, "Verbatim": "salty"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "texture granuleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_4, "Value": 1, "Verbatim": "impression de coller aux dents"},
    {"Category": CAT_OVERALL, "Descriptor": "Texture moyenne", "Recipe": R_4, "Value": 1, "Verbatim": "texture moyenne"}
]

# ============================================================
# 3. MOTEUR DU GRAPHIQUE INTERACTIF
# ============================================================
df = pd.DataFrame(RAW_DATA)

# Filtrage strict selon la nomenclature française
valid_rows = []
for idx, row in df.iterrows():
    cat = row["Category"]
    desc = row["Descriptor"]
    if cat in ALLOWED_ATTRIBUTES and desc in ALLOWED_ATTRIBUTES[cat]:
        valid_rows.append(row)

filtered_df = pd.DataFrame(valid_rows)

clean_df = (
    filtered_df.groupby(["Category", "Descriptor", "Recipe"], as_index=False)
    .agg({
        "Value": "sum",
        "Verbatim": lambda x: " | ".join(set(x.dropna()))
    })
)

# Génération du graphique Sunburst
fig = px.sunburst(
    clean_df,
    path=['Category', 'Descriptor', 'Recipe'], 
    values='Value',
    custom_data=['Verbatim'],
    title="roue du profil sensoriel de 5 recettes de rillettes",
)

ids = fig.data[0].ids
colors_assigned = []

for element_id in ids:
    parts = element_id.split('/')
    leaf = parts[-1]
    if leaf in RECIPE_COLORS:
        colors_assigned.append(RECIPE_COLORS[leaf])
    else:
        assigned_color = "#F2F2F2"
        for category, color in FAMILY_TRACK_COLORS.items():
            if element_id.startswith(category):
                assigned_color = color
                break
        colors_assigned.append(assigned_color)

fig.data[0].marker.colors = colors_assigned

# Application de la configuration du texte ('auto' pour éviter l'écrasement dans les coins)
fig.update_traces(
    textinfo="label",
    insidetextorientation='auto',  
    branchvalues="total",
    insidetextfont=dict(size=12, family="Arial, sans-serif"),
    hovertemplate="<b>Segment :</b> %{label}<br><b>Citations Panel :</b> %{value}<br><br><i>Verbatims :</i><br>%{customdata[0]}<extra></extra>"
)

# Alignement parfait du titre au centre du canevas
fig.update_layout(
    margin=dict(t=80, l=10, r=10, b=10),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=850,
    title_font=dict(size=24, family="Arial, sans-serif"),
    title_x=0.5,            
    title_xanchor='center', 
    title_yanchor='top'
)

# Rendu natif sur Streamlit
st.plotly_chart(fig, use_container_width=True)