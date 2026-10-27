
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ==========================================
# CONFIGURACAO DA PAGINA
# ==========================================

st.set_page_config(
    page_title="OMOPHIS | Chatbot IA",
    page_icon="☕",
    layout="wide"
)

# ==========================================
# CONEXAO COM A GROQ
# ==========================================


load_dotenv()

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("GROQ_API_KEY")


if not API_KEY:
    st.error(
        "Chave da Groq não encontrada. "
        "Confira o arquivo .env."
    )
    st.stop()

client = Groq(api_key=API_KEY)

# ==========================================
# ESTADO DA CONVERSA
# ==========================================

if "historico" not in st.session_state:
    st.session_state.historico = []

if "estilo" not in st.session_state:
    st.session_state.estilo = "Equilibrado"

if "temperatura" not in st.session_state:
    st.session_state.temperatura = 0.7

# ==========================================
# IDENTIDADE VISUAL: CAFE COM LEITE
# ==========================================

st.markdown("""
<style>

/* PALETA PRINCIPAL */

:root {
    --creme: #F3E9DC;
    --bege: #EDE0D0;
    --cappuccino: #E8D9C7;
    --cafe-leite: #D2BCA4;
    --marrom: #49382D;
    --marrom-suave: #765D49;
    --destaque: #A8896C;
    --branco: #FFFCF8;
}

/* FUNDO PRINCIPAL */

.stApp {
    background: var(--creme) !important;
    color: var(--marrom) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* MENU LATERAL */

[data-testid="stSidebar"] {
    background: var(--bege) !important;
    border-right: 1px solid var(--cafe-leite);
}

[data-testid="stSidebar"] * {
    color: var(--marrom);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--marrom);
}

/* CARTAO DA MARCA */

.brand-card {
    text-align: center;
    padding: 28px 14px;
    margin: 5px 0 30px 0;
    background: linear-gradient(
        145deg,
        #F5E9DA,
        #E8D7C3
    );
    border: 1px solid var(--cafe-leite);
    border-radius: 22px;
    box-shadow: 0 4px 16px rgba(73, 56, 45, 0.07);
}

.brand-name {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 30px;
    font-weight: 500;
    letter-spacing: 5px;
    color: var(--marrom);
    text-shadow: none;
}

.brand-subtitle {
    color: var(--marrom-suave);
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 3px;
    margin-top: 12px;
}

.brand-tagline {
    color: var(--marrom-suave);
    font-size: 14px;
    margin-top: 14px;
}

/* TITULOS E TEXTOS */

h1, h2, h3 {
    color: var(--marrom) !important;
}

p, label, .stCaption {
    color: var(--marrom-suave);
}

.section-title {
    color: var(--marrom-suave);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 12px 0;
}

/* SELETOR DE ESTILO */

[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    color: var(--marrom) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: var(--branco) !important;
    color: var(--marrom) !important;
    border-color: var(--cafe-leite) !important;
    border-radius: 10px !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: var(--marrom) !important;
}

[data-baseweb="popover"] {
    background-color: var(--branco) !important;
}

[data-baseweb="menu"] {
    background-color: var(--branco) !important;
}

[data-baseweb="menu"] li {
    background-color: var(--branco) !important;
    color: var(--marrom) !important;
}

[data-baseweb="menu"] li:hover {
    background-color: var(--bege) !important;
}

/* CONTROLE DE CRIATIVIDADE */

[data-testid="stSlider"] [data-baseweb="slider"] {
    color: var(--destaque) !important;
}

/* BOTOES */

.stButton button,
.stDownloadButton button {
    background: #E8D9C7 !important;
    color: var(--marrom) !important;
    border: 1px solid var(--cafe-leite) !important;
    border-radius: 12px !important;
    transition: background 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #DCC7B0 !important;
    color: var(--marrom) !important;
    border-color: var(--destaque) !important;
}

/* MENSAGENS DO CHAT */

[data-testid="stChatMessage"] {
    background: #E8D9C7 !important;
    color: var(--marrom) !important;
    border: 1px solid #D2BCA4 !important;
    border-radius: 15px !important;
    padding: 14px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3 {
    color: var(--marrom) !important;
}

/* CAMPO DE DIGITACAO */

[data-testid="stChatInput"] {
    background: var(--branco) !important;
    border: 1px solid var(--cafe-leite) !important;
    border-radius: 16px !important;
    box-shadow: 0 3px 10px rgba(73, 56, 45, 0.06) !important;
}

[data-testid="stChatInput"] textarea {
    background: var(--branco) !important;
    color: var(--marrom) !important;
    -webkit-text-fill-color: var(--marrom) !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #927B67 !important;
    -webkit-text-fill-color: #927B67 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--destaque) !important;
    box-shadow: 0 0 0 1px var(--destaque) !important;
}

/* CONTADOR DE MENSAGENS */

[data-testid="stMetric"] {
    background: var(--cappuccino) !important;
    border: 1px solid var(--cafe-leite) !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

[data-testid="stMetric"] label,
[data-testid="stMetric"] [data-testid="stMetricValue"],
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: var(--marrom) !important;
}

/* AVISOS E BOAS-VINDAS */

[data-testid="stAlert"] {
    background: #E8D9C7 !important;
    color: var(--marrom) !important;
    border: 1px solid var(--cafe-leite) !important;
    border-radius: 12px !important;
}

[data-testid="stAlert"] p {
    color: var(--marrom) !important;
}

/* LINHAS DIVISORAS */

hr {
    border-color: var(--cafe-leite) !important;
}

/* RODAPE */

.footer {
    text-align: center;
    color: var(--marrom-suave);
    font-size: 12px;
    padding: 25px 8px 10px;
    margin-top: 35px;
    border-top: 1px solid var(--cafe-leite);
}

.footer strong {
    color: var(--marrom);
    letter-spacing: 1px;
}

/* CLAREAR A AREA INFERIOR DO CHAT */

[data-testid="stBottom"],
[data-testid="stBottom"] > div {
    background: #F3E9DC !important;
    background-color: #F3E9DC !important;
}

/* FUNDO AO REDOR DO CAMPO DE MENSAGEM */

[data-testid="stBottom"] [data-testid="stChatInputContainer"] {
    background: #F3E9DC !important;
}

/* CAMPO ONDE A MENSAGEM E DIGITADA */

[data-testid="stChatInput"] {
    background: #FBF7F1 !important;
    border: 1px solid #C7AA8B !important;
    border-radius: 16px !important;
    box-shadow: 0 3px 10px rgba(73, 56, 45, 0.06) !important;
}

[data-testid="stChatInput"] textarea {
    background: #FBF7F1 !important;
    color: #49382D !important;
    -webkit-text-fill-color: #49382D !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #927B67 !important;
    -webkit-text-fill-color: #927B67 !important;
}

/* ACABAMENTO CLARO DA CAIXA DE CONVERSA */

[data-testid="stBottom"] {
    background: #F3E9DC !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div {
    background: #FBF7F1 !important;
    border: 1px solid #C7AA8B !important;
    border-radius: 16px !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea {
    background: #FBF7F1 !important;
    color: #49382D !important;
    -webkit-text-fill-color: #49382D !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] button {
    background: #E8D9C7 !important;
    color: #49382D !important;
    border: 1px solid #C7AA8B !important;
    border-radius: 10px !important;
}

[data-testid="stChatInput"] button:hover {
    background: #D2BCA4 !important;
    color: #49382D !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# MENU LATERAL
# ==========================================

with st.sidebar:

    st.markdown("""
    <div class="brand-card">
        <div class="brand-name">OMOPHIS</div>
        <div class="brand-subtitle">
            INTELIGENCIA ARTIFICIAL
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Ferramentas</div>',
        unsafe_allow_html=True
    )

    st.session_state.estilo = st.selectbox(
        "Estilo das respostas",
        [
            "Equilibrado",
            "Objetivo",
            "Detalhado",
            "Criativo"
        ],
        index=[
            "Equilibrado",
            "Objetivo",
            "Detalhado",
            "Criativo"
        ].index(st.session_state.estilo)
    )

    st.session_state.temperatura = st.slider(
        "Criatividade da IA",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperatura,
        step=0.1
    )

    st.divider()

    st.markdown(
        '<div class="section-title">Gerenciar conversa</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Nova conversa",
        use_container_width=True
    ):
        st.session_state.historico = []
        st.rerun()

    if st.button(
        "Limpar histórico",
        use_container_width=True
    ):
        st.session_state.historico = []
        st.rerun()

    if st.session_state.historico:

        texto_chat = "\n\n".join(
            (
                "Você"
                if mensagem["role"] == "user"
                else "OMOPHIS IA"
            )
            + ":\n"
            + mensagem["content"]
            for mensagem in st.session_state.historico
        )

        st.download_button(
            "Baixar conversa",
            data=texto_chat,
            file_name="conversa_omophis.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

    st.metric(
        "Mensagens na conversa",
        len(st.session_state.historico)
    )

    st.caption("OMOPHIS IA | Versão 4.0")

# ==========================================
# CABECALHO PRINCIPAL
# ==========================================

st.markdown("""
<div class="brand-card">
    <div class="brand-name">OMOPHIS</div>
    <div class="brand-subtitle">
        SEU ASSISTENTE INTELIGENTE
    </div>
    <div class="brand-tagline">
        Tecnologia, ideias e respostas em um só lugar.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MENSAGEM INICIAL
# ==========================================

if not st.session_state.historico:

    st.info(
        "Bem-vindo à OMOPHIS IA! "
        "Digite sua pergunta abaixo para começar."
    )

# ==========================================
# HISTORICO DA CONVERSA
# ==========================================

for mensagem in st.session_state.historico:

    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# ==========================================
# CAMPO DE MENSAGEM
# ==========================================

pergunta = st.chat_input(
    "Converse com a OMOPHIS IA..."
)

# ==========================================
# RESPOSTA DA INTELIGENCIA ARTIFICIAL
# ==========================================

if pergunta:

    st.session_state.historico.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user"):
        st.markdown(pergunta)

    instrucoes = {
        "Equilibrado":
            "Responda de forma clara, natural e útil.",

        "Objetivo":
            "Responda de forma direta e concisa, "
            "mantendo as informações essenciais.",

        "Detalhado":
            "Explique os assuntos com detalhes, "
            "exemplos e boa organização.",

        "Criativo":
            "Use criatividade, ideias originais "
            "e linguagem envolvente."
    }

    mensagens_ia = [
        {
            "role": "system",
            "content": (
                "Você é a OMOPHIS IA, um assistente virtual "
                "útil, educado e confiável. "
                + instrucoes[st.session_state.estilo]
            )
        }
    ] + st.session_state.historico

    with st.chat_message("assistant"):

        with st.spinner("A OMOPHIS IA está pensando..."):

            try:
                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=mensagens_ia,
                    temperature=st.session_state.temperatura
                )

                texto = resposta.choices[0].message.content

                st.markdown(texto)

                st.session_state.historico.append({
                    "role": "assistant",
                    "content": texto
                })

            except Exception:
                st.error(
                    "Não foi possível obter uma resposta. "
                    "Confira a conexão e a configuração "
                    "da API da Groq."
                )

                st.session_state.historico.pop()

# ==========================================
# ASSINATURA DA MARCA
# ==========================================

st.markdown("""
<div class="footer">
    Desenvolvido com tecnologia e criatividade por
    <strong>OMOPHIS</strong>
    <br><br>
    © OMOPHIS | Assistente de Inteligência Artificial
</div>
""", unsafe_allow_html=True)
