# Importações necessárias
# Obsevação: pip freeze > requirements.txt gera uma lista de todas as bibliotecas instaladas no ambiente Python atual, juntamente com
#suas versões,e redirecionar essa lista para um arquivo chamado requirements.txt

import os #os: Usado para executar comandos do sistema operacional.
import streamlit as st # streamlit: Framework para criar aplicativos web rápidos.
from wordcloud import WordCloud # WordCloud: Biblioteca para gerar nuvens de palavras.
import matplotlib.pyplot as plt # matplotlib.pyplot: Biblioteca para criar visualizações gráficas.
from bs4 import BeautifulSoup # BeautifulSoup: Biblioteca para fazer parsing de documentos HTML e XML.
import requests # requests: Biblioteca para fazer requisições HTTP.
import nltk # nltk: Natural Language Toolkit, biblioteca para trabalhar com dados de linguagem humana.
from nltk.corpus import stopwords # stopwords, Counter: Utilidades do nltk e collections para processamento de texto.
from collections import Counter #usando para contar objetos como caracteres em uma string ou itens em uma lista.
import PyPDF2 # PyPDF2 - Biblioteca para extrair texto de arquivos PDF
import docx2txt # docx2txt - Biblioteca para extrair texto de arquivos DOCX.
from io import BytesIO # BytesIO: Utilitário para trabalhar com streams de bytes em memória.

# Baixa dados necessários do NLTK, como stopwords e o tokenizador.
nltk.download('stopwords')
nltk.download('punkt')

# Funções para processamento de texto

# Extrai texto de arquivos PDF.
def extrair_texto_de_pdf(arquivo):
    buffer = BytesIO(arquivo.read())
    leitor = PyPDF2.PdfReader(buffer)
    texto = ''
    for pagina in leitor.pages:
        texto += pagina.extract_text() or ''  # Adiciona texto da página ao total, lidando com None
    return texto

# Extrai texto de arquivos DOCX.
def extrair_texto_de_docx(caminho_arquivo):
    texto = docx2txt.process(caminho_arquivo)
    return texto

# Obtém texto de uma página da web usando sua URL.
def obter_texto_da_web(url):
    resposta = requests.get(url)
    sopa = BeautifulSoup(resposta.content, 'html.parser')
    paragrafos = sopa.find_all('p')
    texto = ' '.join(p.get_text() for p in paragrafos)
    return texto

# Remove stopwords de um texto em português.
def remover_stopwords(texto):
    palavras_parada = set(stopwords.words('portuguese'))
    palavras = nltk.word_tokenize(texto.lower())
    palavras_filtradas = [palavra for palavra in palavras if palavra.isalnum() and palavra not in palavras_parada]
    return ' '.join(palavras_filtradas)

# Gera e exibe uma nuvem de palavras a partir de um texto.
def gerar_nuvem_de_palavras(texto):
    nuvem_palavras = WordCloud(width=800, height=400, background_color='white').generate(texto)
    plt.figure(figsize=(10, 5))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# Início do aplicativo Streamlit

if __name__ == "__main__":
    texto = ''  # Variável para armazenar o texto a ser analisado
    st.title('Aplicação Web - Análise Estatística básica de Texto - Evandro - IESB - Topicos Machine Learning - NLP')  # Título do aplicativo

    # Opções de entrada de dados pelo usuário
    opcao_entrada = st.radio(
        'Senhor (a) usuário (a), escolha o tipo de entrada de dados:',
        ('Word', 'PDF', 'Link da Página', 'Texto do(a) usuário(a)')
    )

    # Processa a entrada conforme a opção escolhida
    
    if opcao_entrada == 'Word':
        arquivo = st.file_uploader('Carregar documento Word:', type=['docx'])
        if arquivo is not None:
            texto = extrair_texto_de_docx(arquivo)
    elif opcao_entrada == 'PDF':
        arquivo = st.file_uploader('Carregar PDF:', type=['pdf'])
        if arquivo is not None:
            texto = extrair_texto_de_pdf(arquivo)
    elif opcao_entrada == 'Link da Página':
        url = st.text_input('Insira o URL da página:')
        if url:
            texto = obter_texto_da_web(url)
    else:
        texto = st.text_area('Redija um texto ou copie e cole aqui:')

   # Se há texto, processa e exibe análises
if texto:
    # Adiciona um subtítulo no aplicativo Streamlit com o texto 'Texto Analisado:'
    st.subheader('Texto extraido da base informada pelo(a) usuário(a):')
    
    # Exibe o texto obtido na interface do aplicativo. Isso permite ao usuário visualizar o texto que está sendo analisado.
    st.write(texto)  
    
    # Chama a função remover_stopwords para filtrar as stopwords do texto. Esta função retorna o texto sem as palavras comuns que não agregam significado significativo para análise de frequência.
    texto_filtrado = remover_stopwords(texto)
    
    # Utiliza a classe Counter para contar a frequência de cada palavra no texto filtrado.
    # O método split() divide o texto em uma lista de palavras, baseando-se em espaços, que é então passada para Counter.
    frequencia_palavras = Counter(texto_filtrado.split())
    
    # Obtém as 20 palavras mais comuns e suas contagens usando o método most_common(20).
    # Isso retorna uma lista de tuplas, onde cada tupla contém uma palavra e sua contagem.
    palavras_mais_comuns = frequencia_palavras.most_common(20)
    
    # Adiciona outro subtítulo no aplicativo Streamlit para indicar que as próximas informações são as 20 palavras mais frequentes, excluindo stopwords.
    st.subheader('20 Palavras Mais Frequentes (sem palavras irrelevantes - stopwords - tais como "e", "ou", "mas", "se", "um", "uma", "os", "das", "de", "em", "para", "com", "não", "é", "por"):')
    
    # Para cada par palavra-frequência nas 20 palavras mais comuns, exibe essa informação no aplicativo.
    # O loop for itera sobre cada tupla na lista palavras_mais_comuns, extraindo a palavra e sua frequência e exibindo-as.
    for palavra, frequencia in palavras_mais_comuns:
        st.write(f'{palavra}: {frequencia}')
    
    # Adiciona um subtítulo para a nuvem de palavras, indicando que a próxima seção do aplicativo mostrará a nuvem de palavras.
    st.subheader('Nuvem de Palavras:')
    
    # Gera a nuvem de palavras a partir do texto filtrado. A função gerar_nuvem_de_palavras cria uma visualização gráfica que mostra as palavras mais frequentes no texto, com o tamanho de cada palavra proporcional à sua frequência.
    # Esta visualização é então exibida no aplicativo usando st.pyplot().
    gerar_nuvem_de_palavras(texto_filtrado)