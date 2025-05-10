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
    "🔄 Limpar bipagem",
    key="clear_bipagem",   # ← key fixa única
    on_click=lambda: (
        st.session_state.contagem.clear(),
        st.session_state.nao_encontrados.clear(),
        setattr(st.session_state, "input_codigo", ""),
        setattr(st.session_state, "finalizado", False)
    )
)

# (Se você ainda usar) Finalizar bipagem
st.button(
    "✅ Finalizar bipagem e gerar QR",
    key="finalize_qr",     # ← key fixa única
    on_click=lambda: setattr(st.session_state, "finalizado", True)
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
