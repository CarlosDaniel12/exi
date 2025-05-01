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
    
    # Exibe alerta para SKUs não encontrados, se houver
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
    
    # Agrupa os pedidos por marca (normalizando para minúsculas)
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
                "nome": produto["nome"],
                "quantidade": quantidade,
                "codigo_produto": produto.get("codigo_produto", "")
            })
    
    # Define os grupos fixos e a ordem desejada (os nomes devem estar em minúsculas)
    grupos = [
        ("Corredor 1", ["kerastase", "fino", "redken", "senscience", "loreal", "carol"]),
        ("Corredor 2", ["kerasys", "mise", "ryo", "ice", "image"]),
        ("Corredor 3", ["tsubaki", "wella", "sebastian", "bedhead", "lee", "banila", "alfapart"]),
        ("Pinceis", ["real", "ecootols"]),
        ("Dr.purederm", ["dr.pawpaw", "dr.purederm"]),
        ("sac", ["sac"])
    ]
    
    # Filtra apenas os grupos que possuem ao menos um pedido para alguma das marcas
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
    
    # Função para formatar produtos TSUBAKI conforme especificado
    def format_tsubaki_produto(prod):
        nome = prod["nome"].strip()
        quantidade = prod["quantidade"]
        lower_nome = nome.lower()
        cor = None
        if "moist repair conditioner" in lower_nome:
            cor = "red"
        elif "moist repair shampoo" in lower_nome:
            cor = "red"
        elif "volume repair conditioner" in lower_nome:
            cor = "yellow"
        elif "volume repair shampoo" in lower_nome:
            cor = "yellow"
        elif "repair mask" in lower_nome:
            cor = "goldenrod"
        if cor:
            nome_formatado = f"<span style='color:{cor};'><strong>{nome}</strong></span>"
            qtd_formatado = f"<span style='color:{cor};'><strong>{quantidade}</strong></span>"
            return nome_formatado, qtd_formatado
        else:
            return f"<strong>{nome}</strong>", f"<strong>{quantidade}</strong>"
    
    # Para cada grupo (aba), exibe os pedidos para as marcas definidas na ordem fixa
    for (titulo, lista_marcas), aba in zip(grupos_filtrados, abas):
        with aba:
            st.header(titulo)
            # Para cada marca do grupo, se houver pedidos, exibe a logo e os itens
            for marca in lista_marcas:
                if marca in agrupado_por_marca:
                    try:
                        logo_path = os.path.join(CAMINHO_LOGOS, f"{marca}.png")
                        with open(logo_path, "rb") as img_file:
                            logo_encoded = base64.b64encode(img_file.read()).decode()
                        st.markdown(
                            f"<img src='data:image/png;base64,{logo_encoded}' width='150' style='margin-bottom: 10px;'>",
                            unsafe_allow_html=True)
                    except Exception:
                        st.warning(f"Logo da marca **{marca}** não encontrada.")
                    for prod in agrupado_por_marca[marca]:
                        cp = prod.get("codigo_produto", "")
                        # Se a marca for tsubaki, verifica para aplicar formatação especial
                        if marca == "tsubaki":
                            nome_fmt, qtd_fmt = format_tsubaki_produto(prod)
                            st.markdown(
                                f"{nome_fmt} | Quantidade: {qtd_fmt} &nbsp;&nbsp;&nbsp; ({cp})",
                                unsafe_allow_html=True)
                        else:
                            st.markdown(
                                f"**{prod['nome']}** | Quantidade: **{prod['quantidade']}** &nbsp;&nbsp;&nbsp; ({cp})",
                                unsafe_allow_html=True)
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

# Função cacheada para ler o CSV a partir dos bytes do arquivo
@st.cache_data(show_spinner=True)
def tentar_ler_csv_cache(file_bytes):
    try:
        df = pd.read_csv(BytesIO(file_bytes), sep=";", dtype=str, encoding="utf-8", 
                         on_bad_lines="skip", engine="python")
    except UnicodeDecodeError:
        df = pd.read_csv(BytesIO(file_bytes), sep=";", dtype=str, encoding="latin-1", 
                         on_bad_lines="skip", engine="python")
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
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{encoded}' width='200'></div>",
                unsafe_allow_html=True)
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
