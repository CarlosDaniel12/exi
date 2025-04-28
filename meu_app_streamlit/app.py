import streamlit as st
import pandas as pd
from PIL import Image
import os, base64
from io import BytesIO
import math, re, qrcode, urllib.parse
import streamlit as st

# Configura layout
st.set_page_config(layout="wide")

# Ajusta o caminho das logos automaticamente
if os.path.exists("C:/meu_app_streamlit/logos"):
    CAMINHO_LOGOS = "C:/meu_app_streamlit/logos"
else:
    CAMINHO_LOGOS = "meu_app_streamlit/logos"

# Produtos cadastrados
produtos_cadastrados = {


  
    "0047": {
        "nome": "ECO KIT BLEND + BLUS DUO",
        "marca": "Ecotools",
        "codigo_produto": "079625440706"
    },
    "ECO-3144": {
        "nome": "Duo Esponjas Para Aplicação De Maquiagem No Rosto - 3144",
        "marca": "Ecotools",
        "codigo_produto": "079625031447"
    },
    "ECO-1202": {
        "nome": "Foundation Brush - Pincel de Base - 1202",
        "marca": "Ecotools",
        "codigo_produto": "079625012026"
    },
    "ECO-3146": {
        "nome": "Kit Holiday Vibes - 3146",
        "marca": "Ecotools",
        "codigo_produto": "000000000"
    },
    "ECO-1606": {
        "nome": "Kit Start The Day Beautiful Makeup Brush - 1606",
        "marca": "Ecotools",
        "codigo_produto": "079625016062"
    },
    "ECO-7572 (C)": {
        "nome": "Massageador Corporal Body Roller Cinza - 7572",
        "marca": "Ecotools",
        "codigo_produto": "079625075724"
    },
    "ECO-7572 (R)": {
        "nome": "Massageador Corporal Body Roller Rosa - 7572",
        "marca": "Ecotools",
        "codigo_produto": "079625075724"
    },
    "ECO-1600": {
        "nome": "Pincel Full Pó - 1600",
        "marca": "Ecotools",
        "codigo_produto": "079625016000"
    },
    "ECO-1608": {
        "nome": "Pincel Para Detalhes - 1608",
        "marca": "Ecotools",
        "codigo_produto": "00000000"
    },
    "ECO-1306": {
        "nome": "Pincel para Blush - 1306",
        "marca": "Ecotools",
        "codigo_produto": "079625013061"
    },
    "ECO-7592": {
        "nome": "Rolo Massageador Facial Contour - 7592",
        "marca": "Ecotools",
        "codigo_produto": "079625075922"
    },
    "ECO-7517": {
        "nome": "Rolo Massageador Facial Pedra Jade - 7517",
        "marca": "Ecotools",
        "codigo_produto": "079625075175"
    },
    "Eco-Necessaire": {
        "nome": "Eco-Necessaire",
        "marca": "Ecotools",
        "codigo_produto": "000000000"
    }
}
 
  
 
"10170840201": {"nome": "Fino Touch Hair Oil Serum AIRY Smooth 70ml", "marca": "fino"},"codigo_produto": "4550516483836"
"10170701202": {"nome": "Fino Touch Hair Oil 70ml", "marca": "fino"},"codigo_produto": "4901872471997"
"10170702202": {"nome": "Fino Touch Hair Mask 230g", "marca": "fino"},"codigo_produto": "4901872837144"
"1015D092202": {"nome": "Máscara 40g", "marca": "fino"},"codigo_produto": "4901824571874"
"1015D354202": {"nome": "Mini Oil 10ml ", "marca": "fino"},"codigo_produto": "4901872471997"
  
 "14145013370": {"nome": "TSUBAKI - Kit com 2 Embalagens de Plastico para Viagem 80ml", "marca": "tsubaki"},"codigo_produto": "2114145013370"
"10170642202": {"nome": "TSUBAKI -  INTENSIVE Repair Conditioner  490ml", "marca": "tsubaki"},"codigo_produto": "4550516474155"
"10170640202": {"nome": "TSUBAKI -  INTENSIVE Repair Shampoo 490ml", "marca": "tsubaki"},"codigo_produto": "4550516474087"
"10170558202": {"nome": "TSUBAKI -  Repair Mask 180g", "marca": "tsubaki"},"codigo_produto": "4901872459957"
"10170636202": {"nome": "TSUBAKI -  VOLUME Repair Conditioner 490ml", "marca": "tsubaki"},"codigo_produto": "4901872466238"
"10170634202": {"nome": "TSUBAKI -  VOLUME Repair Shampoo 490ml", "marca": "tsubaki"},"codigo_produto": "4901872466146"
"10170632202": {"nome": "TSUBAKI -  MOIST Repair Conditioner 490ml", "marca": "tsubaki"},"codigo_produto": "4901872466061"
"10170630202": {"nome": "TSUBAKI -  MOIST Repair Shampoo 490ml", "marca": "tsubaki"},"codigo_produto": "4901872466023"
 
 
 
 
 
  "14072": {"nome": "Argan Oil Condicionador 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708532"
  "14073": {"nome": "Argan Oil Máscara 200ml", "marca": "Lee Stafford"},"codigo_produto": "5060282704640"
  "14074": {"nome": "Argan Oil Nourishing Miracle Oil 50ml", "marca": "Lee Stafford"},"codigo_produto": "5060282704664"
  "14071": {"nome": "Argan Oil Shampoo 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708525"
  "14047": {"nome": "Bleach Blondes Purple Toning Shampoo 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708389"
  "14088": {"nome": "Coco Loco Blow & Go 11-in-1 Lotion 100ml", "marca": "Lee Stafford"},"codigo_produto": "5060282702868"
  "14089": {"nome": "Coco Loco Heat Protection Mist 150ml", "marca": "Lee Stafford"},"codigo_produto": "5060282703520"
  "14086": {"nome": "Coco Loco Shine Condicionador 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708150"
  "14087": {"nome": "Coco Loco Shine Mask 200ml", "marca": "Lee Stafford"},"codigo_produto": "5060282703452"
  "14090": {"nome": "Coco Loco Shine Oil 75ml", "marca": "Lee Stafford"},"codigo_produto": "5060282703575"
  "14085": {"nome": "Coco Loco Shine Shampoo 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708136"
  "14002": {"nome": "Grow Strong & Long Condicionador 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708204"
  "14004": {"nome": "Grow Strong & Long Leave-in 100ml", "marca": "Lee Stafford"},"codigo_produto": "5060282706545"
  "14003": {"nome": "Grow Strong & Long Máscara 200ml", "marca": "Lee Stafford"},"codigo_produto": "5060282706491"
  "14005": {"nome": "Grow Strong & Long Scalp Serum 75ml", "marca": "Lee Stafford"},"codigo_produto": "5060282706538"
  "14001": {"nome": "Grow Strong & Long Shampoo 500ml", "marca": "Lee Stafford"},"codigo_produto": "5060282708198"
  "14037": {"nome": "Hold Tight Hairspray de Fixação 250ml", "marca": "Lee Stafford"},"codigo_produto": "5060282705494"
  "14035": {"nome": "Styling Dry Shampoo 200ml", "marca": "Lee Stafford"},"codigo_produto": "5060282705371"
 
  
         
  "111316309": {"nome": "10 Professional Cica Ceramide Oil Serum 60ml", "marca": "mise"},"codigo_produto": "8809925152816"
  "111315717": {"nome": "CURLING ESSENCE 2X NATURAL CURL 150ml", "marca": "mise"},"codigo_produto": "8809803560610"
  "111315718": {"nome": "CURLING ESSENCE 2X NATURAL CURL 230ml", "marca": "mise"},"codigo_produto": "8809803560627"
  "111315797": {"nome": "CURLING ESSENCE 2X VOLUME CURL 150ml", "marca": "mise"},"codigo_produto": "8809803560924"
  "111315798": {"nome": "CURLING ESSENCE 2X VOLUME CURL 230ml", "marca": "mise"},"codigo_produto": "8809803560917"
  "111316101": {"nome": "CURLING FOR BANGS FIXER 200ml", "marca": "mise"},"codigo_produto": "8809803591720"
  "111316185": {"nome": "DAMAGE CARE RED PROTEIN COND 200ml", "marca": "mise"},"codigo_produto": "8809685746973"
  "111316190": {"nome": "DAMAGE CARE RED PROTEIN MASK 180ml", "marca": "mise"},"codigo_produto": "8809925130104"
  "111316184": {"nome": "DAMAGE CARE RED PROTEIN SHAMPOO 200ml", "marca": "mise"},"codigo_produto": "8809643064088"
  "111316106": {"nome": "PERFECT S. 3 MINUTES HAIR MASK 300ml", "marca": "mise"},"codigo_produto": "8809803592604"
  "111315564": {"nome": "PERFECT S. BASE UP ESSENCE 200ml", "marca": "mise"},"codigo_produto": "8809803556224"
  "111315565": {"nome": "PERFECT S. NO WASH CD TREATMENT CREAM PACK 230ml", "marca": "mise"},"codigo_produto": "8809803556231"
  "111316102": {"nome": "PERFECT S. NO WASH WATER TREATMENT CD 215ml", "marca": "mise"},"codigo_produto": "8809803591669"
  "111315555": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 180ml", "marca": "mise"},"codigo_produto": "8809803556149"
  "111316163": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 330ml", "marca": "mise"},"codigo_produto": "8809803556316"
  "111315583": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 900ml", "marca": "mise"},"codigo_produto": "8809803556262"
  "111316409": {"nome": "PERFECT S. ORIGINAL COND 200ml", "marca": "mise"},"codigo_produto": "8809925173835"
  "111315736": {"nome": "PERFECT S. ORIGINAL CONDI 530ml", "marca": "mise"},"codigo_produto": "8809803540346"
  "111315548": {"nome": "PERFECT S. ORIGINAL CONDI 680ml", "marca": "mise"},"codigo_produto": "8809803549202"
  "111315588": {"nome": "PERFECT S. ORIGINAL MIST 150ml", "marca": "mise"},"codigo_produto": "8809803556293"
  "111316012": {"nome": "PERFECT S. ORIGINAL MIST 250ml", "marca": "mise"},"codigo_produto": "8809803565738"
  "111315567": {"nome": "PERFECT S. ORIGINAL SERUM 200ml", "marca": "mise"},"codigo_produto": "8809803556248"
  "111317310": {"nome": "PERFECT S. ORIGINAL SERUM 30ml", "marca": "mise"},"codigo_produto": "8809925126497"
  "111315560": {"nome": "PERFECT S. ORIGINAL SERUM 80ml", "marca": "mise"},"codigo_produto": "8809803556187"
  "111317290": {"nome": "PERFECT S. ORIGINAL SHAMPOO 140ml", "marca": "mise"},"codigo_produto": "8809803540230"
  "111315553": {"nome": "PERFECT S. ORIGINAL SHAMPOO 200ml", "marca": "mise"},"codigo_produto": "8809803548496"
  "111315735": {"nome": "PERFECT S. ORIGINAL SHAMPOO 530ml", "marca": "mise"},"codigo_produto": "8809803540353"
  "111315547": {"nome": "PERFECT S. ORIGINAL SHAMPOO 680ml", "marca": "mise"},"codigo_produto": "8809803548472"
  "111315554": {"nome": "PERFECT S. ORIGINAL SHAMPOO 900ml", "marca": "mise"},"codigo_produto": "8809803548489"
  "111315563": {"nome": "PERFECT S. ROSE SERUM 80ml", "marca": "mise"},"codigo_produto": "8809803556217"
  "111315561": {"nome": "PERFECT S. SERUM SUPER RICH 80ml", "marca": "mise"},"codigo_produto": "8809803556194"
  "111315738": {"nome": "PERFECT S. STYLING CONDI 530ml", "marca": "mise"},"codigo_produto": "8809803540322"
  "111315550": {"nome": "PERFECT S. STYLING CONDI 680ml", "marca": "mise"},"codigo_produto": "8809803556118"
  "111315562": {"nome": "PERFECT S. STYLING SERUM 80ml", "marca": "mise"},"codigo_produto": "8809803556200"
  "111315737": {"nome": "PERFECT S. STYLING SHAMPOO 530ml", "marca": "mise"},"codigo_produto": "8809803540339"
  "111315549": {"nome": "PERFECT S. STYLING SHAMPOO 680ml", "marca": "mise"},"codigo_produto": "8809803556101"
  "111315575": {"nome": "PERFECT S. WATERY SERUM 80ml", "marca": "mise"},"codigo_produto": "8809803556255"
  "111316081": {"nome": "ROYAL JELLY PROTEIN CONDI TREATMENT 1000ml", "marca": "mise"},"codigo_produto": "8809803586481"
  "111316080": {"nome": "ROYAL JELLY PROTEIN SHAMPOO 1000ml", "marca": "mise"},"codigo_produto": "8809803586474"
  "111316295": {"nome": "SALON 10 DAMAGED HAIR 250ml", "marca": "mise"},"codigo_produto": "8809685832560"
  
  "111316055": {"nome": "SALON 10 DAMAGED HAIR 250ml", "marca": "mise"},"codigo_produto": "8809925152816"
  
  "111316297": {"nome": "SALON 10  DAMAGED HAIR 990ml", "marca": "mise"},"codigo_produto": "8809685797050"
  "111316296": {"nome": "SALON 10  EXTREMELY DAMAGED HAIR 250ml", "marca": "mise"},"codigo_produto": "8809685832577"
  
  
  "111316056": {"nome": "SALON 10  EXTREMELY DAMAGED HAIR 250ml", "marca": "mise"},"codigo_produto": "8809925152816"
  
  
  "111316298": {"nome": "SALON 10 EXTREMELY DAMAGED HAIR 990ml", "marca": "mise"},"codigo_produto": "8809685797227"
  "111316215": {"nome": "SALON 10 DAMAGE HAIR 500ml", "marca": "mise"},"codigo_produto": "8809685815594"
  "111316264": {"nome": "SALON 10 NO-WASH AMPOULE CONDI TREATMENT 200ml", "marca": "mise"},"codigo_produto": "8809803573511"
  "111316216": {"nome": "SALON 10 SHAMPOO FOR EXTREMELY DAMAGED HAIR 500ml", "marca": "mise"},"codigo_produto": "8809685815600"
  "111315788": {"nome": "STYLE CARE P.STRONG HOLD HAIR GEL 500ml", "marca": "mise"},"codigo_produto": "8801042963825"
  "111316410": {"nome": "Perfect Serum Original Kit 110ml + 30ml", "marca": "mise"},"codigo_produto": "8809925175082"
  "111316411": {"nome": "Perfect Serum Styling Kit 110ml + 30ml", "marca": "mise"},"codigo_produto": "8809925175099"
  "111316405": {"nome": "Perfect Serum Super Rich Kit 110ml + 30ml", "marca": "mise"},"codigo_produto": "8809925172708"
  "111316406": {"nome": "Perfect Serum Watery Kit 110ml + 30ml", "marca": "mise"},"codigo_produto": "8809925173910"
  "111316308": {"nome": "Salon 10 Professional Cica Protein Mask 215ml", "marca": "mise"},"codigo_produto": "8809925152809"
  "111316171": {"nome": "MES PERFECT S. ORIGINAL SERUM 30ML", "marca": "mise"},"codigo_produto": "8809803574921"
  "111316351": {"nome": "Magic Straight Shampoo 530m", "marca": "mise"},"codigo_produto": "8809925164741"
  "111316352": {"nome": "Magic Straight Tratamento 230ml", "marca": "mise"},"codigo_produto": "8809925167483"
  "111316353": {"nome": "Magic Straight Sérum 80ml", "marca": "mise"},"codigo_produto": "8809925167490"
  "111316359": {"nome": "SÉRUM CREAM 80ML", "marca": "mise"},"codigo_produto": "8809925167810"
  
  
  
          
         
  "25839-0": {"nome": "Dark Oil Condicionador 1000ml", "marca": "Sebastian"},"codigo_produto": "4064666102375"
  "25840-0": {"nome": "Dark Oil Máscara Capilar 500ml", "marca": "Sebastian"},"codigo_produto": "4064666102382"
  "26500-0": {"nome": "Dark Oil Silkening Fragrância Spray 200ml", "marca": "Sebastian"},"codigo_produto": "4064666314426"
  "26490-0": {"nome": "Dark Oil Óleo Capilar 30ml", "marca": "Sebastian"},"codigo_produto": "7898973417054"
  "24608-0": {"nome": "Dark Oil Óleo Capilar 95ml", "marca": "Sebastian"},"codigo_produto": "7898973417023"
  "24889-0": {"nome": "Flaunt Trilliant Protetor Térmico Trifásico 150ml", "marca": "Sebastian"},"codigo_produto": "8005610569574"
  "25328-0": {"nome": "No Breaker Leave-in 100ml", "marca": "Sebastian"},"codigo_produto": "4064666214467"
  "24890-0": {"nome": "Novo Shine Define Finalizador 200ml", "marca": "Sebastian"},"codigo_produto": "4064666225494"
  "24781-0": {"nome": "Penetraitt Masque - Tratamento 150ml", "marca": "Sebastian"},"codigo_produto": "4064666317380"
  "26050-0": {"nome": "Potion 9 Lite Spray Líquido 150ml", "marca": "Sebastian"},"codigo_produto": "4064666225272"
  "24165-2": {"nome": "Sublimate Creme Invisível Modelador 100ml", "marca": "Sebastian"},"codigo_produto": "8005610580838"
  "26392-0": {"nome": "Trilliance Condicionador 250ml", "marca": "Sebastian"},"codigo_produto": "4064666307015"
  "23489-3": {"nome": "Twisted Curl Elastic Detangler Condicionador 250ml", "marca": "Sebastian"},"codigo_produto": "8005610426648"
  
  "111414201": {"nome": "Damage Care & Nourishing Floral Powdery - Shampoo 180ml", "marca": "RYO"},"codigo_produto": "8809925154216"
  "111413638": {"nome": "Hair Loss Expert Care 9EX - Oily Scalp Shampoo 400ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413647": {"nome": "Root Strength Mk 330ml Couro Cabeludo Oleoso", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413667": {"nome": "Damage Care & Nourishing CD Treatment 180ml", "marca": "RYO"},"codigo_produto": "8801042690608"
  "111414132": {"nome": "Deep Cleansing e Cooling Citrus Herbal Scent Shampoo 480ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413649": {"nome": "Hair Loss Expert Care Treat Deep Nutrition Conditioner 330ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413647": {"nome": "Hair Loss Expert Care Treat Root Strength Conditioner 330ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413639": {"nome": "Hair Loss Expert Care 9EX Dry Scalp Shampoo 400ml", "marca": "RYO"},"codigo_produto": "8806403162817"
  "111413638": {"nome": "Hair Loss Expert Care 9EX Oily Scalp Shampoo 400ml", "marca": "RYO"},"codigo_produto": "8806403117534"
  "111414078": {"nome": "RootGen For Men Hair Loss Shampoo 353ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111414079": {"nome": "RootGen For Women Hair Loss Conditioner Treatment 353ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111413977": {"nome": "RootGen Hair Loss Care Scalp Essence 80ml", "marca": "RYO"},"codigo_produto": "8809803572804"
  "111414077": {"nome": "RootGen Hair Loss Shampoo Women 353ml", "marca": "RYO"},"codigo_produto": "9988776655"
  "111414131": {"nome": "Damage Care & Nourishing Treat Floral Powdery - Mask 300ml", "marca": "RYO"},"codigo_produto": "8809803590259"
  "111414252": {"nome": "Red Ginseng Hair Nutrition Shampoo 820ml", "marca": "RYO"},"codigo_produto": "8809925193666"
  "111414253": {"nome": "Red Ginsens Hair Nutrition Cd Treatment 820ml", "marca": "RYO"},"codigo_produto": "8809925193536"
  "111414260": {"nome": "Damage Care & Nourishing Treat Floral Powdery - Mask 300ml", "marca": "RYO"},"codigo_produto": "8809803590259"
  "111414135": {"nome": "Damage Care & Nourishing - Floral Powdery Shamp 480ml", "marca": "RYO"},"codigo_produto": "8809803590297"
    "111414251": {"nome": "Black Bean Hair Root Nutririon Shampoo 820ml", "marca": "RYO"},"codigo_produto": "8809925193659"
    
    
      "E4031400": {"nome": "Acidic Bonding Concentrate - 5-min Liquid Mask 250ml", "marca": "Redken"},"codigo_produto": "3474637152000"
  "E3845200": {"nome": "Acidic Bonding Concentrate - Condicionador 1L", "marca": "Redken"},"codigo_produto": "3474637089702"
  "E3845400": {"nome": "Acidic Bonding Concentrate - Condicionador 300ml", "marca": "Redken"},"codigo_produto": "0884486456311"
  "P2356100": {"nome": "Acidic Bonding Concentrate - Intensive Treat Pré-Shampoo 150ml", "marca": "Redken"},"codigo_produto": "0884486493866"
  "E3861900": {"nome": "Acidic Bonding Concentrate - Leave-in 150ml", "marca": "Redken"},"codigo_produto": "0884486456380"
  "E3845300": {"nome": "Acidic Bonding Concentrate - Shampoo 1L", "marca": "Redken"},"codigo_produto": "3474637089719"
  "E3845500": {"nome": "Acidic Bonding Concentrate - Shampoo 300ml", "marca": "Redken"},"codigo_produto": "0884486456281"
  "E4068200": {"nome": "Acidic Color Gloss - Condicionador 300ml", "marca": "Redken"},"codigo_produto": "3474637173463"
  "E4069500": {"nome": "Acidic Color Gloss - Leave-in 190ml", "marca": "Redken"},"codigo_produto": "3474637174170"
  "E4068500": {"nome": "Acidic Color Gloss - Shampoo 300ml", "marca": "Redken"},"codigo_produto": "3474637173494"
  "P2567800": {"nome": "Acidic Color Gloss - Tratamento 237ml", "marca": "Redken"},"codigo_produto": "0884486516732"
  "P1997303": {"nome": "All Soft - Argan Oil 111ml", "marca": "Redken"},"codigo_produto": "0884486452993"
  "H2273502": {"nome": "All Soft - Condicionador 1L", "marca": "Redken"},"codigo_produto": "7899706170956"
  "E3458400": {"nome": "All Soft - Condicionador 300ml", "marca": "Redken"},"codigo_produto": "3474636919970"
  "H2499301": {"nome": "All Soft - Heavy Cream Máscara 250ml", "marca": "Redken"},"codigo_produto": "7899706192873"
  "H2398002": {"nome": "All Soft - Heavy Cream Máscara 500ml", "marca": "Redken"},"codigo_produto": "7899706181631"
  "E3930201": {"nome": "All Soft - Moisture Restore Leave-in 150ml", "marca": "Redken"},"codigo_produto": "3474637124823"
  "E3458501": {"nome": "All Soft - Shampoo 300ml", "marca": "Redken"},"codigo_produto": "3474636919987"
  "E3458301": {"nome": "All Soft - Shampoo 1L", "marca": "Redken"},"codigo_produto": "3474636919963"
  "E3996200": {"nome": "All Soft Mega Curls - Condicionador 1L", "marca": "Redken"},"codigo_produto": "3474637135645"
  "E3996400": {"nome": "All Soft Mega Curls - Shampoo 1L", "marca": "Redken"},"codigo_produto": "3474637135669"
  "E3996500": {"nome": "All Soft Mega Curls - Shampoo 300ml", "marca": "Redken"},"codigo_produto": "93474637135676"
  "P1444403": {"nome": "Brews Maneuver - Cream Pomade 100ml", "marca": "Redken"},"codigo_produto": "0884486341518"
  "P2390000": {"nome": "Brews Pliable Paste - Jar 150ml", "marca": "Redken"},"codigo_produto": "0884486497895"
  "E3861600": {"nome": "Extreme - Anti-Snap 250ml", "marca": "Redken"},"codigo_produto": "0884486453402"
  "P2001800": {"nome": "Extreme - Cat 250ml", "marca": "Redken"},"codigo_produto": "0884486453419"
  "E3460400": {"nome": "Extreme - Condicionador 1L", "marca": "Redken"},"codigo_produto": "3474636920174"
  "E3460600": {"nome": "Extreme - Condicionador 300ml", "marca": "Redken"},"codigo_produto": "3474636920198"
  "E3557900": {"nome": "Extreme - Máscara 250ml", "marca": "Redken"},"codigo_produto": "3474636971053"
  "H2499101": {"nome": "Extreme - Máscara 500ml", "marca": "Redken"},"codigo_produto": "7899706192859"
  "E3994301": {"nome": "Extreme - Play Safe 250ml", "marca": "Redken"},"codigo_produto": "3474637134693"
  "E3460501": {"nome": "Extreme - Shampoo 1L", "marca": "Redken"},"codigo_produto": "3474636920181"
  "E3460701": {"nome": "Extreme - Shampoo 300ml", "marca": "Redken"},"codigo_produto": "3474636920204"
  "E3869400": {"nome": "Extreme Length - Máscara 250ml", "marca": "Redken"},"codigo_produto": "3474637105662"
  "E3461600": {"nome": "Frizz Dismiss - Condicionador 300ml", "marca": "Redken"},"codigo_produto": "3474636920297"
  "E3531500": {"nome": "Frizz Dismiss - Máscara 250ml", "marca": "Redken"},"codigo_produto": "3474636961047"
  "P2122000": {"nome": "Acidic Bonding Concentrate - PH Sealer 250ml", "marca": "Redken"},"codigo_produto": "0884486464088"
  "E3531400": {"nome": "Frizz Dismiss - Rebel Tame 250ml", "marca": "Redken"},"codigo_produto": "3474636961030"
  "E3461100": {"nome": "Frizz Dismiss - Sulfate-Free Shampoo 300ml", "marca": "Redken"},"codigo_produto": "3474636920242"
  "E3862300": {"nome": "One United Elixir - Leave-in 150ml", "marca": "Redken"},"codigo_produto": "3474637102555"
  "P1056403": {"nome": "One United Elixir - Leave-in 400ml", "marca": "Redken"},"codigo_produto": "0884486219336"
     
         
         
  "2735182": {"nome": "Balance - Shampoo 280ml", "marca": "Senscience"}, "codigo_produto": "7702029639447"
  "2734948": {"nome": "Balance - Condicionador 1000ml", "marca": "Senscience"},"codigo_produto": "7702045118810"
  "2735509": {"nome": "Balance - Condicionador 240ml", "marca": "Senscience"},"codigo_produto": "7702045664867"
  "2856018": {"nome": "Detangler Moisturizing - Leave-in Spray 200ml", "marca": "Senscience"},"codigo_produto": "7702029918887"
  "2735929": {"nome": "Inner Restore - Máscara Hidratante 200ml", "marca": "Senscience"},"codigo_produto": "7702045762938 "
  "2735536": {"nome": "Inner Restore Intensif - Máscara 500ml", "marca": "Senscience"},"codigo_produto": "7702045169843 "
  "2733023": {"nome": "Inner Restore Intensif - Máscara 50ml", "marca": "Senscience"},"codigo_produto": "7702029471450"
  "2787510": {"nome": "Inner Restore Intensif - Máscara de Tratamento 150ml", "marca": "Senscience"},"codigo_produto": "7702045437119 "
  "466162": {"nome": "Inner Restore Moisturizing - Mask 500ml", "marca": "Senscience"},"codigo_produto": "7702045446616"
  "2732972": {"nome": "Inner Restore Moisturizing - Máscara de Hidratação 50ml", "marca": "Senscience"},"codigo_produto": "7702029791602"
  "2746956": {"nome": "Renewal - Shampoo 280ml", "marca": "Senscience"},"codigo_produto": "7702045668933"
  "2735401": {"nome": "Silk Moisture - Condicionador 240ml", "marca": "Senscience"},"codigo_produto": "7702045286298"
  "2734946": {"nome": "Silk Moisture - Shampoo 1000ml", "marca": "Senscience"},"codigo_produto": "7702029552982"
  "2734977": {"nome": "Silk Moisture - Shampoo 280ml", "marca": "Senscience"},"codigo_produto": "7702045303506"
  "2736443": {"nome": "Silk Moisture Mini - Condicionador 90ml", "marca": "Senscience"},"codigo_produto": "7702045247756"
  "2736439": {"nome": "Silk Moisture Mini - Shampoo 90ml", "marca": "Senscience"},"codigo_produto": "7702045375602"
  "2735508": {"nome": "Smooth - Condicionador 240ml", "marca": "Senscience"},"codigo_produto": "7702029407503"
  "2734943": {"nome": "Smooth - Shampoo 1000ml", "marca": "Senscience"},"codigo_produto": "7702045340785"
  "2735184": {"nome": "Specialty - Shampoo 280ml", "marca": "Senscience"},"codigo_produto": "7702029200753"
  "2735510": {"nome": "True Hue - Condicionador 240ml", "marca": "Senscience"},"codigo_produto": "7702029947313"
  "2735183": {"nome": "True Hue - Shampoo 280ml", "marca": "Senscience"},"codigo_produto": "7702029629967"
  "2736015": {"nome": "True Hue Color Protecting - Treatment 55ml", "marca": "Senscience"},"codigo_produto": "7702045490732"
  "2735511": {"nome": "True Hue Violet - Condicionador 240ml", "marca": "Senscience"},"codigo_produto": "7702029597396"
  "2735185": {"nome": "True Hue Violet - Shampoo 280ml", "marca": "Senscience"},"codigo_produto": "7702029953444"
  "498297": {"nome": "Silk Moisture Travel Size - Shampoo + Condic 90ml + Inner Restore Intensif Máscara 50ml", "marca": "senscience"},"codigo_produto": "7899522324311"
  
  
  "26205-0": {"nome": "Elements Calming Shampoo 250ml", "marca": "Wella"},"codigo_produto": "4064666035628"
  "24586-0": {"nome": "Fusion Máscara Reconstrutora 150ml", "marca": "Wella"},"codigo_produto": "7896235353737"
  "26419-0": {"nome": "Fusion Shampoo 1000ml", "marca": "Wella"},"codigo_produto": "064666318233"
  "24593-0": {"nome": "Invigo Blonde Recharge Shampoo Desamarelador 250ml", "marca": "Wella"},"codigo_produto": "7896235353805"
  "24634-0": {"nome": "Invigo Color Brilliance Condicionador 200ml", "marca": "Wella"},"codigo_produto": "7896235353850"
  "24578-0": {"nome": "Invigo Color Brilliance Máscara Capilar 500ml", "marca": "Wella"},"codigo_produto": "7896235353652"
  "26228-0": {"nome": "Invigo Color Brilliance Shampoo 1000ml", "marca": "Wella"},"codigo_produto": "4064666318356"
  "24635-0": {"nome": "Invigo Nutri-Enrich Condicionador 200ml", "marca": "Wella"},"codigo_produto": "7896235353867"
  "24583-0": {"nome": "Invigo Nutri-Enrich Máscara de Nutrição 500ml", "marca": "Wella"},"codigo_produto": "7896235353706"
  "26230-0": {"nome": "Invigo Nutri-Enrich Shampoo 1000ml", "marca": "Wella"},"codigo_produto": "4064666435459"
  "25877-0": {"nome": "Invigo Sun Condicionador 200ml", "marca": "Wella"},"codigo_produto": "4064666041650"
  "24919-0": {"nome": "Invigo Sun Shampoo 250ml", "marca": "Wella"},"codigo_produto": "3614226745880"
  "25398-0": {"nome": "NutriCurls Shampoo Micellar 250ml", "marca": "Wella"},"codigo_produto": "3614228865647"
  "26390-0": {"nome": "Oil Reflections Light 100ml", "marca": "Wella"},"codigo_produto": "7898973417047"
  "24637-0": {"nome": "Oil Reflections Luminous Instant Condicionador 200ml", "marca": "Wella"},"codigo_produto": "7896235353881"
  "24590-0": {"nome": "Oil Reflections Luminous Reboost Máscara Capilar 500ml", "marca": "Wella"},"codigo_produto": "7896235353775"
  "24591-0": {"nome": "Wella Professionals Oil Reflections - Máscara Capilar 150ml", "marca": "Wella"},"codigo_produto": "7896235353782"
  "99350105838-0": {"nome": "Oil Reflections Luminous Reveal Shampoo 1000ml", "marca": "Wella"},"codigo_produto": "8005610531632"
  "26227-0": {"nome": "Oil Reflections Reflective Light Óleo Capilar 30ml", "marca": "Wella"},"codigo_produto": "7898973417009"
  "26389-0": {"nome": "Oil Reflections Óleo Capilar 100ml", "marca": "Wella"},"codigo_produto": "7898973417030"
  "26226-0": {"nome": "Oil Reflections Óleo Capilar 30ml", "marca": "Wella"},"codigo_produto": "4064666306148"
  "27192-0": {"nome": "Ultimate Repair Miracle Hair Rescue Tratamento Leave-in 30ml", "marca": "Wella"},"codigo_produto": "40646666337104"
  "27191-0": {"nome": "Ultimate Repair Condicionador 500ml", "marca": "Wella"},"codigo_produto": "4064666337043"
  "27193-0": {"nome": "Ultimate Repair Miracle Hair Rescue Leave-in 95ml", "marca": "Wella"},"codigo_produto": "4064666337111"
  "27612-0": {"nome": "Ultimate Repair Máscara 150ml", "marca": "Wella"},"codigo_produto": "4064666337074"
  "27613-0": {"nome": "Ultimate Repair Máscara 500ml", "marca": "Wella"},"codigo_produto": "4064666337081"
  "27194-0": {"nome": "Ultimate Repair Protetor Térmico 140ml", "marca": "Wella"},"codigo_produto": "4064666337128"
  "27188-0": {"nome": "Ultimate Repair Shampoo 1000ml", "marca": "Wella"},"codigo_produto": "4064666337128"
  "27187-0": {"nome": "Ultimate Repair Shampoo 250ml", "marca": "Wella"},"codigo_produto": "4064666337029"
  "26850-0": {"nome": "Fusion - Máscara Reconstrutora 500ml", "marca": "Wella Professionals"},"codigo_produto": "7896235353744"
  "24146-1": {"nome": "EIMI Absolute Set Spray Fixador 300ml", "marca": "Wella"},"codigo_produto": "8005610563244"
  "23799-1": {"nome": "EIMI Body Crafter Spray de Volume 150ml", "marca": "Wella"},"codigo_produto": "8005610589572"
  "23384-1": {"nome": "EIMI Bold Move Pasta Modeladora 150ml", "marca": "Wella"},"codigo_produto": "8005610576206"
  "24765-0": {"nome": "EIMI Glam Mist Spray de Brilho 200ml", "marca": "Wella"},"codigo_produto": "3614227276444"
  "23800-1": {"nome": "EIMI Mistify Me Strong Spray Fixador 500ml", "marca": "Wella"},"codigo_produto": "8005610640327"
  "24172-1": {"nome": "EIMI Perfect Me Leave-in 100ml", "marca": "Wella"},"codigo_produto": "8005610587509"
  "23470-2": {"nome": "EIMI Sugar Lift Spray Texturizador 150ml", "marca": "Wella"},"codigo_produto": "8005610589626"
  "26004-0": {"nome": "SP Luxe Oil Óleo Capilar 100ml", "marca": "Wella"},"codigo_produto": "4064666306162"
  "99350174902-0": {"nome": "Ultimate Luxe Oil Óleo 30ml", "marca": "Wella"},"codigo_produto": "4064666594224"
  "99350174903-0": {"nome": "Ultimate Luxe Oil Óleo 100ml", "marca": "Wella"},"codigo_produto": "7898973417078"
  "99350174375-0": {"nome": "Ultimate Luxe Oil Shampoo 1L", "marca": "Wella"},"codigo_produto": "4064666593562"
  "99350174379-0": {"nome": "Ultimate Luxe Oil Máscara 150ml", "marca": "Wella"},"codigo_produto": "4064666593609"
  "99350174380-0": {"nome": "Ultimate Luxe Oil Máscara 500ml", "marca": "Wella"},"codigo_produto": "4064666593616"
  "99350174381-0": {"nome": "Ultimate Luxe Oil Shampoo 250ml", "marca": "wella"},"codigo_produto": "4064666593623"
"69993370": {"nome": "Q-Tips - Hastes de Algodão - Kit de Viagem 30un", "marca": "wella"},"codigo_produto": "305210221277"
"64360310": {"nome": "Q-Tips - Hastes de Algodão com Pontas de Precisão - Kit de Viagem 30un", "marca": "wella"},"codigo_produto": "305210047693"
"99350161119-0": {"nome": "Marula Oil Blender Primer - Óleo Protetor Capilar 150ml", "marca": "wella"},"codigo_produto": "4064666035376"



  "20423-0": {"nome": "Color Touch Pure Naturals 2/0 Preto - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019255"
  "20424-0": {"nome": "Color Touch Pure Naturals 3/0 Castanho Escuro - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019279"
  "20425-0": {"nome": "Color Touch Pure Naturals 4/0 Castanho Médio - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019286"
  "20426-0": {"nome": "Color Touch Pure Naturals 5/0 Castanho Claro - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019309"
  "20427-0": {"nome": "Color Touch Pure Naturals 6/0 Louro Escuro - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019323"
  "20428-0": {"nome": "Color Touch Pure Naturals 7/0 Louro Médio - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019330"
  "20429-0": {"nome": "Color Touch Pure Naturals 8/0 Louro Claro - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019347"
  "20460-0": {"nome": "Color Touch 1,9% - Emulsão Reveladora 6 Volumes 1000ml", "marca": "sac"},"codigo_produto": "7891182019866"
  "20380-0": {"nome": "Color Touch 5/1 Castanho Claro Acinzentado - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182018685"
  "20381-0": {"nome": "Color Touch 5/3 - Castanho Claro Dourado 60g", "marca": "sac"},"codigo_produto": "7891182018760"
  "20407-0": {"nome": "Color Touch 6/77 Louro Escuro Marrom Intenso - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182019064"
  "20386-0": {"nome": "Color Touch 7/89 Louro Médio Pérola Cendré - Tonalizante 60g", "marca": "sac"},"codigo_produto": "7891182018845"
 "27255-0-2": {"nome": "BlondorPlex N°1 Pó Descolorante 800g", "marca": "sac"}, "codigo_produto": "4064666212579"
  "99350169161-0": {"nome": "Color Motion+ Máscara 150ml", "marca": "sac"}, "codigo_produto": "4064666316147"
  "25154-0": {"nome": "Color Motion+ Máscara 500ml", "marca": "sac"},"codigo_produto": "3614226750723"
  "25153-0": {"nome": "Color Motion+ Shampoo 1000ml", "marca": "sac"},"codigo_produto": "4064666318165"
  "25152-1": {"nome": "Color Motion+ Shampoo 250ml", "marca": "sac"},"codigo_produto": "4064666316109"
  "20305-0": {"nome": "Color Perfect 3/0 Castanho Escuro - Coloração Permanente 60g", "marca": "sac"},"codigo_produto": "7891182017398"
  "20365-0": {"nome": "Color Perfect 8/3 Louro Claro Dourado - Coloração Permanente 60ml", "marca": "sac"},"codigo_produto": "7891182018265"
  "20307-0": {"nome": "Color Perfect Pure Naturals 5/0 Castanho Claro - Coloração Permanente 60ml", "marca": "sac"},"codigo_produto": "7891182017411"
  "20310-0": {"nome": "Color Perfect Pure Naturals 6/0 Louro Escuro - Coloração Permanente 60ml", "marca": "sac"},"codigo_produto": "7891182017442"  
  
  "H0270321": {"nome": "Oxidante Creme 75ml 20 Vol", "marca": "loreal"},
  "E3825500": {"nome": "Curl Expression Gelée Lavante Anti-résidus 300ml", "marca": "loreal"},
  "E3564101": {"nome": "Absolut Repair - Mask 250ml", "marca": "loreal"},
  "E3574500": {"nome": "Absolut Repair - Oil 90ml", "marca": "loreal"},
  "E3795000": {"nome": "Absolut Repair - Óleo 10 em 1 30ml", "marca": "loreal"},
  "H2469500": {"nome": "Absolut Repair Gold - Condicionador 200ml", "marca": "loreal"},
  "H2469700": {"nome": "Absolut Repair Gold - Mask 250ml", "marca": "loreal"},
  "H2469101": {"nome": "Absolut Repair Gold - Shampoo 300ml", "marca": "loreal"},
  "E4033400": {"nome": "Absolut Repair Molecular - Leave-in 100ml", "marca": "loreal"},
  "E4173000": {"nome": "Absolut Repair Molecular - Máscara Capilar 250ml", "marca": "loreal"},
  "E4173200": {"nome": "Absolut Repair Molecular - Máscara Capilar 500ml", "marca": "loreal"},
  "E4033800": {"nome": "Absolut Repair Molecular - Shampoo 300ml", "marca": "loreal"},
  "E4034100": {"nome": "Absolut Repair Molecular - Shampoo 500ml", "marca": "loreal"},
  "H3689700": {"nome": "Absolut Repair Shampoo Refil 240ml", "marca": "loreal"},
  "E3887500": {"nome": "Aminexil - Ampoules 10x6ml", "marca": "loreal"},
  "H2466300": {"nome": "Blondifier - Condicionador 200ml", "marca": "loreal"},
  "H2466501": {"nome": "Blondifier - Mask Gloss 250ml", "marca": "loreal"},
  "H2465900": {"nome": "Blondifier - Shampoo Gloss 300ml", "marca": "loreal"},
  "H2608400": {"nome": "Curl Expression - Leave-in Condicionador 200ml", "marca": "loreal"},
  "H2608500": {"nome": "Curl Expression - Mask 250ml", "marca": "loreal"},
  "H2607200": {"nome": "Curl Expression - Mask Rich 250ml", "marca": "loreal"},
  "E3826600": {"nome": "Curl Expression - Moisturizing Shampoo 300ml", "marca": "loreal"},
  "E3835000": {"nome": "Curl Expression - Reviver Spray 190ml", "marca": "loreal"},
  "7,90862E+12": {"nome": "Diactivateur 15 Volumes 120ml", "marca": "loreal"},
  "H2467500": {"nome": "Inforcer - Mask 250ml", "marca": "loreal"},
  "H2466901": {"nome": "Inforcer - Shampoo 300ml", "marca": "loreal"},
  "E4033200": {"nome": "Metal Detox - Anti-Metal de Alta Proteção Leave-in 100ml", "marca": "loreal"},
  "E3548402": {"nome": "Metal Detox - Mask 250ml", "marca": "loreal"},
  "E3560001": {"nome": "Metal Detox - Mask 500ml", "marca": "loreal"},
  "E3548702": {"nome": "Metal Detox - Shampoo 300ml", "marca": "loreal"},
  "E3549301": {"nome": "Metal Detox - Treatment Spray 500ml", "marca": "loreal"},
  "E4123900": {"nome": "Metal Detox - Pre-Shampoo Treatment 250ml", "marca": "loreal"},
  "H2610800": {"nome": "NutriOil - Leave-In 150ml", "marca": "loreal"},
  "H2611001": {"nome": "NutriOil - Mask 250ml", "marca": "loreal"},
  "H2610201": {"nome": "NutriOil - Shampoo 300ml", "marca": "loreal"},
  "H2468700": {"nome": "Pro Longer - Mask 250ml", "marca": "loreal"},
  "H2467901": {"nome": "Pro Longer - Shampoo 300ml", "marca": "loreal"},
  "E3886000": {"nome": "Scalp Anti-Dandruff - Shampoo 300ml", "marca": "loreal"},
  "E3847900": {"nome": "Scalp Anti-Discomfort - Shampoo 300ml", "marca": "loreal"},
  "E3848800": {"nome": "Scalp Anti-Discomfort - Treatment 200ml", "marca": "loreal"},
  "E3848300": {"nome": "Scalp Anti-Oily - Mask 250ml", "marca": "loreal"},
  "E3848700": {"nome": "Scalp Anti-Oily - Mask 500ml", "marca": "loreal"},
  "E3872900": {"nome": "Scalp Anti-Oily - Shampoo 300ml", "marca": "loreal"},
  "E3872300": {"nome": "Serioxyl Densifying - Shampoo 300ml", "marca": "loreal"},
  "H2470302": {"nome": "Silver Shampoo 300ml", "marca": "loreal"},
  "E3554500": {"nome": "Vitamino Color - 10-in-1 190ml", "marca": "loreal"},
  "H2471100": {"nome": "Vitamino Color - Condicionador 200ml", "marca": "loreal"},
  "H2471300": {"nome": "Vitamino Color - Mask 250ml", "marca": "loreal"},
  "H2470900": {"nome": "Vitamino Color - Shampoo 300ml", "marca": "loreal"},
  "H2689800": {"nome": "Vitamino Color Resveratrol - Shampoo Refil 240ml", "marca": "loreal"},
  "H2471902": {"nome": "Blondifier - Mask COOL 250ml", "marca": "loreal"},
  "E3573901": {"nome": "Pro Longer - Cream 10-IN-1 150ml", "marca": "loreal"},
  "E3573901": {"nome": "Pro Longer - Cream 10-IN-1 150ml", "marca": "loreal"},
  
  
  


  "6134464": {"nome": "Advanced Keratin Bond Deep Repair Shampoo 600ml", "marca": "KERASYS"},
  "6134473": {"nome": "Advanced Keratin Bond Purifying Conditioner Treatment 600ml", "marca": "KERASYS"},
  "6134467": {"nome": "Advanced Keratin Bond Purifying Shampoo 600ml", "marca": "KERASYS"},
  "6134472": {"nome": "Advanced Keratin Bond Silky Moisture Conditioner Treatment 600ml", "marca": "KERASYS"},
  "6134466": {"nome": "Advanced Keratin Bond Silky Moisture Shampoo 600ml", "marca": "KERASYS"},
  "6134465": {"nome": "Advanced Keratin Bond Volume Shampoo 600ml", "marca": "KERASYS"},
  "6098972": {"nome": "Clabo Fresh Citrus Deep Clean Conditioner 960ml", "marca": "KERASYS"},
  "6098969": {"nome": "Clabo Fresh Citrus Deep Clean Shampoo 960ml", "marca": "KERASYS"},
  "6098970": {"nome": "Clabo Romantic Citrus Deep Clean Conditioner 960ml", "marca": "KERASYS"},
  "6098971": {"nome": "Clabo Romantic Citrus Deep Clean Shampoo 960ml", "marca": "KERASYS"},
  "6101625": {"nome": "Clabo Tropical Citrus Deep Clean Conditioner 960ml", "marca": "KERASYS"},
  "6101580": {"nome": "Clabo Tropical Citrus Deep Clean Shampoo 960ml", "marca": "KERASYS"},
  "6103759": {"nome": "Perfume Shampoo Blooming Flowery 180ml", "marca": "KERASYS"},
  "6103758": {"nome": "Perfume Shampoo Elegance Sensual 180ml", "marca": "KERASYS"},
  "6103766": {"nome": "Perfume Shampoo Glam Stylish 180ml", "marca": "KERASYS"},
  "6103767": {"nome": "Perfume Shampoo Lovely Romantic 180ml", "marca": "KERASYS"},
  "6103178": {"nome": "Perfume Shampoo Lovely Romantic 400ml", "marca": "KERASYS"},
  "6103577": {"nome": "Perfume Shampoo Lovely Romantic 600ml", "marca": "KERASYS"},
  "6103764": {"nome": "Perfume Shampoo Pure Charming 180ml", "marca": "KERASYS"},
  "6100535": {"nome": "Advanced Color Protect Shampoo 400ml", "marca": "Kerasys"},
  "6134479": {"nome": "Advanced Keratin Bond Deep Repair Treatment 600ml", "marca": "Kerasys"},
  "6134471": {"nome": "Keratin Bond Volume Treatment 600ml", "marca": "Kerasys"},
  "5019654": {"nome": "Salon de Magie Ampola Premium de Tratamento 200ml", "marca": "Kerasys"},
  "6100543": {"nome": "Advanced Color Protect Conditioner 400ml", "marca": "Kerasys"},
  "6100682": {"nome": "Advanced Colour Protect Ampoule Shampoo 500ml Refil", "marca": "Kerasys"},
  "6103799": {"nome": "Advanced Keramide Damage Clinic 1000ml", "marca": "Kerasys"},
  "6064194": {"nome": "Advanced Keramide Damage Clinic Mask 200ml", "marca": "Kerasys"},
  "5008451": {"nome": "Advanced Keramide Extreme Damage Clinic Serum 70ml", "marca": "Kerasys"},
  "6078916": {"nome": "Advanced Keramide Extreme Damage Rich Serum 70ml", "marca": "Kerasys"},
  "6064195": {"nome": "Advanced Keramide Heat Protection Mask 200ml", "marca": "Kerasys"},
  "5010755": {"nome": "Advanced Moisture Ampoule 10X Cd Serum 80ml", "marca": "Kerasys"},
  "6093519": {"nome": "Advanced Moisture Ampoule 10x Hair Pack 300ml", "marca": "Kerasys"},
  "6100528": {"nome": "Advanced Moisture Ampoule Conditioner 400ml", "marca": "Kerasys"},
  "6100534": {"nome": "Advanced Moisture Ampoule Shampoo 400ml", "marca": "Kerasys"},
  "6100679": {"nome": "Advanced Moisture Ampoule Shampoo 500ml Refil", "marca": "Kerasys"},
  "5019487": {"nome": "Advanced Repair Ampoule 10x Cd Serum 80ml", "marca": "Kerasys"},
  "6093517": {"nome": "Advanced Repair Ampoule 10x Hair Pack 300ml", "marca": "Kerasys"},
  "6103800": {"nome": "Advanced Repair Ampoule 10x Keratin Ampoule Cd Hair Pack 1L", "marca": "Kerasys"},
  "6100531": {"nome": "Advanced Repair Ampoule Shampoo 400ml", "marca": "Kerasys"},
  "6093511": {"nome": "Advanced Repair Ampoule Water Cd Treatment 220ml", "marca": "Kerasys"},
  "6100529": {"nome": "Advanced Volume Ampoule Conditioner 400ml", "marca": "Kerasys"},
  "6103610": {"nome": "Argan Oil Cd Treatment 1000ml", "marca": "Kerasys"},
  "6082090": {"nome": "Argan Oil Conditioner 1000ml", "marca": "Kerasys"},
  "5014075": {"nome": "Argan Oil Serum 100ml", "marca": "Kerasys"},
  "6082084": {"nome": "Argan Oil Shampoo 1000ml", "marca": "Kerasys"},
  "6098817": {"nome": "Black Bean Oil Shampoo 1L", "marca": "Kerasys"},
  "6082088": {"nome": "Coconut Oil Conditioner 1000ml", "marca": "Kerasys"},
  "6082085": {"nome": "Coconut Oil Shampoo 1000ml", "marca": "Kerasys"},
  "6103715": {"nome": "Damage Clinic Cd Treatment 300ml", "marca": "Kerasys"},
  "6103539": {"nome": "Deep Cleansing Shampoo 180ml", "marca": "Kerasys"},
  "6066720": {"nome": "Deep Cleansing Shampoo 500ml Refil", "marca": "Kerasys"},
  "6065902": {"nome": "Deep Cleansing Shampoo 600ml", "marca": "Kerasys"},
  "5010034": {"nome": "Heat Active Damage Repair 200ml", "marca": "Kerasys"},
  "5010023": {"nome": "Heat Active Style Care Essence 200ml", "marca": "Kerasys"},
  "5010675": {"nome": "Heat Primer Blanche Iris 220ml", "marca": "Kerasys"},
  "6112344": {"nome": "Moisture Clinic Cd Treatment 300ml", "marca": "Kerasys"},
  "6066186": {"nome": "Moisturizing Conditioner 180ml", "marca": "Kerasys"},
  "6066715": {"nome": "Moisturizing Conditioner 500ml Refill", "marca": "Kerasys"},
  "6066185": {"nome": "Moisturizing Conditioner 600ml", "marca": "Kerasys"},
  "6066183": {"nome": "Moisturizing Shampoo 180ml", "marca": "Kerasys"},
  "6066711": {"nome": "Moisturizing Shampoo 500ml Refill", "marca": "Kerasys"},
  "6066182": {"nome": "Moisturizing Shampoo 600ml", "marca": "Kerasys"},
  "6059482": {"nome": "Oriental Premium Condicionador 200ml", "marca": "Kerasys"},
  "6060085": {"nome": "Oriental Premium Condicionador 500ml Refil", "marca": "Kerasys"},
  "6130952": {"nome": "Oriental Premium Condicionador 600ml", "marca": "Kerasys"},
  "6055025": {"nome": "Oriental Premium Condicionador 600ml", "marca": "Kerasys"},
  "6067179": {"nome": "Oriental Premium Mask Tr Cond 200ml", "marca": "Kerasys"},
  "6059481": {"nome": "Oriental Premium Shampoo 200ml", "marca": "Kerasys"},
  "6060084": {"nome": "Oriental Premium Shampoo 500ml Refil", "marca": "Kerasys"},
  "6130849": {"nome": "Oriental Premium Shampoo 600ml", "marca": "Kerasys"},
  "6055024": {"nome": "Oriental Premium Shampoo 600ml", "marca": "Kerasys"},
  "6103192": {"nome": "Perfume - Lovely Romantic Conditioner 400ml", "marca": "Kerasys"},
  "6103584": {"nome": "Perfume - Lovely Romantic Conditioner 600ml", "marca": "Kerasys"},
  "6075540": {"nome": "Propolis Energy Shine Shampoo 1000ml", "marca": "Kerasys"},
  "6115358": {"nome": "Propolis Energy Shine Shampoo 180ml", "marca": "Kerasys"},
  "6075545": {"nome": "Propolis Energy Shine Treatment Conditioner 1000ml", "marca": "Kerasys"},
  "6115360": {"nome": "Propolis Energy Shine Treatment Conditioner 180ml", "marca": "Kerasys"},
  "6100811": {"nome": "Propolis Royal Green Shampoo 180ml", "marca": "Kerasys"},
  "6100815": {"nome": "Propolis Royal Green Treatment 180ml", "marca": "Kerasys"},
  "6093951": {"nome": "Propolis Royal Green Treatment 1L", "marca": "Kerasys"},
  "6100817": {"nome": "Propolis Royal Original Treatment 180ml", "marca": "Kerasys"},
  "6093949": {"nome": "Propolis Royal Original Treatment 1L", "marca": "Kerasys"},
  "6093950": {"nome": "Propolis Royal Red Shampoo 1L", "marca": "Kerasys"},
  "6093948": {"nome": "Propolis Royal Red Treatment 1L", "marca": "Kerasys"},
  "6066191": {"nome": "Repairing Conditioner 180ml", "marca": "Kerasys"},
  "6066716": {"nome": "Repairing Conditioner 500ml Refill", "marca": "Kerasys"},
  "6066192": {"nome": "Repairing Conditioner 600ml", "marca": "Kerasys"},
  "6066189": {"nome": "Repairing Shampoo 180ml", "marca": "Kerasys"},
  "6066712": {"nome": "Repairing Shampoo 500ml Refill", "marca": "Kerasys"},
  "6066188": {"nome": "Repairing Shampoo 600ml", "marca": "Kerasys"},
  "6066180": {"nome": "Revitalizing Conditioner 180ml", "marca": "Kerasys"},
  "6103565": {"nome": "Revitalizing Conditioner 500ml Refill", "marca": "Kerasys"},
  "6066179": {"nome": "Revitalizing Conditioner 600ml", "marca": "Kerasys"},
  "6066177": {"nome": "Revitalizing Shampoo 180ml", "marca": "Kerasys"},
  "6103564": {"nome": "Revitalizing Shampoo 500ml Refill", "marca": "Kerasys"},
  "6066176": {"nome": "Revitalizing Shampoo 600ml", "marca": "Kerasys"},
  "5011714": {"nome": "Salon De Magie Treatment Conditioner 200ml", "marca": "Kerasys"},
  "5014454": {"nome": "Salt Scrub Deep Clean Shampoo 600ml", "marca": "Kerasys"},
  "6110516": {"nome": "Salt Scrub Scalp Hair Treatment Conditioner 600ml", "marca": "Kerasys"},
  "6103541": {"nome": "Scalp Balancing Shampoo 180ml", "marca": "Kerasys"},
  "6103537": {"nome": "Scalp Balancing Shampoo 500ml Refill", "marca": "Kerasys"},
  "6065904": {"nome": "Scalp Balancing Shampoo 600ml", "marca": "Kerasys"},
  "5013806": {"nome": "Scalp Spa Agua Blue Serum 70ml", "marca": "Kerasys"},
  "6097701": {"nome": "Tea Tree Oil Conditioner 1L", "marca": "Kerasys"},
  "6092834": {"nome": "Tea Tree Oil Shampoo 1L", "marca": "Kerasys"},
  "6141964": {"nome": "Propolis Hair Bonding Pro Repair Cd Treatment 250ml", "marca": "Kerasys"},
  "5022484": {"nome": "Propolis Hair Bonding No Wash Repair Treatment 200ml", "marca": "Kerasys"},
  "6146885": {"nome": "Propolis Hair Bonding Shamp 450ml", "marca": "Kerasys"},
  "6112581": {"nome": " Keramide Ampoule Damage Clinic - Shampoo 1L", "marca": "Kerasys"},
  "6100527": {"nome": "Kerasys Advanced Repair Ampoule Conditioner 400ml", "marca": "kerasys"},


  
  "E4181100": {"nome": "Blond Absolu - L'Huile Cicagloss - Óleo Capilar 75ml (Refil)", "marca": "kerastase"},
  "H2439101": {"nome": "Blond Absolu - Bain Lumière Shamp 250ml", "marca": "kerastase"},
  "E2920901": {"nome": "Blond Absolu - Bain Ultra-Violet 250ml", "marca": "kerastase"},
  "E2922000": {"nome": "Blond Absolu - Fondant Cicaflash 250ml", "marca": "kerastase"},
  "E3510000": {"nome": "Blond Absolu - Huile Cicaextreme 100ml", "marca": "kerastase"},
  "E3509100": {"nome": "Blond Absolu - Masque Cicaextreme 200ml", "marca": "kerastase"},
  "E2922401": {"nome": "Blond Absolu - Masque Ultra-Violet 200ml", "marca": "kerastase"},
  "E3430101": {"nome": "Blond Absolu - Sérum Cicanuit 90ml", "marca": "kerastase"},
  "E2922601": {"nome": "Blond Absolu - Sérum Cicaplasme 150ml", "marca": "kerastase"},
  "E4070200": {"nome": "Blond Absolu - Sérum Pure Hyaluronic Acid 2% 50ml", "marca": "kerastase"},
  "E3806200": {"nome": "Chroma Absolu - Bain Chroma Respect 250ml", "marca": "kerastase"},
  "E3806100": {"nome": "Chroma Absolu - Bain Riche Chroma Respect 250ml", "marca": "kerastase"},
  "E3806600": {"nome": "Chroma Absolu - Chroma Thermique 150ml", "marca": "kerastase"},
  "E3807900": {"nome": "Chroma Absolu - Fondant Cica Chroma 200ml", "marca": "kerastase"},
  "E3807400": {"nome": "Chroma Absolu - Masque Chroma Filler 200ml", "marca": "kerastase"},
  "E3807100": {"nome": "Chroma Absolu - Soin Acide Chroma Gloss 210ml", "marca": "kerastase"},
  "E4181700": {"nome": "Chroma Absolu - REFILL L'Huile Chroma Éclat Radiance - Oil REFILL 75ml", "marca": "kerastase"},
  "E4182600": {"nome": "Chroma Absolu - Chroma Absolu - L'Huile Chroma Éclat Radiance REFILLABLE - Oil 75ml", "marca": "kerastase"},
  "H2491101": {"nome": "Chronologiste - Bain Régénérant 250ml", "marca": "kerastase"},
  "H2491301": {"nome": "Chronologiste - Masque Intense Régénérant 200ml", "marca": "kerastase"},
  "E3291901": {"nome": "Chronologiste - Thermique Régénérant 150ml", "marca": "kerastase"},
  "E3550700": {"nome": "Curl Manifesto - Bain Hydratation Douceur Shampoo 250ml", "marca": "kerastase"},
  "E3551300": {"nome": "Curl Manifesto - Crème de Jour Fondamentale 150ml", "marca": "kerastase"},
  "E3551700": {"nome": "Curl Manifesto - Fondant Hydratation Essentielle 250ml", "marca": "kerastase"},
  "E3551100": {"nome": "Curl Manifesto - Gelée Curl Contour 150ml", "marca": "kerastase"},
  "E3553500": {"nome": "Curl Manifesto - Lotion Refresh Absolu 190ml", "marca": "kerastase"},
  "E2646102": {"nome": "Densifique - Bain Densité 250ml", "marca": "kerastase"},
  "E1957502": {"nome": "Densifique - Fondant Densité 200ml", "marca": "kerastase"},
  "H1800323": {"nome": "Densifique - Masque Densité 200ml", "marca": "kerastase"},
  "E1936101": {"nome": "Discipline - Bain Fluidealiste 250ml", "marca": "kerastase"},
  "H1800722": {"nome": "Discipline - Maskeratine 200ml", "marca": "kerastase"},
  "E2727900": {"nome": "Elixir Ultime - Huile Rose 100ml", "marca": "kerastase"},
  "E4166800": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 75ml", "marca": "kerastase"},
  "E4167200": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 30ml", "marca": "kerastase"},
  "E4167100": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 75ml Refil", "marca": "kerastase"},
  "E2691701": {"nome": "Elixir Ultime - Le Bain 250ml", "marca": "kerastase"},
  "E2795701": {"nome": "Elixir Ultime - Le Fondant 200ml", "marca": "kerastase"},
  "E2692500": {"nome": "Elixir Ultime - Le Masque 200ml", "marca": "kerastase"},
  "H2517300": {"nome": "Genesis - Bain Nutri-Fortifiant 250ml", "marca": "kerastase"},
  "E3245101": {"nome": "Genesis - Cure Anti-Chute Fortifiant 90ml", "marca": "kerastase"},
  "E3244800": {"nome": "Genesis - Fluide Défense Thermique 150ml", "marca": "kerastase"},
  "E3244001": {"nome": "Genesis - Fondant Renforçateur 200ml", "marca": "kerastase"},
  "H2517100": {"nome": "Genesis - Masque Reconstituant 200ml", "marca": "kerastase"},
  "E3837700": {"nome": "Genesis Homme - Bain de Force 250ml", "marca": "kerastase"},
  "E3837600": {"nome": "Genesis Homme - Bain de Masse 250ml", "marca": "kerastase"},
  "E3838400": {"nome": "Genesis Homme - Cire 75ml", "marca": "kerastase"},
  "E3837400": {"nome": "Genesis Homme - Sérum Anti-Chute Fortifiant 90ml", "marca": "kerastase"},
  "H2516700": {"nome": "Kérastase - Genesis - Bain Hydra-Fortifiant 250ml", "marca": "kerastase"},
  "E4040400": {"nome": "Nutritive - 8h Magic Night Serum 90ml", "marca": "kerastase"},
  "E4039300": {"nome": "Nutritive - Bain Satin 250ml", "marca": "kerastase"},
  "E4039600": {"nome": "Nutritive - Bain Satin Riche 250ml", "marca": "kerastase"},
  "E4040000": {"nome": "Nutritive - Fondant Vital 200ml", "marca": "kerastase"},
  "E4040600": {"nome": "Nutritive - Lotion Thermique Sublimatrice 150ml", "marca": "kerastase"},
  "E4039800": {"nome": "Nutritive - Masque Intense 200ml", "marca": "kerastase"},
  "E4040200": {"nome": "Nutritive - Masque Riche 200ml", "marca": "kerastase"},
  "E4040801": {"nome": "Nutritive - Nectar Thermique 150ml", "marca": "kerastase"},
  "E4042200": {"nome": "Nutritive - Scalp Serum 90ml", "marca": "kerastase"},
  "E4040500": {"nome": "Nutritive - Supplement Split Ends Sérum 50ml", "marca": "kerastase"},
  "E4039700": {"nome": "Nutritive - Bain Satin Riche - Shampoo - 500ml", "marca": "kerastase"},

  "E3073001": {"nome": "Oléo-Relax - Bain 250ml", "marca": "kerastase"},
  "E3063900": {"nome": "Oléo-Relax - Masque 200ml", "marca": "kerastase"},
  "E4109800": {"nome": "Première - Bain Décalcifiant Réparateur 250ml", "marca": "kerastase"},
  "E4113900": {"nome": "Première - Concentré Décalcifiant Ultra-Réparateur - Tratamento Pré-Shampoo 250ml", "marca": "kerastase"},
  "E4114400": {"nome": "Première - Concentré Décalcifiant Ultra-Réparateur - Tratamento Pré-Shampoo 45ml", "marca": "kerastase"},
  "E4114100": {"nome": "Première - Fondant Fluidité Réparateur 200ml", "marca": "kerastase"},
  "E4115200": {"nome": "Première - Huile Gloss Réparatrice (Óleo) 30ml", "marca": "kerastase"},
  "E4113500": {"nome": "Première - Masque Filler Réparateur 200ml", "marca": "kerastase"},
  "E4113800": {"nome": "Première - Sérum Filler Fondamental 90ml", "marca": "kerastase"},
  "E2678500": {"nome": "Résistance - Bain Extentioniste 250ml", "marca": "kerastase"},
  "E1928102": {"nome": "Résistance - Bain Force Architecte 250ml", "marca": "kerastase"},
  "E1928301": {"nome": "Résistance - Bain Thérapiste 250ml", "marca": "kerastase"},
  "E1036204": {"nome": "Résistance - Ciment Thermique 150ml", "marca": "kerastase"},
  "E3134502": {"nome": "Résistance - Extentioniste Thermique 150ml", "marca": "kerastase"},
  "E2680901": {"nome": "Résistance - Fondant Extentioniste 200ml", "marca": "kerastase"},
  "E2683400": {"nome": "Résistance - Masque Extentioniste 200ml", "marca": "kerastase"},
  "H1804921": {"nome": "Résistance - Masque Force Architecte 200ml", "marca": "kerastase"},
  "H1805123": {"nome": "Résistance - Masque Thérapiste 200ml", "marca": "kerastase"},
  "E2755201": {"nome": "Résistance - Sérum Extentioniste Scalp 50ml", "marca": "kerastase"},
  "E1490202": {"nome": "Résistance - Sérum Thérapiste 2x15ml", "marca": "kerastase"},
  "E3520500": {"nome": "Spécifique - Bain Divalent 250ml", "marca": "kerastase"},
  "H1805321": {"nome": "Spécifique - Bain Prévention 250ml", "marca": "kerastase"},
  "E1924220": {"nome": "Spécifique - Masque Hydra Apaisant 200ml", "marca": "kerastase"},
  "E3520300": {"nome": "Spécifique - Masque Réhydratant 200ml", "marca": "kerastase"},
  "E3519900": {"nome": "Spécifique - Sérum Potentialiste 90ml", "marca": "kerastase"},
  "E3996700": {"nome": "Symbiose - Bain Crème Anti-Pelliculaire 250ml", "marca": "kerastase"},
  "E4000000": {"nome": "Symbiose - Fondant Apaisant Essentiel 200ml", "marca": "kerastase"},
  "H2516710": {"nome": "Genesis Bain Hydra-Fortifiant - Shampoo Refil 500ml", "marca": "kerastase"},
"E4181400": {"nome": "Blond Absolu L'Huile Cicagloss - Óleo Capilar 75ml", "marca": "kerastase"},

  
  
  "493.046-G": {"nome": "All In One Leave-In Multifuncional - Spray de Gatilho 240ml", "marca": "Image"},
  "493.046-P": {"nome": "All In One Leave-In Multifuncional - Spray de Pump 240ml", "marca": "Image"},
  "493.021": {"nome": "Cherimoya Clenz Shampoo 1L", "marca": "Image"},
  "493.049": {"nome": "Cherimoya Clenz Shampoo 240ml", "marca": "Image"},
  "493.034": {"nome": "Colors Serum - Finalizador 30ml", "marca": "Image"},
  "493.040": {"nome": "Covalence Extra - Condicionador 240ml", "marca": "Image"},
  "493.006": {"nome": "Covalence Extra - Condicionador 1L", "marca": "Image"},
  "493.044": {"nome": "Heat Defense - Finalizador 240ml", "marca": "Image"},
  "493.000": {"nome": "Intrakera - Finalizador 240ml", "marca": "Image"},
  "493.037": {"nome": "Light Serum - Finalizador 30ml", "marca": "Image"},
  "Big Pink Image": {"nome": "MakeUp - Esponja de Maquiagem - Big Pink", "marca": "Image"},
  "Mini Pink Image": {"nome": "MakeUp Mini Esponja Chanfrada para os Olhos 3D", "marca": "Image"},
  "Big Pink Image BIG - Saik": {"nome": "Image MakeUp - Esponja de Maquiagem - Pink (BIG)", "marca": "Image"},

  "493.048": {"nome": "Milk - Condicionador 240ml", "marca": "Image"},
  "493.001": {"nome": "Milk - Mask 200g", "marca": "Image"},
  "493.041": {"nome": "Milk Clenz Shampoo Condicionante 240ml", "marca": "Image"},
  "493.047": {"nome": "Reconstructor Water - Finalizador 240ml", "marca": "Image"},
  "493.042": {"nome": "Yucca Blossom Energizing Body & Shine - Condicionador 240ml", "marca": "Image"},
  "493.015": {"nome": "Yucca Blossom Energizing Body & Shine - Condicionador 1L", "marca": "Image"},
  "493.045": {"nome": "FINISHING MIST JUMPING CURLS 240mL", "marca": "Image"},
  
    "39852E_5": {"nome": "Keep My Blonde Mask CD 750ml", "marca": "ice"},
  "51038E_5": {"nome": "Tame My Hair Cream 100ml", "marca": "ice"},
  "50895E_5": {"nome": "Refill My Hair Power Booster 30ml", "marca": "ice"},
  "39913E_5": {"nome": "Keep My Color CD Mask 750ml", "marca": "ice"},
  "39906E_5": {"nome": "Keep My Color Shampoo 1L", "marca": "ice"},
  "50239E_5": {"nome": "Keep My Blonde Conditioner Anti-yellow 250ml", "marca": "ice"},
  "51151E_5": {"nome": "Keep My Blonde Mask Anti-Yellow 200ml", "marca": "ice"},
  "50222E_5": {"nome": "Keep My Blonde Shampoo Anti-yellow 250ml", "marca": "ice"},
  "50253E_5": {"nome": "Keep My Color Conditioner 250ml", "marca": "ice"},
  "50956E_5": {"nome": "Keep My Color Mask 200ml", "marca": "ice"},
  "50963E_5": {"nome": "Keep My Color Serum 50ml", "marca": "ice"},
  "50246E_5": {"nome": "Keep My Color Shampoo 250ml", "marca": "ice"},
  "39883E_5": {"nome": "Refill My Hair Cd Mask 750ml", "marca": "ice"},
  "50192E_5": {"nome": "Refill My Hair Conditioner 250ml", "marca": "ice"},
  "50840E_5": {"nome": "Refill My Hair Mask 200ml", "marca": "ice"},
  "03853BR": {"nome": "Refill My Hair Mask 50ml", "marca": "ice"},
  "39876E_5": {"nome": "Refill My Hair Shampoo 1000ml", "marca": "ice"},
  "50185E_5": {"nome": "Refill My Hair Shampoo 250ml", "marca": "ice"},
  "50857E_5": {"nome": "Refill My Hair Spray 100ml", "marca": "ice"},
  "50215E_5": {"nome": "Refresh My Scalp Conditioner 250ml", "marca": "ice"},
  "39890E_5": {"nome": "Refresh My Scalp Shampoo 1000ml", "marca": "ice"},
  "50208E_5": {"nome": "Refresh My Scalp Shampoo 250ml", "marca": "ice"},
  "51076E_5": {"nome": "Repair My Hair Cd Mask 200ml", "marca": "ice"},
  "50291E_5": {"nome": "Repair My Hair Conditioner 250ml", "marca": "ice"},
  "03839BR": {"nome": "Repair My Hair Mask 50ml", "marca": "ice"},
  "39951E_5": {"nome": "Repair My Hair Mask 750ml", "marca": "ice"},
  "51083E_5": {"nome": "Repair My Hair Oil 50ml", "marca": "ice"},
  "39944E_5": {"nome": "Repair My Hair Shampoo 1000ml", "marca": "ice"},
  "50284E_5": {"nome": "Repair My Hair Shampoo 250ml", "marca": "ice"},
  "51090E_5": {"nome": "Repair My Hair Spray 100ml", "marca": "ice"},
  "50277E_5": {"nome": "Tame My Hair Conditioner 250ml", "marca": "ice"},
  "51007E_5": {"nome": "Tame My Hair Mask 200ml", "marca": "ice"},
  "03846BR": {"nome": "Tame My Hair Mask 50ml", "marca": "ice"},
  "39937E_5": {"nome": "Tame My Hair Mask 750ml", "marca": "ice"},
  "51045E_5": {"nome": "Tame My Hair Oil 50ml", "marca": "ice"},
  "51052E_5": {"nome": "Tame My Hair Pre-Shampoo Oil 100ml", "marca": "ice"},
  "39920E_5": {"nome": "Tame My Hair Shampoo 1000ml", "marca": "ice"},
  "50260E_5": {"nome": "Tame My Hair Shampoo 250ml", "marca": "ice"},
  "51014E_5": {"nome": "Tame My Hair Spray 100ml", "marca": "ice"},

    "KIWIMASC1": {"nome": "Máscara Hidratante 250ml", "marca": "Carol"},
  "PA321": {"nome": "Anti-Porosidade - Finalizador Bifásico 150ml", "marca": "Carol"},
  "PA320": {"nome": "Anti-Porosidade - Gel Reconstrutor 150ml", "marca": "Carol"},
  "PA322": {"nome": "Anti-Porosidade - Máscara 250g", "marca": "Carol"},
  "PA319": {"nome": "Anti-Porosidade - Shampoo 290ml", "marca": "Carol"},
  "PA352": {"nome": "Cresce Resist - Leave-In Finalizador Fortalecimento Capilar 150ml", "marca": "Carol"},
  "PA350": {"nome": "Cresce Resist - Máscara Fortalecimento Capilar 250ml", "marca": "Carol"},
  "PA349": {"nome": "Cresce Resist - Shampoo Hidratante 290ml", "marca": "Carol"},
  "PA351": {"nome": "Cresce Resist - Tônico Fortalecimento Capilar 150ml", "marca": "Carol"},
  "PA353": {"nome": "Cresce Resist - Óleo Fortalecimento Capilar 40ml", "marca": "Carol"},
  "PA323": {"nome": "Detox - Shampoo Esfoliante 290ml", "marca": "Carol"},
  "PA443": {"nome": "Hydra Matrix - Máscara 250ml", "marca": "Carol"},
  "PA441": {"nome": "Hydra Matrix - Shampoo Hidratante 290ml", "marca": "Carol"},
  "PA442": {"nome": "Hydra Matrix - Spray Capilar 10-in-1 150ml", "marca": "Carol"},
  "PA526": {"nome": "Vitra Protect - Sérum Anti-Umidade 60ml", "marca": "Carol"},
  "PA523": {"nome": "Vitra Protect - Shampoo Disciplinante 290ml", "marca": "Carol"},
  "PA525": {"nome": "Vitra Protect - Spray Anti-Umidade 150ml", "marca": "Carol"},
  "PA527": {"nome": "Óleo e Tratamento Diurno e Noturno 60ml (Exclusivo)", "marca": "Carol"},
  "PA550": {"nome": "Left Cosméticos - Café + Cacau - Loção Hidratante 150g", "marca": "carol"},
"CK - NÉCESSAIRE": {"nome": "CK - NÉCESSAIRE", "marca": "carol"},

  
  "140804": {"nome": "Artistic Edit Base Player - Protein Spray 250ml", "marca": "BEDHEAD"},
  "140796": {"nome": "Artistic Edit Juxta-Pose Dry Serum 50ml", "marca": "BED HEAD"},
  "140794": {"nome": "Artistic Edit Shine Heist LightWeight Conditioning Cream 100ml", "marca": "BEDHEAD"},
  "140795": {"nome": "Artistic Edit Wave Rider - Versatile Style Cream 100ml", "marca": "BEDHEAD"},
  "140737": {"nome": "CD BACK IT UP CREAM 125ML", "marca": "BEDHEAD"},
  "330506": {"nome": "CD CO COLOUR GODDESS 100ML", "marca": "BEDHEAD"},
  "330508": {"nome": "CD CO COLOUR GODDESS 400ML", "marca": "BEDHEAD"},
  "330564": {"nome": "CD CO COLOUR GODDESS 750ML", "marca": "BEDHEAD"},
  "330496": {"nome": "CD CO GIMME GRIP 400ML", "marca": "BEDHEAD"},
  "330516": {"nome": "CD CO RECOVERY 100ML", "marca": "BEDHEAD"},
  "330518": {"nome": "CD CO RECOVERY 400ML", "marca": "BEDHEAD"},
  "330562": {"nome": "CD CO RECOVERY 750ML", "marca": "BEDHEAD"},
  "330520": {"nome": "CD CO RECOVERY 970ML", "marca": "BEDHEAD"},
  "330522": {"nome": "CD CO RESURRECTION 100ML", "marca": "BEDHEAD"},
  "330524": {"nome": "CD CO RESURRECTION 400ML", "marca": "BEDHEAD"},
  "330563": {"nome": "CD CO RESURRECTION 750ML", "marca": "BEDHEAD"},
  "330526": {"nome": "CD CO RESURRECTION 970ML", "marca": "BEDHEAD"},
  "330499": {"nome": "CD CO SERIAL BLONDE 400ML", "marca": "BEDHEAD"},
  "330565": {"nome": "CD CO SERIAL BLONDE 750ML", "marca": "BEDHEAD"},
  "330501": {"nome": "CD CO SERIAL BLONDE 970ML", "marca": "BEDHEAD"},
  "140817": {"nome": "CD CURLS ROCK AMPLIFIER 113ML", "marca": "BEDHEAD"},
  "140778": {"nome": "CD CURLS ROCK AMPLIFIER 43ML", "marca": "BEDHEAD"},
  "330532": {"nome": "CD DOWN N DIRTY 400ML", "marca": "BEDHEAD"},
  "330338": {"nome": "CD FOR MEN CLEAN UP 200ML", "marca": "BEDHEAD"},
  "330513": {"nome": "CD MAKE IT LAST LEAVE-IN 200ML", "marca": "BEDHEAD"},
  "140736": {"nome": "CD MANIPULATOR MATTE WAX 30G", "marca": "BEDHEAD"},
  "140735": {"nome": "CD MANIPULATOR MATTE WAX 57G", "marca": "BEDHEAD"},
  "140734": {"nome": "CD MANIPULATOR PASTE 30G", "marca": "BEDHEAD"},
  "140733": {"nome": "CD MANIPULATOR PASTE 57G", "marca": "BEDHEAD"},
  "140738": {"nome": "CD SALTY NOT SORRY 100ML", "marca": "BEDHEAD"},
  "330558": {"nome": "COND SELF ABSORBED 400ML", "marca": "BEDHEAD"},
  "330556": {"nome": "COND SELF ABSORBED 750ML", "marca": "BEDHEAD"},
  "140823": {"nome": "CONTROL FREAK 255ml", "marca": "BEDHEAD"},
  "140816": {"nome": "CR AFTER PARTY SMOOTH 100ML", "marca": "BEDHEAD"},
  "140727": {"nome": "CR AFTER PARTY SMOOTH 50ML", "marca": "BEDHEAD"},
  "140821": {"nome": "EGO BOOST 237ml", "marca": "BEDHEAD"},
  "140006": {"nome": "Hair Stick Wax 73G", "marca": "BEDHEAD"},
  "330557": {"nome": "Moisture Maniac Cond 400mL", "marca": "BEDHEAD"},
  "330555": {"nome": "Moisture Maniac Cond 750mL", "marca": "BEDHEAD"},
  "300557": {"nome": "Moisture Maniac Spoo 400mL", "marca": "BEDHEAD"},
  "140740": {"nome": "Row Trouble Maker Spray Wax Aero 160g, 200ml", "marca": "BEDHEAD"},
  "300503": {"nome": "Serial Blonde Purple Toning Spoo 400mL", "marca": "BEDHEAD"},
  "300547": {"nome": "SH Bigger the Better Foam 200mL", "marca": "BEDHEAD"},
  "300506": {"nome": "SH Colour Goddess 100mL", "marca": "BEDHEAD"},
  "300508": {"nome": "SH Colour Goddess 400mL", "marca": "BEDHEAD"},
  "300564": {"nome": "SH Colour Goddess 750mL", "marca": "BEDHEAD"},
  "300545": {"nome": "SH Dry Oh Bee Hive 142g/238ml", "marca": "BEDHEAD"},
  "300538": {"nome": "SH Dry Rock Dirty 179g/300ml", "marca": "BEDHEAD"},
  "300369": {"nome": "SH For Men Clean Up 250mL", "marca": "BEDHEAD"},
  "300496": {"nome": "SH Gimme Grip 400mL", "marca": "BEDHEAD"},
  "300555": {"nome": "SH Moisture Maniac 750mL", "marca": "BEDHEAD"},
  "300516": {"nome": "SH Recovery 100mL", "marca": "BEDHEAD"},
  "300516-1": {"nome": "SH Recovery 100mL", "marca": "BEDHEAD"},
  "300518": {"nome": "SH Recovery 400mL", "marca": "BEDHEAD"},
  "300562": {"nome": "SH Recovery 750mL", "marca": "BEDHEAD"},
  "300520": {"nome": "SH Recovery 970mL", "marca": "BEDHEAD"},
  "300522": {"nome": "SH Resurrection 100mL", "marca": "BEDHEAD"},
  "300524": {"nome": "SH Resurrection 400mL", "marca": "BEDHEAD"},
  "300563": {"nome": "SH Resurrection 750mL", "marca": "BEDHEAD"},
  "300526": {"nome": "SH Resurrection 970mL", "marca": "BEDHEAD"},
  "300558": {"nome": "SH Self Absorbed 400mL", "marca": "BEDHEAD"},
  "300556": {"nome": "SH Self Absorbed 750mL", "marca": "BEDHEAD"},
  "300499": {"nome": "SH Serial Blonde 400mL", "marca": "BEDHEAD"},
  "300565": {"nome": "SH Serial Blonde 750mL", "marca": "BEDHEAD"},
  "140724": {"nome": "Small Talk 125mL", "marca": "BEDHEAD"},
  "140723": {"nome": "Small Talk 240mL", "marca": "BEDHEAD"},
  "140776": {"nome": "Some Like it Hot Heat Protection Spray 100mL", "marca": "BEDHEAD"},
  "140745": {"nome": "SPR Hard Head 385mL", "marca": "BEDHEAD"},
  "140751": {"nome": "SPR Hard Head 85g/100mL", "marca": "BEDHEAD"},
  "140728": {"nome": "SPR Headrush 144g/200mL", "marca": "BEDHEAD"},
  "140754": {"nome": "SPR Masterpiece 255g/340mL", "marca": "BEDHEAD"},
  "140760": {"nome": "SPR Masterpiece 68g/80mL", "marca": "BEDHEAD"},
  "140717": {"nome": "SPR Queen for a Day 298g/311mL", "marca": "BEDHEAD"},
  "140732": {"nome": "Straighten Out Serum 100mL", "marca": "BEDHEAD"},
  "1000665": {"nome": "Treat Me Right Mask 200mL", "marca": "BEDHEAD"},
  "140731": {"nome": "Wanna Glow 100mL", "marca": "BEDHEAD"},
  "1000038": {"nome": "Mini Small Talk Blah Blah Blah - 125ml", "marca": "BEDHEAD"},
  "New140760": {"nome": "Mini Masterpiece 79ml", "marca": "BEDHEAD"},
  
  "BH - Recovery Sh 600": {"nome": "Recovery Shampoo 600ml", "marca": "bedhead"},
"300516-1": {"nome": "Recovery Shampoo  100ml", "marca": "bedhead"},
"1000136": {"nome": "BED HEAD KEEP IT CASUAL HAIRSPRAY 300ML", "marca": "bedhead"},



  
  
  
  "C-ASCL10-001A": {"nome": "B. By Banila Lip & Eye Remover 99ml", "marca": "Banila"},
  "B-ASPM08-007A": {"nome": "Blooming Youth Peach Collagen Mask 20ml", "marca": "Banila"},
  "B-ASFC10-007A": {"nome": "Blooming Youth Peach-Collagen Multi Stick Balm 10.5g", "marca": "Banila"},
  "B-ASCL09-006A": {"nome": "Clean It Zero - Brightening Peeling Gel 120ml", "marca": "Banila"},
  "B-DENS01-325A": {"nome": "Clean It Zero - Calming Foam Cleanser Cica-Relief 30ml", "marca": "Banila"},
  "B-AXST01-382A": {"nome": "Clean It Zero - Christmas Special Edition Gbd 50mlx2", "marca": "Banila"},
  "B-ASCL01-086A": {"nome": "Clean It Zero - Cleansing Balm Brightening 100ml", "marca": "Banila"},
  "B-DENS01-343A": {"nome": "Clean It Zero - Cleansing Balm Calming Mini 7ml", "marca": "Banila"},
  "B-ASCL01-020B": {"nome": "Clean It Zero - Cleansing Balm Nourishing 100ml", "marca": "Banila"},
  "B-DENS01-344A": {"nome": "Clean It Zero - Cleansing Balm Nourishing Mini 7ml", "marca": "Banila"},
  "B-ASCL01-033A": {"nome": "Clean It Zero - Cleansing Balm Original 100ml", "marca": "Banila"},
  "B-ASCL01-042A": {"nome": "Clean It Zero - Cleansing Balm Original 25ml", "marca": "Banila"},
  "B-DENS01-123B": {"nome": "Clean It Zero - Cleansing Balm Original Mini 7ml", "marca": "Banila"},
  "B-CEGT01-024C": {"nome": "Clean It Zero - Cleansing Balm Original Miniature Set (2 Types)", "marca": "Banila"},
  "B-CEGT01-022C": {"nome": "Clean It Zero - Cleansing Balm Original Miniature Set (4 Types)", "marca": "Banila"},
  "B-ASCL01-045A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying 100ml", "marca": "Banila"},
  "B-ASCL01-126A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying 50ml", "marca": "Banila"},
  "B-DENS01-342A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying Mini 7ml", "marca": "Banila Co"},
  "B-ASCL01-022B": {"nome": "Clean It Zero - Cleansing Balm Purifying 100ml", "marca": "Banila"},
  "B-ASCL01-017B": {"nome": "Clean It Zero - Cleansing Balm Revitalizing 100ml", "marca": "Banila"},
  "B-ASCL02-023B": {"nome": "Clean It Zero - Foam Cleanser 150ml", "marca": "Banila"},
  "B-DENS01-130A": {"nome": "Clean It Zero - Foam Cleanser Mini 8ml", "marca": "Banila"},
  "B-ASFC13-001A": {"nome": "Clean It Zero - Green Peel Toner 70 Pads 200ml", "marca": "Banila"},
  "B-ASCL01-137A": {"nome": "Clean It Zero - Hello Kitty Cleansing Balm 100ml", "marca": "Banila"},
  "B-AXST01-307A": {"nome": "Clean It Zero - Kit 3 Mini Foam Favorites X15ml", "marca": "Banila"},
  "B-ASCL01-138A": {"nome": "Clean It Zero - My Melody Cleansing Balm 100ml", "marca": "Banila"},
  "B-ASFC02-045A": {"nome": "Clean It Zero - Pink Hydration Toner 70 Pads 235ml", "marca": "Banila"},
  "B-AXST01-329B": {"nome": "Clean It Zero - Pink Wonderland Set", "marca": "Banila"},
  "B-ASCL02-029A": {"nome": "Clean It Zero - Pore Clarifying Foam Cleanser 150ml", "marca": "Banila"},
  "B-ASCL06-004E": {"nome": "Clean It Zero - Pure Cleansing Water 310ml", "marca": "Banila"},
  "B-ASCL02-036A": {"nome": "Clean It Zero - Purifying Foam Cleanser 150ml", "marca": "Banila"},
  "B-ASCL10-014A": {"nome": "Clean It Zero - Soothing Lip & Eye Makeup Remover 99ml", "marca": "Banila"},
  "B-ASEY01-003A": {"nome": "Dear Hydration - Bounce Eye Cream 20ml", "marca": "Banila"},
  "B-ASFC05-028C": {"nome": "Dear Hydration - Cool Down Mist 99ml", "marca": "Banila"},
  "B-ASFC02-043B": {"nome": "Dear Hydration - Crystal Glow Essence 50ml", "marca": "Banila"},
  "B-AXST01-408A": {"nome": "Kit Set Starter", "marca": "Banila"},
  "B-AXST01-319B": {"nome": "Dear Hydration - Mini Duo Kit", "marca": "Banila"},
  "B-ASFC02-036C": {"nome": "Dear Hydration - Toner 200ml", "marca": "Banila"},
  "B-CEGT01-201A": {"nome": "Dear Hydration - Water Barrier Cream 10ml", "marca": "Banila"},
  "B-ASFC02-038C": {"nome": "Dear Hydration - Water Barrier Cream 50ml", "marca": "Banila"},
  "B-ASFC07-002A": {"nome": "Miss Flower E Mr. Honey Essence Stick 9g", "marca": "Banila"},
  "B-ASFC07-004A": {"nome": "Miss Flower E Mr. Honey Propolis Rejuvenating 50ml", "marca": "Banila"},
  "B-ASFC07-009A": {"nome": "Miss Flower E Mr. Honey Propolis Rejuvenating Ampoule Mist 99ml", "marca": "Banila"},
  "B-AMBS02-001P": {"nome": "Prime Primer - Classic 30ml", "marca": "Banila"},
  "B-AMBS02-007E": {"nome": "Prime Primer - Finish Powder 12g", "marca": "Banila"},
  "B-AMBS02-005E": {"nome": "Prime Primer - Hydrating 30ml", "marca": "Banila"},
  "B-AMBS02-036B": {"nome": "Prime Primer - Tone-Up 30ml", "marca": "Banila"},
  "B-ASFC10-002B": {"nome": "Vv Vitalizing Collagen Essence 50ml", "marca": "Banila"},
  "B-CEGT01-230A": {"nome": "GIFT BANILA CO Twisted Hair Bend", "marca": "Banila"},
  "B-ASCL01-087A": {"nome": "Banila Co - Clean it Zero Cleansing Balm - Ceramide 100ml", "marca": "Banila"},
  "C-AMLP07-006A": {"nome": "PK02", "marca": "Banila"},
  "C-AMLP07-005A": {"nome": "PK01", "marca": "Banila"},
  "C-AMLP07-010A": {"nome": "PP01", "marca": "Banila"},
  "B-AXST01-383A": {"nome": "GBD", "marca": "Banila"},
  "B-DENS01-349A": {"nome": "Mini Enriching Butter 7ml (Avocado+)", "marca": "Banila"},
"C-AMLP07-009A": {"nome": "RD01", "marca": "banila"},
"B-ASCL01-123A": {"nome": "Clean it Zero Balm - Original 50ml (Acerola+)", "marca": "banila"},
"B-ASCL09-008A": {"nome": "Clean It Zero - Tea Tree Pore Peeling Gel 120ml", "marca": "banila"},
"BC - Pore Clarifying - Foam 30": {"nome": "Espuma de Limpeza para Pele Oleosa Pore Clarifying 30ml", "marca": "banila"},




  
  
  "PF026809": {"nome": "Blond Rescue - Shampoo 1000ML", "marca": "Alfaparf MAB"},
  "PF026795": {"nome": "BB Cream 12 em 1 - Leave-In Condicionante 180ml", "marca": "Alfaparf MAB"},
  "PF026810": {"nome": "Blond Rescue - Condicionador 1000ML", "marca": "Alfaparf MAB"},
  "PF026786": {"nome": "Blond Rescue - Condicionador 300ML", "marca": "Alfaparf MAB"},
  "PF026812": {"nome": "Brazilian Curls - Condicionador 1000ML", "marca": "Alfaparf MAB"},
  "PF026788": {"nome": "Brazilian Curls - Condicionador 300ML", "marca": "Alfaparf"},
  "PF026811": {"nome": "Brazilian Curls - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026787": {"nome": "Brazilian Curls - Shampoo 300ML", "marca": "Alfaparf"},
  "PF026806": {"nome": "Color Shield - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026782": {"nome": "Color Shield - Condicionador 300ML", "marca": "Alfaparf"},
  "PF026851": {"nome": "Condicionador Real Liss 300ml", "marca": "Alfaparf"},
  "PF026807": {"nome": "Hidro Control - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026783": {"nome": "Hidro Control - Shampoo 300ML", "marca": "Alfaparf"},
  "PF026808": {"nome": "Hidro Control - Condicionador 1000ML", "marca": "Alfaparf"},
  "PF026791": {"nome": "Long & Force - Condicionador 300ML", "marca": "Alfaparf"},
  "PF026815": {"nome": "Long & Force - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026790": {"nome": "Long & Force - Shampoo 300ML", "marca": "Alfaparf"},
  "PF026798": {"nome": "Love Oil - Óleo Capilar 55ML", "marca": "Alfaparf"},
  "PF026803": {"nome": "Nutri Restore - Condicionador 1000ML", "marca": "Alfaparf"},
  "PF026777": {"nome": "Nutri Restore - Shampoo 300ML", "marca": "Alfaparf"},
  "PF026802": {"nome": "Nutri Restore - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026818": {"nome": "OX 30VOL 900ml", "marca": "Alfaparf"},
  "PF026819": {"nome": "OX 40VOL 900ml", "marca": "Alfaparf"},
  "PF026805": {"nome": "Oils Recovery - Condicionador 1000ML", "marca": "Alfaparf"},
  "PF026804": {"nome": "Oils Recovery - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026821": {"nome": "Power Reconstruction - Máscara 500G", "marca": "Alfaparf"},
  "PF026814": {"nome": "Real Liss - Condicionador 1000ML", "marca": "Alfaparf"},
  "PF026789": {"nome": "Real Liss - Shampoo 300ML", "marca": "Alfaparf"},
  "PF026813": {"nome": "Real Liss - Shampoo 1000ML", "marca": "Alfaparf"},
  "PF026793": {"nome": "Repair - Máscara 300G", "marca": "Alfaparf"},
  "PF026820": {"nome": "Repair - Máscara 500G", "marca": "Alfaparf"},
  "PF026785": {"nome": "Shampoo Blond Rescue 300ml", "marca": "Alfaparf"},

  "PF016447": {"nome": "Diamond Illuminating - Condicionador 200ML", "marca": "Alfaparf"},
  "PF016449": {"nome": "Diamond Illuminating - Máscara 200ML", "marca": "Alfaparf"},
  "PF016450": {"nome": "Diamond Illuminating - Máscara Capilar 500ML", "marca": "Alfaparf"},
  "PF016445": {"nome": "Diamond Illuminating - Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF016417": {"nome": "Moisture Nutritive - Máscara 200ML", "marca": "Alfaparf"},
  "PF016418": {"nome": "Moisture Nutritive - Máscara 500ML", "marca": "Alfaparf"},
  "PF016419": {"nome": "Nutritive Leave-In Conditioner 200ML", "marca": "Alfaparf"},
  "PF016415": {"nome": "Nutritive Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF019474": {"nome": "Scalp Rebalance Balancing - Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF019472": {"nome": "Scalp Rebalance Purifying - Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF019466": {"nome": "Scalp Renew Energizing - Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF020604": {"nome": "Smooth Smoothing - Conditioner 200ML", "marca": "Alfaparf"},
  "PF020602": {"nome": "Smooth Smoothing - Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF020606": {"nome": "Smooth Smoothing - Máscara 200ML", "marca": "Alfaparf"},
  "PF020607": {"nome": "Smooth Smoothing - Máscara 500ML", "marca": "Alfaparf"},
  "PF025387": {"nome": "Sublime Cristalli Liquidi 15ML", "marca": "Alfaparf"},
  "PF016456": {"nome": "Sublime Cristalli Liquidi 50ML", "marca": "Alfaparf"},
  "PF025944": {"nome": "Sublime Essential Oil - Ampola Capilar 13ML Mono-dose", "marca": "Alfaparf"},
  "PF027566": {"nome": "Reconstruction Reparative - Máscara Capilar 200ML", "marca": "Alfaparf"},
  "PF027567": {"nome": "Reconstruction Reparative - Máscara Capilar 500ML", "marca": "Alfaparf"},
  "PF027564": {"nome": "Reconstruction Reparative Low Shampoo 250ML", "marca": "Alfaparf"},
  "PF014102": {"nome": "Pigments Rose Copper 90ml", "marca": "Alfaparf"},
  "PF026816": {"nome": "Mab - Long & Force - Condicionador 1000ML", "marca": "Alfaparf"},
  "PF026607": {"nome": "Semi Di Lino Sunshine - After-Sun Shampoo 250ml", "marca": "Alfaparf"},
  "PF026608": {"nome": "Semi Di Lino Sunshine - After-Sun Treatment 200ml (Máscara)", "marca": "Alfaparf"},
  "PF026610": {"nome": "Semi Di Lino Sunshine - Hair Protective Milk 125ml", "marca": "Alfaparf"},
  "PF026609": {"nome": "Semi Di Lino Sunshine - Hair Protective Oil 125ml", "marca": "Alfaparf"},
  
    "2801754": {"nome": "DR PAWPAW HOT PINK BALM 25ML", "marca": "Dr.PawPaw"},
  "2807275": {"nome": "DR PAWPAW IT DOES IT ALL CONDITIONER 200ML", "marca": "Dr.PawPaw"},
  "2800214": {"nome": "DR PAWPAW IT DOES IT ALL HAIRCARE 150ML", "marca": "Dr.PawPaw"},
  "2807268": {"nome": "DR PAWPAW IT DOES IT ALL SHAMPOO 200ML", "marca": "Dr.PawPaw"},
  "2800269": {"nome": "DR PAWPAW ORIGINAL BALM 10ML", "marca": "Dr.PawPaw"},
  "2800009": {"nome": "DR PAWPAW ORIGINAL BALM 25ML", "marca": "Dr.PawPaw"},
  "2803277": {"nome": "DR PAWPAW OVERNIGHT LIP MASK 25ML", "marca": "Dr.PawPaw"},
  "2800047": {"nome": "DR PAWPAW PEACH PINK BALM 25ML", "marca": "Dr. PawPaw"},
  "2800542": {"nome": "DR PAWPAW PEACH PINK BALM 8ML", "marca": "Dr.PawPaw"},
  "2800085": {"nome": "DR PAWPAW ULTIMATE RED BALM 25ML", "marca": "Dr.PawPaw"},
  "2800566": {"nome": "DR PAWPAW ULTIMATE RED BALM 8ML", "marca": "Dr.PawPaw"},
  "2808418": {"nome": "DR PAWPAW PLUMPING LIP OIL 8ML", "marca": "Dr.PawPaw"},
  "2808425": {"nome": "DR PAWPAW LIP & EYE BALM 8ML", "marca": "Dr.PawPaw"},
  "2800696": {"nome": "DR PAWPAW SHEA BUTTER LIP BALM 8ML", "marca": "Dr.PawPaw"},
  "2803468": {"nome": "DR. PAWPAW OVERNIGHT LIP MASK 10ML", "marca": "Dr.PawPaw"},
  
    
  
  
  "ADS 101": {"nome": "ADS 101", "marca": "purederm"},
  "ADS 748": {"nome": "ADS 748", "marca": "purederm"},
  "ADS 763": {"nome": "Purederm- ADS 763 - Adesivo Hidratante em Gel para os Olhos", "marca": "purederm"},
  "ADS 841": {"nome": "ADS 841", "marca": "purederm"},
  "ADS 200": {"nome": "ADS 200", "marca": "purederm"},
  "ADS 822": {"nome": "ADS 822 PUREDERM TROUBLE CLEAR SPOT 22 PATCHES", "marca": "purederm"},
  "PR 413": {"nome": "PR 413 - DAILYMOSTURE HANDCREAM 50ML", "marca": "purederm"},
  "PR 408": {"nome": "PR 408 - PUREDERM HONEY & BERRY LIP SLEEPING MASK 15G", "marca": "purederm"},
  "PR 419": {"nome": "PR 419 - PUREDERM Prreti: Biome Collagen Eye Cream 30ml", "marca": "purederm"},
  "PR 420": {"nome": "PR 420 - PUREDERM P/R REPAIR CERAMIDE CREAM 50ML", "marca": "purederm"},
  "PR 526": {"nome": "PR 526 - PUREDERM SERUM FACIAL ÁCIDO HIALURÔNICO PURO", "marca": "purederm"},
  "PR 548": {"nome": "PR 548 - BIOME COLLAGEN BLENDING SERUM&CREAM 90G", "marca": "purederm"},
  "PR 538": {"nome": "PR 538", "marca": "purederm"},
  "PR 423": {"nome": "PR 423", "marca": "purederm"},
  "PR 401": {"nome": "PR 401", "marca": "purederm"},




      
  "TSH20": {"nome": "Serum Ampoule Mucina da Caracol 5000", "marca": "exi"},
  "TSH30": {"nome": "Serum Ampoule ácido Hialurônico 6000", "marca": "exi"},
  "TSH40": {"nome": "Sleeping Mask Multifuncional", "marca": "exi"},
  "471170": {"nome": "UB TIGI LARGE PADDLE BRUSH", "marca": "exi"},
  "471169": {"nome": "UB TIGI SMALL PADDLE BRUSH", "marca": "exi"},
  "471168": {"nome": "UB TIGI VENT BRUSH", "marca": "exi"},
  "471167": {"nome": "UB TIGI X-LARGE ROUND BRUSH 2", "marca": "exi"},
  "DS04": {"nome": "Highprime Collagen Ampoule Mist 50ml", "marca": "exi"},
  "DS02": {"nome": "Highprime Collagen Film Cheek (5pcs)", "marca": "exi"},
  "DS01": {"nome": "Highprime Collagen Film Eye or Smilelines (5pcs)", "marca": "exi"},
  "DS03": {"nome": "Highprime Collagen Film Forehead Or Neck (5pcs)", "marca": "exi"},
  "VTPD40136": {"nome": "Essência Reedle Shot 1000 - 15ml", "marca": "exi"},
  "VTPD40019": {"nome": "Essência Reedle Shot 300 - 50ml", "marca": "exi"},
  
   
  
  
  
  
  "24227-2": {"nome": "OPI - Black Onyx - Esmalte Cremoso 15ml", "marca": "sac"},
  "24235-2": {"nome": "OPI - Dulce de Leche - Esmalte Cremoso 15ml", "marca": "sac"},
  "24234-1": {"nome": "OPI - Red Hot Rio - Esmalte Cremoso 15ml", "marca": "sac"},

  "24236-2": {"nome": "Chick Flick Cherry - Esmalte Cremoso 15ml", "marca": "sac"},
  "24241-2": {"nome": "My Private Jet - Esmalte Cintilante 15ml", "marca": "sac"},
  "24327-1": {"nome": "NTT 10 Natural Coat - Base 15ml", "marca": "sac"},
  "3,6163E+12": {"nome": "Start To Finish - Base 3 em 1 15ml", "marca": "sac"},
  "24326-1": {"nome": "Top Coat - Finalizador Brilhante 15ml NTT 30", "marca": "sac"},
  "H0250223": {"nome": "HT Inc 7,3 - Louro Dourado 50g", "marca": "sac"},
  "H0250322": {"nome": "HT Inc 7,31 - Louro Bege Dourado 50g", "marca": "sac"},
  "H0250522": {"nome": "HT Inc 7,4 - Louro Acobreado 50g", "marca": "sac"},
  "H0250822": {"nome": "HT Inc 8,3 - Louro Claro Dourado 50g", "marca": "sac"},
  "H0251022": {"nome": "HT Inc 8,34 - Louro Claro Dourado Acobreado 50g", "marca": "sac"},
  "H2641900": {"nome": "INOA 1 60G", "marca": "sac"},
  "E3972200": {"nome": "INOA 10 60G", "marca": "sac"},
  "H2642000": {"nome": "INOA 3 60G", "marca": "sac"},
  "H2642100": {"nome": "INOA 4 60G", "marca": "sac"},
  "H2642200": {"nome": "INOA 5 60G", "marca": "sac"},
  "E3964100": {"nome": "INOA 5,1 60G", "marca": "sac"},
  "E3974700": {"nome": "INOA 5,3 60G", "marca": "sac"},
  "H2642400": {"nome": "INOA 6 60G", "marca": "sac"},
  "H2642500": {"nome": "INOA 6,0 60G", "marca": "sac"},
  "H2643300": {"nome": "INOA 6,1 60G", "marca": "sac"},
  "E3972700": {"nome": "INOA 6,3 60G", "marca": "sac"},
  "H2642600": {"nome": "INOA 7 60G", "marca": "sac"},
  "H2642700": {"nome": "INOA 7,0 60G", "marca": "sac"},
  "H2643600": {"nome": "INOA 7,1 60G", "marca": "sac"},
  "H2643700": {"nome": "INOA 7,31 60G", "marca": "sac"},
  "E3984600": {"nome": "INOA 7,4 60G", "marca": "sac"},
  "H2642800": {"nome": "INOA 8 60G", "marca": "sac"},
  "H2643800": {"nome": "INOA 8,1 60G", "marca": "sac"},
  "H2642900": {"nome": "INOA 9 60G", "marca": "sac"},
  "E0487122": {"nome": "INOA 9,1 60G", "marca": "sac"},
  "E3743900": {"nome": "Dialight 7,4 - Louro Acobreado 50g", "marca": "sac"},
  "E3730300": {"nome": "Dialight 9,03 - Louro Muito Claro Natural Dourado 50g", "marca": "sac"},
  "H0243523": {"nome": "Majirel 1 - Preto 50g", "marca": "sac"},
  "H0244222": {"nome": "Majirel 3 - Castanho Escuro 50g", "marca": "sac"},
  "H0244322": {"nome": "Majirel 4 - Castanho 50g", "marca": "sac"},
  "H0247522": {"nome": "Majirel 4,0 - Castanho Intenso 50g", "marca": "sac"},
  "H0247622": {"nome": "Majirel 5,0 - Castanho Claro Intenso 50g", "marca": "sac"},
  "H0245022": {"nome": "Majirel 6 - Louro Escuro 50g", "marca": "sac"},
  "H0248022": {"nome": "Majirel 6,0 - Louro Escuro Intenso 50g", "marca": "sac"},
  "H0245222": {"nome": "Majirel 6,1 - Louro Escuro Acinzentado 50g", "marca": "sac"},
  "H0249222": {"nome": "Majirel 6,3 - Louro Escuro Dourado 50g", "marca": "sac"},
  "H0245822": {"nome": "Majirel 7 - Louro 50g", "marca": "sac"},
  "H0247722": {"nome": "Majirel 7,0 - Louro Intenso 50g", "marca": "sac"},
  "H0246022": {"nome": "Majirel 7,1 - Louro Acinzentado 50g", "marca": "sac"},
  "H0246522": {"nome": "Majirel 8 - Louro Claro 50g", "marca": "sac"},
  "H0247822": {"nome": "Majirel 8,0 - Louro Claro Intenso 50g", "marca": "sac"},
  "H0246722": {"nome": "Majirel 8,1 - Louro Claro Acinzentado 50g", "marca": "sac"},
  "H0247122": {"nome": "Majirel 9,1 - Louro Muito Claro 50g", "marca": "sac"},  
  "H0250223": {"nome": "Majirel HT Inc 7,3 - Louro Dourado 50g", "marca": "sac"},
  "H0250322": {"nome": "Majirel HT Inc 7,31 - Louro Bege Dourado 50g", "marca": "sac"},
  "H0250522": {"nome": "Majirel HT Inc 7,4 - Louro Acobreado 50g", "marca": "sac"},
  "H0250822": {"nome": "Majirel HT Inc 8,3 - Louro Claro Dourado 50g", "marca": "sac"},
  "H0251022": {"nome": "Majirel HT Inc 8,34 - Louro Claro Dourado Acobreado 50g", "marca": "sac"},
  "H2641900": {"nome": "LP - INOA 1 60G", "marca": "sac"},
  "E3972200": {"nome": "LP - INOA 10 60G", "marca": "sac"},
  "H2642000": {"nome": "LP - INOA 3 60G", "marca": "sac"},
  "H2642100": {"nome": "LP - INOA 4 60G", "marca": "sac"},
  "H2642200": {"nome": "LP - INOA 5 60G", "marca": "sac"},
  "E3964100": {"nome": "LP - INOA 5,1 60G", "marca": "sac"},
  "E3974700": {"nome": "LP - INOA 5,3 60G", "marca": "sac"},
  "H2642400": {"nome": "LP - INOA 6 60G", "marca": "sac"},
  "H2642500": {"nome": "LP - INOA 6,0 60G", "marca": "sac"},
  "H2643300": {"nome": "LP - INOA 6,1 60G", "marca": "sac"},
  "E3972700": {"nome": "LP - INOA 6,3 60G", "marca": "sac"},
  "H2642600": {"nome": "LP - INOA 7 60G", "marca": "sac"},
  "H2642700": {"nome": "LP - INOA 7,0 60G", "marca": "sac"},
  "H2643600": {"nome": "LP - INOA 7,1 60G", "marca": "sac"},
  "H2643700": {"nome": "LP - INOA 7,31 60G", "marca": "sac"},
  "E3984600": {"nome": "LP - INOA 7,4 60G", "marca": "sac"},
  "H2642800": {"nome": "LP - INOA 8 60G", "marca": "sac"},
  "H2643800": {"nome": "LP - INOA 8,1 60G", "marca": "sac"},
  "H2642900": {"nome": "LP - INOA 9 60G", "marca": "sac"},
  "E0487122": {"nome": "LP - INOA 9,1 60G", "marca": "sac"},
  "7908615012667": {"nome": "L'Oréal Professionnel - Diactivateur 15 Volumes 120ml", "marca": "sac"},
  "G-7908195709889": {"nome": "Girassol Pink By Kern -Top Coat Maldivas - Esmalte 9ml", "marca": "sac"},
  "H2663900": {"nome": "LP - INOA 7.11 60G", "marca": "sac"},
"7790819570995": {"nome": "Girassol Pink By Kern - Kit Proteção MAX para as Unhas - Primer Fortalecedor 9ml + Nivelador 9ml", "marca": "sac"},
"BECHS2747": {"nome": "Gama Italy Pro - Prancha Elegance Led Bivolt", "marca": "sac"},
"LP INOA Ox 20 Vol 6% 1000": {"nome": "LP INOA Ox 20 Vol 6% 1000", "marca": "sac"},
"G-7908195709933": {"nome": "Girassol Pink By Kern -Sérum Noturno - Esmalte 9ml", "marca": "sac"},






  "68600632-sac": {"nome": "Q-Tips - Discos de Algodão para Beleza - Kit 80un", "marca": "exi"},
  "69993370-sac": {"nome": "Q-Tips - Hastes de Algodão - Kit de Viagem 30un", "marca": "exi"},
  "64360311-sac": {"nome": "Q-Tips - Hastes de Algodão Orgânico - Kit de Viagem 30un", "marca": "exi"},
  "64360310-sac": {"nome": "Q-Tips - Hastes de Algodão com Pontas de Precisão - Kit de Viagem 30un", "marca": "exi"}  
    
}

# Inicializa variáveis na sessão
if "contagem" not in st.session_state:
    st.session_state.contagem = {}
if "pedidos_bipados" not in st.session_state:
    st.session_state.pedidos_bipados = []
if "input_codigo" not in st.session_state:
    st.session_state.input_codigo = ""
if "nao_encontrados" not in st.session_state:
    st.session_state.nao_encontrados = []

# ------------ Página de Resultados (corrigido para agrupar produtos corretamente) ------------
params = st.query_params
if "resultado" in params:
    st.title("Resumo do Pedido")
    st.markdown("---")

    # Organiza produtos por marca
    produtos_por_marca = {}
    for codigo, valores in params.items():
        if codigo == "resultado":
            continue
        quantidade = valores[0]
        produto = produtos_cadastrados.get(codigo)
        if produto:
            marca = produto['marca']
            if marca not in produtos_por_marca:
                produtos_por_marca[marca] = []
            produtos_por_marca[marca].append({
                "nome": produto['nome'],
                "quantidade": quantidade
            })

    # Agora exibe por marca agrupado
    for marca, lista_produtos in produtos_por_marca.items():
         

        # Exibe a logo da marca uma vez só
        try:
            logo_path = os.path.join(CAMINHO_LOGOS, f"{marca}.png")
            with open(logo_path, "rb") as img_file:
                logo_encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(
                f"<img src='data:image/png;base64,{logo_encoded}' width='150' style='margin-bottom: 20px;'>",
                unsafe_allow_html=True
            )
        except Exception:
            st.warning(f"⚠️ Logo da marca **{marca}** não encontrada.")

        # Lista todos os produtos da marca
        for produto in lista_produtos:
            st.markdown(f"**{produto['nome']}** | Quantidade: {produto['quantidade']}")

        st.markdown("---")

    st.markdown("[Voltar à página principal](/)", unsafe_allow_html=True)
    st.stop()


# ------------ Página Principal (Interface de Busca) ------------

st.title("Bipagem de Produtos")

uploaded_files = st.file_uploader("Envie os CSVs do pedido exportados do Bling:", type=["csv"], accept_multiple_files=True)

def processar():
    codigos_input = st.session_state.input_codigo.strip()
    if not codigos_input:
        return
    codigos = re.split(r'[\s,]+', codigos_input)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file, sep=";", dtype=str)
            if "SKU" not in df.columns:
                st.error("Não foi encontrada a coluna 'SKU' no CSV. Colunas disponíveis: " + ", ".join(df.columns))
                return
            df["SKU"] = df["SKU"].apply(
                lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip()))) if "E+" in str(x) else str(x).strip()
            )
            for codigo in codigos:
                pedidos = df[df["Número pedido"].astype(str).str.strip() == codigo]
                if not pedidos.empty:
                    for sku in pedidos["SKU"]:
                        for sku_individual in str(sku).split("+"):
                            sku_individual = sku_individual.strip()
                            if sku_individual in produtos_cadastrados:
                                st.session_state.contagem[sku_individual] = st.session_state.contagem.get(sku_individual, 0) + 1
                            else:
                                entrada = f"Pedido {codigo} → SKU: {sku_individual}"
                                if entrada not in st.session_state.nao_encontrados:
                                    st.session_state.nao_encontrados.append(entrada)
                else:
                    if codigo in produtos_cadastrados:
                        st.session_state.contagem[codigo] = st.session_state.contagem.get(codigo, 0) + 1
                    else:
                        entrada = f"Código direto → SKU: {codigo}"
                        if entrada not in st.session_state.nao_encontrados:
                            st.session_state.nao_encontrados.append(entrada)
    else:
        for codigo in codigos:
            if codigo in produtos_cadastrados:
                st.session_state.contagem[codigo] = st.session_state.contagem.get(codigo, 0) + 1
            else:
                entrada = f"Código direto → SKU: {codigo}"
                if entrada not in st.session_state.nao_encontrados:
                    st.session_state.nao_encontrados.append(entrada)
    st.session_state.input_codigo = ""

if st.button("🔄 Limpar pedidos bipados"):
    st.session_state.pedidos_bipados.clear()
    st.session_state.contagem.clear()
    st.session_state.nao_encontrados.clear()

try:
    exi_logo_path = os.path.join(CAMINHO_LOGOS, "exi.png")
    with open(exi_logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded}' width='200'></div>",
        unsafe_allow_html=True,
    )
except Exception:
    st.markdown("<h2 style='text-align: center;'>EXI</h2>", unsafe_allow_html=True)

st.markdown(
    "<p style='font-weight: bold;'>Digite o(s) código(s) do pedido ou SKU direto:<br><small>Exemplo: 12345, 67890 111213</small></p>",
    unsafe_allow_html=True
)
st.text_input("", key="input_codigo", on_change=processar)

if st.session_state.nao_encontrados:
    with st.expander("❗ Códigos não cadastrados no sistema"):
        for entrada in st.session_state.nao_encontrados:
            st.markdown(f"- {entrada}")

marcas_com_produtos = []
for cod in st.session_state.contagem:
    produto = produtos_cadastrados.get(cod)
    if produto and produto["marca"] not in marcas_com_produtos:
        marcas_com_produtos.append(produto["marca"])

marcas_por_linha = 4
linhas = math.ceil(len(marcas_com_produtos) / marcas_por_linha)
for i in range(linhas):
    linha_marcas = marcas_com_produtos[i * marcas_por_linha:(i + 1) * marcas_por_linha]
    cols = st.columns(len(linha_marcas))
    for col, marca in zip(cols, linha_marcas):
        with col:
            try:
                img = Image.open(os.path.join(CAMINHO_LOGOS, f"{marca}.png"))
                st.image(img, width=120)
            except Exception:
                st.write(marca.upper())
            for cod, qtd in st.session_state.contagem.items():
                produto = produtos_cadastrados.get(cod)
                if produto and produto["marca"] == marca:
                    st.markdown(
                        f"<p style='margin-top: 0;'><strong>{produto['nome']}</strong> | Quantidade: {qtd}</p>",
                        unsafe_allow_html=True,
                    )

if st.session_state.contagem:
    base_url = "https://cogpz234emkoeygixmfemn.streamlit.app/"
    params_dict = {"resultado": "1"}
    for sku, qtd in st.session_state.contagem.items():
        params_dict[sku] = str(qtd)
    query_string = urllib.parse.urlencode(params_dict)
    full_url = f"{base_url}/?{query_string}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img_qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="QR Code para a Página de Resultados", use_container_width=False)
    st.markdown(f"[Clique aqui para acessar a página de resultados]({full_url})", unsafe_allow_html=True)
else:
    st.info("Nenhum produto bipado ainda!")

