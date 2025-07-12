import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from datetime import date

# 1. Paramètres
EXCEL_FILE = "MLS Assists.xlsx"   # mettre le chemin vers votre fichier
SHEET_NAME  = "bets"              # ou "xG" si votre feuille s’appelle xG

# 2. Chargement en cache du DataFrame
@st.cache_data
def load_sheet() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    return df

# 3. Fonction append
def append_row_to_excel(new_row: list):
    """
    Ouvre le fichier avec openpyxl, ajoute new_row à la fin de SHEET_NAME et sauvegarde.
    """
    wb = load_workbook(EXCEL_FILE)
    ws = wb[SHEET_NAME]
    ws.append(new_row)
    wb.save(EXCEL_FILE)

# 4. UI Streamlit
st.title("📊 Saisie manuelle des xG par équipe")

# Affichage du tableau existant
st.subheader(f"Feuille '{SHEET_NAME}' actuelle")
df = load_sheet()
st.dataframe(df)

st.markdown("---")

# Formulaire d'ajout
st.subheader("Ajouter un nouveau match avec ses xG")
with st.form("form_xg", clear_on_submit=True):
    d        = st.date_input("Date du match", value=date.today())
    home     = st.text_input("Équipe à domicile", "")
    xg_home  = st.number_input("xG domicile", min_value=0.0, step=0.01, format="%.2f")
    away     = st.text_input("Équipe visiteuse", "")
    xg_away  = st.number_input("xG extérieur", min_value=0.0, step=0.01, format="%.2f")
    submit   = st.form_submit_button("Ajouter ce match")

    if submit:
        # Construire la ligne dans l'ordre des colonnes du fichier Excel
        # Ici j’imagine que vos colonnes sont par exemple:
        # Date | Home | xG_home | Away | xG_away
        new_row = [
            d.strftime("%Y-%m-%d"),
            home,
            xg_home,
            away,
            xg_away
        ]
        append_row_to_excel(new_row)
        st.success("✅ Match ajouté dans la feuille Excel !")
        st.experimental_rerun()  # pour recharger la vue
