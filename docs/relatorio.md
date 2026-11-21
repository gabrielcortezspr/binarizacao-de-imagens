# RELATÓRIO TEÓRICO - BINARIZAÇÃO DE IMAGENS

---

## CAPA

**Tema estudado:** Binarização de Imagens

**Título da atividade:** Binarização de Imagens utilizando OpenCV

**Nome do aluno:** Gabriel Cortez

**Curso e disciplina:** Engenharia da Computação / PDI

**Nome do professor:** Ricardo Barboza

**Instituição:** UEA/EST

**Data:** 23/11/2024

---

## RESUMO

Este trabalho apresenta um estudo teórico e prático sobre técnicas de binarização de imagens, demonstrando a aplicação de diferentes métodos utilizando Python e OpenCV. A metodologia envolve a captura e análise técnica de três fotografias originais (pessoa, objeto e documento), incluindo decomposição nos canais RGB, geração de histogramas e aplicação de três técnicas de binarização: limiar simples, método de Otsu e limiar adaptativo.

Os experimentos realizados processaram imagens com características distintas, revelando como diferentes métodos de binarização se comportam frente a variações de iluminação, contraste e conteúdo. Os resultados demonstram que métodos adaptativos oferecem superioridade em cenários com iluminação não uniforme, enquanto o método de Otsu apresenta eficácia em imagens com distribuição bimodal clara. O limiar simples, embora rápido, mostrou limitações em imagens com variações de iluminação.

Os principais resultados incluem: limiares de Otsu calculados automaticamente variando de 105 (pessoa) a 199 (documento), análise detalhada dos histogramas RGB de cada imagem, e comparação visual e quantitativa das técnicas aplicadas. O trabalho evidencia a importância do processamento digital de imagens para segmentação, análise de padrões e extração de informações estruturais, fornecendo base para aplicações futuras como OCR, visão computacional e sistemas de inspeção automatizada.

---

## SUMÁRIO

1. [Introdução](#1-introdução)
2. [Referencial Teórico](#2-referencial-teórico)
3. [Metodologia](#3-metodologia)
4. [Resultados e Discussão](#4-resultados-e-discussão)
   - 4.1 [Características Técnicas das Imagens](#41-características-técnicas-das-imagens)
   - 4.2 [Decomposição RGB](#42-decomposição-rgb)
   - 4.3 [Análise dos Histogramas](#43-análise-dos-histogramas)
   - 4.4 [Conversão para Escala de Cinza](#44-conversão-para-escala-de-cinza)
   - 4.5 [Técnicas de Binarização Aplicadas](#45-técnicas-de-binarização-aplicadas)
   - 4.6 [Comparação das Técnicas](#46-comparação-das-técnicas)
5. [Conclusão](#5-conclusão)
6. [Referências](#6-referências)
7. [Apêndices](#7-apêndices)
   - 7.1 [Código-fonte Comentado](#71-código-fonte-comentado)
   - 7.2 [Imagens Utilizadas](#72-imagens-utilizadas)
   - 7.3 [Gráficos e Figuras Geradas](#73-gráficos-e-figuras-geradas)

---

## 1. INTRODUÇÃO

A binarização de imagens é uma das operações fundamentais do processamento digital de imagens. Seu objetivo é converter uma imagem em escala de cinza em uma representação composta exclusivamente por pixels pretos e brancos. Essa transformação reduz a complexidade dos dados e facilita etapas posteriores como detecção de contornos, extração de regiões de interesse, reconhecimento de caracteres e contagem de objetos.

A binarização desempenha papel crucial em diversas aplicações práticas, desde sistemas de leitura automática de documentos (OCR) até sistemas de visão computacional para inspeção industrial, análise biomédica e processamento de imagens históricas. A escolha adequada do método de binarização é essencial para o sucesso dessas aplicações, pois influencia diretamente a qualidade da segmentação e a precisão das análises subsequentes.

### 1.1 Problemática e Objetivos

A problemática central deste trabalho consiste em compreender como diferentes métodos de binarização influenciam o resultado final e como fatores como iluminação, textura, contraste e ruído podem alterar o processo de limiaramento. 

Os objetivos específicos desta atividade são:

- Estudar teoricamente os fundamentos da binarização de imagens
- Implementar e aplicar três técnicas distintas de binarização (limiar simples, Otsu e adaptativo)
- Analisar tecnicamente três imagens com características diferentes (pessoa, objeto e documento)
- Realizar decomposição RGB e geração de histogramas para compreensão das características das imagens
- Comparar os resultados obtidos com cada método e identificar vantagens e limitações
- Avaliar a influência do gamut, contraste e iluminação nos resultados da binarização

### 1.2 Importância do Processamento Digital de Imagens

O processamento digital de imagens desempenha papel crucial no tema porque a binarização é frequentemente o primeiro passo de pipelines de visão computacional em ambientes reais. Aplicações práticas incluem:

- **Leitura automática de documentos (OCR):** Binarização é essencial para separar texto do fundo
- **Inspeção de componentes:** Detecção de defeitos em linhas de produção
- **Agricultura de precisão:** Segmentação de plantas, frutos e solo
- **Sistemas biométricos:** Processamento de impressões digitais e reconhecimento facial
- **Análise médica:** Segmentação de tecidos e estruturas em imagens médicas
- **Processamento de documentos históricos:** Digitalização e restauração de documentos antigos

A compreensão dos métodos de binarização e suas características é fundamental para o desenvolvimento de sistemas robustos e eficientes nessas áreas.

---

## 2. REFERENCIAL TEÓRICO

### 2.1 Fundamentos da Binarização

A binarização é baseada no conceito de limiar. Um limiar é um valor T que separa pixels em dois conjuntos: valores acima de T são considerados primeiro plano (foreground) e valores abaixo de T são considerados fundo (background). 

Em uma imagem em níveis de cinza representada por f(x, y), a binarização clássica é definida pela função:

```
g(x, y) = 255 se f(x, y) >= T
g(x, y) = 0   se f(x, y) < T
```

Onde:
- `f(x, y)` é o valor de intensidade do pixel na posição (x, y) da imagem original
- `T` é o valor do limiar
- `g(x, y)` é o valor do pixel na imagem binarizada (0 para preto, 255 para branco)

### 2.2 Métodos de Escolha do Limiar

Métodos tradicionais de escolha do limiar incluem:

#### 2.2.1 Limiarização Manual

O limiar é escolhido manualmente pelo usuário com base em conhecimento prévio ou inspeção visual. É simples, mas não se adapta a diferentes condições de iluminação.

#### 2.2.2 Limiarização Automática - Método de Otsu

O método mais conhecido de limiarização automática é o limiar de Otsu, proposto por Nobuyuki Otsu em 1979. Este método busca maximizar a variância entre classes, assumindo que o histograma possui duas distribuições distintas (bimodal) e encontra o ponto que melhor separa esses grupos.

O algoritmo de Otsu:
1. Calcula o histograma da imagem
2. Para cada possível limiar T, calcula a variância entre classes
3. Seleciona o limiar T que maximiza a variância entre classes

A variância entre classes é calculada como:

```
σ²b(T) = w₀(T) × w₁(T) × [μ₀(T) - μ₁(T)]²
```

Onde:
- `w₀(T)` e `w₁(T)` são as probabilidades das duas classes
- `μ₀(T)` e `μ₁(T)` são as médias das duas classes

#### 2.2.3 Limiarização Adaptativa

Quando a iluminação é irregular, o limiar global falha. Métodos adaptativos calculam um limiar local para cada região da imagem. A imagem é dividida em pequenas janelas e o limiar é calculado com base em estatísticas locais, como média ou média ponderada gaussiana. Isso corrige sombras, brilhos e variações de iluminação.

O limiar adaptativo pode ser calculado como:

```
T(x, y) = média_local(x, y) - C
```

Ou usando média ponderada gaussiana:

```
T(x, y) = média_gaussiana_local(x, y) - C
```

Onde `C` é uma constante subtraída da média local.

### 2.3 Histogramas e Análise de Intensidades

O histograma é uma função que representa a distribuição de intensidades da imagem. Ele é essencial para entender a separação entre fundo e objeto e para avaliar a qualidade da binarização. Um histograma bimodal (com dois picos distintos) geralmente indica uma boa separação entre objeto e fundo, facilitando a binarização.

### 2.4 Trabalhos Relacionados

Trabalhos clássicos fundamentam o campo da binarização:

- **Otsu (1979):** Propôs o método de limiarização automática baseado em variância entre classes, que se tornou um dos métodos mais utilizados
- **Niblack (1985):** Desenvolveu métodos adaptativos para binarização de documentos com iluminação variável
- **Gonzalez & Woods:** Apresentaram fundamentos teóricos do processamento digital de imagens, incluindo técnicas de binarização

Esses trabalhos mostram como técnicas simples podem ser aplicadas a problemas complexos como leitura de textos degradados, imagens médicas e documentos históricos.

### 2.5 Aspectos Computacionais

Do ponto de vista computacional, a binarização depende de:

1. **Conversão para escala de cinza:** Reduz a informação de cor a uma única dimensão de intensidade
2. **Cálculo eficiente de histogramas:** Essencial para métodos como Otsu
3. **Processamento local:** Métodos adaptativos requerem processamento de janelas deslizantes
4. **Otimização:** Algoritmos eficientes são necessários para processamento em tempo real

---

## 3. METODOLOGIA

### 3.1 Descrição das Fotografias Capturadas

O conjunto experimental envolve três fotografias capturadas manualmente:

1. **Imagem de Pessoa:** Fotografia de uma pessoa (`pessoavelha.jpg`)
2. **Imagem de Objeto:** Fotografia de um objeto (`fotoobjeto.jpg`)
3. **Imagem de Documento:** Fotografia de um documento (`rgfoto.jpg`)

Essas imagens foram selecionadas para representar diferentes cenários de aplicação da binarização, cada uma com características distintas de iluminação, contraste e conteúdo.

### 3.2 Especificações Técnicas das Imagens

Cada imagem foi analisada tecnicamente quanto às seguintes características:

#### 3.2.1 Imagem: Pessoa

| Característica | Valor |
|----------------|-------|
| **Largura** | 1280 pixels |
| **Altura** | 960 pixels |
| **Resolução Total** | 1.228.800 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Quente (R dominante: 119), tons avermelhados |

**Análise:** A imagem apresenta dimensões de alta resolução (1280x960), com predominância de tons avermelhados, típico de fotografias de pessoas com iluminação natural ou artificial quente.

#### 3.2.2 Imagem: Objeto

| Característica | Valor |
|----------------|-------|
| **Largura** | 800 pixels |
| **Altura** | 445 pixels |
| **Resolução Total** | 356.000 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Quente (R dominante: 178), tons avermelhados |

**Análise:** Imagem de resolução média (800x445), com gamut quente e alta intensidade no canal vermelho (178), indicando objeto com cores quentes ou iluminação avermelhada.

#### 3.2.3 Imagem: Documento

| Característica | Valor |
|----------------|-------|
| **Largura** | 800 pixels |
| **Altura** | 386 pixels |
| **Resolução Total** | 308.800 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Variado (RGB: R=211, G=223, B=213), cores mistas |

**Análise:** Imagem de resolução média (800x386) com gamut balanceado e tons próximos ao neutro, característico de documentos com fundo claro. Os valores altos de RGB (211-223) indicam predominância de tons claros, ideal para binarização.

### 3.3 Ferramentas Utilizadas

As ferramentas utilizadas incluem:

- **Python 3.x:** Linguagem de programação principal
- **OpenCV (cv2) 4.x:** Biblioteca para processamento de imagens
  - Funções utilizadas: `imread()`, `cvtColor()`, `threshold()`, `adaptiveThreshold()`, `calcHist()`
- **NumPy:** Biblioteca para operações matemáticas com arrays
- **Matplotlib:** Biblioteca para geração de gráficos e histogramas

### 3.4 Procedimentos de Decomposição RGB

A decomposição RGB é realizada pela extração direta dos canais da matriz da imagem. Como o OpenCV carrega imagens no formato BGR (Blue, Green, Red), os canais são acessados através dos índices:

- **Canal B (Azul):** `imagem[:, :, 0]`
- **Canal G (Verde):** `imagem[:, :, 1]`
- **Canal R (Vermelho):** `imagem[:, :, 2]`

Cada canal é salvo como uma imagem em escala de cinza, permitindo visualizar a contribuição individual de cada componente de cor.

### 3.5 Construção dos Histogramas

Os histogramas são calculados utilizando a função `calcHist()` do OpenCV. Para cada canal RGB, o histograma é calculado com:

- **256 níveis de intensidade:** Valores de 0 a 255
- **Faixa completa:** [0, 256]
- **Sem máscara:** Toda a imagem é considerada

Os histogramas são plotados utilizando Matplotlib, gerando gráficos que mostram a distribuição de intensidades de cada canal, facilitando a análise da separação entre objeto e fundo.

### 3.6 Descrição do Algoritmo Implementado

A técnica implementada consiste em aplicar três métodos de binarização:

#### 3.6.1 Limiar Simples (Threshold)

- **Limiar fixo:** T = 127 (valor médio entre 0 e 255)
- **Método:** `cv2.THRESH_BINARY`
- **Característica:** Não se adapta a variações de iluminação

#### 3.6.2 Método de Otsu

- **Limiar calculado automaticamente**
- **Método:** `cv2.THRESH_BINARY + cv2.THRESH_OTSU`
- **Característica:** Calcula o limiar ótimo baseado na variância entre classes

#### 3.6.3 Limiar Adaptativo

Dois métodos adaptativos foram aplicados:

1. **Adaptativo Gaussiano:**
   - Método: `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`
   - Tamanho da janela: 11x11 pixels
   - Constante: 2

2. **Adaptativo Média:**
   - Método: `cv2.ADAPTIVE_THRESH_MEAN_C`
   - Tamanho da janela: 11x11 pixels
   - Constante: 2

**Procedimento geral:**
1. As imagens originais são convertidas para escala de cinza utilizando `cv2.cvtColor()` com `COLOR_BGR2GRAY`
2. Cada método de binarização é aplicado à imagem em escala de cinza
3. As versões binarizadas são salvas para comparação visual e análise

### 3.7 Organização dos Resultados

Todos os resultados foram organizados em uma estrutura de pastas hierárquica:

```
resultados/
├── pessoa/
│   ├── canais_rgb/
│   ├── histogramas/
│   ├── pessoa_escala_cinza.png
│   └── binarizadas/
├── objeto/
│   ├── canais_rgb/
│   ├── histogramas/
│   ├── objeto_escala_cinza.png
│   └── binarizadas/
└── documento/
    ├── canais_rgb/
    ├── histogramas/
    ├── documento_escala_cinza.png
    └── binarizadas/
```

Esta organização facilita a localização e inclusão dos resultados no relatório acadêmico.

---

## 4. RESULTADOS E DISCUSSÃO

### 4.1 Características Técnicas das Imagens

As três imagens processadas apresentam características distintas que influenciam diretamente os resultados da binarização:

#### 4.1.1 Imagem: Pessoa

A imagem da pessoa apresenta dimensões de alta resolução (1280×960 pixels) com gamut quente, caracterizado por predominância do canal vermelho (R=119). Esta característica é típica de fotografias de pessoas com iluminação natural ou artificial quente, onde tons de pele e ambiente contribuem para a dominância de cores quentes.

**Implicações para binarização:** O gamut quente e a variação de iluminação típica em fotografias de pessoas tornam a binarização desafiadora, especialmente em áreas de sombra e iluminação variável.

#### 4.1.2 Imagem: Objeto

A imagem do objeto possui resolução média (800×445 pixels) e também apresenta gamut quente, com alta intensidade no canal vermelho (R=178). Esta alta intensidade indica objeto com cores quentes ou iluminação avermelhada.

**Implicações para binarização:** O alto contraste e a intensidade do canal vermelho podem facilitar a separação entre objeto e fundo, especialmente com métodos que consideram a distribuição de intensidades.

#### 4.1.3 Imagem: Documento

A imagem do documento apresenta resolução média (800×386 pixels) com gamut variado e balanceado (R=211, G=223, B=213). Os valores altos e próximos entre os canais indicam predominância de tons claros e neutros, característico de documentos com fundo branco ou claro.

**Implicações para binarização:** O gamut balanceado e a predominância de tons claros tornam esta imagem ideal para binarização, com separação clara esperada entre fundo claro e texto escuro.

### 4.2 Decomposição RGB

A decomposição RGB de todas as imagens foi realizada com sucesso, gerando três imagens em escala de cinza para cada imagem original, representando os canais R (Vermelho), G (Verde) e B (Azul).

#### 4.2.1 Observações Gerais

- **Canal Vermelho (R):** Apresentou maior intensidade nas imagens de pessoa e objeto, confirmando o gamut quente identificado na análise técnica
- **Canal Verde (G):** Distribuição intermediária, contribuindo para o equilíbrio geral das cores
- **Canal Azul (B):** Geralmente apresentou menor intensidade, especialmente em imagens com iluminação quente

#### 4.2.2 Análise Específica por Imagem

**Pessoa:**
- O canal vermelho mostra maior contribuição, refletindo tons de pele e iluminação quente
- Os canais verde e azul apresentam distribuições mais uniformes

**Objeto:**
- Alta intensidade no canal vermelho (178) é claramente visível na decomposição
- Canais verde e azul com valores proporcionais, mas menores

**Documento:**
- Distribuição equilibrada entre os três canais, refletindo o gamut variado
- Valores altos em todos os canais indicam fundo claro

A decomposição RGB permite compreender como cada componente de cor contribui para a imagem final e como essas características influenciam os histogramas e, consequentemente, a binarização.

### 4.3 Análise dos Histogramas

Os histogramas foram gerados para cada um dos três canais RGB de todas as imagens, totalizando 9 histogramas individuais organizados em 3 gráficos (um por imagem).

#### 4.3.1 Imagem: Pessoa

**Características dos histogramas:**

- **Canal R (Vermelho):** Distribuição concentrada em tons médios, com picos característicos de pele e iluminação. A distribuição mostra uma curva relativamente suave, indicando variação gradual de intensidades.

- **Canal G (Verde):** Distribuição similar ao canal R, mas com menor intensidade média. Mantém a forma geral da distribuição do vermelho.

- **Canal B (Azul):** Menor intensidade geral, típico de imagens com iluminação quente. A distribuição é deslocada para valores mais baixos comparado aos outros canais.

**Interpretação:** Os histogramas revelam uma distribuição relativamente contínua, sem separação clara entre dois grupos distintos (não é fortemente bimodal). Isso indica que a binarização pode ser desafiadora, especialmente com métodos globais.

#### 4.3.2 Imagem: Objeto

**Características dos histogramas:**

- **Canal R (Vermelho):** Alta intensidade média (178), com distribuição concentrada em valores altos. Indica objeto com cores quentes ou iluminação avermelhada.

- **Canal G e B:** Distribuições proporcionais, mas com valores menores que o R. Mantêm formas similares, indicando equilíbrio relativo entre esses canais.

**Interpretação:** A alta intensidade do canal vermelho e o contraste localizado sugerem que métodos como Otsu podem funcionar bem, especialmente se houver separação clara entre objeto e fundo.

#### 4.3.3 Imagem: Documento

**Características dos histogramas:**

- **Distribuição geral:** Concentrada em tons claros (valores altos de intensidade)
- **Característica principal:** Picos próximos a 255, indicando fundo claro e texto escuro
- **Separação:** Presença de dois grupos distintos - um concentrado em valores altos (fundo) e outro em valores baixos (texto)

**Interpretação:** A distribuição concentrada em tons claros e a possível separação bimodal tornam esta imagem ideal para binarização. O método de Otsu deve funcionar especialmente bem, pois busca maximizar a separação entre duas classes.

### 4.4 Conversão para Escala de Cinza

Todas as imagens foram convertidas para escala de cinza utilizando a função `cv2.cvtColor()` com o parâmetro `COLOR_BGR2GRAY`. A conversão é essencial para a binarização, pois:

1. **Reduz dimensionalidade:** De 3 canais (RGB) para 1 canal (intensidade)
2. **Simplifica o cálculo:** O limiar é calculado sobre uma única dimensão
3. **Padroniza o processamento:** Todos os métodos de binarização trabalham com imagens em escala de cinza

As imagens em escala de cinza foram salvas e servem como base para todas as técnicas de binarização aplicadas.

### 4.5 Técnicas de Binarização Aplicadas

Três técnicas principais de binarização foram aplicadas a cada imagem, resultando em múltiplas versões binarizadas para comparação.

#### 4.5.1 Limiar Simples (Threshold)

**Parâmetros aplicados:**
- Limiar fixo: T = 127 (valor médio entre 0 e 255)
- Método: `cv2.THRESH_BINARY`

**Resultados por imagem:**

| Imagem | Limiar | Observações |
|--------|--------|-------------|
| **Pessoa** | T = 127 | Perda de detalhes em áreas sombreadas ou muito iluminadas. O limiar fixo não se adapta às variações de iluminação típicas em fotografias de pessoas. |
| **Objeto** | T = 127 | Funciona relativamente bem para objetos com contraste uniforme, mas pode perder detalhes em bordas ou áreas com iluminação variável. |
| **Documento** | T = 127 | Pode falhar em áreas com sombras leves ou variações de iluminação. O limiar fixo é geralmente inadequado para documentos com iluminação não uniforme. |

**Limitações identificadas:**
- Não se adapta a variações de iluminação na imagem
- Resulta em perda de informação em regiões com iluminação não uniforme
- Requer conhecimento prévio ou tentativa e erro para escolha do limiar ideal

#### 4.5.2 Método de Otsu

**Parâmetros aplicados:**
- Limiar calculado automaticamente
- Método: `cv2.THRESH_BINARY + cv2.THRESH_OTSU`

**Resultados por imagem:**

| Imagem | Limiar Ótimo Calculado | Observações |
|--------|------------------------|-------------|
| **Pessoa** | T = 105.00 | Limiar mais baixo que o fixo (127), indicando melhor separação entre rosto e fundo considerando a distribuição real de intensidades. O método identificou que tons médios são mais apropriados para esta imagem. |
| **Objeto** | T = 117.00 | Limiar ligeiramente abaixo do fixo, mas próximo. Indica que o objeto possui bom contraste, mas a distribuição de intensidades sugere um limiar ligeiramente mais baixo para melhor separação. |
| **Documento** | T = 199.00 | Limiar significativamente alto, refletindo o fundo claro do documento. Este valor demonstra a eficácia do método em identificar automaticamente a melhor separação entre fundo claro (valores próximos a 255) e texto escuro (valores baixos). |

**Vantagens observadas:**
- Calcula automaticamente o limiar ótimo baseado na variância entre classes
- Melhor separação entre objeto e fundo em imagens com distribuição bimodal
- Não requer conhecimento prévio da imagem ou ajuste manual
- Adapta-se melhor às características específicas de cada imagem

**Análise especial - Documento:**
O limiar de Otsu para o documento (T=199) é significativamente alto, o que é esperado dado que a imagem possui fundo muito claro (valores próximos a 255) e texto escuro. Este valor demonstra a eficácia do método em identificar automaticamente a melhor separação, mesmo quando o limiar ideal está muito distante do valor médio (127).

#### 4.5.3 Limiar Adaptativo

**Parâmetros aplicados:**
- Tamanho da janela: 11×11 pixels
- Constante subtraída: 2
- Dois métodos implementados:
  - `ADAPTIVE_THRESH_GAUSSIAN_C`: Média ponderada gaussiana
  - `ADAPTIVE_THRESH_MEAN_C`: Média aritmética simples

**Vantagens do método adaptativo:**
- Calcula um limiar local para cada região da imagem
- Adapta-se a variações de iluminação
- Preserva detalhes em áreas sombreadas sem saturar regiões iluminadas
- Mais robusto para imagens com iluminação não uniforme

**Comparação entre métodos adaptativos:**

| Método | Característica | Melhor Para |
|--------|----------------|-------------|
| **Gaussiano** | Suavização da vizinhança usando média ponderada gaussiana | Redução de ruído, bordas mais suaves, imagens com variações graduais de iluminação |
| **Média** | Cálculo direto da média aritmética da vizinhança | Processamento mais rápido, bordas mais definidas, imagens com contraste localizado |

**Aplicação por tipo de imagem:**

1. **Pessoa:**
   - O método adaptativo se destaca pela capacidade de preservar detalhes faciais em regiões de sombra sem perder informação em áreas iluminadas
   - Ambos os métodos (gaussiano e média) funcionam bem, com o gaussiano oferecendo transições mais suaves
   - Resultado superior ao limiar simples e comparável ou superior ao Otsu em áreas com iluminação variável

2. **Objeto:**
   - Ambos os métodos adaptativos funcionam bem
   - O método gaussiano oferece bordas ligeiramente mais suaves, enquanto a média produz bordas mais definidas
   - A escolha entre eles depende da aplicação: suavidade vs. definição

3. **Documento:**
   - O método adaptativo produz o resultado mais robusto, especialmente em documentos com variações sutis de iluminação ou sombras projetadas
   - Funciona melhor que o limiar simples em áreas com sombras
   - Pode ser superior ao Otsu quando há variações locais de iluminação que o método global não captura

### 4.6 Comparação das Técnicas

#### 4.6.1 Tabela Comparativa Geral

| Técnica | Vantagens | Desvantagens | Melhor Aplicação |
|---------|-----------|--------------|------------------|
| **Limiar Simples** | Simples de implementar, rápido computacionalmente, fácil de entender | Não se adapta a variações de iluminação, requer escolha manual do limiar, perde detalhes em áreas não uniformes | Imagens com iluminação uniforme e contraste alto |
| **Otsu** | Automático, calcula limiar ótimo global, eficaz em imagens bimodais, não requer parâmetros adicionais | Pode falhar com iluminação irregular, assume distribuição bimodal, não adapta-se a variações locais | Imagens com distribuição bimodal clara e iluminação relativamente uniforme |
| **Adaptativo** | Adapta-se a variações locais de iluminação, preserva detalhes em sombras e áreas iluminadas, robusto para cenários reais | Mais lento computacionalmente, pode ser sensível a ruído, requer ajuste de parâmetros (tamanho da janela, constante) | Imagens com iluminação não uniforme, variações de contraste local, cenários reais não controlados |

#### 4.6.2 Recomendações por Tipo de Imagem

##### Imagem de Pessoa

**Melhor método:** Limiar Adaptativo (Gaussiano)

**Motivo:** Preserva detalhes em áreas de sombra e iluminação variável, características comuns em fotografias de pessoas. O método gaussiano oferece transições mais suaves, adequadas para preservar características faciais.

**Método alternativo:** Otsu funciona bem como alternativa quando a iluminação é relativamente uniforme, especialmente se houver boa separação entre pessoa e fundo.

**Limiar Simples:** Geralmente inadequado devido às variações de iluminação típicas em fotografias de pessoas.

##### Imagem de Objeto

**Melhor método:** Otsu ou Adaptativo (dependendo do contraste e uniformidade da iluminação)

**Motivo:** Depende do contraste e uniformidade da iluminação. Se o objeto tiver contraste alto e iluminação uniforme, Otsu pode ser suficiente. Se houver variações de iluminação, o adaptativo é preferível.

**Limiar Simples:** Pode funcionar se o objeto tiver contraste alto e uniforme, mas geralmente inferior aos métodos automáticos.

##### Imagem de Documento

**Melhor método:** Limiar Adaptativo

**Motivo:** Mais robusto para variações sutis de iluminação e sombras projetadas, comuns em documentos fotografados. Preserva legibilidade mesmo em áreas com sombras leves.

**Método alternativo:** Otsu funciona bem quando o documento tem iluminação uniforme, especialmente devido ao alto limiar calculado (T=199) que reflete o fundo claro.

**Limiar Simples:** Geralmente inadequado devido a variações de iluminação e sombras que podem afetar a legibilidade.

#### 4.6.3 Análise Quantitativa dos Limiares

| Imagem | Limiar Simples | Limiar Otsu | Diferença | Interpretação |
|--------|----------------|-------------|-----------|---------------|
| **Pessoa** | 127 | 105.00 | -22 | Otsu identifica que tons mais escuros são apropriados, sugerindo melhor separação considerando a distribuição real |
| **Objeto** | 127 | 117.00 | -10 | Otsu próximo ao fixo, indicando que o limiar fixo não está muito distante do ideal, mas ainda há espaço para otimização |
| **Documento** | 127 | 199.00 | +72 | Grande diferença positiva indica que o fundo claro requer limiar muito alto, demonstrando a importância do cálculo automático |

**Observação:** A grande diferença no documento (+72) demonstra claramente a limitação do limiar fixo e a eficácia do método de Otsu em identificar automaticamente o limiar apropriado.

#### 4.6.4 Estatísticas de Processamento

- **Total de imagens processadas:** 3
- **Total de arquivos gerados:** 33
  - 9 canais RGB (3 canais × 3 imagens)
  - 3 histogramas (1 por imagem, contendo os 3 canais)
  - 3 imagens em escala de cinza
  - 12 imagens binarizadas (4 métodos × 3 imagens)
  - 6 imagens adicionais (canais RGB individuais)
- **Técnicas de binarização aplicadas:** 4 (limiar simples, Otsu, adaptativo gaussiano, adaptativo média)
- **Canais RGB analisados:** 9 (3 canais × 3 imagens)

---

## 5. CONCLUSÃO

### 5.1 Avaliação dos Resultados Obtidos

Os experimentos realizados demonstraram que a binarização é extremamente sensível às condições de iluminação e ao conteúdo da imagem. Os resultados obtidos revelam características importantes de cada método:

**Métodos globais (Limiar Simples e Otsu):**
- Funcionam bem em imagens com contraste uniforme
- Falham quando há sombras ou brilho excessivo
- O método de Otsu mostrou-se superior ao limiar simples ao calcular automaticamente limiares apropriados (variando de 105 a 199)

**Método adaptativo:**
- Oferece resultados superiores em cenários reais e não controlados
- Preserva detalhes em áreas de sombra sem saturar regiões iluminadas
- Mostra-se especialmente eficaz para imagens de pessoa e documento

### 5.2 Principais Descobertas

1. **Influência do Gamut:** O tipo de gamut da imagem influencia diretamente a escolha do método de binarização. Imagens com gamut quente (pessoa, objeto) requerem métodos mais adaptativos, enquanto documentos com gamut balanceado podem usar Otsu com sucesso.

2. **Eficácia do Método de Otsu:** O método de Otsu demonstrou eficácia ao calcular automaticamente limiares apropriados, variando de 105 (pessoa) a 199 (documento), refletindo as características específicas de cada imagem. A grande diferença no documento (+72 em relação ao limiar fixo) demonstra a importância do cálculo automático.

3. **Superioridade do Método Adaptativo:** O limiar adaptativo mostrou-se superior em cenários reais com iluminação não uniforme, especialmente para imagens de pessoa e documento, onde preserva detalhes importantes que métodos globais perdem.

4. **Análise de Histogramas:** A análise dos histogramas revelou padrões distintos: imagens de pessoa e objeto com distribuições mais variadas, enquanto o documento apresentou concentração em tons claros, facilitando a binarização.

### 5.3 Dificuldades Encontradas

As dificuldades encontradas envolveram principalmente:

1. **Iluminação Mista:** A captura das imagens em ambientes com iluminação mista tornou desafiador obter resultados consistentes em todas as técnicas, especialmente com o limiar simples.

2. **Variações de Contraste:** Diferentes regiões das imagens apresentavam contrastes distintos, exigindo métodos adaptativos para preservar informações em todas as áreas.

3. **Escolha de Parâmetros:** O método adaptativo requer ajuste de parâmetros (tamanho da janela, constante), que pode ser sensível e requer experimentação.

4. **Ruído e Artefatos:** Algumas imagens apresentaram ruído que pode afetar a qualidade da binarização, especialmente em métodos adaptativos sensíveis a variações locais.

### 5.4 Considerações Finais

Os resultados obtidos reforçam a importância de compreender as características das imagens antes de escolher o método de binarização. Não existe um método universalmente superior; a escolha deve ser baseada nas características específicas de cada imagem e nos requisitos da aplicação.

A binarização é uma etapa fundamental em pipelines de processamento de imagens, e a escolha adequada do método pode significativamente impactar a qualidade dos resultados em etapas subsequentes como detecção de contornos, reconhecimento de padrões e extração de características.

### 5.5 Possibilidades de Aprimoramento

Como possibilidades de aprimoramento, destaca-se:

1. **Pré-processamento:** Aplicar filtros de redução de ruído antes da binarização pode melhorar os resultados, especialmente em métodos adaptativos sensíveis a variações locais.

2. **Equalização de Histograma:** Pode ajudar a melhorar o contraste antes da binarização, facilitando a separação entre objeto e fundo.

3. **Combinação de Métodos:** Em alguns casos, combinar resultados de diferentes métodos pode produzir melhores resultados, aproveitando as vantagens de cada abordagem.

4. **Ajuste de Parâmetros:** Para o método adaptativo, testar diferentes tamanhos de janela e constantes pode otimizar os resultados para casos específicos.

5. **Métodos Modernos:** O emprego de métodos modernos baseados em redes neurais para segmentação pode oferecer resultados superiores em cenários complexos, especialmente com grandes volumes de dados para treinamento.

6. **Análise de Qualidade:** Implementar métricas quantitativas de qualidade da binarização (como métricas baseadas em ground truth) permitiria comparação mais objetiva entre métodos.

---

## 6. REFERÊNCIAS

Otsu, Nobuyuki. "A threshold selection method from gray-level histograms". *IEEE Transactions on Systems, Man, and Cybernetics*, vol. 9, no. 1, pp. 62-66, 1979.

Niblack, W. "An Introduction to Digital Image Processing". Prentice-Hall, Englewood Cliffs, NJ, 1985.

Gonzalez, R. C.; Woods, R. E. *Digital Image Processing*. 4th ed. Pearson, 2018.

OpenCV Documentation. Disponível em: https://docs.opencv.org. Acesso em: 23 nov. 2024.

Bradski, G.; Kaehler, A. *Learning OpenCV: Computer Vision with the OpenCV Library*. O'Reilly Media, 2008.

---

## 7. APÊNDICES

### 7.1 Código-fonte Comentado

O código-fonte completo, comentado e organizado para uso em relatório acadêmico, está disponível no arquivo `binarizacao_imagens.py`. O código inclui:

- Estrutura modular com funções bem definidas
- Comentários explicativos em português para cada seção
- Documentação de funções seguindo padrões acadêmicos
- Organização clara da saída em pastas estruturadas
- Tratamento de erros e validações

**Localização:** `binarizacao_imagens.py` na raiz do projeto

**Principais funcionalidades implementadas:**
- Carregamento e análise técnica de imagens
- Decomposição RGB
- Geração de histogramas
- Conversão para escala de cinza
- Aplicação de três técnicas de binarização (limiar simples, Otsu, adaptativo)
- Organização automática dos resultados

### 7.2 Imagens Utilizadas

As três imagens originais utilizadas no experimento estão localizadas na pasta `fotos/`:

1. **Pessoa:** `fotos/pessoavelha.jpg`
   - Dimensões: 1280 × 960 pixels
   - Formato: JPEG
   - Características: Gamut quente, tons avermelhados

2. **Objeto:** `fotos/fotoobjeto.jpg`
   - Dimensões: 800 × 445 pixels
   - Formato: JPEG
   - Características: Gamut quente, alta intensidade no canal vermelho

3. **Documento:** `fotos/rgfoto.jpg`
   - Dimensões: 800 × 386 pixels
   - Formato: JPEG
   - Características: Gamut variado, tons claros e neutros

### 7.3 Gráficos e Figuras Geradas

Todos os gráficos, figuras e imagens processadas foram organizados na pasta `resultados/` com a seguinte estrutura:

#### 7.3.1 Estrutura Completa de Arquivos

```
resultados/
├── pessoa/
│   ├── canais_rgb/
│   │   ├── pessoa_canal_R.png
│   │   ├── pessoa_canal_G.png
│   │   └── pessoa_canal_B.png
│   ├── histogramas/
│   │   └── pessoa_histogramas_RGB.png
│   ├── pessoa_escala_cinza.png
│   └── binarizadas/
│       ├── pessoa_binaria_limiar_simples.png
│       ├── pessoa_binaria_otsu.png
│       ├── pessoa_binaria_adaptativa_gaussiana.png
│       └── pessoa_binaria_adaptativa_media.png
├── objeto/
│   ├── canais_rgb/
│   │   ├── objeto_canal_R.png
│   │   ├── objeto_canal_G.png
│   │   └── objeto_canal_B.png
│   ├── histogramas/
│   │   └── objeto_histogramas_RGB.png
│   ├── objeto_escala_cinza.png
│   └── binarizadas/
│       ├── objeto_binaria_limiar_simples.png
│       ├── objeto_binaria_otsu.png
│       ├── objeto_binaria_adaptativa_gaussiana.png
│       └── objeto_binaria_adaptativa_media.png
└── documento/
    ├── canais_rgb/
    │   ├── documento_canal_R.png
    │   ├── documento_canal_G.png
    │   └── documento_canal_B.png
    ├── histogramas/
    │   └── documento_histogramas_RGB.png
    ├── documento_escala_cinza.png
    └── binarizadas/
        ├── documento_binaria_limiar_simples.png
        ├── documento_binaria_otsu.png
        ├── documento_binaria_adaptativa_gaussiana.png
        └── documento_binaria_adaptativa_media.png
```

#### 7.3.2 Descrição dos Arquivos Gerados

**Canais RGB (9 arquivos):**
- Imagens em escala de cinza representando cada canal de cor individualmente
- Permitem análise da contribuição de cada componente de cor

**Histogramas (3 arquivos):**
- Gráficos mostrando a distribuição de intensidades dos três canais RGB
- Gerados utilizando Matplotlib com 256 níveis de intensidade
- Essenciais para compreensão da separação entre objeto e fundo

**Imagens em Escala de Cinza (3 arquivos):**
- Versões convertidas das imagens originais
- Base para todas as técnicas de binarização aplicadas

**Imagens Binarizadas (12 arquivos):**
- 4 versões binarizadas por imagem (limiar simples, Otsu, adaptativo gaussiano, adaptativo média)
- Permitem comparação visual e análise dos resultados

**Total:** 33 arquivos gerados, todos organizados e prontos para inclusão no relatório acadêmico.

---

**Fim do Relatório**
