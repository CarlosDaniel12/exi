import streamlit as st
import pandas as pd
from PIL import Image
import os, base64
from io import BytesIO
import re
import math, qrcode, urllib.parse

# Configura layout
st.set_page_config(layout="wide")

# Ajusta o caminho das logos automaticamente
if os.path.exists("C:/meu_app_streamlit/logos"):
    CAMINHO_LOGOS = "C:/meu_app_streamlit/logos"
else:
    CAMINHO_LOGOS = "meu_app_streamlit/logos"

# Lista reta de produtos
# Lista reta de produtos
lista_produtos = {
     "H0270321": {"nome": "Oxidante Creme 75ml 20 Vol", "marca": "loreal", "codigo_produto": "7896014179541"},
  "E3825500": {"nome": "Curl Expression Gelée Lavante Anti-résidus 300ml", "marca": "loreal", "codigo_produto": "3474637069087"},
  "E3564101": {"nome": "Absolut Repair - Mask 250ml", "marca": "loreal", "codigo_produto": "3474636975310"},
  "E3574500": {"nome": "Absolut Repair - Oil 90ml", "marca": "loreal", "codigo_produto": "3474636977369"},
  "E3795000": {"nome": "Absolut Repair - Óleo 10 em 1 30ml", "marca": "loreal", "codigo_produto": "3474637052263"},
  "H2469500": {"nome": "Absolut Repair Gold - Condicionador 200ml", "marca": "loreal", "codigo_produto": "7899706189644"},
  "H2469700": {"nome": "Absolut Repair Gold - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706189668"},
  "H2469101": {"nome": "Absolut Repair Gold - Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706189606"},
  "E4033400": {"nome": "Absolut Repair Molecular - Leave-in 100ml", "marca": "loreal", "codigo_produto": "3474637153489"},
  "E4173000": {"nome": "Absolut Repair Molecular - Máscara Capilar 250ml", "marca": "loreal", "codigo_produto": "3474637217884"},
  "E4173200": {"nome": "Absolut Repair Molecular - Máscara Capilar 500ml", "marca": "loreal", "codigo_produto": "3474637217907"},
  "E4033800": {"nome": "Absolut Repair Molecular - Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637153526"},
  "E4034100": {"nome": "Absolut Repair Molecular - Shampoo 500ml", "marca": "loreal", "codigo_produto": "3474637153557"},
  "H3689700": {"nome": "Absolut Repair Shampoo Refil 240ml", "marca": "loreal", "codigo_produto": "7908785404958"},
  "E3887500": {"nome": "Aminexil - Ampoules 10x6ml", "marca": "loreal", "codigo_produto": "3474637109523"},
  "H2466300": {"nome": "Blondifier - Condicionador 200ml", "marca": "loreal", "codigo_produto": "7899706189323"},
  "H2466501": {"nome": "Blondifier - Mask Gloss 250ml", "marca": "loreal", "codigo_produto": "7899706189347"},
  "H2465900": {"nome": "Blondifier - Shampoo Gloss 300ml", "marca": "loreal", "codigo_produto": "7899706189279"},
  "H2608400": {"nome": "Curl Expression - Leave-in Condicionador 200ml", "marca": "loreal", "codigo_produto": "7899706203906"},
  "H2608500": {"nome": "Curl Expression - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706203944"},
  "H2607200": {"nome": "Curl Expression - Mask Rich 250ml", "marca": "loreal", "codigo_produto": "7899706203579"},
  "E3826600": {"nome": "Curl Expression - Moisturizing Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637069193"},
  "E3835000": {"nome": "Curl Expression - Reviver Spray 190ml", "marca": "loreal", "codigo_produto": "3474637076498"},
  "7908615012667": {"nome": "Diactivateur 15 Volumes 120ml", "marca": "loreal", "codigo_produto": "000000000"},
  "H2467500": {"nome": "Inforcer - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706189446"},
  "H2466901": {"nome": "Inforcer - Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706189385"},
  "E4033200": {"nome": "Metal Detox - Anti-Metal de Alta Proteção Leave-in 100ml", "marca": "loreal", "codigo_produto": "30161153"},
  "E3548402": {"nome": "Metal Detox - Mask 250ml", "marca": "loreal", "codigo_produto": "30160606"},
  "E3560001": {"nome": "Metal Detox - Mask 500ml", "marca": "loreal", "codigo_produto": "30163478"},
  "E3548702": {"nome": "Metal Detox - Shampoo 300ml", "marca": "loreal", "codigo_produto": "30158078"},
  "E3549301": {"nome": "Metal Detox - Treatment Spray 500ml", "marca": "loreal", "codigo_produto": "0000030164840"},
  "E4123900": {"nome": "Metal Detox - Pre-Shampoo Treatment 250ml", "marca": "loreal", "codigo_produto": "3474637199708"},
  "H2610800": {"nome": "NutriOil - Leave-In 150ml", "marca": "loreal", "codigo_produto": "7899706205177"},
  "H2611001": {"nome": "NutriOil - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706205252"},
  "H2610201": {"nome": "NutriOil - Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706204934"},
  "H2468700": {"nome": "Pro Longer - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706189569"},
  "H2467901": {"nome": "Pro Longer - Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706189484"},
  "E3886000": {"nome": "Scalp Anti-Dandruff - Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637109370"},
  "E3847900": {"nome": "Scalp Anti-Discomfort - Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637090487"},
  "E3848800": {"nome": "Scalp Anti-Discomfort - Treatment 200ml", "marca": "loreal", "codigo_produto": "3474637090579"},
  "E3848300": {"nome": "Scalp Anti-Oily - Mask 250ml", "marca": "loreal", "codigo_produto": "3474637090524"},
  "E3848700": {"nome": "Scalp Anti-Oily - Mask 500ml", "marca": "loreal", "codigo_produto": "3474637090562"},
  "E3872900": {"nome": "Scalp Anti-Oily - Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637106454"},
  "E3872300": {"nome": "Serioxyl Densifying - Shampoo 300ml", "marca": "loreal", "codigo_produto": "3474637106393"},
  "H2470302": {"nome": "Silver Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706189729"},
  "E3554500": {"nome": "Vitamino Color - 10-in-1 190ml", "marca": "loreal", "codigo_produto": "3474636974368"},
  "H2471100": {"nome": "Vitamino Color - Condicionador 200ml", "marca": "loreal", "codigo_produto": "7899706189804"},
  "H2471300": {"nome": "Vitamino Color - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706189828"},
  "H2471302": {"nome": "Vitamino Color - Mask 250ml", "marca": "loreal", "codigo_produto": "7899706189828"},
  "H2470900": {"nome": "Vitamino Color - Shampoo 300ml", "marca": "loreal", "codigo_produto": "7899706189781"},
  "H2689800": {"nome": "Vitamino Color Resveratrol - Shampoo Refil 240ml", "marca": "loreal", "codigo_produto": "7908785404996"},
  "H2471902": {"nome": "Blondifier - Mask COOL 250ml", "marca": "loreal", "codigo_produto": "7899706189880"},
  "E3573901": {"nome": "Pro Longer - Cream 10-IN-1 150ml", "marca": "loreal", "codigo_produto": "3474636977307"},
  "6134464": {"nome": "Advanced Keratin Bond Deep Repair Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046316573"},
  "6134473": {"nome": "Advanced Keratin Bond Purifying Conditioner Treatment 600ml", "marca": "kerasys","codigo_produto": "8801046421901"},
  "6134467": {"nome": "Advanced Keratin Bond Purifying Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046421871"},
  "6134472": {"nome": "Advanced Keratin Bond Silky Moisture Conditioner Treatment 600ml", "marca": "kerasys","codigo_produto": "8801046316696"},
  "6134466": {"nome": "Advanced Keratin Bond Silky Moisture Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046316603"},
  "6134465": {"nome": "Advanced Keratin Bond Volume Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046316634"},
  "6098972": {"nome": "Clabo Fresh Citrus Deep Clean Conditioner 960ml", "marca": "kerasys","codigo_produto": "8801046371169"},
  "6098969": {"nome": "Clabo Fresh Citrus Deep Clean Shampoo 960ml", "marca": "kerasys","codigo_produto": "8801046371138"},
  "6098970": {"nome": "Clabo Romantic Citrus Deep Clean Conditioner 960ml", "marca": "kerasys","codigo_produto": "8801046371152"},
  "6098971": {"nome": "Clabo Romantic Citrus Deep Clean Shampoo 960ml", "marca": "kerasys","codigo_produto": "8801046371121"},
  "6101625": {"nome": "Clabo Tropical Citrus Deep Clean Conditioner 960ml", "marca": "kerasys","codigo_produto": "8801046371145"},
  "6101580": {"nome": "Clabo Tropical Citrus Deep Clean Shampoo 960ml", "marca": "kerasys","codigo_produto": "8801046371114"},
  "6103759": {"nome": "Perfume Shampoo Blooming Flowery 180ml", "marca": "kerasys","codigo_produto": "8801046396896"},
  "6103758": {"nome": "Perfume Shampoo Elegance Sensual 180ml", "marca": "kerasys","codigo_produto": "8801046396926"},
  "6103766": {"nome": "Perfume Shampoo Glam Stylish 180ml", "marca": "kerasys","codigo_produto": "8801046396902"},
  "6103767": {"nome": "Perfume Shampoo Lovely Romantic 180ml", "marca": "kerasys","codigo_produto": "8801046396919"},
  "6103178": {"nome": "Perfume Shampoo Lovely Romantic 400ml", "marca": "kerasys","codigo_produto": "8801046313732"},
  "6103577": {"nome": "Perfume Shampoo Lovely Romantic 600ml", "marca": "kerasys","codigo_produto": "8801046992708"},
  "6103764": {"nome": "Perfume Shampoo Pure Charming 180ml", "marca": "kerasys","codigo_produto": "8801046396933"},
  "6100535": {"nome": "Advanced Color Protect Shampoo 400ml", "marca": "kerasys","codigo_produto": "8801046376591"},
  "6134479": {"nome": "Advanced Keratin Bond Deep Repair Treatment 600ml", "marca": "kerasys","codigo_produto": "8801046316665"},
  "6134471": {"nome": "Keratin Bond Volume Treatment 600ml", "marca": "kerasys","codigo_produto": "8801046316719"},
  "5019654": {"nome": "Salon de Magie Ampola Premium de Tratamento 200ml", "marca": "kerasys","codigo_produto": "8801046411834"},
  "6100543": {"nome": "Advanced Color Protect Conditioner 400ml", "marca": "kerasys","codigo_produto": "8801046376607"},
  "6100682": {"nome": "Advanced Colour Protect Ampoule Shampoo 500ml Refil", "marca": "kerasys","codigo_produto": "8801046378762"},
  "6103799": {"nome": "Advanced Keramide Damage Clinic 1000ml", "marca": "kerasys","codigo_produto": "8801046370704"},
  "6064194": {"nome": "Advanced Keramide Damage Clinic Mask 200ml", "marca": "kerasys","codigo_produto": "8801046276983"},
  "5008451": {"nome": "Advanced Keramide Extreme Damage Clinic Serum 70ml", "marca": "kerasys","codigo_produto": "8801046277041"},
  "6078916": {"nome": "Advanced Keramide Extreme Damage Rich Serum 70ml", "marca": "kerasys","codigo_produto": "8801046336793"},
  "6064195": {"nome": "Advanced Keramide Heat Protection Mask 200ml", "marca": "kerasys","codigo_produto": "8801046276990"},
  "5010755": {"nome": "Advanced Moisture Ampoule 10X Cd Serum 80ml", "marca": "kerasys","codigo_produto": "8801046357835"},
  "6093519": {"nome": "Advanced Moisture Ampoule 10x Hair Pack 300ml", "marca": "kerasys","codigo_produto": "8801046357811"},
  "6100528": {"nome": "Advanced Moisture Ampoule Conditioner 400ml", "marca": "kerasys","codigo_produto": "8801046376669"},
  "6100534": {"nome": "Advanced Moisture Ampoule Shampoo 400ml", "marca": "kerasys","codigo_produto": "8801046376652"},
  "6100679": {"nome": "Advanced Moisture Ampoule Shampoo 500ml Refil", "marca": "kerasys","codigo_produto": "8801046378748"},
  "5019487": {"nome": "Advanced Repair Ampoule 10x Cd Serum 80ml", "marca": "kerasys","codigo_produto": "8801046357828"},
  "6093517": {"nome": "Advanced Repair Ampoule 10x Hair Pack 300ml", "marca": "kerasys","codigo_produto": "8801046357804"},
  "6103800": {"nome": "Advanced Repair Ampoule 10x Keratin Ampoule Cd Hair Pack 1L", "marca": "kerasys","codigo_produto": "8801046387115"},
  "6100531": {"nome": "Advanced Repair Ampoule Shampoo 400ml", "marca": "kerasys","codigo_produto": "8801046376638"},
  "6093511": {"nome": "Advanced Repair Ampoule Water Cd Treatment 220ml", "marca": "kerasys","codigo_produto": "8801046341421"},
  "6100529": {"nome": "Advanced Volume Ampoule Conditioner 400ml", "marca": "kerasys","codigo_produto": "8801046376683"},
  "6103610": {"nome": "Argan Oil Cd Treatment 1000ml", "marca": "kerasys","codigo_produto": "8801046359587"},
  "6082090": {"nome": "Argan Oil Conditioner 1000ml", "marca": "kerasys","codigo_produto": "8801046342992"},
  "5014075": {"nome": "Argan Oil Serum 100ml", "marca": "kerasys","codigo_produto": "8801046354513"},
  "6082084": {"nome": "Argan Oil Shampoo 1000ml", "marca": "kerasys","codigo_produto": "8801046342985"},
  "6098817": {"nome": "Black Bean Oil Shampoo 1L", "marca": "kerasys","codigo_produto": "8801046369760"},
  "6082088": {"nome": "Coconut Oil Conditioner 1000ml", "marca": "kerasys","codigo_produto": "8801046343012"},
  "6082085": {"nome": "Coconut Oil Shampoo 1000ml", "marca": "kerasys","codigo_produto": "8801046343005"},
  "6103715": {"nome": "Damage Clinic Cd Treatment 300ml", "marca": "kerasys","codigo_produto": "8801046285756"},
  "6103539": {"nome": "Deep Cleansing Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046288979"},
  "6066720": {"nome": "Deep Cleansing Shampoo 500ml Refil", "marca": "kerasys","codigo_produto": "8801046902134"},
  "6065902": {"nome": "Deep Cleansing Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046866214"},
  "5010034": {"nome": "Heat Active Damage Repair 200ml", "marca": "kerasys","codigo_produto": "8801046311035"},
  "5010023": {"nome": "Heat Active Style Care Essence 200ml", "marca": "kerasys","codigo_produto": "8801046311042"},
  "5010675": {"nome": "Heat Primer Blanche Iris 220ml", "marca": "kerasys","codigo_produto": "8801046376881"},
  "6112344": {"nome": "Moisture Clinic Cd Treatment 300ml", "marca": "kerasys","codigo_produto": "8801046285763"},
  "6066186": {"nome": "Moisturizing Conditioner 180ml", "marca": "kerasys","codigo_produto": "8801046288931"},
  "6066715": {"nome": "Moisturizing Conditioner 500ml Refill", "marca": "kerasys","codigo_produto": "8801046902066"},
  "6066185": {"nome": "Moisturizing Conditioner 600ml", "marca": "kerasys","codigo_produto": "8801046849682"},
  "6066183": {"nome": "Moisturizing Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046288900"},
  "6066711": {"nome": "Moisturizing Shampoo 500ml Refill", "marca": "kerasys","codigo_produto": "8801046900703"},
  "6066182": {"nome": "Moisturizing Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046848883"},
  "6059482": {"nome": "Oriental Premium Condicionador 200ml", "marca": "kerasys","codigo_produto": "8801046876244"},
  "6059482-W": {"nome": "Oriental Premium Condicionador 200ml", "marca": "kerasys", "codigo_produto": "8801046876244"},
  
  
  "6060085": {"nome": "Oriental Premium Condicionador 500ml Refil", "marca": "kerasys","codigo_produto": "8801046989869"},
  "6130952": {"nome": "Oriental Premium Condicionador 600ml", "marca": "kerasys","codigo_produto": "8801046871003"},
  "6055025": {"nome": "Oriental Premium Condicionador 600ml", "marca": "kerasys","codigo_produto": "8801046871003"},
  "6067179": {"nome": "Oriental Premium Mask Tr Cond 200ml", "marca": "kerasys","codigo_produto": "8801046871348"},
  "6067179-W": {"nome": "Oriental Premium Mask Tr Cond 200ml", "marca": "kerasys","codigo_produto": "8801046871348"},
  "6059481": {"nome": "Oriental Premium Shampoo 200ml", "marca": "kerasys","codigo_produto": "8801046876237"},
  "6059481-W": {"nome": "Oriental Premium Shampoo 200ml", "marca": "kerasys","codigo_produto": "8801046876237"},
  "6060084": {"nome": "Oriental Premium Shampoo 500ml Refil", "marca": "kerasys","codigo_produto": "8801046989845"},
  "6130849": {"nome": "Oriental Premium Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046870990"},
  "6055024": {"nome": "Oriental Premium Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046870990"},
  "6103192": {"nome": "Perfume - Lovely Romantic Conditioner 400ml", "marca": "kerasys","codigo_produto": "8801046313848"},
  "6103584": {"nome": "Perfume - Lovely Romantic Conditioner 600ml", "marca": "kerasys","codigo_produto": "8801046992739"},
  "6075540": {"nome": "Propolis Energy Shine Shampoo 1000ml", "marca": "kerasys","codigo_produto": "8801046277904"},
  "6115358": {"nome": "Propolis Energy Shine Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046413685"},
  "6075545": {"nome": "Propolis Energy Shine Treatment Conditioner 1000ml", "marca": "kerasys","codigo_produto": "8801046269015"},
  "6115360": {"nome": "Propolis Energy Shine Treatment Conditioner 180ml", "marca": "kerasys","codigo_produto": "8801046413692"},
  "6100811": {"nome": "Propolis Royal Green Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046379219"},
  "6100815": {"nome": "Propolis Royal Green Treatment 180ml", "marca": "kerasys","codigo_produto": "8801046379226"},
  "6093951": {"nome": "Propolis Royal Green Treatment 1L", "marca": "kerasys","codigo_produto": "8801046359150"},
  "6100817": {"nome": "Propolis Royal Original Treatment 180ml", "marca": "kerasys","codigo_produto": "8801046379202"},
  "6093949": {"nome": "Propolis Royal Original Treatment 1L", "marca": "kerasys","codigo_produto": "8801046359136"},
  "6093950": {"nome": "Propolis Royal Red Shampoo 1L", "marca": "kerasys","codigo_produto": "8801046359167"},
  "6093948": {"nome": "Propolis Royal Red Treatment 1L", "marca": "kerasys","codigo_produto": "8801046359174"},
  "6066191": {"nome": "Repairing Conditioner 180ml", "marca": "kerasys","codigo_produto": "8801046288948"},
  "6066716": {"nome": "Repairing Conditioner 500ml Refill", "marca": "kerasys","codigo_produto": "8801046902059"},
  "6066192": {"nome": "Repairing Conditioner 600ml", "marca": "kerasys","codigo_produto": "8801046849705"},
  "6066189": {"nome": "Repairing Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046288917"},
  "6066712": {"nome": "Repairing Shampoo 500ml Refill", "marca": "kerasys","codigo_produto": "8801046900727"},
  "6066188": {"nome": "Repairing Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046848906"},
  "6066180": {"nome": "Revitalizing Conditioner 180ml", "marca": "kerasys","codigo_produto": "8801046288955"},
  "6066180-W": {"nome": "Revitalizing Conditioner 180ml", "marca": "kerasys","codigo_produto": "8801046288955"},
  "6103565": {"nome": "Revitalizing Conditioner 500ml Refill", "marca": "kerasys","codigo_produto": "8801046902042"},
  "6066179": {"nome": "Revitalizing Conditioner 600ml", "marca": "kerasys","codigo_produto": "8801046849699"},
  "6066177": {"nome": "Revitalizing Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046288924"},
  "6103564": {"nome": "Revitalizing Shampoo 500ml Refill", "marca": "kerasys","codigo_produto": "8801046900710"},
  "6066176": {"nome": "Revitalizing Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046848890"},
  "5011714": {"nome": "Salon De Magie Treatment Conditioner 200ml", "marca": "kerasys","codigo_produto": "8801046375501"},
  "5014454": {"nome": "Salt Scrub Deep Clean Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046408681"},
  "6110516": {"nome": "Salt Scrub Scalp Hair Treatment Conditioner 600ml", "marca": "kerasys","codigo_produto": "8801046408704"},
  "6103541": {"nome": "Scalp Balancing Shampoo 180ml", "marca": "kerasys","codigo_produto": "8801046288962"},
  "6103537": {"nome": "Scalp Balancing Shampoo 500ml Refill", "marca": "kerasys","codigo_produto": "8801046902127"},
  "6065904": {"nome": "Scalp Balancing Shampoo 600ml", "marca": "kerasys","codigo_produto": "8801046862285"},
  "5013806": {"nome": "Scalp Spa Agua Blue Serum 70ml", "marca": "kerasys","codigo_produto": "8801046403969"},
  "6097701": {"nome": "Tea Tree Oil Conditioner 1L", "marca": "kerasys","codigo_produto": "8801046364222"},
  "6092834": {"nome": "Tea Tree Oil Shampoo 1L", "marca": "kerasys","codigo_produto": "8801046353523"},
  "6141964": {"nome": "Propolis Hair Bonding Pro Repair Cd Treatment 250ml", "marca": "kerasys","codigo_produto": "8801046426982"},
  "5022484": {"nome": "Propolis Hair Bonding No Wash Repair Treatment 200ml", "marca": "kerasys","codigo_produto": "8801046429235"},
  "6146885": {"nome": "Propolis Hair Bonding Shamp 450ml", "marca": "kerasys","codigo_produto": "8801046437087"},
  "6112581": {"nome": " Keramide Ampoule Damage Clinic - Shampoo 1L", "marca": "kerasys","codigo_produto": "8801046411513"},
  "6100527": {"nome": "Kerasys Advanced Repair Ampoule Conditioner 400ml", "marca": "kerasys",  "codigo_produto": "8801046376645"},
  
  "E4181100": {"nome": "Blond Absolu - L'Huile Cicagloss - Óleo Capilar 75ml (Refil)", "marca": "kerastase","codigo_produto": "3474637219505"},
  "H2439101": {"nome": "Blond Absolu - Bain Lumière Shamp 250ml", "marca": "kerastase","codigo_produto": "7899706186285"},
  "E2920901": {"nome": "Blond Absolu - Bain Ultra-Violet 250ml", "marca": "kerastase","codigo_produto": "3474636692231"},
  "E2922000": {"nome": "Blond Absolu - Fondant Cicaflash 250ml", "marca": "kerastase","codigo_produto": "3474636692361"},
  "E3510000": {"nome": "Blond Absolu - Huile Cicaextreme 100ml", "marca": "kerastase","codigo_produto": "3474636948888"},
  "E3509100": {"nome": "Blond Absolu - Masque Cicaextreme 200ml", "marca": "kerastase","codigo_produto": "3474636948529"},
  "E2922401": {"nome": "Blond Absolu - Masque Ultra-Violet 200ml", "marca": "kerastase","codigo_produto": "3474636692408"},
  "E3430101": {"nome": "Blond Absolu - Sérum Cicanuit 90ml", "marca": "kerastase","codigo_produto": "3474636909292"},
  "E2922601": {"nome": "Blond Absolu - Sérum Cicaplasme 150ml", "marca": "kerastase","codigo_produto": "3474636692422"},
  "E4070200": {"nome": "Blond Absolu - Sérum Pure Hyaluronic Acid 2% 50ml", "marca": "kerastase","codigo_produto": "3474637175306"},
  "E3806200": {"nome": "Chroma Absolu - Bain Chroma Respect 250ml", "marca": "kerastase","codigo_produto": "3474637059019"},
  "E3806100": {"nome": "Chroma Absolu - Bain Riche Chroma Respect 250ml", "marca": "kerastase","codigo_produto": "3474637059002"},
  "E3806600": {"nome": "Chroma Absolu - Chroma Thermique 150ml", "marca": "kerastase","codigo_produto": "3474637059057"},
  "E3807900": {"nome": "Chroma Absolu - Fondant Cica Chroma 200ml", "marca": "kerastase","codigo_produto": "3474637059187"},
  "E3807400": {"nome": "Chroma Absolu - Masque Chroma Filler 200ml", "marca": "kerastase","codigo_produto": "3474637059132"},
  "E3807100": {"nome": "Chroma Absolu - Soin Acide Chroma Gloss 210ml", "marca": "kerastase","codigo_produto": "3474637059101"},
  "E4181700": {"nome": "Chroma Absolu - REFILL L'Huile Chroma Éclat Radiance - Oil REFILL 75ml", "marca": "kerastase","codigo_produto": "3474637219567"},
  "E4182600": {"nome": "Chroma Absolu - Chroma Absolu - L'Huile Chroma Éclat Radiance REFILLABLE - Oil 75ml", "marca": "kerastase","codigo_produto": "3474637219659"},
  "H2491101": {"nome": "Chronologiste - Bain Régénérant 250ml", "marca": "kerastase","codigo_produto": "7899706191975"},
  "H2491301": {"nome": "Chronologiste - Masque Intense Régénérant 200ml", "marca": "kerastase","codigo_produto": "7899706191999"},
  "E3291901": {"nome": "Chronologiste - Thermique Régénérant 150ml", "marca": "kerastase","codigo_produto": "3474636874033"},
  "E3550700": {"nome": "Curl Manifesto - Bain Hydratation Douceur Shampoo 250ml", "marca": "kerastase","codigo_produto": "3474636968688"},
  "E3551300": {"nome": "Curl Manifesto - Crème de Jour Fondamentale 150ml", "marca": "kerastase","codigo_produto": "3474636968749"},
  "E3551700": {"nome": "Curl Manifesto - Fondant Hydratation Essentielle 250ml", "marca": "kerastase","codigo_produto": "3474636968787"},
  "E3551100": {"nome": "Curl Manifesto - Gelée Curl Contour 150ml", "marca": "kerastase","codigo_produto": "3474636968725"},
  "E3553500": {"nome": "Curl Manifesto - Lotion Refresh Absolu 190ml", "marca": "kerastase","codigo_produto": "3474636970155"},
  "E2646102": {"nome": "Densifique - Bain Densité 250ml", "marca": "kerastase","codigo_produto": "3474636403912"},
  "E1957502": {"nome": "Densifique - Fondant Densité 200ml", "marca": "kerastase","codigo_produto": "3474636404391"},
  "H1800323": {"nome": "Densifique - Masque Densité 200ml", "marca": "kerastase","codigo_produto": "7899706139335"},
  "E1936101": {"nome": "Discipline - Bain Fluidealiste 250ml", "marca": "kerastase","codigo_produto": "3474636400188"},
  "H1800722": {"nome": "Discipline - Maskeratine 200ml", "marca": "kerastase","codigo_produto": "7899706139373"},
  "E2727900": {"nome": "Elixir Ultime - Huile Rose 100ml", "marca": "kerastase","codigo_produto": "3474636624768"},
  "E4166800": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 75ml", "marca": "kerastase","codigo_produto": "3474637215132"},
  "E4167200": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 30ml", "marca": "kerastase","codigo_produto": "3474637215170"},
  "E4167100": {"nome": "Elixir Ultime - L'Huile Originale Camélia Sauvage 75ml Refil", "marca": "kerastase","codigo_produto": "3474637215163"},
  "E2691701": {"nome": "Elixir Ultime - Le Bain 250ml", "marca": "kerastase","codigo_produto": "3474636614103"},
  "E2795701": {"nome": "Elixir Ultime - Le Fondant 200ml", "marca": "kerastase","codigo_produto": "3474636614028"},
  "E2692500": {"nome": "Elixir Ultime - Le Masque 200ml", "marca": "kerastase","codigo_produto": "3474636614172"},
  "H2517300": {"nome": "Genesis - Bain Nutri-Fortifiant 250ml", "marca": "kerastase","codigo_produto": "7899706194747"},
  "E3245101": {"nome": "Genesis - Cure Anti-Chute Fortifiant 90ml", "marca": "kerastase","codigo_produto": "3474636858002"},
  "E3244800": {"nome": "Genesis - Fluide Défense Thermique 150ml", "marca": "kerastase","codigo_produto": "3474636857975"},
  "E3244001": {"nome": "Genesis - Fondant Renforçateur 200ml", "marca": "kerastase","codigo_produto": "3474636857883"},
  "H2517100": {"nome": "Genesis - Masque Reconstituant 200ml", "marca": "kerastase","codigo_produto": "7899706194839"},
  "E3837700": {"nome": "Genesis Homme - Bain de Force 250ml", "marca": "kerastase","codigo_produto": "3474637077525"},
  "E3837600": {"nome": "Genesis Homme - Bain de Masse 250ml", "marca": "kerastase","codigo_produto": "3474637077518"},
  "E3838400": {"nome": "Genesis Homme - Cire 75ml", "marca": "kerastase","codigo_produto": "3474637077594"},
  "E3837400": {"nome": "Genesis Homme - Sérum Anti-Chute Fortifiant 90ml", "marca": "kerastase","codigo_produto": "3474637077495"},
  "H2516700": {"nome": "Kérastase - Genesis - Bain Hydra-Fortifiant 250ml", "marca": "kerastase","codigo_produto": "7899706194662"},
  "E4040400": {"nome": "Nutritive - 8h Magic Night Serum 90ml", "marca": "kerastase","codigo_produto": "3474637155025"},
  "E4039300": {"nome": "Nutritive - Bain Satin 250ml", "marca": "kerastase","codigo_produto": "7908615015392"},
  "E4039600": {"nome": "Nutritive - Bain Satin Riche 250ml", "marca": "kerastase","codigo_produto": "7908615015378"},
  "E4040000": {"nome": "Nutritive - Fondant Vital 200ml", "marca": "kerastase","codigo_produto": "3474637154981"},
  "E4040600": {"nome": "Nutritive - Lotion Thermique Sublimatrice 150ml", "marca": "kerastase","codigo_produto": "3474637155049"},
  "E4039800": {"nome": "Nutritive - Masque Intense 200ml", "marca": "kerastase","codigo_produto": "7908615015293"},
  "E4040200": {"nome": "Nutritive - Masque Riche 200ml", "marca": "kerastase","codigo_produto": "7908615015279"},
  "E4040801": {"nome": "Nutritive - Nectar Thermique 150ml", "marca": "kerastase","codigo_produto": "3474637155063"},
  "E4042200": {"nome": "Nutritive - Scalp Serum 90ml", "marca": "kerastase","codigo_produto": "3474637155209"},
  "E4040500": {"nome": "Nutritive - Supplement Split Ends Sérum 50ml", "marca": "kerastase","codigo_produto": "3474637155032"},
  "E4039700": {"nome": "Nutritive - Bain Satin Riche - Shampoo - 500ml", "marca": "kerastase","codigo_produto": "3474637154950"},
  "E3073001": {"nome": "Oléo-Relax - Bain 250ml", "marca": "kerastase","codigo_produto": "3474636803637"},
  "E3063900": {"nome": "Oléo-Relax - Masque 200ml", "marca": "kerastase","codigo_produto": "3474636800438"},
  "E4109800": {"nome": "Première - Bain Décalcifiant Réparateur 250ml", "marca": "kerastase","codigo_produto": "3474637195809"},
  "E4113900": {"nome": "Première - Concentré Décalcifiant Ultra-Réparateur - Tratamento Pré-Shampoo 250ml", "marca": "kerastase","codigo_produto": "3474637196684"},
  "E4114400": {"nome": "Première - Concentré Décalcifiant Ultra-Réparateur - Tratamento Pré-Shampoo 45ml", "marca": "kerastase","codigo_produto": "3474637196738"},
  "E4114100": {"nome": "Première - Fondant Fluidité Réparateur 200ml", "marca": "kerastase","codigo_produto": "3474637196707"},
  "E4115200": {"nome": "Première - Huile Gloss Réparatrice (Óleo) 30ml", "marca": "kerastase","codigo_produto": "3474637196813"},
  "E4113500": {"nome": "Première - Masque Filler Réparateur 200ml", "marca": "kerastase","codigo_produto": "3474637196646"},
  "E4113800": {"nome": "Première - Sérum Filler Fondamental 90ml", "marca": "kerastase","codigo_produto": "3474637196677"},
  "E2678500": {"nome": "Résistance - Bain Extentioniste 250ml", "marca": "kerastase","codigo_produto": "3474636612666"},
  "E1928102": {"nome": "Résistance - Bain Force Architecte 250ml", "marca": "kerastase","codigo_produto": "3474636397945"},
  "E1928301": {"nome": "Résistance - Bain Thérapiste 250ml", "marca": "kerastase","codigo_produto": "3474636397969"},
  "E1036204": {"nome": "Résistance - Ciment Thermique 150ml", "marca": "kerastase","codigo_produto": "3474630652439"},
  "E3134502": {"nome": "Résistance - Extentioniste Thermique 150ml", "marca": "kerastase","codigo_produto": "3474636818259"},
  "E2680901": {"nome": "Résistance - Fondant Extentioniste 200ml", "marca": "kerastase","codigo_produto": "3474636612918"},
  "E2683400": {"nome": "Résistance - Masque Extentioniste 200ml", "marca": "kerastase","codigo_produto": "3474636613168"},
  "H1804921": {"nome": "Résistance - Masque Force Architecte 200ml", "marca": "kerastase","codigo_produto": "7899706139793"},
  "H1805123": {"nome": "Résistance - Masque Thérapiste 200ml", "marca": "kerastase","codigo_produto": "7899706139816"},
  "E2755201": {"nome": "Résistance - Sérum Extentioniste Scalp 50ml", "marca": "kerastase","codigo_produto": "3474636636341"},
  "E1490202": {"nome": "Résistance - Sérum Thérapiste 2x15ml", "marca": "kerastase","codigo_produto": "3474630713383"},
  "E3520500": {"nome": "Spécifique - Bain Divalent 250ml", "marca": "kerastase","codigo_produto": "3474636954766"},
  "H1805321": {"nome": "Spécifique - Bain Prévention 250ml", "marca": "kerastase","codigo_produto": "7899706139830"},
  "E1924220": {"nome": "Spécifique - Masque Hydra Apaisant 200ml", "marca": "kerastase","codigo_produto": "3474636397495"},
  "E3520300": {"nome": "Spécifique - Masque Réhydratant 200ml", "marca": "kerastase","codigo_produto": "3474636954742"},
  "E3519900": {"nome": "Spécifique - Sérum Potentialiste 90ml", "marca": "kerastase","codigo_produto": "3474636954704"},
  "E3996700": {"nome": "Symbiose - Bain Crème Anti-Pelliculaire 250ml", "marca": "kerastase","codigo_produto": "3474637135690"},
  "E4000000": {"nome": "Symbiose - Fondant Apaisant Essentiel 200ml", "marca": "kerastase","codigo_produto": "3474637136383"},
  "H2516710": {"nome": "Genesis Bain Hydra-Fortifiant - Shampoo Refil 500ml", "marca": "kerastase","codigo_produto": "000000000"},
  "E4181400": {"nome": "Blond Absolu L'Huile Cicagloss - Óleo Capilar 75ml", "marca": "kerastase", "codigo_produto": "3474637219536"},
    
  "493.046-G": {"nome": "All In One Leave-In Multifuncional - Spray de Gatilho 240ml", "marca": "image","codigo_produto": "0860005042456"},
  "493.046-P": {"nome": "All In One Leave-In Multifuncional - Spray de Pump 240ml", "marca": "image","codigo_produto": "0860005042456"},
  "493.021": {"nome": "Cherimoya Clenz Shampoo 1L", "marca": "image","codigo_produto": "036954338159"},
  "493.049": {"nome": "Cherimoya Clenz Shampoo 240ml", "marca": "image","codigo_produto": "860010127803"},
  "493.034": {"nome": "Colors Serum - Finalizador 30ml", "marca": "i mage","codigo_produto": "0860010127896"},
  "493.040": {"nome": "Covalence Extra - Condicionador 240ml", "marca": "image","codigo_produto": "0860010127810"},
  "493.006": {"nome": "Covalence Extra - Condicionador 1L", "marca": "image","codigo_produto": "0369543355634"},
  "493.044": {"nome": "Heat Defense - Finalizador 240ml", "marca": "image","codigo_produto": "0860005042463"},
  "493.000": {"nome": "Intrakera - Finalizador 240ml", "marca": "image","codigo_produto": "0860005042487"},
  "493.037": {"nome": "Light Serum - Finalizador 30ml", "marca": "image","codigo_produto": "860005042449"},
  "Big Pink Image": {"nome": "MakeUp - Esponja de Maquiagem - Big Pink", "marca": "image","codigo_produto": "6940197902111"},
  "Mini Pink Image": {"nome": "MakeUp Mini Esponja Chanfrada para os Olhos 3D", "marca": "image","codigo_produto": "6940197902111"},
  "Big Pink Image BIG - Saik": {"nome": "Image MakeUp - Esponja de Maquiagem - Pink (BIG)", "marca": "image","codigo_produto": "6940197902111"},
  "493.048": {"nome": "Milk - Condicionador 240ml", "marca": "image","codigo_produto": "0860010127889"},
  "493.001": {"nome": "Milk - Mask 200g", "marca": "image","codigo_produto": "0369541066006"},
  "493.041": {"nome": "Milk Clenz Shampoo Condicionante 240ml", "marca": "image","codigo_produto": "0860005042470"},
  "493.047": {"nome": "Reconstructor Water - Finalizador 240ml", "marca": "image","codigo_produto": "0860010127872"},
  "493.042": {"nome": "Yucca Blossom Energizing Body & Shine - Condicionador 240ml", "marca": "image","codigo_produto": "0860010127834"},
  "493.015": {"nome": "Yucca Blossom Energizing Body & Shine - Condicionador 1L", "marca": "image","codigo_produto": "036954332515"},
  "493.045": {"nome": "FINISHING MIST JUMPING CURLS 240mL", "marca": "image","codigo_produto": "0860005042494"},
  
  "39852E_5": {"nome": "Keep My Blonde Mask CD 750ml", "marca": "ice","codigo_produto": "4743318139852"},
  "51038E_5": {"nome": "Tame My Hair Cream 100ml", "marca": "ice","codigo_produto": "4743318151038"},
  "50895E_5": {"nome": "Refill My Hair Power Booster 30ml", "marca": "ice","codigo_produto": "4743318150895"},
  "39913E_5": {"nome": "Keep My Color CD Mask 750ml", "marca": "ice","codigo_produto": "4743318139913"},
  "39906E_5": {"nome": "Keep My Color Shampoo 1L", "marca": "ice","codigo_produto": "4743318139906"},
  "50239E_5": {"nome": "Keep My Blonde Conditioner Anti-yellow 250ml", "marca": "ice","codigo_produto": "4743318150239"},
  "51151E_5": {"nome": "Keep My Blonde Mask Anti-Yellow 200ml", "marca": "ice","codigo_produto": "4743318151151"},
  "50222E_5": {"nome": "Keep My Blonde Shampoo Anti-yellow 250ml", "marca": "ice","codigo_produto": "4743318150222"},
  "50253E_5": {"nome": "Keep My Color Conditioner 250ml", "marca": "ice","codigo_produto": "4743318150253"},
  "50956E_5": {"nome": "Keep My Color Mask 200ml", "marca": "ice","codigo_produto": "4743318150956"},
  "50963E_5": {"nome": "Keep My Color Serum 50ml", "marca": "ice","codigo_produto": "4743318150963"},
  "50246E_5": {"nome": "Keep My Color Shampoo 250ml", "marca": "ice","codigo_produto": "4743318150246"},
  "39883E_5": {"nome": "Refill My Hair Cd Mask 750ml", "marca": "ice","codigo_produto": "4743318139883"},
  "50192E_5": {"nome": "Refill My Hair Conditioner 250ml", "marca": "ice","codigo_produto": "4743318150192"},
  "50840E_5": {"nome": "Refill My Hair Mask 200ml", "marca": "ice","codigo_produto": "4743318150840"},
  "03853BR": {"nome": "Refill My Hair Mask 50ml", "marca": "ice","codigo_produto": "4743318103853"},
  "39876E_5": {"nome": "Refill My Hair Shampoo 1000ml", "marca": "ice","codigo_produto": "4743318139876"},
  "50185E_5": {"nome": "Refill My Hair Shampoo 250ml", "marca": "ice","codigo_produto": "4743318150185"},
  "50857E_5": {"nome": "Refill My Hair Spray 100ml", "marca": "ice","codigo_produto": "4743318150857"},
  "50215E_5": {"nome": "Refresh My Scalp Conditioner 250ml", "marca": "ice","codigo_produto": "4743318150215"},
  "39890E_5": {"nome": "Refresh My Scalp Shampoo 1000ml", "marca": "ice","codigo_produto": "4743318139890"},
  "50208E_5": {"nome": "Refresh My Scalp Shampoo 250ml", "marca": "ice","codigo_produto": "4743318150208"},
  "51076E_5": {"nome": "Repair My Hair Cd Mask 200ml", "marca": "ice","codigo_produto": "4743318151076"},
  "50291E_5": {"nome": "Repair My Hair Conditioner 250ml", "marca": "ice","codigo_produto": "4743318150291"},
  "03839BR": {"nome": "Repair My Hair Mask 50ml", "marca": "ice","codigo_produto": "4743318103839"},
  "39951E_5": {"nome": "Repair My Hair Mask 750ml", "marca": "ice","codigo_produto": "4743318139951"},
  "51083E_5": {"nome": "Repair My Hair Oil 50ml", "marca": "ice","codigo_produto": "4743318151083"},
  "39944E_5": {"nome": "Repair My Hair Shampoo 1000ml", "marca": "ice","codigo_produto": "4743318139944"},
  "50284E_5": {"nome": "Repair My Hair Shampoo 250ml", "marca": "ice","codigo_produto": "4743318150284"},
  "51090E_5": {"nome": "Repair My Hair Spray 100ml", "marca": "ice","codigo_produto": "4743318151090"},
  "50277E_5": {"nome": "Tame My Hair Conditioner 250ml", "marca": "ice","codigo_produto": "4743318150277"},
  "51007E_5": {"nome": "Tame My Hair Mask 200ml", "marca": "ice","codigo_produto": "4743318151007"},
  "03846BR": {"nome": "Tame My Hair Mask 50ml", "marca": "ice","codigo_produto": "4743318103846"},
  "39937E_5": {"nome": "Tame My Hair Mask 750ml", "marca": "ice","codigo_produto": "4743318139937"},
  "51045E_5": {"nome": "Tame My Hair Oil 50ml", "marca": "ice","codigo_produto": "4743318151045"},
  "51052E_5": {"nome": "Tame My Hair Pre-Shampoo Oil 100ml", "marca": "ice","codigo_produto": "4743318151052"},
  "39920E_5": {"nome": "Tame My Hair Shampoo 1000ml", "marca": "ice","codigo_produto": "4743318139920"},
  "50260E_5": {"nome": "Tame My Hair Shampoo 250ml", "marca": "ice","codigo_produto": "4743318150260"},
  "51014E_5": {"nome": "Tame My Hair Spray 100ml", "marca": "ice","codigo_produto": "4743318151014"},

    "KIWIMASC1": {"nome": "Máscara Hidratante 250ml", "marca": "carol","codigo_produto": "7908666400079"},
  "PA321": {"nome": "Anti-Porosidade - Finalizador Bifásico 150ml", "marca": "carol","codigo_produto": "7898652332500"},
  "PA320": {"nome": "Anti-Porosidade - Gel Reconstrutor 150ml", "marca": "carol","codigo_produto": "7898652332494"},
  "PA322": {"nome": "Anti-Porosidade - Máscara 250g", "marca": "carol","codigo_produto": "7898652332517"},
  "PA319": {"nome": "Anti-Porosidade - Shampoo 290ml", "marca": "carol","codigo_produto": "7898652332487"},
  "PA352": {"nome": "Cresce Resist - Leave-In Finalizador Fortalecimento Capilar 150ml", "marca": "carol", "codigo_produto": "7898652332555"},
  "PA350": {"nome": "Cresce Resist - Máscara Fortalecimento Capilar 250ml", "marca": "carol","codigo_produto": "7898652332579"},
  "PA349": {"nome": "Cresce Resist - Shampoo Hidratante 290ml", "marca": "carol","codigo_produto": "7898652332548"},
  "PA351": {"nome": "Cresce Resist - Tônico Fortalecimento Capilar 150ml", "marca": "carol","codigo_produto": "7898652332562"},
  "PA353": {"nome": "Cresce Resist - Óleo Fortalecimento Capilar 40ml", "marca": "carol","codigo_produto": "7898652332586"},
  "PA323": {"nome": "Detox - Shampoo Esfoliante 290ml", "marca": "carol","codigo_produto": "7898652332524"},
  "PA443": {"nome": "Hydra Matrix - Máscara 250ml", "marca": "carol","codigo_produto": "7898652332807"},
  "PA441": {"nome": "Hydra Matrix - Shampoo Hidratante 290ml", "marca": "carol","codigo_produto": "7898652332784"},
  "PA442": {"nome": "Hydra Matrix - Spray Capilar 10-in-1 150ml", "marca": "carol","codigo_produto": "7898652332791"},
  "PA526": {"nome": "Vitra Protect - Sérum Anti-Umidade 60ml", "marca": "carol","codigo_produto": "7898652333637"},
  "PA523": {"nome": "Vitra Protect - Shampoo Disciplinante 290ml", "marca": "carol","codigo_produto": "7898652333606"},
  "PA525": {"nome": "Vitra Protect - Spray Anti-Umidade 150ml", "marca": "carol","codigo_produto": "7898652333620"},
  "PA527": {"nome": "Óleo e Tratamento Diurno e Noturno 60ml (Exclusivo)", "marca": "carol","codigo_produto": "7898652333644"},
  "PA550": {"nome": "Left Cosméticos - Café + Cacau - Loção Hidratante 150g", "marca": "carol","codigo_produto": "7898652333934"},
"CK - NÉCESSAIRE": {"nome": "CK - NÉCESSAIRE", "marca": "carol","codigo_produto": "000000000"}

}

produtos_cadastrados = {codigo: produto for codigo, produto in lista_produtos.items()}
# Continua o seu código daqui em diante normalmente...

# Inicializa variáveis na sessão
if "contagem" not in st.session_state:
    st.session_state.contagem = {}
if "pedidos_bipados" not in st.session_state:
    st.session_state.pedidos_bipados = []
if "input_codigo" not in st.session_state:
    st.session_state.input_codigo = ""
if "nao_encontrados" not in st.session_state:
    st.session_state.nao_encontrados = []
# ------------ Página de Resultados (corrigido para agrupar produtos corretamente e mostrar código_produto) ------------
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
                "quantidade": quantidade,
                "codigo_produto": produto.get('codigo_produto', '')
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
            codigo_produto = produto.get('codigo_produto', '')
            if codigo_produto:
                st.markdown(f"**{produto['nome']}** | Quantidade: {produto['quantidade']} ({codigo_produto})")
            else:
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

    # Separando os códigos usando espaços e vírgulas
    codigos = re.split(r'[\s,]+', codigos_input)

    # Verificando se arquivos foram carregados
    uploaded_files = st.session_state.get('uploaded_files', [])
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = tentar_ler_csv(uploaded_file)
            if df is None:
                return  # Se falhar ao carregar o CSV, interrompe a execução

            # Verificando a presença da coluna 'SKU'
            if "SKU" not in df.columns:
                st.error(f"Não foi encontrada a coluna 'SKU' no CSV. Colunas disponíveis: " + ", ".join(df.columns))
                return

            # Processando a coluna 'SKU'
            df["SKU"] = df["SKU"].apply(
                lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip())) 
                if "E+" in str(x) else str(x).strip())
            )

            # Processando os códigos dos pedidos
            for codigo in codigos:
                pedidos = df[df["Número pedido"].astype(str).str.strip() == codigo]
                if not pedidos.empty:
                    for sku in pedidos["SKU"]:
                        for sku_individual in str(sku).split("+"):
                            sku_individual = sku_individual.strip()
                            # Verificando se o SKU foi cadastrado
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
        # Se nenhum arquivo CSV foi carregado, apenas processa os códigos diretamente
        for codigo in codigos:
            if codigo in produtos_cadastrados:
                st.session_state.contagem[codigo] = st.session_state.contagem.get(codigo, 0) + 1
            else:
                entrada = f"Código direto → SKU: {codigo}"
                if entrada not in st.session_state.nao_encontrados:
                    st.session_state.nao_encontrados.append(entrada)

    # Limpa o campo de entrada de código
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

