import numpy as np
import streamlit as st
import firebase_admin
import logging
from firebase_admin import credentials, firestore
from datetime import datetime
from google import genai
from google.genai import types
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
import mimetypes
import re

INSTRUCOES = """
você é um assistente de IA que converte anotações manuscritas em **LaTeX puro**  
seu objetivo é reproduzir o texto com **fidelidade total**, prestando atenção especial a:

1. **Equações inline**: identifique expressões matemáticas e envolva-as em `$...$`  
- ex: `E = m c^2` → `$E = m c^2$`

2. **Equações de exibição** (bloco): envolva em `$$...$$`  
- garanta uma linha em branco antes e depois  
- preserve quebras de linha internas  
- ex:  
    ```
    integral de a a b
    f(x) dx
    ```  
    →  
    $$
    \int_a^b f(x)\,dx
    $$

3. **Comandos LaTeX**: use sempre `\int`, `\sum`, subscritos `_{}`, sobrescritos `^{}` etc., sem simplificar ou omitir nada

4. **Texto normal**: mantenha parágrafos, espaçamentos e quebras de linha exatamente como no manuscrito

5. **Nada extra**: não adicione títulos, legendas, comentários ou qualquer texto além da conversão solicitada  
"""

def generate(imagem_bytes, type):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    modelo = "gemini-2.5-flash-preview-05-20"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type=type,
                    data=imagem_bytes,
                ), 
                types.Part.from_text(text=INSTRUCOES),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    resposta = client.models.generate_content(
        model = modelo,
        contents = contents,
        config = generate_content_config,
    )

    return resposta.text

INSTRUCOES_MARKDOWN = """
você é um assistente de IA que converte anotações manuscritas em markdown com suporte a LaTeX  
seu objetivo é reproduzir o texto exatamente, incluindo espaços e quebras de linha nas equações  

regras essenciais:
1. identifique expressões matemáticas inline e envolva-as em `$...$`, sem alterar espaçamentos internos  
2. equações em bloco devem ficar entre `$$...$$`  
- garanta uma linha em branco **antes e depois** de cada bloco de equação  
- preserve quebras de linha internas à equação como no original  
3. use comandos LaTeX (ex: `\\int`, subscrito `_{}`, sobrescrito `^{}`)  
4. preserve quebras de parágrafo e espaçamento entre blocos de texto  
5. não adicione observações, títulos ou comentários extras — apenas o texto formatado  

exemplos:
- `E = m c^2` → `$E = m c^2$`  
-                                                                                           
`integral de a a b  
f(x) dx`  

→  

$$
\int_a^b f(x)\,dx
$$  
"""

def gerar_markdown(imagem_bytes, type):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    modelo = "gemini-2.5-flash-preview-05-20"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type=type,
                    data=imagem_bytes,
                ), 
                types.Part.from_text(text=INSTRUCOES_MARKDOWN),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    resposta = client.models.generate_content(
        model = modelo,
        contents = contents,
        config = generate_content_config,
    )

    return resposta.text


INSTRUCOES_LATEX = """
A partir do texto que vou fornecer, estruture um código LaTeX com uma formatação limpa,
organizada e visualmente agradável (seguindo boas práticas de formatação de documentos).
Não deve modificar o conteúdo do texto de forma alguma.
A saída deve ser todo esse texto em LaTeX completo, pronto para compilar.
Não coloque nenhum texto adicional, apenas o código LaTeX. Não use ```latex antes do texto e nem ``` no final.
Use uma estrutura básica de documento LaTeX, incluindo:
- `\documentclass{article}`
"""

ESTRUTURAR_MD = """
A partir do texto que vou fornecer, estruture um código Markdown com uma formatação limpa,
organizada e visualmente agradável (seguindo boas práticas de formatação de documentos Markdown).
O código Markdown deve tentar reproduzir visualmente o layout e a estrutura da matemática da imagem usando as capacidades do Markdown.
Para notações matemáticas complexas, utilize a sintaxe de LaTeX para equações (delimitadas por `$`) ou blocos de equações (delimitadas por `$$`), que são comumente renderizadas em Markdown por ferramentas como MathJax ou KaTeX.
Não deve adicionar, remover ou modificar qualquer conteúdo matemático ou sua estrutura que não esteja visivelmente presente na imagem.
A saída deve ser apenas o código Markdown completo, sem nenhum texto adicional, explicações ou blocos de código (` ``` `). O código deve começar diretamente com o conteúdo Markdown.
Priorize a clareza e a legibilidade do código Markdown gerado.
"""

def estruturar_latex(texto: str) -> str:
    """
    Recebe um texto bruto e retorna um código LaTeX completo,
    sem alterar o conteúdo, apenas adicionando toda a estrutura
    (documentclass, pacotes, seções, etc.) de forma organizada.
    """
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    model = "gemini-2.5-flash-preview-05-20"

    # monta o conteúdo do prompt, unindo instruções e seu texto
    combined_prompt = f"{INSTRUCOES_LATEX}\n\nTexto de entrada:\n{texto}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=combined_prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain"
    )

    # faz a chamada e já pega a resposta toda
    resposta = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    return resposta.text

def estruturar_markdown(texto: str) -> str:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    model = "gemini-2.5-flash-preview-05-20"

    # monta o conteúdo do prompt, unindo instruções e seu texto
    combined_prompt = f"{ESTRUTURAR_MD}\n\nTexto de entrada:\n{texto}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=combined_prompt)]
        )
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain"
    )

    # faz a chamada e já pega a resposta toda
    resposta = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    return resposta.text

# Firebase
@st.cache_resource
def conectar_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

def gerar_estruturado(imagem_bytes, type):
    """
    Faz uma única chamada à API e retorna LaTeX e Markdown estruturados.
    """
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    modelo = "gemini-2.5-flash-preview-05-20"

    prompt = f"""
    Converta as anotações manuscritas da imagem fornecida e entregue **somente** em duas partes:
    
    [MARKDOWN]
    (Markdown estruturado com LaTeX inline e em bloco, preservando quebras de linha)
    
    [LATEX]
    (Documento LaTeX completo com estrutura básica \documentclass, pacotes essenciais e o conteúdo reproduzido)
    """

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type=type,
                    data=imagem_bytes,
                ),
                types.Part.from_text(text=prompt),
            ],
        ),
    ]

    config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    resposta = client.models.generate_content(
        model=modelo,
        contents=contents,
        config=config,
    )

    # separa os dois blocos pelo marcador
    texto = resposta.text
    try:
        md_part = texto.split("[MARKDOWN]")[1].split("[LATEX]")[0].strip()
        latex_part = texto.split("[LATEX]")[1].strip()
    except Exception:
        md_part, latex_part = texto, ""

    return md_part, latex_part



def salvar_saidas(markdown, latex, markdown_estruturado, latex_estruturado, imagem_bytes = None):
    """
    Salva as saídas de processamento (Markdown e LaTeX) no Firestore.

    Estrutura no Firestore:
        usuarios2 (coleção)
            └── <email_do_usuario> (documento)
                    └── saidas (subcoleção)
                            └── <doc_id_timestamp> (documento)
                                ├── saida_markdown
                                ├── saida_latex
                                ├── markdown_estruturado
                                └── latex_estruturado

    Args:
        markdown (str): Código em Markdown bruto.
        latex (str): Código em LaTeX bruto.
        markdown_estruturado (str): Versão estruturada do Markdown.
        latex_estruturado (str): Versão estruturada do LaTeX.
        imagem_bytes (str): código bytes da imagem

    Returns:
        str | bool: O ID do documento criado em caso de sucesso,
                    ou False se não for possível salvar.
    """

    if not hasattr(st.user, 'email'):
        logging.warning("Tentativa de salvar saída sem usuário autenticado.")
        return False

    try:
        db = conectar_firebase()
        colecao = 'usuarios2'
        doc_id = datetime.now().strftime("%Y%m%d%H%M%S")

        referencia = (
            db.collection(colecao)
              .document(st.user.email)
              .collection('saidas')
              .document(doc_id)
        )

        dicionario = {
            'saida_markdown': markdown,
            'saida_latex': latex,
            'markdown_estruturado': markdown_estruturado,
            'latex_estruturado': latex_estruturado
        }

        if imagem_bytes:
            dicionario['imagem'] = base64.b64encode(imagem_bytes).decode("utf-8")
            
        referencia.set(dicionario)
        logging.info(f"Saída salva com sucesso. DocID={referencia.id}, User={st.user.email}")
        return referencia.id

    except Exception as e:
        logging.error(f"Erro ao salvar saída no Firestore: {e}", exc_info=True)
        return False


def enviar_emails(documento, lista_destinatarios):
    email_remetente = st.secrets["gmail"]["email"]
    senha_app = st.secrets["gmail"]["app_password"]
    nome_remetente = st.secrets["gmail"]["nome"]

    # --- Montagem do E-mail (feito uma vez, pois o conteúdo é o mesmo para todos) ---
    assunto = " Seu Código está pronto!"
    corpo_texto = " Segue anexo dos códigos em LateX e Markdow" # Fallback de texto puro
    documento = documento

    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = formataddr((nome_remetente, email_remetente))
    # Junta a lista de e-mails em uma string separada por vírgulas
    msg['To'] = ", ".join(lista_destinatarios)
    msg.set_content(corpo_texto)
    msg.add_alternative(documento, subtype='txt')
   
    try:
        contexto_ssl = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto_ssl) as servidor:
            servidor.login(email_remetente, senha_app)
            servidor.send_message(msg)
        return True, f"E-mail enviado com sucesso para {len(lista_destinatarios)} destinatário(s)!"
    except Exception as e:
        return False, f"Ocorreu um erro inesperado: {e}"
