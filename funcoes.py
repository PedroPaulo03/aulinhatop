import numpy as np
import streamlit as st
from google import genai
from google.genai import types


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
