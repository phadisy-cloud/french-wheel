import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration & Input Data
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

RECIPE_COLORS = {R_BASE: "#A6A6A6", R_1: "#F4B6ED", R_2: "#D633B0", R_3: "#94C4EB", R_4: "#4A004A"}
FAMILY_TRACK_COLORS = {
    CAT_APPEARANCE: "#FFD966", CAT_AROMA: "#F4C430", CAT_TASTE: "#FFEAA7",
    CAT_TEXTURE: "#C29200", CAT_OVERALL: "#FFF0C2"
}

# AJUSTEMENT TECHNIQUE : Ajout d'un espace invisible pour différencier les doublons de catégories
ALLOWED_ATTRIBUTES = {
    CAT_APPEARANCE: ["Clair", "Coloré", "Épais", "Particules", "Huileux"],
    CAT_AROMA: ["Poisson", "Échalote", "Végétal", "Poivron", "Soufré", "Arôme faible", "Arôme fort"],
    CAT_TASTE: ["Poisson ", "Frais", "Épicé", "Salé"], # "Poisson " avec espace pour différencier du goût
    CAT_TEXTURE: ["Lisse", "Liquide", "Granuleux", "Grumeleux", "Collant", "Facile à avaler", "Difficile à avaler"],
    CAT_OVERALL: ["Peu appétissant", "Hétérogène"]
}

RAW_DATA = [
    {"Category": CAT_APPEARANCE, "Descriptor": "Clair", "Recipe": R_BASE, "Value": 2, "Verbatim": "pale color"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_BASE, "Value": 2, "Verbatim": "liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_BASE, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_BASE, "Value": 1, "Verbatim": "petites particules"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Huileux", "Recipe": R_BASE, "Value": 2, "Verbatim": "brillant"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_BASE, "Value": 1, "Verbatim": "échalotte"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_BASE, "Value": 2, "Verbatim": "très peu d’odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson ", "Recipe": R_BASE, "Value": 2, "Verbatim": "goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_BASE, "Value": 2, "Verbatim": "humide"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_BASE, "Value": 1, "Verbatim": "fondant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_BASE, "Value": 1, "Verbatim": "peu granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_BASE, "Value": 1, "Verbatim": "couleur peu attractive"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_1, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_1, "Value": 1, "Verbatim": "particule végétale"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme fort", "Recipe": R_1, "Value": 1, "Verbatim": "plus forte"},
    {"Category": CAT_AROMA, "Descriptor": "Soufré", "Recipe": R_1, "Value": 1, "Verbatim": "note soufrée"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_1, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_1, "Value": 2, "Verbatim": "Peu d’odeur"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_1, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_1, "Value": 2, "Verbatim": "épicé"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson ", "Recipe": R_1, "Value": 1, "Verbatim": "Bon goût"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_1, "Value": 2, "Verbatim": "plus granuleux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_1, "Value": 1, "Verbatim": "plus grumelux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_1, "Value": 1, "Verbatim": "moins crémeux"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_1, "Value": 1, "Verbatim": "texture pas super"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_2, "Value": 1, "Verbatim": "Fait un peu bouillie"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_2, "Value": 2, "Verbatim": "Plus coloré"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Particules", "Recipe": R_2, "Value": 1, "Verbatim": "particules végétales"},
    {"Category": CAT_AROMA, "Descriptor": "Poivron", "Recipe": R_2, "Value": 2, "Verbatim": "odeur de poivron"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_2, "Value": 1, "Verbatim": "Bonne odeur"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_2, "Value": 2, "Verbatim": "très faible"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_2, "Value": 1, "Verbatim": "poisson très présent"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson ", "Recipe": R_2, "Value": 1, "Verbatim": "on ne sent pas"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_2, "Value": 1, "Verbatim": "salé"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_2, "Value": 1, "Verbatim": "Goût frais"},
    {"Category": CAT_TASTE, "Descriptor": "Épicé", "Recipe": R_2, "Value": 1, "Verbatim": "piquant"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_2, "Value": 1, "Verbatim": "aspect un peu grumeleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_2, "Value": 1, "Verbatim": "collant aux dents"},
    {"Category": CAT_TEXTURE, "Descriptor": "Difficile à avaler", "Recipe": R_2, "Value": 1, "Verbatim": "moyen"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_2, "Value": 1, "Verbatim": "plus granuleux"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_2, "Value": 1, "Verbatim": "la texture"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 1, "Verbatim": "bien lisse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Liquide", "Recipe": R_3, "Value": 1, "Verbatim": "white and liquid-like"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Clair", "Recipe": R_3, "Value": 2, "Verbatim": "un peu pâle"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_3, "Value": 1, "Verbatim": "aspect de bouillie"},
    {"Category": CAT_AROMA, "Descriptor": "Échalote", "Recipe": R_3, "Value": 1, "Verbatim": "échalote"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_3, "Value": 1, "Verbatim": "arôme de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_3, "Value": 2, "Verbatim": "odeur assez faible"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson ", "Recipe": R_3, "Value": 1, "Verbatim": "goût de poisson"},
    {"Category": CAT_TASTE, "Descriptor": "Frais", "Recipe": R_3, "Value": 2, "Verbatim": "humide; frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_3, "Value": 1, "Verbatim": "très salé"},
    {"Category": CAT_TEXTURE, "Descriptor": "Lisse", "Recipe": R_3, "Value": 2, "Verbatim": "très crémeux"},
    {"Category": CAT_TEXTURE, "Descriptor": "Facile à avaler", "Recipe": R_3, "Value": 1, "Verbatim": "fondant en bouche"},
    {"Category": CAT_TEXTURE, "Descriptor": "Grumeleux", "Recipe": R_3, "Value": 1, "Verbatim": "texture un peu grumeleuse"},
    {"Category": CAT_OVERALL, "Descriptor": "Peu appétissant", "Recipe": R_3, "Value": 1, "Verbatim": "not appealing"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Épais", "Recipe": R_4, "Value": 1, "Verbatim": "Aspect de bouillie"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "aspect granuleux"},
    {"Category": CAT_APPEARANCE, "Descriptor": "Coloré", "Recipe": R_4, "Value": 1, "Verbatim": "de la couleur"},
    {"Category": CAT_AROMA, "Descriptor": "Arôme faible", "Recipe": R_4, "Value": 1, "Verbatim": "could be stronger"},
    {"Category": CAT_AROMA, "Descriptor": "Poisson", "Recipe": R_4, "Value": 1, "Verbatim": "odeur de poisson"},
    {"Category": CAT_AROMA, "Descriptor": "Végétal", "Recipe": R_4, "Value": 1, "Verbatim": "odeur végétale"},
    {"Category": CAT_TASTE, "Descriptor": "Poisson ", "Recipe": R_4, "Value": 1, "Verbatim": "Bon parfum"},
    {"Category": CAT_TASTE, "Recipe": R_4, "Descriptor": "Frais", "Value": 1, "Verbatim": "plus frais"},
    {"Category": CAT_TASTE, "Descriptor": "Salé", "Recipe": R_4, "Value": 1, "Verbatim": "salty"},
    {"Category": CAT_TEXTURE, "Descriptor": "Granuleux", "Recipe": R_4, "Value": 1, "Verbatim": "texture granuleuse"},
    {"Category": CAT_TEXTURE, "Descriptor": "Collant", "Recipe": R_4, "Value": 1, "Verbatim": "impression de coller"},
    {"Category": CAT_OVERALL, "Descriptor": "Hétérogène", "Recipe": R_4, "Value": 1, "Verbatim": "texture moyenne"}
]

df = pd.DataFrame(RAW_DATA)
valid_rows = [row for idx, row in df.iterrows() if row["Category"] in ALLOWED_ATTRIBUTES and row["Descriptor"] in ALLOWED_ATTRIBUTES[row["Category"]]]
filtered_df = pd.DataFrame(valid_rows)
clean_df = filtered_df.groupby(["Category", "Descriptor", "Recipe"], as_index=False).agg({"Value": "sum", "Verbatim": lambda x: " | ".join(set(x.dropna()))})

# Génération initiale via Plotly Express (Votre code exact)
fig = px.sunburst(clean_df, path=['Category', 'Descriptor', 'Recipe'], values='Value', custom_data=['Verbatim'], title="Roue sensorielle des cinq recettes de rillettes de carpe")

ids = fig.data[0].ids
colors_assigned = []
for element_id in ids:
    parts = element_id.split('/')
    leaf = parts[-1]
    if leaf in RECIPE_COLORS:
        colors_assigned.append(RECIPE_COLORS[leaf])
    else:
        assigned_color = "#F2F2F2"
        # CORRECTION LOGIQUE DES COULEURS DES PARENTS (Prend en compte l'encodage HTML interne de Plotly)
        for category, color in FAMILY_TRACK_COLORS.items():
            if element_id.startswith(category) or element_id.startswith(category.replace("<b>", "").replace("</b>", "")):
                assigned_color = color
                break
        colors_assigned.append(assigned_color)

fig.data[0].marker.colors = colors_assigned
fig.update_traces(textinfo="label", insidetextorientation='auto', branchvalues="total", insidetextfont=dict(size=12, family="Arial, sans-serif"))
fig.update_layout(margin=dict(t=80, l=10, r=10, b=10), plot_bgcolor="white", paper_bgcolor="white", height=850, title_font=dict(size=24, family="Arial, sans-serif"), title_x=0.5, title_xanchor='center', title_yanchor='top')

# Affichage dans l'application Streamlit
st.plotly_chart(fig, use_container_width=True)
