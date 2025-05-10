import streamlit as st
import pandas as pd
from PIL import Image
import os, base64
from io import BytesIO
import re
import math
import qrcode
import urllib.parse
import uuid

# Configura layout
st.set_page_config(layout="wide")

# Define o caminho das logos
CAMINHO_LOGOS = "C:/meu_app_streamlit/logos" if os.path.exists("C:/meu_app_streamlit/logos") else "meu_app_streamlit/logos"

# INSIRA SUA BASE DE PRODUTOS AQUI
lista_produtos = {
  "10170578202": {"nome": "White Clay 120g", "marca": "senka", "codigo_produto": "4550516474636"},
  "LP INOA Ox 20 Vol 6% 1000": {"nome": "LP INOA Ox 20 Vol 6% 1000", "marca": "sac"},
 "10170584202": {"nome": " Whip Speedy 150ml", "marca": "senka", "codigo_produto": "4550516705846"},
 "10170766201": {"nome": " Low PH Calming Cica 100g", "marca": "senka", "codigo_produto": "4550516707666"}, 
 "10170588202": {"nome": " Whip Fresh 100", "marca": "senka", "codigo_produto": "4550516705884"}, 
 "10170583202": {"nome": " Whip Collagen In 50g", "marca": "senka", "codigo_produto": "4550516705839"}, 
 "10170581202": {"nome": " Whip Collagen 120g", "marca": "senka", "codigo_produto": "4550516474582"},
 "10170577202": {"nome": " Whip A 50G", "marca": "senka", "codigo_produto": "4550516705778"}, 
 "10170573202": {"nome": " Whip 120g", "marca": "senka", "codigo_produto": "4550516474568"},
 "5D267": {"nome": " Foamy Foam Maker 100ml", "marca": "senka", "codigo_produto": "2114284531193"},

  
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


  "PA552": {"nome": "Café + Cacau - Esfoliante Corporal 300ml", "marca": "carol","codigo_produto": "7898652333958"},
  "PA549": {"nome": "Café + Cacau - Sabonete Líquido Hidratante 150ml", "marca": "carol","codigo_produto": "7898652333927"},
  "PA551": {"nome": "Café + Cacau - Body Splash 150ml", "marca": "carol","codigo_produto": "7898652333941"},
  "PA550": {"nome": "Café + Cacau - Loção Hidratante Corporal 150ml", "marca": "carol","codigo_produto": "7898652333934"},
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
"CK - NÉCESSAIRE": {"nome": "CK - NÉCESSAIRE", "marca": "carol","codigo_produto": "000000000"},
  "140804": {"nome": "Artistic Edit Base Player - Protein Spray 250ml", "marca": "bedhead","codigo_produto": "615908432985"},
  "140796": {"nome": "Artistic Edit Juxta-Pose Dry Serum 50ml", "marca":"bedhead","codigo_produto": "615908432909"},
  "140794": {"nome": "Artistic Edit Shine Heist LightWeight Conditioning Cream 100ml", "marca": "bedhead","codigo_produto": "615908432886"},
  "140795": {"nome": "Artistic Edit Wave Rider - Versatile Style Cream 100ml", "marca": "bedhead","codigo_produto": "615908432893"},
  "140737": {"nome": "CD BACK IT UP CREAM 125ML", "marca": "bedhead","codigo_produto": "615908431612"},
  "330506": {"nome": "CD CO COLOUR GODDESS 100ML", "marca": "bedhead","codigo_produto": "615908432428"},
  "330508": {"nome": "CD CO COLOUR GODDESS 400ML", "marca": "bedhead","codigo_produto": "615908432442"},
  "330564": {"nome": "CD CO COLOUR GODDESS 750ML", "marca": "bedhead","codigo_produto": "615908433579"},
  "330496": {"nome": "CD CO GIMME GRIP 400ML", "marca": "bedhead","codigo_produto": "615908431551"},
  "330516": {"nome": "RECOVERY COND 100ML", "marca": "bedhead","codigo_produto": "615908433364"},
  "330518": {"nome": "RECOVERY COND 400ML", "marca": "bedhead","codigo_produto": "615908432053"},
  "330562": {"nome": "RECOVERY COND 750ML", "marca": "bedhead","codigo_produto": "615908433531"},
  "330520": {"nome": "RECOVERY COND 970ML", "marca": "bedhead","codigo_produto": "615908433401"},
  "330522": {"nome": "Resurrection COND 100ML", "marca": "bedhead","codigo_produto": "615908433388"},
  "330524": {"nome": "Resurrection COND 400ML", "marca": "bedhead","codigo_produto": "615908432077"},
  "330563": {"nome": "Resurrection COND 750ML", "marca": "bedhead","codigo_produto": "615908433555"},
  "330526": {"nome": "Resurrection COND 970ML", "marca": "bedhead","codigo_produto": "615908432091"},
  "330499": {"nome": "Serial Blonde COND 400ML", "marca": "bedhead","codigo_produto": "615908432299"},
  "330565": {"nome": "Serial Blonde COND 750ML", "marca": "bedhead","codigo_produto": "615908433593"},
  "330501": {"nome": "Serial Blonde COND 970ML", "marca": "bedhead","codigo_produto": "615908432312"},
  "140817": {"nome": "CD CURLS ROCK AMPLIFIER 113ML", "marca": "bedhead","codigo_produto": "615908433197"},
  "140778": {"nome": "CD CURLS ROCK AMPLIFIER 43ML", "marca": "bedhead","codigo_produto": "615908432169"},
  "330532": {"nome": "CD DOWN N DIRTY 400ML", "marca": "bedhead","codigo_produto": "615908432619"},
  "330338": {"nome": "CD FOR MEN CLEAN UP 200ML", "marca": "bedhead","codigo_produto": "615908424676"},
  "330513": {"nome": "CD MAKE IT LAST LEAVE-IN 200ML", "marca": "bedhead","codigo_produto": "615908432480"},
  "140736": {"nome": "CD MANIPULATOR MATTE WAX 30G", "marca": "bedhead","codigo_produto": "615908431605"},
  "140735": {"nome": "CD MANIPULATOR MATTE WAX 57G", "marca": "bedhead","codigo_produto": "615908431599"},
  "140734": {"nome": "CD MANIPULATOR PASTE 30G", "marca": "bedhead","codigo_produto": "615908431582"},
  "140733": {"nome": "CD MANIPULATOR PASTE 57G", "marca": "bedhead","codigo_produto": "615908431575"},
  "140738": {"nome": "CD SALTY NOT SORRY 100ML", "marca": "bedhead","codigo_produto": "615908431629"},
  "330558": {"nome": "Self Absorbed COND 400ML", "marca": "bedhead","codigo_produto": "615908433517"},
  "330556": {"nome": "Self Absorbed COND 750ML", "marca": "bedhead","codigo_produto": "615908433470"},
  "140823": {"nome": "CONTROL FREAK 255ml", "marca": "bedhead","codigo_produto": "615908426496"},
  "140816": {"nome": "CR AFTER PARTY SMOOTH 100ML", "marca": "bedhead","codigo_produto": "615908433180"},
  "140727": {"nome": "CR AFTER PARTY SMOOTH 50ML", "marca": "bedhead","codigo_produto": "615908431438"},
  "140821": {"nome": "EGO BOOST 237ml", "marca": "bedhead","codigo_produto": "615908426151"},
  "140006": {"nome": "Hair Stick Wax 73G", "marca": "bedhead","codigo_produto": "615908403718"},
  "330557": {"nome": "Moisture Maniac Cond 400mL", "marca": "bedhead","codigo_produto": "615908433494"},
  "330555": {"nome": "Moisture Maniac Cond 750mL", "marca": "bedhead","codigo_produto": "615908433456"},
  "300557": {"nome": "Moisture Maniac Shamp 400mL", "marca": "bedhead","codigo_produto": "615908433487"},
  "140740": {"nome": "Row Trouble Maker Spray Wax Aero 160g, 200ml", "marca": "bedhead","codigo_produto": "615908431643"},
  "300503": {"nome": "Serial Blonde Purple Toning Spoo 400mL", "marca": "bedhead","codigo_produto": "615908432343"},
  "300547": {"nome": "SH Bigger the Better Foam 200mL", "marca": "bedhead","codigo_produto": "615908431377"},
  "300506": {"nome": "SH Colour Goddess 100mL", "marca": "bedhead","codigo_produto": "615908432374"},
  "300508": {"nome": "SH Colour Goddess 400mL", "marca": "bedhead","codigo_produto": "615908432398"},
  "300564": {"nome": "SH Colour Goddess 750mL", "marca": "bedhead","codigo_produto": "615908433562"},
  "300545": {"nome": "SH Dry Oh Bee Hive 142g/238ml", "marca": "bedhead","codigo_produto": "615908431292"},
  "300538": {"nome": "SH Dry Rock Dirty 179g/300ml", "marca": "bedhead","codigo_produto": "615908432688"},
  "300369": {"nome": "SH For Men Clean Up 250mL", "marca": "bedhead","codigo_produto": "615908426786"},
  "300496": {"nome": "SH Gimme Grip 400mL", "marca": "bedhead","codigo_produto": "615908431520"},
  "300555": {"nome": "Moisture Maniac Shamp 750mL", "marca": "bedhead","codigo_produto": "615908433449"},
  "300516": {"nome": "SH Recovery 100mL", "marca": "bedhead","codigo_produto": "615908431988"},
  "300516-1": {"nome": "SH Recovery 100mL", "marca": "bedhead","codigo_produto": "615908431988"},
  "300518": {"nome": "SH Recovery 400mL", "marca": "bedhead","codigo_produto": "615908432008"},
  "300562": {"nome": "SH Recovery 750mL", "marca": "bedhead","codigo_produto": "615908433524"},
  "300520": {"nome": "SH Recovery 970mL", "marca": "bedhead","codigo_produto": "615908433357"},
 
  "300522": {"nome": "Resurrection SHAMP 100mL", "marca": "bedhead","codigo_produto": "615908433333"},
  "300524": {"nome": "Resurrection SHAMP 400mL", "marca": "bedhead","codigo_produto": "615908432022"},
  "300563": {"nome": "Resurrection SHAMP 750mL", "marca": "bedhead","codigo_produto": "615908433548"},
  "300526": {"nome": "Resurrection SHAMP 970mL", "marca": "bedhead","codigo_produto": "615908432046"},
  "300558": {"nome": "Self Absorbed SHAMP 400mL", "marca": "bedhead","codigo_produto": "615908433500"},
  "300556": {"nome": "Self Absorbed SHAMP 750mL", "marca": "bedhead","codigo_produto": "615908433463"},
  "300499": {"nome": "Serial Blonde SHAMP 400mL", "marca": "bedhead","codigo_produto": "615908432251"},
  "300565": {"nome": "Serial Blonde SHAMP 750mL", "marca": "bedhead","codigo_produto": "615908433586"},
  "140724": {"nome": "Small Talk 125mL", "marca": "bedhead","codigo_produto": "615908431346"},
  "140724-W": {"nome": "Small Talk 125mL", "marca": "bedhead","codigo_produto": "615908431346"},
  "140723": {"nome": "Small Talk 240mL", "marca": "bedhead","codigo_produto": "615908431339"},
  "140776": {"nome": "Some Like it Hot Heat Protection Spray 100mL", "marca": "bedhead","codigo_produto": "615908432138"},
  "140745": {"nome": "SPR Hard Head 385mL", "marca": "bedhead","codigo_produto": "615908431667"},
  "140751": {"nome": "SPR Hard Head 85g/100mL", "marca": "bedhead","codigo_produto": "615908431735"},
  "140728": {"nome": "SPR Headrush 144g/200mL", "marca": "bedhead","codigo_produto": "615908431469"},
  "140754": {"nome": "SPR Masterpiece 255g/340mL", "marca": "bedhead","codigo_produto": "615908431766"},
  "140760": {"nome": "SPR Masterpiece 68g/80mL", "marca": "bedhead","codigo_produto": "615908431827"},
  "140717": {"nome": "SPR Queen for a Day 298g/311mL", "marca": "bedhead","codigo_produto": "615908431209"},
  "140732": {"nome": "Straighten Out Serum 100mL", "marca": "bedhead","codigo_produto": "615908431490"},
  "1000665": {"nome": "Treat Me Right Mask 200mL", "marca": "bedhead","codigo_produto": "615908433937"},
  "140731": {"nome": "Wanna Glow 100mL", "marca": "bedhead","codigo_produto": "615908431483"},
  "1000038": {"nome": "Mini Small Talk Blah Blah Blah - 125ml", "marca": "bedhead","codigo_produto": "615908427172"},
  "New140760": {"nome": "Mini Masterpiece 79ml", "marca": "bedhead","codigo_produto": "000000000"},
  "BH - Recovery Sh 600": {"nome": "Recovery Shampoo 600ml", "marca": "bedhead","codigo_produto": "615908432015"},
"300516-1": {"nome": "Recovery Shampoo  100ml", "marca": "bedhead","codigo_produto": "615908431988"},
"1000136": {"nome": "BED HEAD KEEP IT CASUAL HAIRSPRAY 300ML", "marca": "bedhead",  "codigo_produto": "615908433814"},
  "C-ASCL10-001A": {"nome": "B. By banila Lip & Eye Remover 99ml", "marca": "banila","codigo_produto": "8809560221427"},
  "B-ASPM08-007A": {"nome": "Blooming Youth Peach Collagen Mask 20ml", "marca": "banila","codigo_produto": "8809759906166"},
  "B-ASFC10-007A": {"nome": "Blooming Youth Peach-Collagen Multi Stick Balm 10.5g", "marca": "banila","codigo_produto": "8809759906142"},
  "B-ASCL09-006A": {"nome": "Clean It Zero - Brightening Peeling Gel 120ml", "marca": "banila","codigo_produto": "8809759903455"},
  "B-DENS01-325A": {"nome": "Clean It Zero - Calming Foam Cleanser Cica-Relief 30ml", "marca": "banila","codigo_produto": "8809759907965"},
  "B-AXST01-382A": {"nome": "Clean It Zero - Christmas Special Edition Gbd 50mlx2", "marca": "banila","codigo_produto": "8800248700357"},
  "B-ASCL01-086A": {"nome": "Clean It Zero - Cleansing Balm Brightening 100ml", "marca": "banila","codigo_produto": "8809759904438"},
  "B-DENS01-343A": {"nome": "Clean It Zero - Cleansing Balm Calming Mini 7ml", "marca": "banila","codigo_produto": "8800248700050"},
  "B-ASCL01-020B": {"nome": "Clean It Zero - Cleansing Balm Nourishing 100ml", "marca": "banila","codigo_produto": "8809759908429"},
  "B-DENS01-344A": {"nome": "Clean It Zero - Cleansing Balm Nourishing Mini 7ml", "marca": "banila","codigo_produto": "8800248700067"},
  "B-ASCL01-033A": {"nome": "Clean It Zero - Cleansing Balm Original 100ml", "marca": "banila","codigo_produto": "8809759908399"},
  "B-ASCL01-042A": {"nome": "Clean It Zero - Cleansing Balm Original 25ml", "marca": "banila","codigo_produto": "8809759908535"},
  "B-DENS01-123B": {"nome": "Clean It Zero - Cleansing Balm Original Mini 7ml", "marca": "banila","codigo_produto": "8800248700036"},
  "B-CEGT01-024C": {"nome": "Clean It Zero - Cleansing Balm Original Miniature Set (2 Types)", "marca": "banila","codigo_produto": "8809759908580"},
  "B-CEGT01-022C": {"nome": "Clean It Zero - Cleansing Balm Original Miniature Set (4 Types)", "marca": "banila","codigo_produto": "000000000"},
  "B-ASCL01-045A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying 100ml", "marca": "banila","codigo_produto": "8809759908405"},
  "B-ASCL01-126A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying 50ml", "marca": "banila","codigo_produto": "8809759908559"},
  "B-DENS01-342A": {"nome": "Clean It Zero - Cleansing Balm Pore Clarifying Mini 7ml", "marca": "banila Co","codigo_produto": "8800248700043"},
  "B-ASCL01-022B": {"nome": "Clean It Zero - Cleansing Balm Purifying 100ml", "marca": "banila","codigo_produto": "8809759908412"},
  "B-ASCL01-017B": {"nome": "Clean It Zero - Cleansing Balm Revitalizing 100ml", "marca": "banila","codigo_produto": "8809560226453"},
  "B-ASCL02-023B": {"nome": "Clean It Zero - Foam Cleanser 150ml", "marca": "banila","codigo_produto": "8809560220062"},
  "B-DENS01-130A": {"nome": "Clean It Zero - Foam Cleanser Mini 8ml", "marca": "banila","codigo_produto": "8809560223827"},
  "B-ASFC13-001A": {"nome": "Clean It Zero - Green Peel Toner 70 Pads 200ml", "marca": "banila","codigo_produto": "8809759905121"},
  "B-ASCL01-137A": {"nome": "Clean It Zero - Hello Kitty Cleansing Balm 100ml", "marca": "banila","codigo_produto": "8809759909235"},
  "B-AXST01-307A": {"nome": "Clean It Zero - Kit 3 Mini Foam Favorites X15ml", "marca": "banila","codigo_produto": "8809759906098"},
  "B-ASCL01-138A": {"nome": "Clean It Zero - My Melody Cleansing Balm 100ml", "marca": "banila","codigo_produto": "8809759909242"},
  "B-ASFC02-045A": {"nome": "Clean It Zero - Pink Hydration Toner 70 Pads 235ml", "marca": "banila","codigo_produto": "8809759905114"},
  "B-AXST01-329B": {"nome": "Clean It Zero - Pink Wonderland Set", "marca": "banila","codigo_produto": "8800248700371"},
  "B-ASCL02-029A": {"nome": "Clean It Zero - Pore Clarifying Foam Cleanser 150ml", "marca": "banila","codigo_produto": "8809759903127"},
  "B-ASCL06-004E": {"nome": "Clean It Zero - Pure Cleansing Water 310ml", "marca": "banila","codigo_produto": "8809759903059"},
  "B-ASCL02-036A": {"nome": "Clean It Zero - Purifying Foam Cleanser 150ml", "marca": "banila","codigo_produto": "8809759907958"},
  "B-ASCL10-014A": {"nome": "Clean It Zero - Soothing Lip & Eye Makeup Remover 99ml", "marca": "banila","codigo_produto": "8809759900942"},
  "B-ASEY01-003A": {"nome": "Dear Hydration - Bounce Eye Cream 20ml", "marca": "banila","codigo_produto": "8809759903103"},
  "B-ASFC05-028C": {"nome": "Dear Hydration - Cool Down Mist 99ml", "marca": "banila","codigo_produto": "8809759903097"},
  "B-ASFC02-043B": {"nome": "Dear Hydration - Crystal Glow Essence 50ml", "marca": "banila","codigo_produto": "8809759903073"},
  "B-AXST01-408A": {"nome": "Kit Set Starter", "marca": "banila","codigo_produto": "8800248701095"},
  "B-AXST01-319B": {"nome": "Dear Hydration - Mini Duo Kit", "marca": "banila","codigo_produto": "8809759909440"},
  "B-ASFC02-036C": {"nome": "Dear Hydration - Toner 200ml", "marca": "banila","codigo_produto": "8809759903066"},
  "B-CEGT01-201A": {"nome": "Dear Hydration - Water Barrier Cream 10ml", "marca": "banila","codigo_produto": "8809759903516"},
  "B-ASFC02-038C": {"nome": "Dear Hydration - Water Barrier Cream 50ml", "marca": "banila","codigo_produto": "8809759903080"},
  "B-ASFC07-002A": {"nome": "Miss Flower E Mr. Honey Essence Stick 9g", "marca": "banila","codigo_produto": "8809560225258"},
  "B-ASFC07-004A": {"nome": "Miss Flower E Mr. Honey Propolis Rejuvenating 50ml", "marca": "banila","codigo_produto": "8809560226637"},
  "B-ASFC07-009A": {"nome": "Miss Flower E Mr. Honey Propolis Rejuvenating Ampoule Mist 99ml", "marca": "banila","codigo_produto": "8809759900003"},
  "B-AMBS02-001P": {"nome": "Prime Primer - Classic 30ml", "marca": "banila","codigo_produto": "8809759902892"},
  "B-AMBS02-007E": {"nome": "Prime Primer - Finish Powder 12g", "marca": "banila","codigo_produto": "8809759902922"},
  "B-AMBS02-005E": {"nome": "Prime Primer - Hydrating 30ml", "marca": "banila","codigo_produto": "8809759902908"},
  "B-AMBS02-036B": {"nome": "Prime Primer - Tone-Up 30ml", "marca": "banila","codigo_produto": "8809759902915"},
  "B-ASFC10-002B": {"nome": "Vv Vitalizing Collagen Essence 50ml", "marca": "banila","codigo_produto": "8809759901642"},
  "B-CEGT01-230A": {"nome": "GIFT banila CO Twisted Hair Bend", "marca": "banila","codigo_produto": "8809759906487"},
  "B-ASCL01-087A": {"nome": "banila Co - Clean it Zero Cleansing Balm - Ceramide 100ml", "marca": "banila", "codigo_produto": "8809759904629"},
  "C-AMLP07-006A": {"nome": "PK02", "marca": "banila","codigo_produto": "8800248700579"},
  "C-AMLP07-005A": {"nome": "PK01", "marca": "banila","codigo_produto": "8800248700562"},
  "C-AMLP07-010A": {"nome": "PP01", "marca": "banila","codigo_produto": "8800248700616"},
  "B-AXST01-383A": {"nome": "GBD", "marca": "banila","codigo_produto": "8800248700388"},
  "B-DENS01-349A": {"nome": "Mini Enriching Butter 7ml (Avocado+)", "marca": "banila", "codigo_produto": "000000000"},
"C-AMLP07-009A": {"nome": "RD01", "marca": "banila","codigo_produto": "8800248700609"},
"B-ASCL01-123A": {"nome": "Clean it Zero Balm - Original 50ml (Acerola+)", "marca": "banila", "codigo_produto": "8809759908528"},
"B-ASCL09-008A": {"nome": "Clean It Zero - Tea Tree Pore Peeling Gel 120ml", "marca": "banila", "codigo_produto": "8809759909471"},
"BC - Pore Clarifying - Foam 30": {"nome": "Espuma de Limpeza para Pele Oleosa Pore Clarifying 30ml", "marca": "banila","codigo_produto": "000000000"  },
  "PF026809": {"nome": "Blond Rescue - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223215"},
  "PF026795": {"nome": "BB Cream 12 em 1 - Leave-In Condicionante 180ml", "marca": "alfaparf","codigo_produto": "7899884223079"},
  "PF026810": {"nome": "Blond Rescue - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223222"},
  "PF026786": {"nome": "Blond Rescue - Condicionador 300ML", "marca": "alfaparf","codigo_produto": "7899884222980"},
  "PF026812": {"nome": "Brazilian Curls - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223246"},
  "PF026788": {"nome": "Brazilian Curls - Condicionador 300ML", "marca": "alfaparf","codigo_produto": "7899884223000"},
  "PF026811": {"nome": "Brazilian Curls - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223239"},
  "PF026787": {"nome": "Brazilian Curls - Shampoo 300ML", "marca": "alfaparf","codigo_produto": "7899884222997"},
  "PF026806": {"nome": "Color Shield - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223185"},
  "PF026782": {"nome": "Color Shield - Condicionador 300ML", "marca": "alfaparf","codigo_produto": "7899884222942"},
  "PF026851": {"nome": "Condicionador Real Liss 300ml", "marca": "alfaparf","codigo_produto": "7899884223345"},
  "PF026807": {"nome": "Hidro Control - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223192"},
  "PF026783": {"nome": "Hidro Control - Shampoo 300ML", "marca": "alfaparf","codigo_produto": "7899884222959"},
  "PF026808": {"nome": "Hidro Control - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223208"},
  "PF026791": {"nome": "Long & Force - Condicionador 300ML", "marca": "alfaparf","codigo_produto": "7899884223031"},
  "PF026815": {"nome": "Long & Force - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223277"},
  "PF026790": {"nome": "Long & Force - Shampoo 300ML", "marca": "alfaparf","codigo_produto": "7899884223024"},
  "PF026798": {"nome": "Love Oil - Óleo Capilar 55ML", "marca": "alfaparf","codigo_produto": "7899884223109"},
  "PF026803": {"nome": "Nutri Restore - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223154"},
  "PF026777": {"nome": "Nutri Restore - Shampoo 300ML", "marca": "alfaparf","codigo_produto": "7899884222898"},
  "PF026802": {"nome": "Nutri Restore - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223147"},
  "PF026818": {"nome": "OX 30VOL 900ml", "marca": "alfaparf","codigo_produto": "7899884223307"},
  "PF026819": {"nome": "OX 40VOL 900ml", "marca": "alfaparf","codigo_produto": "7899884223314"},
  "PF026805": {"nome": "Oils Recovery - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223178"},
  "PF026804": {"nome": "Oils Recovery - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223161"},
  "PF026821": {"nome": "Power Reconstruction - Máscara 500G", "marca": "alfaparf","codigo_produto": "7899884223338"},
  "PF026814": {"nome": "Real Liss - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223260"},
  "PF026789": {"nome": "Real Liss - Shampoo 300ML", "marca": "alfaparf","codigo_produto": "7899884223017"},
  "PF026813": {"nome": "Real Liss - Shampoo 1000ML", "marca": "alfaparf","codigo_produto": "7899884223253"},
  "PF026793": {"nome": "Repair - Máscara 300G", "marca": "alfaparf","codigo_produto": "7899884223055"},
  "PF026820": {"nome": "Repair - Máscara 500G", "marca": "alfaparf","codigo_produto": "7899884223321"},
  "PF026785": {"nome": "Shampoo Blond Rescue 300ml", "marca": "alfaparf","codigo_produto": "7899884222973"},
  "PF016447": {"nome": "Diamond Illuminating - Condicionador 200ML", "marca": "alfaparf","codigo_produto": "7899884207109"},
  "PF016449": {"nome": "Diamond Illuminating - Máscara 200ML", "marca": "alfaparf","codigo_produto": "7899884207031"},
  "PF016450": {"nome": "Diamond Illuminating - Máscara Capilar 500ML", "marca": "alfaparf","codigo_produto": "7899884207154"},
  "PF016445": {"nome": "Diamond Illuminating - Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "7899884207000"},
  "PF016417": {"nome": "Moisture Nutritive - Máscara 200ML", "marca": "alfaparf","codigo_produto": "7899884207048"},
  "PF016418": {"nome": "Moisture Nutritive - Máscara 500ML", "marca": "alfaparf","codigo_produto": "7899884207178"},
  "PF016419": {"nome": "Nutritive Leave-In Conditioner 200ML", "marca": "alfaparf","codigo_produto": "9988776655"},
  "PF016415": {"nome": "Nutritive Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "7899884207017"},
  "PF019474": {"nome": "Scalp Rebalance Balancing - Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "8022297095912"},
  "PF019472": {"nome": "Scalp Rebalance Purifying - Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "8022297095899"},
  "PF019466": {"nome": "Scalp Renew Energizing - Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "8022297095837"},
  "PF020604": {"nome": "Smooth Smoothing - Conditioner 200ML", "marca": "alfaparf","codigo_produto": "7899884216354"},
  "PF020602": {"nome": "Smooth Smoothing - Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "7899884216323"},
  "PF020606": {"nome": "Smooth Smoothing - Máscara 200ML", "marca": "alfaparf","codigo_produto": "7899884216361"},
  "PF020607": {"nome": "Smooth Smoothing - Máscara 500ML", "marca": "alfaparf","codigo_produto": "7899884216378"},
  "PF025387": {"nome": "Sublime Cristalli Liquidi 15ML", "marca": "alfaparf","codigo_produto": "7899884219805"},
  "PF016456": {"nome": "Sublime Cristalli Liquidi 50ML", "marca": "alfaparf","codigo_produto": "7899884219829"},
  "PF025944": {"nome": "Sublime Essential Oil - Ampola Capilar 13ML Mono-dose", "marca": "alfaparf","codigo_produto": "7899884225547"},
  "PF027566": {"nome": "Reconstruction Reparative - Máscara Capilar 200ML", "marca": "alfaparf","codigo_produto": "7899884226476"},
  "PF027567": {"nome": "Reconstruction Reparative - Máscara Capilar 500ML", "marca": "alfaparf","codigo_produto": "7899884226483"},
  "PF027564": {"nome": "Reconstruction Reparative Low Shampoo 250ML", "marca": "alfaparf","codigo_produto": "7899884226452"},
  "PF014102": {"nome": "Pigments Rose Copper 90ml", "marca": "alfaparf","codigo_produto": "8022297042374"},
  "PF026816": {"nome": "Mab - Long & Force - Condicionador 1000ML", "marca": "alfaparf","codigo_produto": "7899884223284"},
  "PF026607": {"nome": "Semi Di Lino Sunshine - After-Sun Shampoo 250ml", "marca": "alfaparf","codigo_produto": "8022297169156"},
  "PF026608": {"nome": "Semi Di Lino Sunshine - After-Sun Treatment 200ml (Máscara)", "marca": "alfaparf","codigo_produto": "8022297169163"},
  "PF026610": {"nome": "Semi Di Lino Sunshine - Hair Protective Milk 125ml", "marca": "alfaparf","codigo_produto": "8022297169187"},
  "PF026609": {"nome": "Semi Di Lino Sunshine - Hair Protective Oil 125ml", "marca": "alfaparf",   "codigo_produto": "8022297169170"},
 "2801754": {"nome": "DR PAWPAW HOT PINK BALM 25ML", "marca": "Dr.PawPaw","codigo_produto": "5060372801754"},
  "2807275": {"nome": "DR PAWPAW IT DOES IT ALL CONDITIONER 200ML", "marca": "Dr.PawPaw","codigo_produto": "5060372807275"},
  "2800214": {"nome": "DR PAWPAW IT DOES IT ALL HAIRCARE 150ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800214"},
  "2807268": {"nome": "DR PAWPAW IT DOES IT ALL SHAMPOO 200ML", "marca": "Dr.PawPaw","codigo_produto": "5060372807268"},
  "2800269": {"nome": "DR PAWPAW ORIGINAL BALM 10ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800856"},
  "2800009": {"nome": "DR PAWPAW ORIGINAL BALM 25ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800009"},
  "2803277": {"nome": "DR PAWPAW OVERNIGHT LIP MASK 25ML", "marca": "Dr.PawPaw","codigo_produto": "5060372803277"},
  "2800047": {"nome": "DR PAWPAW PEACH PINK BALM 25ML", "marca": "Dr. PawPaw","codigo_produto": "5060372800047"},
  "2800542": {"nome": "DR PAWPAW PEACH PINK BALM 8ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800542"},
  "2800085": {"nome": "DR PAWPAW ULTIMATE RED BALM 25ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800085"},
  "2800566": {"nome": "DR PAWPAW ULTIMATE RED BALM 8ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800566"},
  "2808418": {"nome": "DR PAWPAW PLUMPING LIP OIL 8ML", "marca": "Dr.PawPaw","codigo_produto": "5060372808418"},
  "2808425": {"nome": "DR PAWPAW LIP & EYE BALM 8ML", "marca": "Dr.PawPaw","codigo_produto": "5060372808425"},
  "2800696": {"nome": "DR PAWPAW SHEA BUTTER LIP BALM 8ML", "marca": "Dr.PawPaw","codigo_produto": "5060372800696"},
  "2803468": {"nome": "DR. PAWPAW OVERNIGHT LIP MASK 10ML", "marca": "Dr.PawPaw",  "codigo_produto": "5060372803468"     },
  "ADS 101": {"nome": "ADS 101", "marca": "purederm","codigo_produto": "8809052581015"},
  "ADS 748": {"nome": "ADS 748", "marca": "purederm","codigo_produto": "8809541199011"},
  "ADS 763": {"nome": "Purederm- ADS 763 - Adesivo Hidratante em Gel para os Olhos", "marca": "purederm","codigo_produto": "8809541199004"},
  "ADS 841": {"nome": "ADS 841", "marca": "purederm","codigo_produto": "8809541198625"},
  "ADS 200": {"nome": "ADS 200", "marca": "purederm","codigo_produto": "8809052582593"},
  "ADS 822": {"nome": "ADS 822 PUREDERM TROUBLE CLEAR SPOT 22 PATCHES", "marca": "purederm","codigo_produto": "8809738321089"},
  "PR 413": {"nome": "PR 413 - DAILYMOSTURE HANDCREAM 50ML", "marca": "purederm","codigo_produto": "8809738320365"},
  "PR 408": {"nome": "PR 408 - PUREDERM HONEY & BERRY LIP SLEEPING MASK 15G", "marca": "purederm","codigo_produto": "8809411188657"},
  "PR 419": {"nome": "PR 419 - PUREDERM Prreti: Biome Collagen Eye Cream 30ml", "marca": "purederm","codigo_produto": "8809738323694"},
  "PR 420": {"nome": "PR 420 - PUREDERM P/R REPAIR CERAMIDE CREAM 50ML", "marca": "purederm","codigo_produto": "8809738323700"},
  "PR 526": {"nome": "PR 526 - PUREDERM SERUM FACIAL ÁCIDO HIALURÔNICO PURO", "marca": "purederm","codigo_produto": "8809541198779"},
  "PR 548": {"nome": "PR 548 - BIOME COLLAGEN BLENDING SERUM&CREAM 90G", "marca": "purederm","codigo_produto": "9988776655"},
  "PR 538": {"nome": "PR 538", "marca": "purederm","codigo_produto": "8809823390037"},
  "PR 423": {"nome": "PR 423", "marca": "purederm","codigo_produto": "8809738325155"},
  "PR 401": {"nome": "PR 401", "marca": "purederm", "codigo_produto": "8809411187315"},
 "TSH10": {"nome": "Serum Ampoule Colágeno EGF 30ml ", "marca": "exi","codigo_produto": "8809080823408"},
  "TSH20": {"nome": "Serum Ampoule Mucina da Caracol 5000", "marca": "exi","codigo_produto": "8809080823392"},
  "TSH30": {"nome": "Serum Ampoule ácido Hialurônico 6000", "marca": "exi","codigo_produto": "8809080823415"},
  "TSH40": {"nome": "Sleeping Mask Multifuncional", "marca": "exi","codigo_produto": "8809080823460"},
  "471170": {"nome": "UB TIGI LARGE PADDLE BRUSH", "marca": "exi","codigo_produto": "615908416633"},
  "471169": {"nome": "UB TIGI SMALL PADDLE BRUSH", "marca": "exi","codigo_produto": "615908416626"},
  "471168": {"nome": "UB TIGI VENT BRUSH", "marca": "exi","codigo_produto": "615908416619"},
  "471167": {"nome": "UB TIGI X-LARGE ROUND BRUSH 2", "marca": "exi","codigo_produto": "615908416602"},
  "DS04": {"nome": "Highprime Collagen Ampoule Mist 50ml", "marca": "exi","codigo_produto": "8809630091684"},
  "DS02": {"nome": "Highprime Collagen Film Cheek (5pcs)", "marca": "exi","codigo_produto": "8809630091660"},
  "DS01": {"nome": "Highprime Collagen Film Eye or Smilelines (5pcs)", "marca": "exi","codigo_produto": "8809630091653"},
  "DS03": {"nome": "Highprime Collagen Film Forehead Or Neck (5pcs)", "marca": "exi","codigo_produto": "8809630091677"},
  "VTPD40136": {"nome": "Essência Reedle Shot 1000 - 15ml", "marca": "exi","codigo_produto": "8803463003500"},
  "VTPD40019": {"nome": "Essência Reedle Shot 300 - 50ml", "marca": "exi","codigo_produto": "8809695678431"},
  "68600632": {"nome": "Q-Tips - Discos de Algodão para Beleza - Kit 80un", "marca": "exi", "codigo_produto": "305210045736"},
  "69993370": {"nome": "Q-Tips - Hastes de Algodão - Kit de Viagem 30un", "marca": "exi","codigo_produto": "305210221277"},
  "64360311": {"nome": "Q-Tips - Hastes de Algodão Orgânico - Kit de Viagem 30un", "marca": "exi","codigo_produto": "305210047709"},
  "64360310": {"nome": "Q-Tips - Hastes de Algodão com Pontas de Precisão - Kit de Viagem 30un", "marca": "exi", "codigo_produto": "305210047693"},
  "1486": {"nome": "1486", "marca": "real","codigo_produto": "079625014860"},
  "1894": {"nome": "1894", "marca": "real","codigo_produto": "079625018943"},
  "1786": {"nome": "1786", "marca": "real","codigo_produto": "079625017861"},
  "1895": {"nome": "1895", "marca": "real","codigo_produto": "079625018950"},
  "1991": {"nome": "1991", "marca": "real","codigo_produto": "079625019919"},
  "1993": {"nome": "1993", "marca": "real","codigo_produto": "079625019933"},
  "1994": {"nome": "1994", "marca": "real","codigo_produto": "079625019940"},
  "1492": {"nome": "1492", "marca": "real","codigo_produto": "079625014921"},
  "1700": {"nome": "1700", "marca": "real","codigo_produto": "079625017007"},
  "1704": {"nome": "1704", "marca": "real","codigo_produto": "079625017045"},
  "10009300": {"nome": "0093", "marca": "real","codigo_produto": "079625439397"},
  "1854": {"nome": "1854", "marca": "real","codigo_produto": "079625018547"},
  "1855": {"nome": "1855", "marca": "real","codigo_produto": "079625018554"},
  "1965": {"nome": "1965", "marca": "real","codigo_produto": "079625019650"},
  "10005200": {"nome": "0052", "marca": "real","codigo_produto": "079625438390"},
  "10006000": {"nome": "0060", "marca": "real","codigo_produto": "079625438475"},
  "10006200": {"nome": "0062", "marca": "real","codigo_produto": "079625438499"},
  "10006500": {"nome": "0065", "marca": "real","codigo_produto": "079625438901"},
  "10007158": {"nome": "0071", "marca": "real","codigo_produto": "079625439021"},
  "10007261": {"nome": "0072", "marca": "real","codigo_produto": "079625439038"},
  "10008900": {"nome": "0089", "marca": "real","codigo_produto": "079625439328"},
  "10013860": {"nome": "0138", "marca": "real","codigo_produto": "079625440935"},
  "10009760": {"nome": "0097", "marca": "real","codigo_produto": "079625439496"},
  "10010700": {"nome": "0107", "marca": "real","codigo_produto": "079625441079"},
  "10012600": {"nome": "0126", "marca": "real","codigo_produto": "079625440812"},
  "10013000": {"nome": "0130", "marca": "real","codigo_produto": "079625440850"},
  "10013860": {"nome": "0138", "marca": "real","codigo_produto": "079625440935"},
  "10030500": {"nome": "0305", "marca": "real","codigo_produto": "079625446012"},
  "10031100": {"nome": "0311", "marca": "real","codigo_produto": "079625446067"},
  "10031200": {"nome": "0312", "marca": "real","codigo_produto": "079625446111"},
  "10009960": {"nome": "0099", "marca": "real","codigo_produto": "079625439519"},
  "10010060": {"nome": "0100", "marca": "real","codigo_produto": "079625439526"},
  "10010400": {"nome": "0104", "marca": "real","codigo_produto": "079625439762" },
  "10012458": {"nome": "0124", "marca": "real","codigo_produto": "079625440119"},
  "1401": {"nome": "1401", "marca": "real","codigo_produto": "079625014013"},
  "1407": {"nome": "1407", "marca": "real","codigo_produto": "079625014075"},
  "1411": {"nome": "1411", "marca": "real","codigo_produto": "079625014112"},
  "1413": {"nome": "1413", "marca": "real","codigo_produto": "079625014136"},
  "1489": {"nome": "1489", "marca": "real","codigo_produto": "079625014891"},
  "1529": {"nome": "1529", "marca": "real","codigo_produto": "079625915297"},
  "1542": {"nome": "1542", "marca": "RT","codigo_produto": "079625915426"},
  "1553": {"nome": "1553", "marca": "real","codigo_produto": "079625915532"},
  "10156600": {"nome": "10156600", "marca": "RT","codigo_produto": "079625915662"},
  "1570": {"nome": "1570", "marca": "real","codigo_produto": "079625915709"},
  "4054": {"nome": "4054", "marca": "real","codigo_produto": "079625040548"},
  "4218": {"nome": "4218  DAY ADVENT CALENDAR", "marca": "real","codigo_produto": "079625042184"},
  "4222": {"nome": "4222", "marca": "real","codigo_produto": "079625042221"},
  "4224": {"nome": "4224", "marca": "real","codigo_produto": "079625042245"},
  "4247": {"nome": "4247", "marca": "real","codigo_produto": "079625042474"},
  "4285": {"nome": "4285", "marca": "real","codigo_produto": "079625042856"},
  "4318": {"nome": "4318", "marca": "real","codigo_produto": "079625043181"},
  "1490LGSTND": {"nome": "RT PORTA ESPONJA", "marca": "real","codigo_produto": "20079625558542"},
  "1972": {"nome": "1972", "marca": "real","codigo_produto": "079625019728"},
  "4244": {"nome": "4244", "marca": "real","codigo_produto": "079625042443"  },
  "4245": {"nome": "4245", "marca": "real","codigo_produto": "0000000000"  },
  "4267": {"nome": "4267", "marca": "real","codigo_produto": "079625042672"},
  "10009200": {"nome": "RT MIRACLE CONCEALER SPONGE", "marca": "real","codigo_produto": "079625439380"},
  "10009400": {"nome": "10009400", "marca": "real","codigo_produto": "079625439403"},
  "10012700": {"nome": "10012700", "marca": "real","codigo_produto": "079625440829"},
  "10012800": {"nome": "10012800", "marca": "real","codigo_produto": "079625440836"},
  "10012900": {"nome": "10012900", "marca": "real","codigo_produto": "079625440843"},
  "10013100": {"nome": "10013100", "marca": "real","codigo_produto": "079625440867"},
  "10013200": {"nome": "10013200", "marca": "real","codigo_produto": "079625440874"},
  "10013400": {"nome": "10013400", "marca": "real","codigo_produto": "079625440898" },
  "10014158": {"nome": "10014158", "marca": "real","codigo_produto": "079625441017"},
  "10014300": {"nome": "10014300", "marca":"real","codigo_produto": "079625441147"},
  "10020961": {"nome": "10020961", "marca": "real","codigo_produto": "079625441918"},
  "10021561": {"nome": "10021561", "marca": "real","codigo_produto": "079625441963"},
  "10022062": {"nome": "10022062", "marca": "real","codigo_produto": "079625441949"},
  "10026800": {"nome": "10026800", "marca": "real","codigo_produto": "079625442205"},
  "1462": {"nome": "1462", "marca": "real","codigo_produto": "079625014624"},
  "1966": {"nome": "1966", "marca": "real","codigo_produto": "079625019667"},
  "1977": {"nome": "1977", "marca": "real", "codigo_produto": "079625019773"},
  "4067": {"nome": "4067", "marca": "real","codigo_produto": "079625040678"},
  "4161": {"nome": "4161", "marca": "real","codigo_produto": "079625041613"},
  "4193": {"nome": "4193", "marca": "real","codigo_produto": "079625041934"},
  "4257": {"nome": "4257", "marca": "real","codigo_produto": "079625042573"},
  "4258": {"nome": "4258", "marca": "real","codigo_produto": "079625042580"},
  "4259": {"nome": "4259", "marca": "real","codigo_produto": "079625042597"},
  "4263": {"nome": "4263", "marca": "real","codigo_produto": "079625042634"},
  "4265": {"nome": "4265", "marca": "real","codigo_produto": "079625042658"},
  "4268": {"nome": "4268", "marca": "real","codigo_produto": "079625042689"},
  "4269": {"nome": "4269", "marca":"real","codigo_produto": "079625042696"},
  "4270": {"nome": "4270", "marca": "real","codigo_produto": "079625042702"},
  "10431000": {"nome": "10431000", "marca": "real","codigo_produto": "079625043105"},
  "4262": {"nome": "4262", "marca": "real","codigo_produto": "079625042627"},
  "4266": {"nome": "4266", "marca": "real","codigo_produto": "079625042665"  },
  "4271": {"nome": "4271", "marca": "RT","codigo_produto": "079625042719"},
  "10013300": {"nome": "0133", "marca": "real","codigo_produto": "079625440881"},
  "10047010": {"nome": "0470", "marca": "real","codigo_produto": "079625451047"},
  "10046710": {"nome": "0467", "marca": "real","codigo_produto": "079625450804"},
  "1917": {"nome": "1917", "marca": "real","codigo_produto": "079625019179"},
  "10047210": {"nome": "0472", "marca": "real","codigo_produto": "079625450972"},
  "10005200": {"nome": "0052", "marca": "real","codigo_produto": "079625438390"},
  "4211": {"nome": "4211", "marca": "real","codigo_produto": "079625042115"},
  "10047210": {"nome": "0472", "marca": "real","codigo_produto": "079625450972"},
  "10012600": {"nome": "0126", "marca": "real","codigo_produto": "079625440812"},
  "10045610": {"nome": "0456", "marca": "real","codigo_produto": "079625450675"},
  "10013860": {"nome": "0138", "marca": "real","codigo_produto": "079625440935"},
  "10015240": {"nome": "0152", "marca": "real","codigo_produto": "079625441383"},
  "10045810": {"nome": "0458", "marca": "real","codigo_produto": "079625450781"},
   "10052300": {"nome": "0523", "marca": "real","codigo_produto": "079625453560"   },
   "10034760": {"nome": "0347", "marca": "real","codigo_produto": "079625448719"},
   "10059760": {"nome": "0597", "marca": "real","codigo_produto": "079625459951"},
   "10059160": {"nome": "0591", "marca": "real","codigo_produto": "079625459920"},
   "10013000": {"nome": "0130", "marca": "real","codigo_produto": "079625440850"},
   "10006000": {"nome": "0060", "marca": "real","codigo_produto": "079625438475"},
    "10048910": {"nome": "0489", "marca": "real","codigo_produto": "079625451245"},
    "10009000": {"nome": "0090", "marca": "real","codigo_produto": "079625439366"},
"10031800": {"nome": "0318", "marca": "real","codigo_produto": "079625446364"},
"10007261": {"nome": "0072", "marca": "real","codigo_produto": "079625439038"},
"10081000": {"nome": "10081000- RT MAKEUP EXPERT FAVORITES SET BR", "marca": "real","codigo_produto": "079625444841 "},
"10007158": {"nome": "0071", "marca": "real","codigo_produto": "079625439021"},
"10048310": {"nome": "0483", "marca": "real","codigo_produto": "079625451146"},
"10031100": {"nome": "0311", "marca": "real","codigo_produto": "079625446067"},
"10031200": {"nome": "0312", "marca": "real","codigo_produto": "079625446111"},
"10005400": {"nome": "0054  RT Real Clean XL Makeup Removing Wipes", "marca": "real","codigo_produto": "079625438413"},
"10052400": {"nome": "0524 ", "marca": "real","codigo_produto": "079625452525"},
"10051500": {"nome": "0515  ", "marca": "real","codigo_produto": "079625452495"},
"4223": {"nome": "4223", "marca": "real","codigo_produto": "079625042238"},
"PS-1": {"nome": "Apontador Duplo", "marca": "real","codigo_produto": "9780201379624"},
"Facial Hair Shaping Tool": {"nome": "pente para barba", "marca": "real","codigo_produto": "7896818203527"},
  "0047": {"nome": "ECO KIT BLEND + BLUS DUO", "marca": "Ecotools", "codigo_produto": "079625440706"},
  "ECO-3144": {"nome": "3144", "marca": "Ecotools", "codigo_produto": "079625031447"},
  "ECO-1202": {"nome": "1202", "marca": "Ecotools","codigo_produto": "079625012026"},
  "ECO-3146": {"nome": "3146", "marca": "Ecotools","codigo_produto": "000000000"},
  "ECO-1606": {"nome": "1606", "marca": "Ecotools","codigo_produto": "079625016062"},
  "ECO-7572 (C)": {"nome": "Massageador Corporal Body Roller Cinza - 7572", "marca": "Ecotools","codigo_produto": "079625075724"},
  "ECO-7572 (R)": {"nome": "Massageador Corporal Body Roller Rosa - 7572", "marca": "Ecotools","codigo_produto": "079625075724"},
  "ECO-1600": {"nome": "1600", "marca": "Ecotools","codigo_produto": "079625016000"},
  "ECO-1608": {"nome": "1608", "marca": "Ecotools","codigo_produto": "00000000"},
  "ECO-1306": {"nome": "1306", "marca": "Ecotools","codigo_produto": "079625013061"},
  "ECO-7592": {"nome": "Rolo Massageador Facial Contour - 7592", "marca": "Ecotools","codigo_produto": "079625075922"},
  "ECO-7517": {"nome": "Rolo Massageador Facial Pedra Jade - 7517", "marca": "Ecotools","codigo_produto": "079625075175"},
  "Eco-Necessaire": {"nome": "Eco-Necessaire", "marca": "Ecotools","codigo_produto": "000000000"},
"10170840201": {"nome": "Fino Touch Hair Oil Serum AIRY Smooth 70ml", "marca": "fino","codigo_produto": "4550516483836"},
"10170701202": {"nome": "Fino Touch Hair Oil 70ml", "marca": "fino","codigo_produto": "4901872471997"},
"10170702202": {"nome": "Fino Touch Hair Mask 230g", "marca": "fino","codigo_produto": "4901872837144"},
"1015D092202": {"nome": "Máscara 40g", "marca": "fino","codigo_produto": "4901824571874"},
"1015D354202": {"nome": "Mini Oil 10ml ", "marca": "fino","codigo_produto": "4901872471997"},
 "14145013370": {"nome": "Kit com 2 Embalagens de Plastico para Viagem 80ml", "marca": "tsubaki","codigo_produto": "2114145013370"},
"10170642202": {"nome": "INTENSIVE Repair Conditioner  490ml", "marca": "tsubaki","codigo_produto": "4550516474155"},
"10170640202": {"nome": "INTENSIVE Repair Shampoo 490ml", "marca": "tsubaki","codigo_produto": "4550516474087"},
"10170558202": {"nome": "Repair Mask 180g", "marca": "tsubaki","codigo_produto": "4901872459957"},
"10170636202": {"nome": "VOLUME Repair Conditioner 490ml", "marca": "tsubaki","codigo_produto": "4901872466238"},
"10170634202": {"nome": "VOLUME Repair Shampoo 490ml", "marca": "tsubaki","codigo_produto": "4901872466146"},
"10170632202": {"nome": "MOIST Repair Conditioner 490ml", "marca": "tsubaki","codigo_produto": "4901872466061"},
"10170630202": {"nome": "MOIST Repair Shampoo 490ml", "marca": "tsubaki","codigo_produto": "4901872466023"},
  "14072": {"nome": "Argan Oil Condicionador 500ml", "marca": "lee","codigo_produto": "5060282708532"},
  "14073": {"nome": "Argan Oil Máscara 200ml", "marca": "lee","codigo_produto": "5060282704640"},
  "14074": {"nome": "Argan Oil Nourishing Miracle Oil 50ml", "marca": "lee","codigo_produto": "5060282704664"},
  "14071": {"nome": "Argan Oil Shampoo 500ml", "marca": "lee","codigo_produto": "5060282708525"},
  "14047": {"nome": "Bleach Blondes Purple Toning Shampoo 500ml", "marca": "lee","codigo_produto": "5060282708389"},
  "14088": {"nome": "Coco Loco Blow & Go 11-in-1 Lotion 100ml", "marca": "lee","codigo_produto": "5060282702868"},
  "14089": {"nome": "Coco Loco Heat Protection Mist 150ml", "marca": "lee","codigo_produto": "5060282703520"},
  "14086": {"nome": "Coco Loco Shine Condicionador 500ml", "marca": "lee","codigo_produto": "5060282708150"},
  "14087": {"nome": "Coco Loco Shine Mask 200ml", "marca": "lee","codigo_produto": "5060282703452"},
  "14090": {"nome": "Coco Loco Shine Oil 75ml", "marca": "lee","codigo_produto": "5060282703575"},
  "14085": {"nome": "Coco Loco Shine Shampoo 500ml", "marca": "lee","codigo_produto": "5060282708136"},
  "14002": {"nome": "Grow Strong & Long Condicionador 500ml", "marca": "lee","codigo_produto": "5060282708204"},
  "14004": {"nome": "Grow Strong & Long Leave-in 100ml", "marca": "lee","codigo_produto": "5060282706545"},
  "14003": {"nome": "Grow Strong & Long Máscara 200ml", "marca": "lee","codigo_produto": "5060282706491"},
  "14005": {"nome": "Grow Strong & Long Scalp Serum 75ml", "marca": "lee","codigo_produto": "5060282706538"},
  "14001": {"nome": "Grow Strong & Long Shampoo 500ml", "marca": "lee","codigo_produto": "5060282708198"},
  "14037": {"nome": "Hold Tight Hairspray de Fixação 250ml", "marca": "lee","codigo_produto": "5060282705494"},
  "14035": {"nome": "Styling Dry Shampoo 200ml", "marca": "lee","codigo_produto": "5060282705371"         },
  "111316309": {"nome": "10 Professional Cica Ceramide Oil Serum 60ml", "marca": "mise","codigo_produto": "8809925152816"},
  "111315717": {"nome": "CURLING ESSENCE 2X NATURAL CURL 150ml", "marca": "mise","codigo_produto": "8809803560610"},
  "111315718": {"nome": "CURLING ESSENCE 2X NATURAL CURL 230ml", "marca": "mise","codigo_produto": "8809803560627"},
  "111315797": {"nome": "CURLING ESSENCE 2X VOLUME CURL 150ml", "marca": "mise","codigo_produto": "8809803560924"},
  "111315798": {"nome": "CURLING ESSENCE 2X VOLUME CURL 230ml", "marca": "mise","codigo_produto": "8809803560917"},
  "111316101": {"nome": "CURLING FOR BANGS FIXER 200ml", "marca": "mise","codigo_produto": "8809803591720"},
  "111316185": {"nome": "DAMAGE CARE RED PROTEIN COND 200ml", "marca": "mise","codigo_produto": "8809685746973"},
  "111316190": {"nome": "DAMAGE CARE RED PROTEIN MASK 180ml", "marca": "mise","codigo_produto": "8809925130104"},
  "111316184": {"nome": "DAMAGE CARE RED PROTEIN SHAMPOO 200ml", "marca": "mise","codigo_produto": "8809643064088"},
  "111316106": {"nome": "PERFECT S. 3 MINUTES HAIR MASK 300ml", "marca": "mise","codigo_produto": "8809803592604"},
  "111315564": {"nome": "PERFECT S. BASE UP ESSENCE 200ml", "marca": "mise","codigo_produto": "8809803556224"},
  "111315565": {"nome": "PERFECT S. NO WASH CD TREATMENT CREAM PACK 230ml", "marca": "mise","codigo_produto": "8809803556231"},
  "111316102": {"nome": "PERFECT S. NO WASH WATER TREATMENT CD 215ml", "marca": "mise","codigo_produto": "8809803591669"},
  "111315555": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 180ml", "marca": "mise","codigo_produto": "8809803556149"},
  "111316163": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 330ml", "marca": "mise","codigo_produto": "8809803556316"},
  "111315583": {"nome": "PERFECT S. ORIGINAL CD TREATMENT 900ml", "marca": "mise","codigo_produto": "8809803556262"},
  "111316409": {"nome": "PERFECT S. ORIGINAL COND 200ml", "marca": "mise","codigo_produto": "8809925173835"},
  "111315736": {"nome": "PERFECT S. ORIGINAL CONDI 530ml", "marca": "mise","codigo_produto": "8809803540346"},
  "111315548": {"nome": "PERFECT S. ORIGINAL CONDI 680ml", "marca": "mise","codigo_produto": "8809803549202"},
  "111315588": {"nome": "PERFECT S. ORIGINAL MIST 150ml", "marca": "mise","codigo_produto": "8809803556293"},
  "111316012": {"nome": "PERFECT S. ORIGINAL MIST 250ml", "marca": "mise","codigo_produto": "8809803565738"},
  "111315567": {"nome": "PERFECT S. ORIGINAL SERUM 200ml", "marca": "mise","codigo_produto": "8809803556248"},
  "111317310": {"nome": "PERFECT S. ORIGINAL SERUM 30ml", "marca": "mise","codigo_produto": "8809925126497"},
  "111315560": {"nome": "PERFECT S. ORIGINAL SERUM 80ml", "marca": "mise","codigo_produto": "8809803556187"},
  "111317290": {"nome": "PERFECT S. ORIGINAL SHAMPOO 140ml", "marca": "mise","codigo_produto": "8809803540230"},
  "111315553": {"nome": "PERFECT S. ORIGINAL SHAMPOO 200ml", "marca": "mise","codigo_produto": "8809803548496"},
  "111315735": {"nome": "PERFECT S. ORIGINAL SHAMPOO 530ml", "marca": "mise","codigo_produto": "8809803540353"},
  "111315547": {"nome": "PERFECT S. ORIGINAL SHAMPOO 680ml", "marca": "mise","codigo_produto": "8809803548472"},
  "111315554": {"nome": "PERFECT S. ORIGINAL SHAMPOO 900ml", "marca": "mise","codigo_produto": "8809803548489"},

"111315576": {"nome": "Serum watery 110ml", "marca": "mise","codigo_produto": "00000000000"},




  "111315563": {"nome": "PERFECT S. ROSE SERUM 80ml", "marca": "mise","codigo_produto": "8809803556217"},
  "111315561": {"nome": "PERFECT S. SERUM SUPER RICH 80ml", "marca": "mise","codigo_produto": "8809803556194"},
  "111315738": {"nome": "PERFECT S. STYLING CONDI 530ml", "marca": "mise","codigo_produto": "8809803540322"},
  "111315550": {"nome": "PERFECT S. STYLING CONDI 680ml", "marca": "mise","codigo_produto": "8809803556118"},
  "111315562": {"nome": "PERFECT S. STYLING SERUM 80ml", "marca": "mise","codigo_produto": "8809803556200"},
  "111315737": {"nome": "PERFECT S. STYLING SHAMPOO 530ml", "marca": "mise","codigo_produto": "8809803540339"},
  "111315549": {"nome": "PERFECT S. STYLING SHAMPOO 680ml", "marca": "mise","codigo_produto": "8809803556101"},
  "111315575": {"nome": "PERFECT S. WATERY SERUM 80ml", "marca": "mise","codigo_produto": "8809803556255"},
  "111316081": {"nome": "ROYAL JELLY PROTEIN CONDI TREATMENT 1000ml", "marca": "mise","codigo_produto": "8809803586481"},
  "111316080": {"nome": "ROYAL JELLY PROTEIN SHAMPOO 1000ml", "marca": "mise","codigo_produto": "8809803586474"},
  "111316295": {"nome": "SALON 10 DAMAGED HAIR 250ml", "marca": "mise","codigo_produto": "8809685832560" },
  "111316215": {"nome": "SALON 10 DAMAGED HAIR 250ml", "marca": "mise","codigo_produto": "8809925152816"},
  "111316297": {"nome": "SALON 10  DAMAGED HAIR 990ml", "marca": "mise","codigo_produto": "8809685797050"},
  "111316296": {"nome": "SALON 10  EXTREMELY DAMAGED HAIR 250ml", "marca": "mise","codigo_produto": "8809685832577"},
  "111316056": {"nome": "SALON 10  EXTREMELY DAMAGED HAIR 250ml", "marca": "mise","codigo_produto": "8809925152816"  },
  "111316298": {"nome": "SALON 10 EXTREMELY DAMAGED HAIR 990ml", "marca": "mise","codigo_produto": "8809685797227"},
  "111316215": {"nome": "SALON 10 DAMAGE HAIR 500ml", "marca": "mise","codigo_produto": "8809685815594"},
  "111316264": {"nome": "SALON 10 NO-WASH AMPOULE CONDI TREATMENT 200ml", "marca": "mise","codigo_produto": "8809803573511"},
  "111316216": {"nome": "SALON 10 SHAMPOO FOR EXTREMELY DAMAGED HAIR 500ml", "marca": "mise","codigo_produto": "8809685815600"},
  "111315788": {"nome": "STYLE CARE P.STRONG HOLD HAIR GEL 500ml", "marca": "mise","codigo_produto": "8801042963825"},
  "111316410": {"nome": "Perfect Serum Original Kit 110ml + 30ml", "marca": "mise","codigo_produto": "8809925175082"},
  "111316411": {"nome": "Perfect Serum Styling Kit 110ml + 30ml", "marca": "mise","codigo_produto": "8809925175099"},
  "111316405": {"nome": "Perfect Serum Super Rich Kit 110ml + 30ml", "marca": "mise","codigo_produto": "8809925172708"},
  "111316406": {"nome": "Perfect Serum Watery Kit 110ml + 30ml", "marca": "mise","codigo_produto": "8809925173910"},

"KD1100": {"nome": "MES PERFECTS. serum original 110ml", "marca": "mise","codigo_produto": "00000000"},
"111315566 110ml": {"nome": "MES PERFECTS. serum styling 110ml", "marca": "mise","codigo_produto": "00000000"},



  "111316308": {"nome": "Salon 10 Professional Cica Protein Mask 215ml", "marca": "mise","codigo_produto": "8809925152809"},
  "111316171": {"nome": "MES PERFECT S. ORIGINAL SERUM 30ML", "marca": "mise","codigo_produto": "8809803574921"},
  "111316351": {"nome": "Magic Straight Shampoo 530m", "marca": "mise","codigo_produto": "8809925164741"},
  "111316352": {"nome": "Magic Straight Tratamento 230ml", "marca": "mise","codigo_produto": "8809925167483"},
  "111316353": {"nome": "Magic Straight Sérum 80ml", "marca": "mise","codigo_produto": "8809925167490"},
  "111316359": {"nome": "SÉRUM CREAM 80ML", "marca": "mise","codigo_produto": "8809925167810"         },
  "25839-0": {"nome": "Dark Oil Condicionador 1000ml", "marca": "sebastian","codigo_produto": "4064666102375"},
  "25840-0": {"nome": "Dark Oil Máscara Capilar 500ml", "marca": "sebastian","codigo_produto": "4064666102382"},
  "26500-0": {"nome": "Dark Oil Silkening Fragrância Spray 200ml", "marca": "sebastian","codigo_produto": "4064666314426"},
  "26490-0": {"nome": "Dark Oil Óleo Capilar 30ml", "marca": "sebastian","codigo_produto": "7898973417054"},
  "24608-0": {"nome": "Dark Oil Óleo Capilar 95ml", "marca": "sebastian","codigo_produto": "7898973417023"},
  "24889-0": {"nome": "Flaunt Trilliant Protetor Térmico Trifásico 150ml", "marca": "sebastian","codigo_produto": "8005610569574"},
  "25328-0": {"nome": "No Breaker Leave-in 100ml", "marca": "sebastian","codigo_produto": "4064666214467"},
  "24890-0": {"nome": "Novo Shine Define Finalizador 200ml", "marca": "sebastian","codigo_produto": "4064666225494"},
  "24781-0": {"nome": "Penetraitt Masque - Tratamento 150ml", "marca": "sebastian","codigo_produto": "4064666317380"},
  "26050-0": {"nome": "Potion 9 Lite Spray Líquido 150ml", "marca": "sebastian","codigo_produto": "4064666225272"},
  "24165-2": {"nome": "Sublimate Creme Invisível Modelador 100ml", "marca": "sebastian","codigo_produto": "8005610580838"},
  "26392-0": {"nome": "Trilliance Condicionador 250ml", "marca": "sebastian","codigo_produto": "4064666307015"},
  "23489-3": {"nome": "Twisted Curl Elastic Detangler Condicionador 250ml", "marca": "sebastian","codigo_produto": "8005610426648" },
  "111414201": {"nome": "Damage Care & Nourishing Floral Powdery - Shampoo 180ml", "marca": "ryo","codigo_produto": "8809925154216"},
  "111413638": {"nome": "Hair Loss Expert Care 9EX - Oily Scalp Shampoo 400ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111413647": {"nome": "Root Strength Mk 330ml Couro Cabeludo Oleoso", "marca": "ryo","codigo_produto": "9988776655"},
  "111413667": {"nome": "Damage Care & Nourishing CD Treatment 180ml", "marca": "ryo","codigo_produto": "8801042690608"},
  "111414132": {"nome": "Deep Cleansing e Cooling Citrus Herbal Scent Shampoo 480ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111413649": {"nome": "Hair Loss Expert Care Treat Deep Nutrition Conditioner 330ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111413647": {"nome": "Hair Loss Expert Care Treat Root Strength Conditioner 330ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111413639": {"nome": "Hair Loss Expert Care 9EX Dry Scalp Shampoo 400ml", "marca": "ryo","codigo_produto": "8806403162817"},
  "111413638": {"nome": "Hair Loss Expert Care 9EX Oily Scalp Shampoo 400ml", "marca": "ryo","codigo_produto": "8806403117534"},
  "111414078": {"nome": "RootGen For Men Hair Loss Shampoo 353ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111414079": {"nome": "RootGen For Women Hair Loss Conditioner Treatment 353ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111413977": {"nome": "RootGen Hair Loss Care Scalp Essence 80ml", "marca": "ryo","codigo_produto": "8809803572804"},
  "111414077": {"nome": "RootGen Hair Loss Shampoo Women 353ml", "marca": "ryo","codigo_produto": "9988776655"},
  "111414131": {"nome": "Damage Care & Nourishing Treat Floral Powdery - Mask 300ml", "marca": "ryo","codigo_produto": "8809803590259"},
  "111414252": {"nome": "Red Ginseng Hair Nutrition Shampoo 820ml", "marca": "ryo","codigo_produto": "8809925193666"},
  "111414253": {"nome": "Red Ginsens Hair Nutrition Cd Treatment 820ml", "marca": "ryo","codigo_produto": "8809925193536"},
  "111414260": {"nome": "Damage Care & Nourishing Treat Floral Powdery - Mask 300ml", "marca": "ryo","codigo_produto": "8809803590259"},
  "111414135": {"nome": "Damage Care & Nourishing - Floral Powdery Shamp 480ml", "marca": "ryo","codigo_produto": "8809803590297"},
  "111414251": {"nome": "Black Bean Hair Root Nutririon Shampoo 820ml", "marca": "ryo","codigo_produto": "8809925193659"   },
  "E4031400": {"nome": "Acidic Bonding Concentrate - 5-min Liquid Mask 250ml", "marca": "redken","codigo_produto": "3474637152000"},
  "E3845200": {"nome": "Acidic Bonding Concentrate - Condicionador 1L", "marca": "redken","codigo_produto": "3474637089702"},
  "E3845400": {"nome": "Acidic Bonding Concentrate - Condicionador 300ml", "marca": "redken","codigo_produto": "0884486456311"},
  "P2356100": {"nome": "Acidic Bonding Concentrate - Intensive Treat Pré-Shampoo 150ml", "marca": "redken","codigo_produto": "0884486493866"},
  "E3861900": {"nome": "Acidic Bonding Concentrate - Leave-in 150ml", "marca": "redken","codigo_produto": "0884486456380"},
  "E3845300": {"nome": "Acidic Bonding Concentrate - Shampoo 1L", "marca": "redken","codigo_produto": "3474637089719"},
  "E3845500": {"nome": "Acidic Bonding Concentrate - Shampoo 300ml", "marca": "redken","codigo_produto": "0884486456281"},
  "E4068200": {"nome": "Acidic Color Gloss - Condicionador 300ml", "marca": "redken","codigo_produto": "3474637173463"},
  "E4069500": {"nome": "Acidic Color Gloss - Leave-in 190ml", "marca": "redken","codigo_produto": "3474637174170"},
  "E4068500": {"nome": "Acidic Color Gloss - Shampoo 300ml", "marca": "redken","codigo_produto": "3474637173494"},
  "P2567800": {"nome": "Acidic Color Gloss - Tratamento 237ml", "marca": "redken","codigo_produto": "0884486516732"},
  "P1997303": {"nome": "All Soft - Argan Oil 111ml", "marca": "redken","codigo_produto": "0884486452993"},
  "H2273502": {"nome": "All Soft - Condicionador 1L", "marca": "redken","codigo_produto": "7899706170956"},
  "E3458400": {"nome": "All Soft - Condicionador 300ml", "marca": "redken","codigo_produto": "3474636919970"},
  "H2499301": {"nome": "All Soft - Heavy Cream Máscara 250ml", "marca": "redken","codigo_produto": "7899706192873"},
  "H2398002": {"nome": "All Soft - Heavy Cream Máscara 500ml", "marca": "redken","codigo_produto": "7899706181631"},
  "E3930201": {"nome": "All Soft - Moisture Restore Leave-in 150ml", "marca": "redken","codigo_produto": "3474637124823"},
  "E3458501": {"nome": "All Soft - Shampoo 300ml", "marca": "redken","codigo_produto": "3474636919987"},
  "E3458301": {"nome": "All Soft - Shampoo 1L", "marca": "redken","codigo_produto": "3474636919963"},
  "E3996200": {"nome": "All Soft Mega Curls - Condicionador 1L", "marca": "redken","codigo_produto": "3474637135645"},
  "E3996400": {"nome": "All Soft Mega Curls - Shampoo 1L", "marca": "redken","codigo_produto": "3474637135669"},
  "E3996500": {"nome": "All Soft Mega Curls - Shampoo 300ml", "marca": "redken","codigo_produto": "93474637135676"},
  "P1444403": {"nome": "Brews Maneuver - Cream Pomade 100ml", "marca": "redken","codigo_produto": "0884486341518"},
  "P2390000": {"nome": "Brews Pliable Paste - Jar 150ml", "marca": "redken","codigo_produto": "0884486497895"},
  "E3861600": {"nome": "Extreme - Anti-Snap 250ml", "marca": "redken","codigo_produto": "0884486453402"},
  "P2001800": {"nome": "Extreme - Cat 250ml", "marca": "redken","codigo_produto": "0884486453419"},
  "E3460400": {"nome": "Extreme - Condicionador 1L", "marca": "redken","codigo_produto": "3474636920174"},
  "E3460600": {"nome": "Extreme - Condicionador 300ml", "marca": "redken","codigo_produto": "3474636920198"},
  "E3557900": {"nome": "Extreme - Máscara 250ml", "marca": "redken","codigo_produto": "3474636971053"},
  "H2499101": {"nome": "Extreme - Máscara 500ml", "marca": "redken","codigo_produto": "7899706192859"},
  "E3994301": {"nome": "Extreme - Play Safe 250ml", "marca": "redken","codigo_produto": "3474637134693"},
  "E3460501": {"nome": "Extreme - Shampoo 1L", "marca": "redken","codigo_produto": "3474636920181"},
  "E3460701": {"nome": "Extreme - Shampoo 300ml", "marca": "redken","codigo_produto": "3474636920204"},
  "E3869400": {"nome": "Extreme Length - Máscara 250ml", "marca": "redken","codigo_produto": "3474637105662"},
  "E3461600": {"nome": "Frizz Dismiss - Condicionador 300ml", "marca": "redken","codigo_produto": "3474636920297"},
  "E3531500": {"nome": "Frizz Dismiss - Máscara 250ml", "marca": "redken","codigo_produto": "3474636961047"},
  "P2122000": {"nome": "Acidic Bonding Concentrate - PH Sealer 250ml", "marca": "redken","codigo_produto": "0884486464088"},
  "E3531400": {"nome": "Frizz Dismiss - Rebel Tame 250ml", "marca": "redken","codigo_produto": "3474636961030"},
  "E3461100": {"nome": "Frizz Dismiss - Sulfate-Free Shampoo 300ml", "marca": "redken","codigo_produto": "3474636920242"},
  "E3862300": {"nome": "One United Elixir - Leave-in 150ml", "marca": "redken","codigo_produto": "3474637102555"},
  "P1056403": {"nome": "One United Elixir - Leave-in 400ml", "marca": "redken","codigo_produto": "0884486219336"},
  "E4195600": {"nome": "Acidic Bonding Concentrate - 24/7 Night & Day Serum 100ml", "marca": "redken","codigo_produto": "884486532879"},


  "2735182": {"nome": "Balance - Shampoo 280ml", "marca": "Senscience", "codigo_produto": "7702029639447"},
  "2734948": {"nome": "Balance - Condicionador 1000ml", "marca": "Senscience","codigo_produto": "7702045118810"},
  "2735509": {"nome": "Balance - Condicionador 240ml", "marca": "Senscience","codigo_produto": "7702045664867"},
  "2856018": {"nome": "Detangler Moisturizing - Leave-in Spray 200ml", "marca": "Senscience","codigo_produto": "7702029918887"},
  "2735929": {"nome": "Inner Restore - Máscara Hidratante 200ml", "marca": "Senscience","codigo_produto": "7702045762938 "},
  "2735536": {"nome": "Inner Restore Intensif - Máscara 500ml", "marca": "Senscience","codigo_produto": "7702045169843 "},
  "2733023": {"nome": "Inner Restore Intensif - Máscara 50ml", "marca": "Senscience","codigo_produto": "7702029471450"},
  "2787510": {"nome": "Inner Restore Intensif - Máscara de Tratamento 150ml", "marca": "Senscience","codigo_produto": "7702045437119 "},
  "466162": {"nome": "Inner Restore Moisturizing - Mask 500ml", "marca": "Senscience","codigo_produto": "7702045446616"},
  "2732972": {"nome": "Inner Restore Moisturizing - Máscara de Hidratação 50ml", "marca": "Senscience","codigo_produto": "7702029791602"},
  "2746956": {"nome": "Renewal - Shampoo 280ml", "marca": "Senscience","codigo_produto": "7702045668933"},
  "2735401": {"nome": "Silk Moisture - Condicionador 240ml", "marca": "Senscience","codigo_produto": "7702045286298"},
  "2734946": {"nome": "Silk Moisture - Shampoo 1000ml", "marca": "Senscience","codigo_produto": "7702029552982"},
  "2734977": {"nome": "Silk Moisture - Shampoo 280ml", "marca": "Senscience","codigo_produto": "7702045303506"},
  "2736443": {"nome": "Silk Moisture Mini - Condicionador 90ml", "marca": "Senscience","codigo_produto": "7702045247756"},
  "2736439": {"nome": "Silk Moisture Mini - Shampoo 90ml", "marca": "Senscience","codigo_produto": "7702045375602"},
  "2735508": {"nome": "Smooth - Condicionador 240ml", "marca": "Senscience","codigo_produto": "7702029407503"},
  "2734943": {"nome": "Smooth - Shampoo 1000ml", "marca": "Senscience","codigo_produto": "7702045340785"},
  "2735184": {"nome": "Specialty - Shampoo 280ml", "marca": "Senscience","codigo_produto": "7702029200753"},
  "2735510": {"nome": "True Hue - Condicionador 240ml", "marca": "Senscience","codigo_produto": "7702029947313"},
  "2735183": {"nome": "True Hue - Shampoo 280ml", "marca": "Senscience","codigo_produto": "7702029629967"},
  "2736015": {"nome": "True Hue Color Protecting - Treatment 55ml", "marca": "Senscience","codigo_produto": "7702045490732"},
  "2735511": {"nome": "True Hue Violet - Condicionador 240ml", "marca": "Senscience","codigo_produto": "7702029597396"},
  "2735185": {"nome": "True Hue Violet - Shampoo 280ml", "marca": "Senscience","codigo_produto": "7702029953444"},
  "498297": {"nome": "Silk Moisture Travel Size - Shampoo + Condic 90ml + Inner Restore Intensif Máscara 50ml", "marca": "senscience","codigo_produto": "7899522324311" },
  "26205-0": {"nome": "Elements Calming Shampoo 250ml", "marca": "wella","codigo_produto": "4064666035628"},
  "24586-0": {"nome": "Fusion Máscara Reconstrutora 150ml", "marca": "wella","codigo_produto": "7896235353737"},
  "26419-0": {"nome": "Fusion Shampoo 1000ml", "marca": "wella","codigo_produto": "064666318233"},
  "24593-0": {"nome": "Invigo Blonde Recharge Shampoo Desamarelador 250ml", "marca": "wella","codigo_produto": "7896235353805"},
  "24634-0": {"nome": "Invigo Color Brilliance Condicionador 200ml", "marca": "wella","codigo_produto": "7896235353850"},
  "24578-0": {"nome": "Invigo Color Brilliance Máscara Capilar 500ml", "marca": "wella","codigo_produto": "7896235353652"},
  "26228-0": {"nome": "Invigo Color Brilliance Shampoo 1000ml", "marca": "wella","codigo_produto": "4064666318356"},
  "24635-0": {"nome": "Invigo Nutri-Enrich Condicionador 200ml", "marca": "wella","codigo_produto": "7896235353867"},
  "24583-0": {"nome": "Invigo Nutri-Enrich Máscara de Nutrição 500ml", "marca": "wella","codigo_produto": "7896235353706"},
  "26230-0": {"nome": "Invigo Nutri-Enrich Shampoo 1000ml", "marca": "wella","codigo_produto": "4064666435459"},
  "25877-0": {"nome": "Invigo Sun Condicionador 200ml", "marca": "wella","codigo_produto": "4064666041650"},
  "24919-0": {"nome": "Invigo Sun Shampoo 250ml", "marca": "wella","codigo_produto": "3614226745880"},
  "25398-0": {"nome": "NutriCurls Shampoo Micellar 250ml", "marca": "wella","codigo_produto": "3614228865647"},

"99350182189-0": {"nome": "ultimate repair night serum 30ml", "marca": "wella","codigo_produto": "000000000"},



  "26390-0": {"nome": "Oil Reflections Light 100ml", "marca": "wella","codigo_produto": "7898973417047"},
  "24637-0": {"nome": "Oil Reflections Luminous Instant Condicionador 200ml", "marca": "wella","codigo_produto": "7896235353881"},
  "24590-0": {"nome": "Oil Reflections Luminous Reboost Máscara Capilar 500ml", "marca": "wella","codigo_produto": "7896235353775"},
  "24591-0": {"nome": "wella Professionals Oil Reflections - Máscara Capilar 150ml", "marca": "wella","codigo_produto": "7896235353782"},
  "99350105838-0": {"nome": "Oil Reflections Luminous Reveal Shampoo 1000ml", "marca": "wella","codigo_produto": "8005610531632"},
  "26227-0": {"nome": "Oil Reflections Reflective Light Óleo Capilar 30ml", "marca": "wella","codigo_produto": "7898973417009"},
  "26389-0": {"nome": "Oil Reflections Óleo Capilar 100ml", "marca": "wella","codigo_produto": "7898973417030"},
  "26226-0": {"nome": "Oil Reflections Óleo Capilar 30ml", "marca": "wella","codigo_produto": "4064666306148"},
  "27192-0": {"nome": "Ultimate Repair Miracle Hair Rescue Tratamento Leave-in 30ml", "marca": "wella","codigo_produto": "40646666337104"},
  "27191-0": {"nome": "Ultimate Repair Condicionador 500ml", "marca": "wella","codigo_produto": "4064666337043"},
  "27193-0": {"nome": "Ultimate Repair Miracle Hair Rescue Leave-in 95ml", "marca": "wella","codigo_produto": "4064666337111"},
  "27612-0": {"nome": "Ultimate Repair Máscara 150ml", "marca": "wella","codigo_produto": "4064666337074"},
  "27613-0": {"nome": "Ultimate Repair Máscara 500ml", "marca": "wella","codigo_produto": "4064666337081"},
  "27194-0": {"nome": "Ultimate Repair Protetor Térmico 140ml", "marca": "wella","codigo_produto": "4064666337128"},
  "27188-0": {"nome": "Ultimate Repair Shampoo 1000ml", "marca": "wella","codigo_produto": "4064666337128"},
  "27187-0": {"nome": "Ultimate Repair Shampoo 250ml", "marca": "wella","codigo_produto": "4064666337029"},
  "26850-0": {"nome": "Fusion - Máscara Reconstrutora 500ml", "marca": "wella Professionals","codigo_produto": "7896235353744"},
  "24146-1": {"nome": "EIMI Absolute Set Spray Fixador 300ml", "marca": "wella","codigo_produto": "8005610563244"},
  "23799-1": {"nome": "EIMI Body Crafter Spray de Volume 150ml", "marca": "wella","codigo_produto": "8005610589572"},
  "23384-1": {"nome": "EIMI Bold Move Pasta Modeladora 150ml", "marca": "wella","codigo_produto": "8005610576206"},
  "24765-0": {"nome": "EIMI Glam Mist Spray de Brilho 200ml", "marca": "wella","codigo_produto": "3614227276444"},
  "23800-1": {"nome": "EIMI Mistify Me Strong Spray Fixador 500ml", "marca": "wella","codigo_produto": "8005610640327"},
  "24172-1": {"nome": "EIMI Perfect Me Leave-in 100ml", "marca": "wella","codigo_produto": "8005610587509"},
  "23470-2": {"nome": "EIMI Sugar Lift Spray Texturizador 150ml", "marca": "wella","codigo_produto": "8005610589626"},
  "26004-0": {"nome": "SP Luxe Oil Óleo Capilar 100ml", "marca": "wella","codigo_produto": "4064666306162"},
  "99350174902-0": {"nome": "Ultimate Luxe Oil Óleo 30ml", "marca": "wella","codigo_produto": "4064666594224"},
  "99350174903-0": {"nome": "Ultimate Luxe Oil Óleo 100ml", "marca": "wella","codigo_produto": "7898973417078"},
  "99350174375-0": {"nome": "Ultimate Luxe Oil Shampoo 1L", "marca": "wella","codigo_produto": "4064666593562"},
  "99350174379-0": {"nome": "Ultimate Luxe Oil Máscara 150ml", "marca": "wella","codigo_produto": "4064666593609"},
  "99350174380-0": {"nome": "Ultimate Luxe Oil Máscara 500ml", "marca": "wella","codigo_produto": "4064666593616"},
  "99350174381-0": {"nome": "Ultimate Luxe Oil Shampoo 250ml", "marca": "wella","codigo_produto": "4064666593623"},
"69993370": {"nome": "Q-Tips - Hastes de Algodão - Kit de Viagem 30un", "marca": "wella","codigo_produto": "305210221277"},
"64360310": {"nome": "Q-Tips - Hastes de Algodão com Pontas de Precisão - Kit de Viagem 30un", "marca": "wella","codigo_produto": "305210047693"},
"99350161119-0": {"nome": "Marula Oil Blender Primer - Óleo Protetor Capilar 150ml", "marca": "wella","codigo_produto": "4064666035376"},
  "20423-0": {"nome": "Color Touch Pure Naturals 2/0 Preto - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019255"},
  "20424-0": {"nome": "Color Touch Pure Naturals 3/0 Castanho Escuro - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019279"},
  "20425-0": {"nome": "Color Touch Pure Naturals 4/0 Castanho Médio - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019286"},
  "20426-0": {"nome": "Color Touch Pure Naturals 5/0 Castanho Claro - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019309"},
  "20427-0": {"nome": "Color Touch Pure Naturals 6/0 Louro Escuro - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019323"},
  "20428-0": {"nome": "Color Touch Pure Naturals 7/0 Louro Médio - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019330"},
  "20429-0": {"nome": "Color Touch Pure Naturals 8/0 Louro Claro - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019347"},
  "20460-0": {"nome": "Color Touch 1,9% - Emulsão Reveladora 6 Volumes 1000ml", "marca": "sac","codigo_produto": "7891182019866"},
  "20380-0": {"nome": "Color Touch 5/1 Castanho Claro Acinzentado - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182018685"},
  "20381-0": {"nome": "Color Touch 5/3 - Castanho Claro Dourado 60g", "marca": "sac","codigo_produto": "7891182018760"},
  "20407-0": {"nome": "Color Touch 6/77 Louro Escuro Marrom Intenso - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182019064"},
  "20386-0": {"nome": "Color Touch 7/89 Louro Médio Pérola Cendré - Tonalizante 60g", "marca": "sac","codigo_produto": "7891182018845"},
 "27255-0-2": {"nome": "BlondorPlex N°1 Pó Descolorante 800g", "marca": "sac", "codigo_produto": "4064666212579"},
  "99350169161-0": {"nome": "Color Motion+ Máscara 150ml", "marca": "sac", "codigo_produto": "4064666316147"},
  "25154-0": {"nome": "Color Motion+ Máscara 500ml", "marca": "sac","codigo_produto": "3614226750723"},
  "25153-0": {"nome": "Color Motion+ Shampoo 1000ml", "marca": "sac","codigo_produto": "4064666318165"},
  "25152-1": {"nome": "Color Motion+ Shampoo 250ml", "marca": "sac","codigo_produto": "4064666316109"},
  "20305-0": {"nome": "Color Perfect 3/0 Castanho Escuro - Coloração Permanente 60g", "marca": "sac","codigo_produto": "7891182017398"},
  "20365-0": {"nome": "Color Perfect 8/3 Louro Claro Dourado - Coloração Permanente 60ml", "marca": "sac","codigo_produto": "7891182018265"},
  "20307-0": {"nome": "Color Perfect Pure Naturals 5/0 Castanho Claro - Coloração Permanente 60ml", "marca": "sac","codigo_produto": "7891182017411"},
  "20310-0": {"nome": "Color Perfect Pure Naturals 6/0 Louro Escuro - Coloração Permanente 60ml", "marca": "sac","codigo_produto": "7891182017442"},
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

    "G-7908195709933": {"nome": "Girassol Pink By Kern - Sérum Noturno - Esmalte 9ml", "marca": "sac"}
}
produtos_cadastrados = {codigo: produto for codigo, produto in lista_produtos.items()}

# Mapeamento de cores para ICE, KERASYS, TSUBAKI e BANILA
produto_color_mapping = {
    # TSUBAKI
    "10170558202": "#daa520",
    "10170636202": "#faeba9",
    "10170634202": "#faeba9",
    "10170632202": "#ff0000",
    "10170630202": "#ff0000",

    # ICE
    "50277E_5": "#faeba9", "51007E_5": "#faeba9", "03846BR": "#faeba9",
    "39937E_5": "#faeba9", "51045E_5": "#faeba9", "51052E_5": "#faeba9",
    "39920E_5": "#faeba9", "50260E_5": "#faeba9", "51014E_5": "#faeba9",
    "51038E_5": "#faeba9", "51076E_5": "#ecc7cc", "50291E_5": "#ecc7cc",
    "03839BR": "#ecc7cc", "39951E_5": "#ecc7cc", "51083E_5": "#ecc7cc",
    "39944E_5": "#ecc7cc", "50284E_5": "#ecc7cc", "51090E_5": "#ecc7cc",

    # SENKA
    "10170578202": "#ffffff", "5D267": "#ffffff", "10170584202": "#0190cb",
    "10170573202": "#0190cb", "10170577202": "#0190cb", "10170581202": "#dc9fac",
    "10170583202": "#dc9fac", "10170766201": "#27a584", "10170588202": "#acc674",

     # CAROL
    "PA321": "#7CFC00", "PA320": "#7CFC00", "PA322": "#7CFC00", "PA319": "#7CFC00",
    "PA352": "#CD853F", "PA350": "#CD853F", "PA349": "#CD853F", "PA351": "#CD853F", "PA353": "#CD853F", "PA323": "#CD853F",
    "PA443": "#A020F0", "PA441": "#A020F0", "PA442": "#A020F0", 
    "PA526": "#00BFFF", "PA523": "#00BFFF", "PA525": "#00BFFF",
    "PA527": "#FF1493", "KIWIMASC1": "#FFB6C1",

     # BEDHEAD
    "10170578202": "#ffffff", "5D267": "#ffffff", "10170584202": "#0190cb",
    "10170573202": "#0190cb", "10170577202": "#0190cb", "10170581202": "#dc9fac",
    "10170583202": "#dc9fac", "10170766201": "#27a584", "10170588202": "#acc674",
    "300499": "#A020F0", "300565": "#A020F0", "330499": "#A020F0", "330565": "#A020F0","330501": "#A020F0","300503": "#4B0082",
     "300557": "#FFA07A", "330557": "#FFA07A", "330555": "#FFA07A", "300555": "#FFA07A",
    "330558": "#FF1493", "300558": "#FF1493", "300556": "#FF1493", "330556": "#FF1493",
    "300522": "#FF0000", "300524": "#FF0000", "300563": "#FF0000", "300526": "#FF0000",
    "330522": "#FF0000", "330524": "#FF0000", "330563": "#FF0000", "330526": "#FF0000",
    "300516": "#00BFFF", "300516-1": "#00BFFF", "330532": "#0000FF",
    "BH - Recovery Sh 600": "#00BFFF", "300520": "#00BFFF", "300562": "#00BFFF", "300518": "#00BFFF",
    "330520": "#00BFFF", "330562": "#00BFFF", "330518": "#00BFFF", "330516": "#00BFFF",


   # KERASYS
    "6134467": "#00FA9A", "6134473": "#00FA9A", "6134479": "#FFDEAD",
    "6134464": "#FFDEAD", "6134472": "#00BFFF", "6134466": "#00BFFF",
    "6134465": "#FF69B4", "6134471": "#FF69B4", "6100529": "#FF69B4",
    "6066191": "#FF1493", "6066189": "#FF1493", "6066716": "#FF1493",
    "6066192": "#FF1493", "6066712": "#FF1493", "6066188": "#FF1493",
    "6066183": "#0000FF", "6066186": "#0000FF", "6066715": "#0000FF",
    "6066185": "#0000FF", "6066711": "#0000FF", "6066182": "#0000FF",
    "5019487": "#DAA520", "6093517": "#DAA520", "6100527": "#DAA520",
    "6100531": "#DAA520",
    "6093519": "#0000FF", "6100528": "#0000FF", "6100534": "#0000FF",
    "6100679": "#0000FF",
    "6098970": "#FFA500", "6098971": "#FFA500",
    "6098972": "#0000CD", "6098969": "#0000CD",
    "6101625": "#00CED1", "6101580": "#00CED1"

}

# Funções de callback para remoção e restauração
def remove_sku(sku):
    """Remove o SKU da lista ativa"""
    ativos = st.session_state.ativos
    if sku in ativos:
        ativos.remove(sku)

# Inicializa variáveis na sessão básicas
for var in ["contagem", "pedidos_bipados", "input_codigo", "nao_encontrados", "uploaded_files"]:
    if var not in st.session_state:
        st.session_state[var] = [] if var != "input_codigo" else ""

#################################
# Página de Resultados
#################################
params = st.query_params
if "resultado" in params:
    st.title("Resumo do Pedido - Organizado")
    st.markdown("---")

    # Agrupa os pedidos por marca
    agrupado_por_marca = {}
    for codigo, valores in params.items():
        if codigo == "resultado":
            continue
        quantidade = valores[0] if valores else "0"
        produto = produtos_cadastrados.get(codigo)
        if produto:
            marca = produto["marca"].lower().strip()
            agrupado_por_marca.setdefault(marca, []).append({
                "sku": codigo,
                "nome": produto["nome"],
                "quantidade": quantidade,
                "codigo_produto": produto.get("codigo_produto", "")
            })

    # 1) Inicializa sessão de SKUs ativos para remoção
    if "ativos" not in st.session_state:
        st.session_state.ativos = [item["sku"] for sub in agrupado_por_marca.values() for item in sub]

    # 2) Cabeçalho e botão de restaurar com callback
    st.markdown("## Resultados")
    st.button(
        "♻️ Restaurar todos",
        on_click=lambda: st.session_state.ativos.clear() or st.session_state.ativos.extend(
            [item["sku"] for sub in agrupado_por_marca.values() for item in sub]
        )
    )

    # 3) Define grupos de corredores (omitido para brevidade)
    grupos = [
    ("Corredor 1", ["kerastase", "fino", "redken", "senscience", "loreal", "carol"]),
    ("Corredor 2", ["kerasys", "mise", "ryo", "ice", "image"]),
    ("Corredor 3", ["tsubaki", "wella", "senka", "sebastian", "bedhead", "lee", "banila", "alfapart"]),
    ("Pinceis", ["real", "ecootols"]),
    ("Dr.purederm", ["dr.pawpaw", "dr.purederm"]),
    ("senka", ["senka"]),
    ("Sac", ["sac"])
]
    grupos_filtrados = [(t, m) for t, m in grupos if any(marca in agrupado_por_marca for marca in m)]
    grupos_filtrados = [(t, m) for t, m in grupos if any(marca.lower().strip() in agrupado_por_marca for marca in m)]

    abas = st.tabs([titulo for titulo, _ in grupos_filtrados])

    # 4) Exibição interativa dentro das abas
    for (titulo, marcas), aba in zip(grupos_filtrados, abas):
        with aba:
            st.header(titulo)
            for marca in marcas:
                if marca not in agrupado_por_marca:
                    continue

                # Logo da marca
                try:
                    caminho = os.path.join(CAMINHO_LOGOS, f"{marca}.png")
                    with open(caminho, "rb") as f:
                        logo = base64.b64encode(f.read()).decode()
                    st.markdown(
                        f"<img src='data:image/png;base64,{logo}' width='100'>",
                        unsafe_allow_html=True
                    )
                except FileNotFoundError:
                    st.write(marca.upper())

                # Listagem com botão de remoção (usando callback)
                for prod in agrupado_por_marca[marca]:
                    sku = prod["sku"]
                    if sku not in st.session_state.ativos:
                        continue

                    col1, col2 = st.columns([5, 1])
                    with col1:
                        color = produto_color_mapping.get(sku, "#000")
                        nome_fmt = (
                            f"<span style='color:{color};'>"
                            f"<strong>{prod['nome']}</strong>"
                            f"</span>"
                        )
                        st.markdown(
                            f"{nome_fmt}  \n"
                            f"Código do Produto: **{prod['codigo_produto']}**  \n"
                            f"Quantidade: **{prod['quantidade']}**",
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.button(
                            "❌",
                            key=f"rm_{sku}",
                            on_click=remove_sku,
                            args=(sku,)
                        )
                st.markdown("---")

    # 5) Finaliza para que o Streamlit atualize após callbacks
    st.stop()
#################################
st.title("Bipagem de Produtos")

uploaded_files = st.file_uploader("Envie os CSVs do pedido exportados do Bling:", type=["csv"], accept_multiple_files=True)
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

@st.cache_data(show_spinner=True)
def tentar_ler_csv_cache(file_bytes):
    try:
        df = pd.read_csv(BytesIO(file_bytes), sep=";", dtype=str, encoding="utf-8", on_bad_lines="skip", engine="python")
    except UnicodeDecodeError:
        df = pd.read_csv(BytesIO(file_bytes), sep=";", dtype=str, encoding="latin-1", on_bad_lines="skip", engine="python")
    df.columns = df.columns.str.strip().str.lower()
    return df

def tentar_ler_csv(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    return tentar_ler_csv_cache(file_bytes)

def processar():
    # ─────────── Inicialização segura ───────────
    # Contagem deve ser dict
    if "contagem" not in st.session_state or not isinstance(st.session_state.contagem, dict):
        st.session_state.contagem = {}
    # nao_encontrados deve ser lista
    if "nao_encontrados" not in st.session_state or not isinstance(st.session_state.nao_encontrados, list):
        st.session_state.nao_encontrados = []

    codigos_input = st.session_state.input_codigo.strip()
    if not codigos_input:
        return

    codigos = re.split(r'[\s,]+', codigos_input)
    uploaded_files = st.session_state.get('uploaded_files', [])
    if not uploaded_files:
        st.error("⚠️ Nenhum arquivo CSV carregado!")
        return

    for uploaded_file in uploaded_files:
        df = tentar_ler_csv(uploaded_file)
        if df is None:
            continue
        if "sku" not in df.columns or "número pedido" not in df.columns:
            st.error(f"CSV {uploaded_file.name} inválido. As colunas obrigatórias 'SKU' e 'Número pedido' não foram encontradas.")
            return

        df["sku"] = df["sku"].apply(
            lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip())))
            if "E+" in str(x) else str(x).strip()
        )

        for codigo in codigos:
            pedidos = df[df["número pedido"].astype(str).str.strip() == codigo]
            if not pedidos.empty:
                for sku in pedidos["sku"]:
                    for sku_individual in str(sku).split("+"):
                        sku_individual = sku_individual.strip()
                        if sku_individual in produtos_cadastrados:
                            # aqui contagem é dict, get vai funcionar
                            st.session_state.contagem[sku_individual] = (
                                st.session_state.contagem.get(sku_individual, 0) + 1
                            )
                        else:
                            entrada = f"Pedido {codigo} → SKU: {sku_individual}"
                            if entrada not in st.session_state.nao_encontrados:
                                st.session_state.nao_encontrados.append(entrada)
            else:
                # código direto (sem pedido)
                if codigo in produtos_cadastrados:
                    st.session_state.contagem[codigo] = (
                        st.session_state.contagem.get(codigo, 0) + 1
                    )
                else:
                    entrada = f"Código direto → SKU: {codigo}"
                    if entrada not in st.session_state.nao_encontrados:
                        st.session_state.nao_encontrados.append(entrada)

    # limpa input
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
        unsafe_allow_html=True
    )
except:
    st.markdown("<h2 style='text-align: center;'>EXI</h2>", unsafe_allow_html=True)

st.markdown(
    "<p style='font-weight: bold;'>Digite o(s) código(s) do pedido ou SKU direto:<br>"
    "<small>Exemplo: 12345, 67890 111213</small></p>",
    unsafe_allow_html=True
)
st.text_input("", key="input_codigo", on_change=processar)

if st.session_state.nao_encontrados:
    qtd_nao = len(st.session_state.nao_encontrados)
    # Mensagem de alerta persistente
    st.markdown(
        f"<div style='background-color:#ffcccc; padding:10px; border-radius:5px; color:red; text-align:center;'>"
        f"⚠️ ATENÇÃO: {qtd_nao} pedido(s) não foram lidos!"
        f"</div>",
        unsafe_allow_html=True
    )

    # Expander para visualizar os SKUs não lidos
    titulo_expander = f"<span style='color:red;'>Clique aqui para visualizar os {qtd_nao} pedidos não lidos.</span>"
    with st.expander(titulo_expander, expanded=False):
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
            except:
                st.write(marca.upper())
            for cod, qtd in st.session_state.contagem.items():
                produto = produtos_cadastrados.get(cod)
                if produto and produto["marca"] == marca:
                    st.markdown(
                        f"<p style='margin-top: 0;'><strong>{produto['nome']}</strong> | Quantidade: {qtd}</p>",
                        unsafe_allow_html=True
                    )

if st.session_state.contagem:
    base_url = "https://cogpz234emkoeygixmfemn.streamlit.app/"
    params_dict = {"resultado": "1"}
    for sku, qtd in st.session_state.contagem.items():
        params_dict[sku] = str(qtd)
    query_string = urllib.parse.urlencode(params_dict)
    full_url = f"{base_url}/?{query_string}"

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(full_url)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img_qr.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="QR Code para a Página de Resultados", use_container_width=False)
    st.markdown(f"[Clique aqui para acessar a página de resultados]({full_url})", unsafe_allow_html=True)
else:
    st.info("Nenhum produto bipado ainda!")


