import streamlit as st
import pandas as pd
from PIL import Image
import os, base64
from io import BytesIO
import math, re, qrcode, urllib.parse

# Configura layout
st.set_page_config(layout="wide")

# Caminho para as logos (ajuste se necessário)
CAMINHO_LOGOS = "meu_app_streamlit/logos"

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
    "39852E_5": {"nome": "Keep My Blonde Mask CD 750ml", "marca": "alfaparf"}
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

# ------------ Página de Resultados (Atualizada) ------------

params = st.query_params
if "resultado" in params:
    st.title("Resumo do Pedido")
    st.markdown("---")

    # Produtos encontrados (exceto 'resultado' que é só um marcador)
    produtos_listados = [
        (codigo, valores[0]) for codigo, valores in params.items() if codigo != "resultado"
    ]

    # Exibe em 2 colunas
    colunas = st.columns(2)

    for idx, (codigo, quantidade) in enumerate(produtos_listados):
        produto = produtos_cadastrados.get(codigo)
        if produto:
            with colunas[idx % 2]:
                st.markdown(f"""
                    <div style="
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        padding: 20px;
                        margin-bottom: 20px;
                        background-color: #f9f9f9;
                        height: 100%;
                    ">
                        <h3 style="margin-top: 0;">{produto['nome']}</h3>
                        <p><strong>Marca:</strong> {produto['marca']}<br><strong>Quantidade:</strong> {quantidade}</p>
                """, unsafe_allow_html=True)

                try:
                    logo_path = os.path.join(CAMINHO_LOGOS, f"{produto['marca']}.png")
                    with open(logo_path, "rb") as img_file:
                        logo_encoded = base64.b64encode(img_file.read()).decode()
                    st.markdown(
                        f"<img src='data:image/png;base64,{logo_encoded}' width='120' style='display: block; margin: 10px auto;'>",
                        unsafe_allow_html=True
                    )
                except Exception:
                    st.markdown(
                        f"<p style='color: red; text-align: center;'>⚠️ Logo da marca <strong>{produto['marca']}</strong> não encontrada.</p>",
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<a href='/' style='text-decoration: none; font-size: 18px;'>⬅️ Voltar à página principal</a>", unsafe_allow_html=True)
    st.stop()
