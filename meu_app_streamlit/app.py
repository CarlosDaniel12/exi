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


