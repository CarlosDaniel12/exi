produtos_cadastrados = {codigo: produto for codigo, produto in lista_produtos.items()}

# Inicializa variáveis na sessão
if "contagem" not in st.session_state:
    st.session_state.contagem = {}
if "pedidos_bipados" not in st.session_state:
    st.session_state.pedidos_bipados = []
if "input_codigo" not in st.session_state:
    st.session_state.input_codigo = ""
if "nao_encontrados" not in st.session_state:
    st.session_state.nao_encontrados = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

#################################
# Página de Resultados
#################################
params = st.query_params
if "resultado" in params:
    st.title("Resumo do Pedido - Organizado")
    st.markdown("---")
    
    # Se houver SKUs não encontrados, exibe alerta fixo e um expander
    if st.session_state.nao_encontrados:
        qtd_nao = len(st.session_state.nao_encontrados)
        st.markdown(
            f"<div style='background-color:#ffcccc; padding:10px; border-radius:5px; color:red; text-align:center;'>"
            f"⚠️ ATENÇÃO: {qtd_nao} pedido(s) não foram lidos!"
            f"</div>",
            unsafe_allow_html=True
        )
        titulo_expander = f"<span style='color:red;'>Clique aqui para visualizar os {qtd_nao} pedidos não lidos.</span>"
        with st.expander(titulo_expander, expanded=False):
            for entrada in st.session_state.nao_encontrados:
                st.markdown(f"- {entrada}")
    
    # Agrupa os pedidos por marca (normalizando para minúsculas) e armazena também a chave SKU
    agrupado_por_marca = {}
    for codigo, valores in params.items():
        if codigo == "resultado":
            continue
        try:
            quantidade = valores[0]
        except IndexError:
            quantidade = "0"
        produto = produtos_cadastrados.get(codigo)
        if produto:
            marca = produto["marca"].lower().strip()
            if marca not in agrupado_por_marca:
                agrupado_por_marca[marca] = []
            agrupado_por_marca[marca].append({
                "sku": codigo,
                "nome": produto["nome"],
                "quantidade": quantidade,
                "codigo_produto": produto.get("codigo_produto", "")
            })
    
    # Dicionário para formatação personalizada para produtos da marca "ice"
    ice_color_mapping = {
        # Grupo 1 (amarelo – #faeba9)
        "50277E_5": "#faeba9",
        "51007E_5": "#faeba9",
        "03846BR": "#faeba9",
        "39937E_5": "#faeba9",
        "51045E_5": "#faeba9",
        "51052E_5": "#faeba9",
        "39920E_5": "#faeba9",
        "50260E_5": "#faeba9",
        "51014E_5": "#faeba9",
        "51038E_5": "#faeba9",
        # Grupo 2 (rosa – #ecc7cc)
        "51076E_5": "#ecc7cc",
        "50291E_5": "#ecc7cc",
        "03839BR": "#ecc7cc",
        "39951E_5": "#ecc7cc",
        "51083E_5": "#ecc7cc",
        "39944E_5": "#ecc7cc",
        "50284E_5": "#ecc7cc",
        "51090E_5": "#ecc7cc",
        # Grupo 3 (verde claro – #dbedd2)
        "50215E_5": "#dbedd2",
        "39890E_5": "#dbedd2",
        "50208E_5": "#dbedd2",
        # Grupo 4 (azul – #b6e1e0)
        "39883E_5": "#b6e1e0",
        "50192E_5": "#b6e1e0",
        "50840E_5": "#b6e1e0",
        "03853BR": "#b6e1e0",
        "39876E_5": "#b6e1e0",
        "50185E_5": "#b6e1e0",
        "50857E_5": "#b6e1e0",
        "50895E_5": "#b6e1e0",
        # Grupo 5 (azul – #b31c4a)
        "50253E_5": "#b31c4a",
        "50956E_5": "#b31c4a",
        "50963E_5": "#b31c4a",
        "50246E_5": "#b31c4a",
        "39913E_5": "#b31c4a",
        "39906E_5": "#b31c4a",
        # Grupo 6 (azul – #97b5f5)
        "50239E_5": "#97b5f5",
        "51151E_5": "#97b5f5",
        "50222E_5": "#97b5f5",
        "39852E_5": "#97b5f5"
    }
    
    # Define os grupos fixos e a ordem desejada (os nomes devem estar em minúsculas)
    grupos = [
        ("Corredor 1", ["kerastase", "fino", "redken", "senscience", "loreal", "carol"]),
        ("Corredor 2", ["kerasys", "mise", "ryo", "ice", "image"]),
        ("Corredor 3", ["tsubaki", "wella", "sebastian", "bedhead", "lee", "banila", "alfapart"]),
        ("Pinceis", ["real", "ecootols"]),
        ("Dr.purederm", ["dr.pawpaw", "dr.purederm"]),
        ("sac", ["sac"])
    ]
    
    # Filtra apenas os grupos que possuem algum pedido
    grupos_filtrados = []
    for titulo, marcas in grupos:
        for m in marcas:
            if m in agrupado_por_marca:
                grupos_filtrados.append((titulo, marcas))
                break

    if not grupos_filtrados:
        st.info("Nenhum produto encontrado.")
        st.stop()
    
    # Cria as abas somente para os grupos filtrados
    titulos_abas = [titulo for titulo, marcas in grupos_filtrados]
    abas = st.tabs(titulos_abas)
    
    # Exibe os pedidos para cada grupo em sua aba
    for (titulo, lista_marcas), aba in zip(grupos_filtrados, abas):
        with aba:
            st.header(titulo)
            for marca in lista_marcas:
                if marca in agrupado_por_marca:
                    # Exibe a logo com fundo branco fixo
                    try:
                        logo_path = os.path.join(CAMINHO_LOGOS, f"{marca}.png")
                        with open(logo_path, "rb") as img_file:
                            logo_encoded = base64.b64encode(img_file.read()).decode()
                        st.markdown(
                            f"<div style='background-color:white; display:inline-block; padding:5px;'>"
                            f"<img src='data:image/png;base64,{logo_encoded}' width='150' style='margin-bottom: 10px;'>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                    except Exception:
                        st.warning(f"Logo da marca **{marca}** não encontrada.")
                    for prod in agrupado_por_marca[marca]:
                        cp = prod.get("codigo_produto", "")
                        # Para produtos da marca "ice", aplica formatação personalizada se o SKU estiver no mapping
                        if marca == "ice" and prod.get("sku") in ice_color_mapping:
                            cor = ice_color_mapping[prod.get("sku")]
                            nome_fmt = f"<span style='color:{cor};'><strong>{prod['nome']}</strong></span>"
                            qtd_fmt = f"<strong>{prod['quantidade']}</strong>"
                            st.markdown(
                                f"{nome_fmt} | Quantidade: {qtd_fmt} &nbsp;&nbsp;&nbsp; ({cp})",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"**{prod['nome']}** | Quantidade: **{prod['quantidade']}** &nbsp;&nbsp;&nbsp; ({cp})",
                                unsafe_allow_html=True
                            )
                    st.markdown("---")
    
    st.markdown("[Voltar à página principal](/)", unsafe_allow_html=True)
    st.stop()

#################################
# Página Principal (Interface)
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
        df["sku"] = df["sku"].apply(lambda x: str(int(float(str(x).replace(",", "").replace(" ", "").strip()))) if "E+" in str(x) else str(x).strip())
        for codigo in codigos:
            pedidos = df[df["número pedido"].astype(str).str.strip() == codigo]
            if not pedidos.empty:
                for sku in pedidos["sku"]:
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
