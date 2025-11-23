# Relatório de Resultados - Binarização de Imagens

## Resumo Executivo

Este relatório apresenta os resultados obtidos através do processamento de três imagens utilizando técnicas de binarização implementadas em Python com OpenCV. As imagens processadas foram: uma fotografia de pessoa, uma de objeto e uma de documento.

---

## 1. Características Técnicas das Imagens

### 1.1 Imagem: Pessoa

| Característica | Valor |
|----------------|-------|
| **Largura** | 1280 pixels |
| **Altura** | 960 pixels |
| **Resolução Total** | 1.228.800 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Quente (R dominante: 119), tons avermelhados |

**Análise:** A imagem apresenta dimensões padrão de alta resolução (1280x960), com predominância de tons avermelhados, típico de fotografias de pessoas com iluminação natural ou artificial quente.

### 1.2 Imagem: Objeto

| Característica | Valor |
|----------------|-------|
| **Largura** | 800 pixels |
| **Altura** | 445 pixels |
| **Resolução Total** | 356.000 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Quente (R dominante: 178), tons avermelhados |

**Análise:** Imagem de resolução média (800x445), também com gamut quente e alta intensidade no canal vermelho (178), indicando objeto com cores quentes ou iluminação avermelhada.

### 1.3 Imagem: Documento

| Característica | Valor |
|----------------|-------|
| **Largura** | 800 pixels |
| **Altura** | 386 pixels |
| **Resolução Total** | 308.800 pixels |
| **Número de Canais** | 3 (RGB) |
| **Tipo de Paleta** | RGB (3 canais) |
| **Gamut** | Variado (RGB: R=211, G=223, B=213), cores mistas |

**Análise:** Imagem de resolução média (800x386) com gamut balanceado e tons próximos ao neutro, característico de documentos com fundo claro. Os valores altos de RGB (211-223) indicam predominância de tons claros, ideal para binarização.

---

## 2. Decomposição RGB

### 2.1 Resultados da Decomposição

Todas as três imagens foram decompostas nos canais R (Vermelho), G (Verde) e B (Azul). Os arquivos gerados estão organizados em:

- `resultados/[tipo]/canais_rgb/[tipo]_canal_R.png`
- `resultados/[tipo]/canais_rgb/[tipo]_canal_G.png`
- `resultados/[tipo]/canais_rgb/[tipo]_canal_B.png`

**Observações:**
- A decomposição permite analisar a contribuição individual de cada canal para a imagem final
- O canal vermelho (R) apresentou maior intensidade nas imagens de pessoa e objeto, confirmando o gamut quente
- O documento apresentou distribuição mais equilibrada entre os canais, refletindo seu gamut variado

---

## 3. Histogramas RGB

### 3.1 Análise dos Histogramas

Os histogramas foram gerados para cada um dos três canais RGB de todas as imagens e salvos em:

- `resultados/[tipo]/histogramas/[tipo]_histogramas_RGB.png`

**Características Observadas:**

#### Imagem: Pessoa
- **Canal R:** Distribuição concentrada em tons médios, com picos característicos de pele e iluminação
- **Canal G:** Distribuição similar ao R, mas com menor intensidade média
- **Canal B:** Menor intensidade geral, típico de imagens com iluminação quente

#### Imagem: Objeto
- **Canal R:** Alta intensidade (média 178), indicando objeto com cores quentes
- **Canal G e B:** Distribuições proporcionais, mas com valores menores que o R

#### Imagem: Documento
- **Distribuição:** Concentrada em tons claros (valores altos de intensidade)
- **Característica:** Picos próximos a 255, indicando fundo claro e texto escuro
- **Ideal para binarização:** A separação clara entre fundo e texto facilita o processo de limiaramento

---

## 4. Conversão para Escala de Cinza

Todas as imagens foram convertidas para escala de cinza utilizando a função `cv2.cvtColor()` com o parâmetro `COLOR_BGR2GRAY`. As imagens em escala de cinza foram salvas em:

- `resultados/[tipo]/[tipo]_escala_cinza.png`

**Propósito:** A conversão para escala de cinza é essencial para a binarização, pois reduz a informação de cor a uma única dimensão de intensidade, simplificando o cálculo do limiar.

---

## 5. Técnicas de Binarização Aplicadas

### 5.1 Limiar Simples (Threshold)

**Parâmetros:**
- Limiar fixo: T = 127 (valor médio entre 0 e 255)
- Método: `cv2.THRESH_BINARY`

**Resultados por Imagem:**

| Imagem | Limiar | Observações |
|--------|--------|-------------|
| Pessoa | T = 127 | Pode perder detalhes em áreas sombreadas ou muito iluminadas |
| Objeto | T = 127 | Funciona bem para objetos com contraste uniforme |
| Documento | T = 127 | Pode falhar em áreas com sombras leves ou variações de iluminação |

**Limitações:** O limiar fixo não se adapta às variações de iluminação na imagem, resultando em perda de informação em regiões com iluminação não uniforme.

### 5.2 Método de Otsu

**Parâmetros:**
- Limiar calculado automaticamente
- Método: `cv2.THRESH_BINARY + cv2.THRESH_OTSU`

**Resultados por Imagem:**

| Imagem | Limiar Ótimo | Observações |
|--------|--------------|-------------|
| Pessoa | T = 105.00 | Limiar mais baixo que o fixo, melhor separação entre rosto e fundo |
| Objeto | T = 117.00 | Limiar ligeiramente abaixo do fixo, boa nitidez de bordas |
| Documento | T = 199.00 | Limiar alto, refletindo o fundo claro do documento |

**Vantagens:**
- Calcula automaticamente o limiar ótimo baseado na variância entre classes
- Melhor separação entre objeto e fundo em imagens com distribuição bimodal
- Não requer conhecimento prévio da imagem

**Análise Especial - Documento:**
O limiar de Otsu para o documento (T=199) é significativamente alto, o que é esperado dado que a imagem possui fundo muito claro (valores próximos a 255) e texto escuro. Este valor demonstra a eficácia do método em identificar automaticamente a melhor separação.

### 5.3 Limiar Adaptativo

**Parâmetros:**
- Tamanho da janela: 11x11 pixels
- Constante subtraída: 2
- Métodos aplicados:
  - `ADAPTIVE_THRESH_GAUSSIAN_C`: Média ponderada gaussiana
  - `ADAPTIVE_THRESH_MEAN_C`: Média aritmética simples

**Resultados:**

**Vantagens do Método Adaptativo:**
- Calcula um limiar local para cada região da imagem
- Adapta-se a variações de iluminação
- Preserva detalhes em áreas sombreadas sem saturar regiões iluminadas

**Comparação entre Métodos Adaptativos:**

| Método | Característica | Melhor Para |
|--------|----------------|-------------|
| Gaussiano | Suavização da vizinhança | Redução de ruído, bordas mais suaves |
| Média | Cálculo direto | Processamento mais rápido, bordas mais definidas |

**Aplicação por Tipo de Imagem:**

1. **Pessoa:** O método adaptativo se destaca pela capacidade de preservar detalhes faciais em regiões de sombra sem perder informação em áreas iluminadas.

2. **Objeto:** Ambos os métodos adaptativos funcionam bem, com o gaussiano oferecendo bordas ligeiramente mais suaves.

3. **Documento:** O método adaptativo produz o resultado mais robusto, especialmente em documentos com variações sutis de iluminação ou sombras projetadas.

---

## 6. Comparação das Técnicas

### 6.1 Tabela Comparativa

| Técnica | Vantagens | Desvantagens | Melhor Aplicação |
|---------|-----------|--------------|------------------|
| **Limiar Simples** | Simples, rápido | Não se adapta a variações | Imagens com iluminação uniforme |
| **Otsu** | Automático, ótimo global | Pode falhar com iluminação irregular | Imagens com distribuição bimodal |
| **Adaptativo** | Adapta-se a variações locais | Mais lento, pode ser sensível a ruído | Imagens com iluminação não uniforme |

### 6.2 Recomendações por Tipo de Imagem

#### Imagem de Pessoa
- **Melhor método:** Limiar Adaptativo (Gaussiano)
- **Motivo:** Preserva detalhes em áreas de sombra e iluminação variável
- **Otsu:** Funciona bem como alternativa quando a iluminação é relativamente uniforme

#### Imagem de Objeto
- **Melhor método:** Otsu ou Adaptativo
- **Motivo:** Depende do contraste e uniformidade da iluminação
- **Limiar Simples:** Pode funcionar se o objeto tiver contraste alto e uniforme

#### Imagem de Documento
- **Melhor método:** Limiar Adaptativo
- **Motivo:** Mais robusto para variações sutis de iluminação e sombras
- **Otsu:** Funciona bem quando o documento tem iluminação uniforme
- **Limiar Simples:** Geralmente inadequado devido a variações de iluminação

---

## 7. Estrutura de Arquivos Gerados

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

**Total de arquivos gerados:** 33 arquivos (9 por imagem × 3 imagens + 3 imagens em escala de cinza)

---

## 8. Conclusões

### 8.1 Principais Descobertas

1. **Gamut e Binarização:** O tipo de gamut da imagem influencia diretamente a escolha do método de binarização. Imagens com gamut quente (pessoa, objeto) requerem métodos mais adaptativos, enquanto documentos com gamut balanceado podem usar Otsu com sucesso.

2. **Limiar de Otsu:** O método de Otsu demonstrou eficácia ao calcular automaticamente limiares apropriados, variando de 105 (pessoa) a 199 (documento), refletindo as características específicas de cada imagem.

3. **Método Adaptativo:** O limiar adaptativo mostrou-se superior em cenários reais com iluminação não uniforme, especialmente para imagens de pessoa e documento.

4. **Histogramas:** A análise dos histogramas revelou padrões distintos: imagens de pessoa e objeto com distribuições mais variadas, enquanto o documento apresentou concentração em tons claros, facilitando a binarização.

### 8.2 Limitações Identificadas

1. **Limiar Simples:** Falha em imagens com iluminação não uniforme, resultando em perda de detalhes.

2. **Otsu:** Pode não funcionar bem quando o histograma não apresenta distribuição bimodal clara.

3. **Adaptativo:** Pode ser sensível a ruído e requer ajuste de parâmetros (tamanho da janela, constante).

### 8.3 Recomendações para Aplicações Futuras

1. **Pré-processamento:** Aplicar filtros de redução de ruído antes da binarização pode melhorar os resultados.

2. **Equalização de Histograma:** Pode ajudar a melhorar o contraste antes da binarização.

3. **Combinação de Métodos:** Em alguns casos, combinar resultados de diferentes métodos pode produzir melhores resultados.

4. **Ajuste de Parâmetros:** Para o método adaptativo, testar diferentes tamanhos de janela e constantes pode otimizar os resultados para casos específicos.

---

## 9. Dados Técnicos Resumidos

### 9.1 Valores de Limiar Calculados

| Imagem | Limiar Simples | Limiar Otsu | Observação |
|--------|----------------|-------------|------------|
| Pessoa | 127 | 105.00 | Otsu mais baixo, melhor para tons médios |
| Objeto | 127 | 117.00 | Otsu próximo ao fixo, objeto com bom contraste |
| Documento | 127 | 199.00 | Otsu muito alto, reflete fundo claro |

### 9.2 Estatísticas de Processamento

- **Total de imagens processadas:** 3
- **Total de arquivos gerados:** 33
- **Técnicas de binarização aplicadas:** 4 (limiar simples, Otsu, adaptativo gaussiano, adaptativo média)
- **Canais RGB analisados:** 9 (3 canais × 3 imagens)
- **Histogramas gerados:** 3 (um por imagem, contendo os 3 canais)

---

## 10. Referências dos Arquivos

Todos os arquivos gerados estão disponíveis na pasta `resultados/`, organizados por tipo de imagem e categoria de processamento. Os arquivos podem ser utilizados diretamente no relatório acadêmico como figuras e anexos.

---

**Data de Geração:** [Data atual]  
**Ferramentas Utilizadas:** Python 3.x, OpenCV 4.x, NumPy, Matplotlib  
**Versão do Programa:** 1.0

