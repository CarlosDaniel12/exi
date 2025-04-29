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
    "6093517": {"nome": "Advanced Repair Ampoule 10x Hair Pack 300ml", "marca": "Kerasys","codigo_produto": "8801046357804"},
    "E3573901": {"nome": "Pro Longer - Cream 10-IN-1 150ml", "marca": "loreal", "codigo_produto": "3474636977307"}
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

