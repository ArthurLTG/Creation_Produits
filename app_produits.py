import streamlit as st
import pandas as pd

from back_CreationProduits import *



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
            #st.success("Fichier Shopify CSV a télécharger ici: "+ "https://docs.google.com/spreadsheets/d/10JfYG93ARlx-H9XvO-Ml4DCETvTrdDglgvXkOTl4ImI/edit#gid=0&range=A1")
            
        elif catalogue == "BigBlue":
            st.subheader("Création de produits : BIGBLUE")
            st.dataframe(dfFINAL)
            #st.success("Fichier BigBlue CSV a télécharger ici: "+ "https://docs.google.com/spreadsheets/d/10JfYG93ARlx-H9XvO-Ml4DCETvTrdDglgvXkOTl4ImI/edit#gid=544025935&range=A1")
        
        csv = convert_df(dfFINAL)
        st.download_button("Télécharger fichier",csv,f"Creation_Produits_{catalogue}.csv","text/csv",key='download-csv')


# -------------------------------------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.title("Création de produits")
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


 





