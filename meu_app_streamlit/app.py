import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64
from io import BytesIO
import math
import re
import qrcode

# Configura layout
st.set_page_config(layout="wide")

CAMINHO_LOGOS = "C:/meu_app_streamlit/logos"

# Produtos cadastrados
produtos_cadastrados = {
    "2735182": {"nome": "Balance - Shampoo 280ml", "marca": "Senscience"},
    "25154-0": {"nome": "Color Motion+ Máscara 500ml", "marca": "fino"},
    "25839-0": {"nome": "Dark Oil Condicionador 1000ml", "marca": "Sebastian"},
    "111414201": {"nome": "Damage Care & Nourishing Floral Powdery - Shampoo 180ml", "marca": "carol"},
    "E4031400": {"nome": "Acidic Bonding Concentrate - 5-min Liquid Mask 250ml", "marca": "Redken"},
    "111316309": {"nome": "10 Professional Cica Ceramide Oil Serum 60ml", "marca": "sebastian"},
    "H0270321": {"nome": "Oxidante Creme 75ml 20 Vol", "marca": "Ecotools"},
    "H0270322": {"nome": "Oxidante Creme 75ml 20 Vol", "marca": "sac"},

    "6134464": {"nome": "Advanced Keratin Bond Deep Repair Shampoo 600ml", "marca": "purederm"},
    "E4181100": {"nome": "Blond Absolu - L'Huile Cicagloss - Óleo Capilar 75ml (Refil)", "marca": "tsubaki"},
    "493.046-G": {"nome": "All In One Leave-In Multifuncional - Spray de Gatilho 240ml", "marca": "Dr.PawPaw"},
    "39852E_5": {"nome": "Keep My Blonde Mask CD 750ml", "marca": "alfaparf"},
    
    

}

# Marcas
marcas = [
    "kerastase", "kerasys", "mise", "ice", "image", "carol", "redken",
    "banila", "bedhead", "wella", "real", "exi", "fino", "tsubaki", "senscience",
    "sebastian", "sac", "Ecotools", "purederm", "alfaparf", "Dr.PawPaw"
]

# Inicializa sessão
if "contagem" not in st.session_state:
    st.session_state.contagem = {}
if "pedidos_bipados" not in st.session_state:
    st.session_state.pedidos_bipados = []
if "input_codigo" not in st.session_state:
    st.session_state.input_codigo = ""
if "nao_encontrados" not in st.session_state:
    st.session_state.nao_encontrados = []

# Upload dos arquivos CSV
uploaded_files = st.file_uploader("Envie os CSVs do pedido exportados do Bling:", type=["csv"], accept_multiple_files=True)

# Função para processar input dos pedidos
def processar():
    codigos_input = st.session_state.input_codigo.strip()
    if not codigos_input:
        return

    codigos = re.split(r'[\s,]+', codigos_input)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file, sep=";", dtype=str)
            df["SKU"] = df["SKU"].apply(lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip()))) if "E+" in str(x) else str(x).strip())
            for codigo in codigos:
                pedidos = df[df["Número pedido"].astype(str).str.strip() == codigo]
                if not pedidos.empty:
                    for sku in pedidos["SKU"]:
                        skus_separados = str(sku).split("+")
                        for sku_individual in skus_separados:
                            sku_individual = sku_individual.strip()
                            if sku_individual in produtos_cadastrados:
                                st.session_state.contagem[sku_individual] = st.session_state.contagem.get(sku_individual, 0) + 1
                            else:
                                entrada = f"Pedido {codigo} → SKU: {sku_individual}"
                                if entrada not in st.session_state.nao_encontrados:
                                    st.session_state.nao_encontrados.append(entrada)
                else:
                    # Se não encontrar pedido, tenta como SKU direto
                    if codigo in produtos_cadastrados:
                        st.session_state.contagem[codigo] = st.session_state.contagem.get(codigo, 0) + 1
                    else:
                        entrada = f"Código direto → SKU: {codigo}"
                        if entrada not in st.session_state.nao_encontrados:
                            st.session_state.nao_encontrados.append(entrada)
    else:
        # Se não tiver arquivo enviado, tenta usar códigos como SKU
        for codigo in codigos:
            if codigo in produtos_cadastrados:
                st.session_state.contagem[codigo] = st.session_state.contagem.get(codigo, 0) + 1
            else:
                entrada = f"Código direto → SKU: {codigo}"
                if entrada not in st.session_state.nao_encontrados:
                    st.session_state.nao_encontrados.append(entrada)

    st.session_state.input_codigo = ""

# Botão limpar contagem
if st.button("🔄 Limpar pedidos bipados"):
    st.session_state.pedidos_bipados.clear()
    st.session_state.contagem.clear()
    st.session_state.nao_encontrados.clear()

# Exibe logo da EXI
try:
    exi_logo_path = os.path.join(CAMINHO_LOGOS, "exi.png")
    with open(exi_logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{encoded}' width='200'>
            </div>
            """,
            unsafe_allow_html=True,
        )
except Exception:
    st.markdown("<h2 style='text-align: center;'>EXI</h2>", unsafe_allow_html=True)

# Campo de input de códigos
st.markdown("<p style='font-weight: bold;'>Digite o(s) código(s) do pedido ou SKU direto:<br><small>Exemplo: 12345, 67890 111213</small></p>", unsafe_allow_html=True)
st.text_input("", key="input_codigo", on_change=processar)

# Exibe códigos não encontrados
if st.session_state.nao_encontrados:
    with st.expander("❗ Códigos não cadastrados no sistema"):
        for entrada in st.session_state.nao_encontrados:
            st.markdown(f"- {entrada}")

# Exibe logos + produtos bipados
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
                    st.markdown(f"<p style='margin-top: 0;'><strong>{produto['nome']}</strong> | Quantidade: {qtd}</p>", unsafe_allow_html=True)

# ------------------------------
# Função para gerar QR Code automático
# ------------------------------

# Função para gerar texto dos produtos
def gerar_texto_produtos():
    linhas = []
    for cod, qtd in st.session_state.contagem.items():
        produto = produtos_cadastrados.get(cod)
        if produto:
            linhas.append(f"{produto['nome']} - {qtd}x")
    return "\n".join(linhas)

# Função para gerar QR code imagem
def gerar_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

st.markdown("---")

if st.session_state.contagem:
    texto = gerar_texto_produtos()
    img = gerar_qr_code(texto)

    buf = BytesIO()
    img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="QR Code dos Produtos", use_container_width=False)

    st.download_button(
        label="Baixar QR Code",
        data=buf.getvalue(),
        file_name="produtos_qrcode.png",
        mime="image/png"
    )
else:
    st.info("Nenhum produto bipado ainda!")



