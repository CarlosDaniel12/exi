def processar():
    codigos_input = st.session_state.input_codigo.strip()
    if not codigos_input:
        return
    codigos = re.split(r'[\s,]+', codigos_input)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Prévia para visualização e detecção de problemas
                try:
                    preview = uploaded_file.read().decode("utf-8")
                    encoding_used = "utf-8"
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    preview = uploaded_file.read().decode("latin1")
                    encoding_used = "latin1"

                uploaded_file.seek(0)  # Reset do ponteiro do arquivo para leitura com pandas

                st.text_area("Prévia do arquivo CSV", preview[:1000], height=200)

                # Leitura com tolerância a erros
                df = pd.read_csv(uploaded_file, sep=";", dtype=str, encoding=encoding_used, on_bad_lines="skip")
            except Exception as e:
                st.error(f"Erro ao ler o CSV: {e}")
                continue

            if "SKU" not in df.columns or "Número pedido" not in df.columns:
                st.error("❌ Colunas esperadas ('SKU' e 'Número pedido') não encontradas. Colunas no CSV: " + ", ".join(df.columns))
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
