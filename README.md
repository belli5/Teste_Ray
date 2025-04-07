# Teste_Ray

# Nome: Gabriel Henriques Belliato

# 🏎️ Dashboard YouTube - Highlights F1 2024

Este projeto tem como objetivo criar um dashboard interativo que analisa o desempenho dos vídeos de **highlights da Fórmula 1 (temporada 2024)** postados no canal oficial da F1 no YouTube. Utilizando **Dash**, **Plotly** e a **YouTube Data API**, a aplicação transforma dados reais em insights visuais envolventes.

---

## ✅ Como rodar o projeto

### 🔧 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)
- Uma chave de API da **YouTube Data API v3**

---

### 📥 Passo a passo

### Instale as dependências necessarias
- pip install pandas
- pip install plotly
- pip install dash
- pip install google-api-python-client

### Execute o projeto
python desafio.py

### OBS:
- se estiver no VsCode é so clicar no run, mas dando qualquer erro é so rodar ( python desafio.py)

⚙️ Decisões Técnicas no Desenvolvimento do Projeto
Durante o desenvolvimento deste dashboard, tomei algumas decisões técnicas estratégicas para tornar a análise mais eficiente, clara e direcionada. Abaixo, explico as principais escolhas:

### Foco direto em uma playlist específica:
Em vez de buscar todos os vídeos do canal da Fórmula 1, optei por utilizar diretamente a playlist oficial de highlights da temporada 2024. Essa decisão proporcionou uma análise mais objetiva e segmentada, evitando ruído com vídeos não relacionados às corridas.

### Redução pontual da quantidade de dados exibidos:
Para alguns gráficos, como os de comentários e visualizações, filtrei os dados para mostrar apenas os 13 vídeos com mais comentarios e 10 vídeos com maior desempenho. Isso foi feito para melhorar a legibilidade dos gráficos e focar nos vídeos mais relevantes, sem comprometer a proposta da análise.

### 📊 3. Escolha intencional dos tipos de gráfico
Cada gráfico foi selecionado com base em como ele poderia melhor representar a informação, por exemplo:

- Gráfico de barras horizontais → para facilitar a leitura dos títulos em listas longas (ex: comentários),

- Gráfico de pizza → para mostrar a proporção das visualizações no Top 10,

- Gráficos de dispersão → para evidenciar correlações entre métricas (ex: curtidas vs comentários, visualizações vs curtidas),

- Gráfico de linha temporal → para observar a evolução do interesse ao longo da temporada.

### 4. Comparações escolhidas com propósito analítico
As comparações feitas no dashboard foram escolhidas com base em perguntas analíticas-chave, como:

Curtidas x Comentários
Para identificar se vídeos mais curtidos também geraram mais debate (comentários). Isso ajuda a entender o nível emocional da audiência.

Visualizações x Curtidas
Para avaliar se vídeos muito assistidos também foram bem recebidos. Um vídeo com muitas views e poucas curtidas pode indicar desempenho mecânico (recomendação do algoritmo, mas sem engajamento real).

Engajamento x Faixa de visualização
Para investigar se vídeos menos populares conseguiram gerar mais impacto proporcionalmente. Ou seja, entender qualidade de engajamento além da quantidade.

Evolução ao longo do tempo
Para observar se o público perdeu o interesse com o tempo ou se houve picos em determinadas corridas.

Essas decisões ajudaram a tornar o dashboard mais intuitivo, visualmente agradável e, principalmente, focado na entrega de informações relevantes com boa experiência de navegação e storytelling. 

### 🧩 Desafios Encontrados ao Implementar a Solução
Durante o desenvolvimento do projeto, enfrentei alguns desafios importantes que exigiram aprendizado prático e adaptação ao longo do processo. Abaixo destaco os principais:

Aprendizado da biblioteca Dash:
Um dos primeiros desafios foi aprender a utilizar a biblioteca Dash, pois até então eu nunca havia construído um dashboard diretamente em Python. Sempre utilizei ferramentas visuais separadas, como Power BI.
Isso exigiu um período inicial de estudo, especialmente para entender a estrutura dos componentes, como layout, html, dcc e como integrar gráficos com plotly.

Interação com a API do YouTube:
Após dominar o básico do Dash, comecei a trabalhar na conexão com a YouTube Data API v3. Mesmo já tendo alguma experiência com APIs em projetos anteriores, fiz questão de revisar a documentação para garantir que a extração dos dados fosse feita de forma eficiente e precisa.
Esse processo foi feito com calma, validando cada etapa antes de avançar, para evitar erros e consolidar o aprendizado.

Desafios de visualização e lógica de dados:
Conforme fui obtendo os dados e começando a gerar gráficos, surgiu o desafio de como apresentar essas informações da melhor forma possível. Tive que pensar em como organizar os dados, filtrar o que era mais relevante e escolher os tipos de gráficos que facilitassem a interpretação visual.
Além disso, foi necessário implementar algumas lógicas específicas, como ordenações, cálculos de engajamento e criação de rankings, o que exigiu atenção e testes.
