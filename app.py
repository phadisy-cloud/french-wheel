import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Configuration de la page en mode large
st.set_page_config(page_title="Roue Sensorielle des Rillettes", layout="wide")

# ============================================================
# 1. CONSTANTES & CONFIGURATION SENSORIELLE ORIGINALE
# ============================================================
CAT_APPEARANCE = "<b>Aspect visuel</b>"
CAT_AROMA = "<b>Arôme</b>"
CAT_TASTE = "<b>Goût</b>"
CAT_TEXTURE = "<b>Texture</b>"
CAT_OVERALL = "<b>Global</b>"

R_BASE = "Recette de Base"
R_1 = "Recette 1"
R_2 = "Recette 2"
R_3 = "Recette 3"
R_4 = "Recette 4"

RECIPE_COLORS = {
    R_BASE: "#A6A6A6", 
    R_1: "#F4B6ED", 
    R_2: "#D633B0", 
    R_3: "#94C4EB", 
    R_4: "#4A004A"
}

FAMILY_TRACK_COLORS = {
    CAT_APPEARANCE: "#FFD966", 
    CAT_AROMA: "#F4C430", 
    CAT_TASTE: "#FFEAA7",
    CAT_TEXTURE: "#C29200", 
    CAT_OVERALL: "#FFF0C2"
}

ALLOWED_ATTRIBUTES = {
    CAT_APPEARANCE: ["Clair", "Coloré", "Épais", "Particules", "Huileux"],
    CAT_AROMA: ["Poisson", "Échalote", "Végétal", "Poivron", "Soufré", "Arôme faible", "Arôme fort"],
    CAT_TASTE: ["Poisson", "Frais", "Épicé", "Salé"],
    CAT_TEXTURE: ["Lisse", "Liquide", "Granuleux", "Grumeleux", "Collant", "Facile à avaler", "Difficile à avaler"],
    CAT_OVERALL: ["Peu appétissant", "Hétérogène"]
}

RAW_DATA = [
    # --- RECETTE DE BASE ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Clair", "Recipe": R_BASE, "Value": 2, "Verbatim": "pale color"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_BASE, "Value": 2, "Verbatim": "liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_BASE, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_BASE, "Value": 1, "Verbatim": "petites particules"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Huileux", "Recipe": R_BASE, "Value": 2, "Verbatim": "brillant"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_BASE, "Value": 1, "Verbatim": "échalotte"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_BASE, "Value": 2, "Verbatim": "très peu d’odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_BASE, "Value": 2, "Verbatim": "goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_BASE, "Value": 2, "Verbatim": "humide"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_BASE, "Value": 1, "Verbatim": "fondant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "peu granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_BASE, "Value": 1, "Verbatim": "couleur peu attractive"},
    
    # --- RECETTE 1 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_1, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_1, "Value": 1, "Verbatim": "particule végétale"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme fort", "Recipe": R_1, "Value": 1, "Verbatim": "plus forte"},
    {"Category": CAT_AROMA, "Descriptor": "Soufré", "Recipe": R_1, "Value": 1, "Verbatim": "note soufrée"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_1, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_1, "Value": 2, "Verbatim": "Peu d’odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_1, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_1, "Value": 2, "Verbatim": "épicé"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_1, "Value": 1, "Verbatim": "Bon goût"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_1, "Value": 2, "Verbatim": "plus granuleux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_1, "Value": 1, "Verbatim": "plus grumelux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_1, "Value": 1, "Verbatim": "moins crémeux"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_1, "Value": 1, "Verbatim": "texture pas super"},
    
    # --- RECETTE 2 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_2, "Value": 1, "Verbatim": "Fait un peu bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_2, "Value": 2, "Verbatim": "Plus coloré"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_2, "Value": 1, "Verbatim": "particules végétales"},
    {"Category": CAT_AROMA, "Descriptor": "Poivron", "Recipe": R_2, "Value": 2, "Verbatim": "odeur de poivron"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_2, "Value": 1, "Verbatim": "Bonne odeur"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_2, "Value": 2, "Verbatim": "très faible"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_2, "Value": 1, "Verbatim": "poisson très présent"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_2, "Value": 1, "Verbatim": "on ne sent pas"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_2, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_2, "Value": 1, "Verbatim": "Goût frais"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_2, "Value": 1, "Verbatim": "piquant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_2, "Value": 1, "Verbatim": "aspect un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_2, "Value": 1, "Verbatim": "collant aux dents"},
    {"Category": CAT_TEXTURE, "Descriptor": "Difficile à avaler", "Recipe": R_2, "Value": 1, "Verbatim": "moyen"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_2, "Value": 1, "Verbatim": "plus granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_2, "Value": 1, "Verbatim": "la texture"},
    
    # --- RECETTE 3 ---
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 1, "Verbatim": "bien lisse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_3, "Value": 1, "Verbatim": "white and liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Clair", "Recipe": R_3, "Value": 2, "Verbatim": "un peu pâle"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_3, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_3, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_3, "Value": 1, "Verbatim": "arôme de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_3, "Value": 2, "Verbatim": "odeur assez faible"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_3, "Value": 1, "Verbatim": "goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_3, "Value": 2, "Verbatim": "humide; frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_3, "Value": 1, "Verbatim": "très salé"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 2, "Verbatim": "très crémeux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_3, "Value": 1, "Verbatim": "fondant en bouche"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_3, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_3, "Value": 1, "Verbatim": "not appealing"},
    
    # --- RECETTE 4 ---
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_4, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "aspect granuleux"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_4, "Value": 1, "Verbatim": "de la couleur"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_4, "Value": 1, "Verbatim": "could be stronger"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_4, "Value": 1, "Verbatim": "odeur de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_4, "Value": 1, "Verbatim": "odeur végétale"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson", "Recipe": R_4, "Value": 1, "Verbatim": "Bon parfum"},
    {"Category": CAT_TASTE, "Recipe": R_4, "Descriptor": "Frais", "Value": 1, "Verbatim": "plus frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_4, "Value": 1, "Verbatim": "salty"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "texture granuleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_4, "Value": 1, "Verbatim": "impression de coller"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_4, "Value": 1, "Verbatim": "texture moyenne"}
]

# ============================================================
# 2. TRAITEMENT STRUCTURÉ DES DONNÉES (SÉPARATION DES CHEMINS)
# ============================================================
df = pd.DataFrame(RAW_DATA)

# Filtrage strict
valid_rows = [row for idx, row in df.iterrows() if row["Category"] in ALLOWED_ATTRIBUTES and row["Descriptor"] in ALLOWED_ATTRIBUTES[row["Category"]]]
filtered_df = pd.DataFrame(valid_rows)

# Agrégation des valeurs et regroupement des verbatims
clean_df = filtered_df.groupby(["Category", "Descriptor", "Recipe"], as_index=False).agg({
    "Value": "sum",
    "Verbatim": lambda x: " | ".join(set(x.dropna()))
})

# Construction manuelle explicite de l'arbre pour éviter les collisions d'IDs
ids = []
labels = []
parents = []
values = []
verbatims = []
colors = []

# Niveau 1 : Les Catégories principales
for cat in clean_df["Category"].unique():
    ids.append(cat)
    labels.append(cat)
    parents.append("")
    values.append(0)  # Calculé automatiquement par sommation des feuilles
    verbatims.append("")
    colors.append(FAMILY_TRACK_COLORS.get(cat, "#F2F2F2"))

# Niveau 2 : Les Descripteurs reliés à leur Catégorie parente
for c_under in clean_df["Category"].unique():
    desc_list = clean_df[clean_df["Category"] == c_under]["Descriptor"].unique()
    for d in desc_list:
        unique_desc_id = f"{c_under}-->{d}"
        ids.append(unique_desc_id)
        labels.append(d)
        parents.append(c_under)
        values.append(0)
        verbatims.append("")
        colors.append(FAMILY_TRACK_COLORS.get(c_under, "#F2F2F2"))

# Niveau 3 : Les Recettes (Feuilles de l'arbre)
for _, row in clean_df.iterrows():
    unique_rec_id = f"{row['Category']}-->{row['Descriptor']}-->{row['Recipe']}"
    parent_desc_id = f"{row['Category']}-->{row['Descriptor']}"
    
    ids.append(unique_rec_id)
    labels.append(row["Recipe"])
    parents.append(parent_desc_id)
    values.append(row["Value"])
    verbatims.append(row["Verbatim"])
    colors.append(RECIPE_COLORS.get(row["Recipe"], "#A6A6A6"))

# ============================================================
# 3. CONSTRUIRE LE GRAPHIQUE VIA GRAPH OBJECTS (PLUS SÉCURISÉ)
# ============================================================
fig = go.Figure(go.Sunburst(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(colors=colors),
    customdata=verbatims,
    hovertemplate="<b>Segment :</b> %{label}<br><b>Nombre de Citations :</b> %{value}<br><br><i>Verbatims :</i><br>%{customdata}<extra></extra>"
))

fig.update_traces(
    textinfo="label", 
    insidetextorientation='auto', 
    insidetextfont=dict(size=12, family="Arial, sans-serif")
)

fig.update_layout(
    title=dict(
        text="Roue sensorielle des cinq recettes de rillettes de carpe",
        font=dict(size=24, family="Arial, sans-serif"),
        x=0.5,
        xanchor='center'
    ),
    margin=dict(t=80, l=10, r=10, b=10),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=850
)

# ============================================================
# 4. EXPORT ET BOUTONS STREAMLIT
# ============================================================
plot_config = {
    'toImageButtonOptions': {
        'format': 'svg',
        'filename': 'roue_sensorielle_rillettes',
        'height': 850,
        'width': 950,
        'scale': 1
    }
}

st.plotly_chart(fig, use_container_width=True, config=plot_config)

try:
    svg_string = fig.to_image(format="svg").decode("utf-8")
    st.download_button(
        label="📥 Download Wheel as SVG",
        data=svg_string,
        file_name="roue_sensorielle_rillettes.svg",
        mime="image/svg+xml"
    )
except Exception as e:
    st.error("Engine waiting for build initialization. Check dependencies or download directly using the camera icon on the chart top-right.")
