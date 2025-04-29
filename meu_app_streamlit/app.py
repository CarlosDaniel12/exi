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
  "6059482-W": {"nome": "Oriental Premium Condicionador 200ml", "marca": "kerasys", "codigo_produto": "8801046876244"}

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

