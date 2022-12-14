
import pandas as pd
import requests
import certifi
import urllib3



#df = pd.read_csv(r'shy.csv')



def Export_to_Gsheet(wsheet,sheet,df):
    ws = client.open(wsheet)
    sh = ws.worksheet(sheet)
    sh.clear()
    df = df.fillna("-")
    sh.update([df.columns.values.tolist()] + df.values.tolist())
    

def MasterShopify(dfSH):
    
    # REcherche les photos dans les files Shopify -----------------------
    def check_Photo_v2():
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        list_SKU = dfSH["SKU_RefCo"].unique().tolist()
        dfre = pd.DataFrame(columns=["SKU_RefCo","Imgs","CodeJoinPhoto"])

        def getStatuscode(url):
                    try:
                        r = requests.head(url,verify=True,timeout=5) # it is faster to only request the header
                        return (r.status_code)
                    except:
                        return -1


        for e in list_SKU:
            OutputURL = []
            for i in range(1,6):

                urlPack = "https://cdn.shopify.com/s/files/1/0104/2212/4601/files/"+e+"-2"+str(i)+".jpg"
                
                
                if getStatuscode(urlPack) == 200:
                    OutputURL.append(urlPack)
            if len(OutputURL) > 0:
                OutputURL = str(OutputURL).replace('[','').replace(']','').replace('\'','').replace(',',';').replace('https','http')
                dfre = pd.concat([dfre,pd.DataFrame({'SKU_RefCo':[e],'Imgs':[OutputURL],'CodeJoinPhoto':[e+"/1"]})],ignore_index=True)
                #dfre = pd.concat([dfre,pd.DataFrame({'SKU_RefCo':[e],'Imgs':str(OutputURL).replace(',',';'),'CodeJoinPhoto':[e+"/1"]})],ignore_index=True)

        return dfre
    
    # Ordonne le set de tailles --------------------------------
    def Order_by_Size():

        list_RefCo = dfSH["SKU_RefCo"].unique()
        print(list_RefCo)

        list_Row = []
        for ref in list_RefCo:
            is_Ref = dfSH["SKU_RefCo"] == ref
            df_Temp = dfSH[is_Ref].copy()
            df_Temp.sort_values(by=["SKU_RefCo","taille3"], ascending =True, inplace=True)
            df_Temp.reset_index(inplace=True, drop=True)
            df_Temp["Row #"] = df_Temp.index.astype("int64") + 1
            df_Temp = df_Temp[["SKU","Row #"]]
            for i in df_Temp.values.tolist():
                list_Row.append(i) 

        dfSHlist = pd.DataFrame(list_Row, columns=["SKU","Row #"])
        return dfSHlist

    def CountryCode(pays):
        if pays == "CHINE":
            codeISO = "CN"
        elif pays == "TUNISIE":
            codeISO = "TN"
        elif pays == "PORTUGAL":
            codeISO = "PT"
       
        return codeISO

    # MAIN ------------------------------------------------------
    dfSH["ID"] = "" # -> Généré par Shopify lors de la création
    dfSH["Handle"] = ""  # -> Généré par Shopify à partir du title
    dfSH["Command"] = "MERGE"
    dfSH["Title"] = dfSH["Designation"].apply(lambda x: x.title()) + " ( " + dfSH["saison_groupe"] + " / " + dfSH["Rayon"] + " / " + dfSH["couleur_1"] + " )"
    dfSH["Vendor"] = "FROMFUTURE"
    dfSH["Type"] = dfSH["Designation"] + " / " + dfSH["saison_groupe"] + " / " + dfSH["Rayon"]
    dfSH["Tags"] = dfSH["Rayon"] + ", " + dfSH["saison_groupe"] + ", " + dfSH["Famille"] + ", " + dfSH["SsFamille"] + ", " + dfSH["TypeProduit"] + ", " + dfSH["Couleur mère"]+ ", " + dfSH["BarCode"] + "-" + dfSH["Couleur"].apply(lambda x : x.split(" ")[0])
    dfSH["Tags Command"] = "REPLACE"
    dfSH["Status"] = "Draft"
    dfSH["Published"] = "TRUE"
    dfSH["Published Scope"] = "web"
    dfSH["Template Suffix"] = dfSH["Rayon"] + "-" + dfSH["TypeProduit"]
    dfSH["Gift Card"] =  "FALSE"
    dfSH["Variant Command"] = "MERGE"
    dfSH["Option1 Name"] = "Size"
    dfSH["Option1 Value"] = dfSH["taille3_2"]
    dfSH["Option2 Name"] = "Color"
    dfSH["Option2 Value"] = dfSH["couleur_1"]
    dfSH["SKU"] = dfSH["BarCode"] + "-" + dfSH["Couleur"].apply(lambda x : x.split(" ")[0]) + "-" + dfSH["taille3_2"]
    dfSH["Variant Barcode"] = dfSH["GenCod"]
    dfSH["Variant Weight"] = dfSH["Poids"].apply(lambda x : float(x) * 1000)
    dfSH["Variant Weight Unit"] = "g"
    dfSH["Variant Price"] = dfSH["PrixVente"]
    dfSH["Variant Taxable"] = "TRUE"
    dfSH["Variant Inventory Tracker"] = "bigblue-fulfillment"
    dfSH["Variant Inventory Policy"] =  "deny"
    dfSH["Variant Fulfillment Service"] ="bigblue-fulfillment"
    dfSH["Variant Requires Shipping"] = "TRUE"
    dfSH["Variant Cost"] =  dfSH["PrixAchat"]
    dfSH["SKU_RefCo"] = dfSH["BarCode"] + "-" + dfSH["Couleur"].apply(lambda x : x.split(" ")[0])
    dfSH["Metafield: sf_product_infos.matiere [string]"] = dfSH["TypeProduit"].apply(lambda x: x.title())
    dfSH["Metafield: sf_product_infos.country_of_origin [string]"] = dfSH["OrigineFab"].apply(lambda x : CountryCode(x))
    dfSH["Metafield: sf_product_infos.logistic_position [string]"] = dfSH["Plie/Suspendu"].apply(lambda x: x.title())
    dfSH["Metafield: sf_product_infos.commodity_code [string]"] =  dfSH["Nomenclature"]
    dfSH["Metafield: sf_product_infos.category [string]"] =  (dfSH["Famille"] + ", " + dfSH["SsFamille"]).apply(lambda x : x.title())
    dfSH["Metafield: sf_product_infos.gender [string]"] =  dfSH["Rayon"].apply(lambda x : x.title())

    dfSHlist = Order_by_Size()
    dfSH = pd.merge(dfSH, dfSHlist, how="left", on="SKU")

    dfSH["Variant Position"] = dfSH["Row #"]
    dfSH["Top Row"] = dfSH["Row #"].apply(lambda x : "True" if str(x) == "1" else "" )
    dfSH["Variant SKU"] = dfSH["SKU"]
    dfSH["VariantPosition_str"] = dfSH["Variant Position"].apply(lambda x : str(x))
    dfSH["CodeJoinPhoto"] = dfSH["SKU_RefCo"] + "/" + dfSH["VariantPosition_str"]

    dfPhoto = check_Photo_v2()
    dfSH = pd.merge(dfSH, dfPhoto, how="left",left_on="CodeJoinPhoto", right_on="CodeJoinPhoto")
    dfSH["Image Src"] = dfSH["Imgs"].apply(lambda x :"" if type(x)!=str else x)

    dfOutputShopify = dfSH[["ID",
                "Handle",
                "Command",
                "Title",
                "Vendor",
                "Type",
                "Tags",
                "Tags Command",
                "Status",
                "Published",
                "Published Scope",
                "Template Suffix",
                "Gift Card",
                "Row #",
                "Top Row",
                "Variant Command",
                "Option1 Name",
                "Option1 Value",
                "Option2 Name",
                "Option2 Value",
                "Variant Position",
                "Variant SKU",
                "Variant Barcode",
                "Variant Weight",
                "Variant Weight Unit",
                "Variant Price",
                "Variant Taxable",
                "Variant Inventory Tracker",
                "Variant Inventory Policy",
                "Variant Fulfillment Service",
                "Variant Requires Shipping",
                "Variant Cost",
                "Metafield: sf_product_infos.matiere [string]",
                "Metafield: sf_product_infos.country_of_origin [string]",
                "Metafield: sf_product_infos.logistic_position [string]",
                "Metafield: sf_product_infos.commodity_code [string]",
                "Metafield: sf_product_infos.category [string]",
                "Metafield: sf_product_infos.gender [string]",
                "Image Src"
                ]]


    dfOutputShopify = dfOutputShopify.sort_values(by=["Title","Row #"], ascending =True)
    dfOutputShopify.head(20)

    return dfOutputShopify


def Master_Bigblue(dfBB):

    print(dfBB.columns)

    def CountryCode(pays):
        if pays == "CHINE":
            codeISO = "CN"
        elif pays == "TUNISIE":
            codeISO = "TN"
        elif pays == "PORTUGAL":
            codeISO = "PT"
        return codeISO

    dfBB["Option-3-name"] = "SKU-FROM"
    dfBB["Option-3-value"] = dfBB["BarCode"] + "-" + dfBB["Couleur"].apply(lambda x : x.split(" ")[0]) + "-" + dfBB["taille3_2"]
    dfBB["SKU"] = dfBB["frof_pour_template_bb"]
    dfBB["ProductName"] = dfBB["Option-3-value"] + " - " + dfBB["Designation"] + " - " + dfBB["Couleur"].apply(lambda x : x.split(" ",1)[1])
    dfBB["Barcode"] = dfBB["GenCod"]
    dfBB["TariffNumber"] = dfBB["Nomenclature"]
    dfBB["OriginCountry"] = dfBB["OrigineFab"].apply(lambda x : CountryCode(x))
    dfBB["TrackLots"] = "n"
    dfBB["Foldable"] = dfBB["Plie/Suspendu"].apply(lambda x : "y" if x == "PLIE" else "n")
    dfBB["AlreadyPackaged"] = "n"
    dfBB["ProductValue"] = dfBB["PrixAchat]
    dfBB["Currency"] = "EUR"
    dfBB["Description"] = ""
    dfBB["Customs"] = ""
    dfBB["EnglishName"] = ""
    dfBB["FrenchName"] = ""
    dfBB["ChineseName"] = ""
    dfBB["Option-1-name"] = "Size"
    dfBB["Option-1-value"] = dfBB["taille3_2"]
    dfBB["Option-2-name"] = "Color"
    dfBB["Option-2-value"] = dfBB["Couleur"]
    dfBB["Option-4-name"] = "Saison"
    dfBB["Option-4-value"] = dfBB["Saison"]


    dfOutputBB = dfBB[["SKU",
                    "ProductName",
                    "Barcode",
                    "TariffNumber",
                    "OriginCountry",
                    "TrackLots",
                    "Foldable",
                    "AlreadyPackaged",
                    "ProductValue",
                    "Currency",
                    "Description",
                    "Customs",
                    "EnglishName",
                    "FrenchName",
                    "ChineseName",
                    "Option-1-name",
                    "Option-1-value",
                    "Option-2-name",
                    "Option-2-value",
                    "Option-3-name",
                    "Option-3-value",
                    "Option-4-name",
                    "Option-4-value"]]


    print(dfOutputBB)
    return dfOutputBB

def Traitement(df,mode):
    print(df.columns)
    
    # Variables de préparation ----------------------------------------------
    df["saison_groupe"] = df["Saison"].apply(lambda x : x.split("-")[0])
    df["couleur_1"] = df["Couleur"].apply(lambda x : x.split(" ",1)[1].title())
    df["taille3_2"] = df["taille3"].apply(lambda x : str(x).replace("_",""))
    df["Plie/Suspendu"] = df["Saison"].apply(lambda x : x.split("-")[1])
    df["SKU_RefCo"] = df["BarCode"] + "-" + df["Couleur"].apply(lambda x : x.split(" ")[0])


    if mode == "Shopify":

        dfSH = df[df["existe_shopify"]=="Non"].copy()
        dfOutputShopify = MasterShopify(dfSH)
        #Export_to_Gsheet("Automatisation ECom","Products",dfOutputShopify)
        return dfOutputShopify
    
    elif mode == "BigBlue":
        
        dfBB = df[df["existe_BigBlue"]=="Non"].copy()
        dfOutputBB = Master_Bigblue(dfBB)
        #Export_to_Gsheet("Automatisation ECom","BigBlue",dfOutputBB)
        return dfOutputBB
    
#Traitement(df,"Shopify")
