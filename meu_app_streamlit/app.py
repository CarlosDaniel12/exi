import streamlit as st
import pandas as pd
from PIL import Image
import os, base64
from io import BytesIO
import math, re, qrcode, urllib.parse

# Configura layout
st.set_page_config(layout="wide")

# Caminho para as logos (ajuste se necessário)
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
    "493.046-G": {"nome": "All In One Leave-In Multifuncional - Spray de Gatilho 240ml", "marca": "tsubaki"},
    "39852E_5": {"nome": "Keep My Blonde Mask CD 750ml", "marca": "tsubaki"}
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

# ------------ Página de Resultados ------------
# Se a URL contiver o parâmetro 'resultado', exibe a página de resultados.
params = st.query_params  # st.query_params é uma propriedade, sem parênteses!
if "resultado" in params:
    st.title("Resultados dos Produtos Bipados")
    st.markdown("---")
    # Agrupar produtos por marca: para cada marca, os produtos com o mesmo nome terão suas quantidades somadas.
    produtos_por_marca = {}
    for cod, qtd in st.session_state.contagem.items():
        produto = produtos_cadastrados.get(cod)
        if produto:
            marca = produto["marca"]
            nome = produto["nome"]
            if marca not in produtos_por_marca:
                produtos_por_marca[marca] = {}
            # Agrupa por nome do produto
            produtos_por_marca[marca][nome] = produtos_por_marca[marca].get(nome, 0) + qtd

    # Exibe os resultados agrupados por marca
    for marca, produtos in produtos_por_marca.items():
        st.markdown(f"## {marca}")
        # Tenta exibir a logo (convertendo o nome para minúsculas)
        try:
            logo_path = os.path.join(CAMINHO_LOGOS, f"{marca.lower()}.png")
            with open(logo_path, "rb") as img_file:
                logo_encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(f"<img src='data:image/png;base64,{logo_encoded}' width='100'>", unsafe_allow_html=True)
        except Exception as e:
            st.write(f"Logo não encontrada para {marca}")
        for nome, total in produtos.items():
            st.markdown(f"- **{nome}** | Quantidade: {total}")
        st.markdown("---")
    st.markdown("[Voltar à página principal](/)", unsafe_allow_html=True)
    st.stop()

# ------------ Página Principal (Interface de Busca) ------------
st.title("Bipagem de Produtos")

# Upload opcional de arquivos CSV
uploaded_files = st.file_uploader("Envie os CSVs do pedido exportados do Bling:", type=["csv"], accept_multiple_files=True)

# Função para processar os códigos de entrada
def processar():
    codigos_input = st.session_state.input_codigo.strip()
    if not codigos_input:
        return
    codigos = re.split(r'[\s,]+', codigos_input)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file, sep=";", dtype=str)
            # Verifica se a coluna 'SKU' existe
            if "SKU" not in df.columns:
                st.error("Não foi encontrada a coluna 'SKU' no CSV. Colunas disponíveis: " + ", ".join(df.columns))
                return
            df["SKU"] = df["SKU"].apply(lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip()))) if "E+" in str(x) else str(x).strip())
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

# Botão para limpar os pedidos
if st.button("🔄 Limpar pedidos bipados"):
    st.session_state.pedidos_bipados.clear()
    st.session_state.contagem.clear()
    st.session_state.nao_encontrados.clear()

# Exibe o logo principal da EXI
try:
    exi_logo_path = os.path.join(CAMINHO_LOGOS, "exi.png")
    with open(exi_logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded}' width='200'></div>", unsafe_allow_html=True)
except Exception:
    st.markdown("<h2 style='text-align: center;'>EXI</h2>", unsafe_allow_html=True)

# Aba de pesquisa para entrada dos códigos
st.markdown("<p style='font-weight: bold;'>Digite o(s) código(s) do pedido ou SKU direto:<br><small>Exemplo: 12345, 67890 111213</small></p>", unsafe_allow_html=True)
st.text_input("", key="input_codigo", on_change=processar)

# Se houver códigos não encontrados, exibe-os em um expander
if st.session_state.nao_encontrados:
    with st.expander("❗ Códigos não cadastrados no sistema"):
        for entrada in st.session_state.nao_encontrados:
            st.markdown(f"- {entrada}")

# Exibe os produtos bipados agrupados por marca (com a agregação que já fizemos na página de resultados, agora opcional na página principal)
# Aqui podemos listar individualmente, mas se preferir pode retirar essa seção e deixar os resultados apenas na página de resultados.
st.markdown("### Produtos Bipados Agrupados por Marca")
produtos_por_marca = {}
for cod, qtd in st.session_state.contagem.items():
    produto = produtos_cadastrados.get(cod)
    if produto:
        marca = produto["marca"]
        nome = produto["nome"]
        if marca not in produtos_por_marca:
            produtos_por_marca[marca] = {}
        produtos_por_marca[marca][nome] = produtos_por_marca[marca].get(nome, 0) + qtd

for marca, prods in produtos_por_marca.items():
    st.markdown(f"**{marca}**")
    for nome, total in prods.items():
        st.markdown(f"- {nome} | Quantidade: {total}")
    st.markdown("---")

# Geração do QR Code que redireciona para a página de resultados
if st.session_state.contagem:
    # Defina o base_url para a URL pública do seu app (no Streamlit Community Cloud)
    base_url = "https://tdkdeaxrzoguoscmiieqwp.streamlit.app/"  # Substitua pela URL do seu app
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


