import streamlit as st
import pandas as pd
import gspread 
from oauth2client.service_account import ServiceAccountCredentials 
from back_CreationProduits import *

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"] 

creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/arthu/Desktop/VSC/Creds.json", scope) 
client = gspread.authorize(creds) 

#df = pd.read_csv(r'Produits.csv')



@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')



    
def run():

    if __name__ == "__main__":
        st.markdown("---")
        df = pd.read_csv(file)
        dfFINAL = Traitement(df,catalogue)
        
        if catalogue == "Shopify":
            st.subheader("Création de produits : SHOPIFY")
            st.dataframe(dfFINAL)
            st.success("Fichier Shopify CSV a télécharger ici: "+ "https://docs.google.com/spreadsheets/d/10JfYG93ARlx-H9XvO-Ml4DCETvTrdDglgvXkOTl4ImI/edit#gid=0&range=A1")
            
        elif catalogue == "BigBlue":
            st.subheader("Création de produits : BIGBLUE")
            st.dataframe(dfFINAL)
            st.success("Fichier BigBlue CSV a télécharger ici: "+ "https://docs.google.com/spreadsheets/d/10JfYG93ARlx-H9XvO-Ml4DCETvTrdDglgvXkOTl4ImI/edit#gid=544025935&range=A1")
        
        csv = convert_df(dfFINAL)
        st.download_button("Télécharger fichier",csv,f"Creation_Produits_{catalogue}.csv","text/csv",key='download-csv')


# -------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("Gestion de catalogue")
st.markdown("---")

col1, col2, col3, col4, col5 = st.columns([1,1,5,1,1])

with col1:
    catalogue = st.radio("Produits à créer",('Shopify','BigBlue'))

with col3:
    file = st.file_uploader(label="Importer le fichier de création (.csv)", type='.csv', key='fileUpload')
    if file is not None:
        st.success("Upload ✅")
   
    
with col5:
    st.write("##")
    st.write("##")
    st.button(label="Création", key="boutonRun", on_click=run)
st.markdown("---")

col11, col22 = st.columns(2)
if catalogue == 'Shopify':
    
    with col11:
       
        with st.expander(label="Colonnes FIELDS", expanded=False):
            st.markdown("- 'Template Suffix'")
            st.markdown("- 'Tags'  : à compléter : Rayon, Saison, Famille, SsFamille, Matiere, Couleur Mere, RefCo")
            st.markdown("- 'Image Src' : Uniquement les packshots sont intégrés depuis les Files Shopify donc nomenclature des photo cruciale")
    
    with col22:
      
        with st.expander(label="Colonnes METAFIELDS", expanded=False):
            
            st.markdown("- Metafield: sf_product_infos.style [string] = Keywords des filtres de grille (best practices à definir)")
            st.markdown("- Metafield: sf_product_infos.shape [string] = Keyword de forme du vetement")
            st.markdown("- Metafield: sf_product_infos.category [string] = Keywords des filtres de grille : lors de la création ajout auto Famille, SousFamille (à compléter)")
            st.markdown("- Metafield: sf_product_infos.thickness [string] = Nombre de fils ex: '2 fils'")
            st.markdown("- Metafield: sf_product_infos.thread_number [integer] = Nombre de fils ex: '2'")
            st.markdown("- Metafield: sf_product_infos.thread_number_description [string] = Vide")
            st.markdown("- Metafield: sf_product_infos.length [string] = Vide")
            st.markdown("- Metafield: sf_product_infos.sleeve [string] = Vide")
            st.markdown("- Metafield: sf_product_tabs.infos_size [string] = Toggle: Texte à récupérer/adapter ⚠️")
            st.markdown("- Metafield: sf_product_tabs.infos_compo [string] = Toggle: Texte à récupérer/adapter aupres du CRM ⚠️")
            st.markdown("- Metafield: sf_product_tabs.infos_shipping [string] = Vide")

 





