"""
Programa de Binarização de Imagens utilizando OpenCV
=====================================================

Este programa realiza análise técnica, decomposição RGB, geração de histogramas
e aplicação de técnicas de binarização em três imagens: pessoa, objeto e documento.

Autor: [Preencher com nome]
Data: [Preencher com data]
"""

import cv2
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Backend sem interface gráfica para ambientes headless
import matplotlib.pyplot as plt
from pathlib import Path


def criar_estrutura_pastas():
    """
    Cria a estrutura de pastas para organizar os resultados.
    
    Estrutura criada:
    - resultados/
      - pessoa/
        - canais_rgb/
        - histogramas/
        - binarizadas/
      - objeto/
        - canais_rgb/
        - histogramas/
        - binarizadas/
      - documento/
        - canais_rgb/
        - histogramas/
        - binarizadas/
    """
    base_dir = Path("resultados")
    tipos_imagem = ["pessoa", "objeto", "documento"]
    
    for tipo in tipos_imagem:
        (base_dir / tipo / "canais_rgb").mkdir(parents=True, exist_ok=True)
        (base_dir / tipo / "histogramas").mkdir(parents=True, exist_ok=True)
        (base_dir / tipo / "binarizadas").mkdir(parents=True, exist_ok=True)
    
    return base_dir


def obter_tipo_paleta(imagem):
    """
    Determina o tipo de paleta de cores da imagem.
    
    Args:
        imagem: Array numpy da imagem
        
    Returns:
        String descrevendo o tipo de paleta
    """
    if len(imagem.shape) == 2:
        return "Escala de Cinza"
    elif len(imagem.shape) == 3:
        if imagem.shape[2] == 3:
            return "RGB (3 canais)"
        elif imagem.shape[2] == 4:
            return "RGBA (4 canais com transparência)"
    return "Desconhecido"


def descrever_gamut(imagem):
    """
    Fornece uma descrição aproximada do gamut (faixa de cores) da imagem.
    
    Args:
        imagem: Array numpy da imagem
        
    Returns:
        String descrevendo o gamut aproximado
    """
    if len(imagem.shape) == 2:
        # Imagem em escala de cinza
        min_val = np.min(imagem)
        max_val = np.max(imagem)
        media = np.mean(imagem)
        
        if max_val - min_val < 50:
            return f"Gamut restrito (variação: {max_val - min_val:.0f}), imagem de baixo contraste"
        elif media < 85:
            return f"Gamut escuro (média: {media:.0f}), predominância de tons escuros"
        elif media > 170:
            return f"Gamut claro (média: {media:.0f}), predominância de tons claros"
        else:
            return f"Gamut balanceado (média: {media:.0f}), distribuição equilibrada de tons"
    else:
        # Imagem colorida
        media_r = np.mean(imagem[:, :, 2])  # OpenCV usa BGR
        media_g = np.mean(imagem[:, :, 1])
        media_b = np.mean(imagem[:, :, 0])
        
        if abs(media_r - media_g) < 10 and abs(media_g - media_b) < 10:
            return f"Gamut neutro (RGB médio: R={media_r:.0f}, G={media_g:.0f}, B={media_b:.0f}), tons próximos ao cinza"
        elif media_r > media_g and media_r > media_b:
            return f"Gamut quente (R dominante: {media_r:.0f}), tons avermelhados"
        elif media_b > media_r and media_b > media_g:
            return f"Gamut frio (B dominante: {media_b:.0f}), tons azulados"
        else:
            return f"Gamut variado (RGB: R={media_r:.0f}, G={media_g:.0f}, B={media_b:.0f}), cores mistas"


def exibir_caracteristicas_tecnicas(imagem, nome_imagem):
    """
    Exibe as características técnicas da imagem no console.
    
    Args:
        imagem: Array numpy da imagem
        nome_imagem: Nome da imagem para exibição
    """
    altura, largura = imagem.shape[:2]
    num_canais = 1 if len(imagem.shape) == 2 else imagem.shape[2]
    tipo_paleta = obter_tipo_paleta(imagem)
    descricao_gamut = descrever_gamut(imagem)
    
    print(f"\n{'='*60}")
    print(f"CARACTERÍSTICAS TÉCNICAS: {nome_imagem.upper()}")
    print(f"{'='*60}")
    print(f"Largura: {largura} pixels")
    print(f"Altura: {altura} pixels")
    print(f"Número de canais: {num_canais}")
    print(f"Tipo de paleta: {tipo_paleta}")
    print(f"Descrição do gamut: {descricao_gamut}")
    print(f"{'='*60}\n")


def decompor_canais_rgb(imagem, caminho_saida, nome_base):
    """
    Decompõe a imagem nos canais R, G e B e salva cada canal como imagem separada.
    
    Args:
        imagem: Array numpy da imagem colorida (BGR)
        caminho_saida: Caminho da pasta onde salvar os canais
        nome_base: Nome base para os arquivos de saída
    """
    # OpenCV carrega imagens em BGR, então os índices são invertidos
    canal_b = imagem[:, :, 0]  # Canal Azul (Blue)
    canal_g = imagem[:, :, 1]  # Canal Verde (Green)
    canal_r = imagem[:, :, 2]  # Canal Vermelho (Red)
    
    # Salva cada canal como imagem em escala de cinza
    cv2.imwrite(str(caminho_saida / f"{nome_base}_canal_R.png"), canal_r)
    cv2.imwrite(str(caminho_saida / f"{nome_base}_canal_G.png"), canal_g)
    cv2.imwrite(str(caminho_saida / f"{nome_base}_canal_B.png"), canal_b)
    
    print(f"  ✓ Canais RGB salvos em: {caminho_saida}")


def gerar_histogramas_rgb(imagem, caminho_saida, nome_base):
    """
    Gera e salva os histogramas dos três canais RGB da imagem.
    
    Args:
        imagem: Array numpy da imagem colorida (BGR)
        caminho_saida: Caminho da pasta onde salvar os histogramas
        nome_base: Nome base para os arquivos de saída
    """
    # Separa os canais
    canal_b = imagem[:, :, 0]
    canal_g = imagem[:, :, 1]
    canal_r = imagem[:, :, 2]
    
    # Calcula os histogramas usando calcHist do OpenCV
    # Parâmetros: [imagem], [canal], máscara (None = toda imagem), 
    # [tamanho do histograma], [faixa de valores]
    hist_r = cv2.calcHist([canal_r], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([canal_g], [0], None, [256], [0, 256])
    hist_b = cv2.calcHist([canal_b], [0], None, [256], [0, 256])
    
    # Cria a figura com três subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Plota histograma do canal R
    axes[0].plot(hist_r, color='red', linewidth=1.5)
    axes[0].set_title('Histograma - Canal R (Vermelho)')
    axes[0].set_xlabel('Intensidade')
    axes[0].set_ylabel('Frequência')
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim([0, 255])
    
    # Plota histograma do canal G
    axes[1].plot(hist_g, color='green', linewidth=1.5)
    axes[1].set_title('Histograma - Canal G (Verde)')
    axes[1].set_xlabel('Intensidade')
    axes[1].set_ylabel('Frequência')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim([0, 255])
    
    # Plota histograma do canal B
    axes[2].plot(hist_b, color='blue', linewidth=1.5)
    axes[2].set_title('Histograma - Canal B (Azul)')
    axes[2].set_xlabel('Intensidade')
    axes[2].set_ylabel('Frequência')
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim([0, 255])
    
    plt.tight_layout()
    plt.savefig(str(caminho_saida / f"{nome_base}_histogramas_RGB.png"), dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Histogramas RGB salvos em: {caminho_saida}")


def aplicar_binarizacoes(imagem_cinza, caminho_saida, nome_base):
    """
    Aplica três técnicas de binarização: limiar simples, Otsu e limiar adaptativo.
    
    Args:
        imagem_cinza: Array numpy da imagem em escala de cinza
        caminho_saida: Caminho da pasta onde salvar as imagens binarizadas
        nome_base: Nome base para os arquivos de saída
    """
    # 1. Binarização com Limiar Simples (Threshold)
    # Calcula a média dos valores de intensidade como limiar
    limiar_manual = 127  # Valor médio comum para limiarização
    _, binaria_simples = cv2.threshold(imagem_cinza, limiar_manual, 255, cv2.THRESH_BINARY)
    cv2.imwrite(str(caminho_saida / f"{nome_base}_binaria_limiar_simples.png"), binaria_simples)
    
    # 2. Binarização com Método de Otsu
    # Otsu calcula automaticamente o limiar ótimo baseado na variância entre classes
    # cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU: combina inversão com Otsu
    limiar_otsu, binaria_otsu = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(str(caminho_saida / f"{nome_base}_binaria_otsu.png"), binaria_otsu)
    
    # 3. Binarização com Limiar Adaptativo
    # Calcula um limiar local para cada pixel baseado em uma janela ao redor
    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C: usa média ponderada gaussiana da vizinhança
    # cv2.ADAPTIVE_THRESH_MEAN_C: usa média aritmética simples da vizinhança
    # 11: tamanho da janela de vizinhança (deve ser ímpar)
    # 2: constante subtraída da média
    binaria_adaptativa_gauss = cv2.adaptiveThreshold(
        imagem_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    cv2.imwrite(str(caminho_saida / f"{nome_base}_binaria_adaptativa_gaussiana.png"), binaria_adaptativa_gauss)
    
    binaria_adaptativa_media = cv2.adaptiveThreshold(
        imagem_cinza, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    cv2.imwrite(str(caminho_saida / f"{nome_base}_binaria_adaptativa_media.png"), binaria_adaptativa_media)
    
    print(f"  ✓ Imagens binarizadas salvas em: {caminho_saida}")
    print(f"    - Limiar simples (T={limiar_manual})")
    print(f"    - Otsu (T={limiar_otsu:.2f})")
    print(f"    - Adaptativa (Gaussiana e Média)")


def processar_imagem(caminho_imagem, tipo_imagem, base_dir):
    """
    Processa uma imagem completa: análise, decomposição, histogramas e binarização.
    
    Args:
        caminho_imagem: Caminho para o arquivo de imagem
        tipo_imagem: Tipo da imagem (pessoa, objeto ou documento)
        base_dir: Diretório base de resultados
    """
    print(f"\n{'#'*60}")
    print(f"PROCESSANDO: {tipo_imagem.upper()}")
    print(f"{'#'*60}")
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"ERRO: Arquivo não encontrado: {caminho_imagem}")
        return
    
    # Carrega a imagem
    imagem = cv2.imread(caminho_imagem)
    
    if imagem is None:
        print(f"ERRO: Não foi possível carregar a imagem: {caminho_imagem}")
        return
    
    # 1. Exibe características técnicas
    exibir_caracteristicas_tecnicas(imagem, tipo_imagem)
    
    # Define os caminhos de saída
    caminho_tipo = base_dir / tipo_imagem
    caminho_canais = caminho_tipo / "canais_rgb"
    caminho_histogramas = caminho_tipo / "histogramas"
    caminho_binarizadas = caminho_tipo / "binarizadas"
    
    # 2. Decompõe nos canais RGB
    print("Decompondo imagem nos canais RGB...")
    decompor_canais_rgb(imagem, caminho_canais, tipo_imagem)
    
    # 3. Gera histogramas RGB
    print("Gerando histogramas dos canais RGB...")
    gerar_histogramas_rgb(imagem, caminho_histogramas, tipo_imagem)
    
    # 4. Converte para escala de cinza
    print("Convertendo para escala de cinza...")
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(str(caminho_tipo / f"{tipo_imagem}_escala_cinza.png"), imagem_cinza)
    print(f"  ✓ Imagem em escala de cinza salva")
    
    # 5. Aplica técnicas de binarização
    print("Aplicando técnicas de binarização...")
    aplicar_binarizacoes(imagem_cinza, caminho_binarizadas, tipo_imagem)
    
    print(f"\n✓ Processamento de '{tipo_imagem}' concluído com sucesso!\n")


def main():
    """
    Função principal do programa.
    Coordena o carregamento e processamento das três imagens.
    """
    print("="*60)
    print("PROGRAMA DE BINARIZAÇÃO DE IMAGENS - OpenCV")
    print("="*60)
    
    # Cria a estrutura de pastas
    print("\nCriando estrutura de pastas...")
    base_dir = criar_estrutura_pastas()
    print(f"✓ Estrutura criada em: {base_dir}")
    
    # Define os caminhos das imagens de entrada na pasta 'fotos'
    imagens = {
        "pessoa": "fotos/pessoavelha.jpg",
        "objeto": "fotos/fotoobjeto.jpg",
        "documento": "fotos/rgfoto.jpg"
    }
    
    # Processa cada imagem
    for tipo, caminho_imagem in imagens.items():
        if os.path.exists(caminho_imagem):
            processar_imagem(caminho_imagem, tipo, base_dir)
        else:
            print(f"\nAVISO: Imagem '{tipo}' não encontrada.")
            print(f"  Procurando em: {caminho_imagem}\n")
    
    print("="*60)
    print("PROCESSAMENTO CONCLUÍDO!")
    print("="*60)
    print(f"\nTodos os resultados foram salvos em: {base_dir.absolute()}")
    print("\nEstrutura de saída:")
    print("  resultados/")
    print("    ├── pessoa/")
    print("    │   ├── canais_rgb/")
    print("    │   ├── histogramas/")
    print("    │   └── binarizadas/")
    print("    ├── objeto/")
    print("    │   ├── canais_rgb/")
    print("    │   ├── histogramas/")
    print("    │   └── binarizadas/")
    print("    └── documento/")
    print("        ├── canais_rgb/")
    print("        ├── histogramas/")
    print("        └── binarizadas/")
    print()


if __name__ == "__main__":
    main()

