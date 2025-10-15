from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Wedge
import numpy as np

app = Flask(__name__, template_folder='.')
CORS(app)


# ======== Funções de Conjuntos =========

def uniao(A, B):
    return list(set(A) | set(B))

def intersecao(A, B):
    return list(set(A) & set(B))

def diferenca(A, B):
    return list(set(A) - set(B))

def diferenca_b(A, B):
    return list(set(B) - set(A))

def simetrica(A, B):
    return list(set(A) ^ set(B))

def cartesiano(A, B):
    return [f"({a}, {b})" for a in A for b in B]


# ======== Geração do Diagrama de Venn =========

def gerar_diagrama(A, B, operacao="uniao"):
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.2, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Fundo branco suave
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    
    set_A = set(A)
    set_B = set(B)
    
    apenas_A = set_A - set_B
    apenas_B = set_B - set_A
    inter = set_A & set_B
    
    # Posições dos círculos
    pos_A = (-0.6, 0)
    pos_B = (0.6, 0)
    raio = 1.2
    
    # NOVA PALETA HARMÔNICA: Rosa pastel + Azul pastel + Roxo claro
    cor_A = '#F49AC2'           # Rosa suave
    cor_B = '#A7C7E7'           # Azul pastel
    cor_intersecao = '#C9A0DC'  # Roxo claro elegante
    cor_borda = '#B284BE'       # Lilás para bordas
    
    # Opacidades e configurações por operação
    if operacao == "uniao":
        # União: ambos destacados com mesma cor
        alpha_A = 0.6
        alpha_B = 0.6
        alpha_AB = 0.75
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = cor_intersecao
        
    elif operacao == "intersecao":
        # Interseção: só o centro destacado
        alpha_A = 0.3
        alpha_B = 0.3
        alpha_AB = 0.8
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = cor_intersecao
        
    elif operacao == "diferenca":
        # A - B: só A destacado
        alpha_A = 0.7
        alpha_B = 0.25
        alpha_AB = 0.25
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = cor_B
        
    elif operacao == "diferenca_b":
        # B - A: só B destacado
        alpha_A = 0.25
        alpha_B = 0.7
        alpha_AB = 0.25
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = cor_A
        
    elif operacao == "simetrica":
        # Diferença simétrica: A e B destacados, interseção apagada
        alpha_A = 0.7
        alpha_B = 0.7
        alpha_AB = 0.15
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = '#E8E8E8'
        
    else:  # cartesiano
        # Produto cartesiano: mesma paleta harmônica
        alpha_A = 0.55
        alpha_B = 0.55
        alpha_AB = 0.7
        cor_destaque_A = cor_A
        cor_destaque_B = cor_B
        cor_destaque_AB = cor_intersecao
    
    # Desenhar círculo A (fundo)
    circle_A_bg = Circle(pos_A, raio, color=cor_destaque_A, alpha=alpha_A, 
                         ec=cor_borda, linewidth=2.5, zorder=1)
    ax.add_patch(circle_A_bg)
    
    # Desenhar círculo B (fundo)
    circle_B_bg = Circle(pos_B, raio, color=cor_destaque_B, alpha=alpha_B, 
                         ec=cor_borda, linewidth=2.5, zorder=1)
    ax.add_patch(circle_B_bg)
    
    # Desenhar interseção se houver elementos comuns
    if len(inter) > 0:
        # Criar máscara para a interseção
        x_range = np.linspace(-2.5, 2.5, 500)
        y_range = np.linspace(-2.2, 2.5, 500)
        X, Y = np.meshgrid(x_range, y_range)
        
        # Distâncias aos centros
        dist_A = np.sqrt((X - pos_A[0])**2 + (Y - pos_A[1])**2)
        dist_B = np.sqrt((X - pos_B[0])**2 + (Y - pos_B[1])**2)
        
        # Interseção: dentro de ambos
        mask_inter = (dist_A <= raio) & (dist_B <= raio)
        
        # Desenhar interseção
        ax.contourf(X, Y, mask_inter.astype(int), levels=[0.5, 1.5], 
                   colors=[cor_destaque_AB], alpha=alpha_AB, zorder=2)
    
    # Adicionar brilho sutil nos círculos destacados
    if operacao in ["diferenca", "simetrica"]:
        glow_A = Circle(pos_A, raio + 0.08, color=cor_A, alpha=0.15, 
                       ec='none', linewidth=0, zorder=0)
        ax.add_patch(glow_A)
    
    if operacao in ["diferenca_b", "simetrica"]:
        glow_B = Circle(pos_B, raio + 0.08, color=cor_B, alpha=0.15, 
                       ec='none', linewidth=0, zorder=0)
        ax.add_patch(glow_B)
    
    if operacao == "intersecao" and len(inter) > 0:
        # Brilho na interseção
        ax.contourf(X, Y, mask_inter.astype(int), levels=[0.5, 1.5], 
                   colors=[cor_intersecao], alpha=0.25, zorder=0)
    
    # Labels dos conjuntos
    ax.text(pos_A[0], raio + 0.5, 'A', fontsize=26, fontweight='bold', 
            ha='center', color='#7B68EE', zorder=10)
    ax.text(pos_B[0], raio + 0.5, 'B', fontsize=26, fontweight='bold', 
            ha='center', color='#7B68EE', zorder=10)
    
    # Mostrar elementos
    def formatar_elementos(elementos, max_items=6):
        lista = sorted(list(elementos))
        if len(lista) == 0:
            return ""
        if len(lista) > max_items:
            texto = ', '.join(map(str, lista[:max_items]))
            return f"{texto}\n..."
        return ', '.join(map(str, lista))
    
    # Elementos apenas em A (lado esquerdo)
    if len(apenas_A) > 0:
        texto_A = formatar_elementos(apenas_A)
        ax.text(pos_A[0] - 0.5, 0, texto_A, fontsize=10, ha='center', va='center', 
                color='#333', fontweight='600', zorder=5,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, 
                         edgecolor='#E0E7FF', linewidth=1.5))
    
    # Elementos apenas em B (lado direito)
    if len(apenas_B) > 0:
        texto_B = formatar_elementos(apenas_B)
        ax.text(pos_B[0] + 0.5, 0, texto_B, fontsize=10, ha='center', va='center', 
                color='#333', fontweight='600', zorder=5,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, 
                         edgecolor='#E0E7FF', linewidth=1.5))
    
    # Elementos na interseção (centro)
    if len(inter) > 0:
        texto_inter = formatar_elementos(inter)
        ax.text(0, 0, texto_inter, fontsize=10, ha='center', va='center', 
                color='#333', fontweight='600', zorder=5,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, 
                         edgecolor='#E0E7FF', linewidth=1.5))
    
    # Título com gradiente visual
    titulos = {
        "uniao": "União (A ∪ B)",
        "intersecao": "Interseção (A ∩ B)",
        "diferenca": "Diferença (A - B)",
        "diferenca_b": "Diferença (B - A)",
        "simetrica": "Diferença Simétrica (A △ B)",
        "cartesiano": "Produto Cartesiano (A × B)"
    }
    
    # Cores do título por operação
    cores_titulo = {
        "uniao": "#D16BA5",
        "intersecao": "#7B68EE",
        "diferenca": "#F49AC2",
        "diferenca_b": "#A7C7E7",
        "simetrica": "#B284BE",
        "cartesiano": "#86A8E7"
    }
    
    plt.title(titulos.get(operacao, "Operação de Conjuntos"), 
              fontsize=20, fontweight='bold', 
              color=cores_titulo.get(operacao, '#7B68EE'), pad=20)
    
    # Legenda explicativa
    descricoes = {
        "uniao": "Todos os elementos de A ou B",
        "intersecao": "Elementos comuns a A e B",
        "diferenca": "Elementos em A que não estão em B",
        "diferenca_b": "Elementos em B que não estão em A",
        "simetrica": "Elementos em A ou B, mas não em ambos",
        "cartesiano": "Todos os pares ordenados (a, b)"
    }
    
    ax.text(0, -2, descricoes.get(operacao, ""), 
            fontsize=11, ha='center', color='#666', style='italic')
    
    # Para produto cartesiano, adicionar box com pares
    if operacao == "cartesiano" and len(A) * len(B) <= 20:
        pares = cartesiano(A, B)
        texto_pares = ', '.join(pares[:15])
        if len(pares) > 15:
            texto_pares += '...'
        
        ax.text(0, -1.4, texto_pares, fontsize=9, ha='center', 
                color='#555', zorder=5, wrap=True,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FAF5FF', 
                         alpha=0.9, edgecolor='#E0D4F7', linewidth=2))
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor='#FFFFFF', dpi=120)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)

    return f"data:image/png;base64,{img_base64}"


# ======== Rotas Flask =========

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/operacao', methods=['POST'])
def operacao():
    data = request.get_json()

    A = data.get('A', [])
    B = data.get('B', [])
    operacao_nome = data.get('operacao', '').lower()
    sort_results = data.get('sort', False)

    resultado = []

    try:
        if operacao_nome == 'uniao':
            resultado = uniao(A, B)
        elif operacao_nome == 'intersecao':
            resultado = intersecao(A, B)
        elif operacao_nome == 'diferenca':
            resultado = diferenca(A, B)
        elif operacao_nome == 'diferenca_b':
            resultado = diferenca_b(A, B)
        elif operacao_nome == 'simetrica':
            resultado = simetrica(A, B)
        elif operacao_nome == 'cartesiano':
            resultado = cartesiano(A, B)
        else:
            return jsonify({'erro': 'Operação inválida'}), 400

        if sort_results and operacao_nome != 'cartesiano':
            try:
                resultado = sorted(resultado)
            except:
                pass

        img_base64 = gerar_diagrama(A, B, operacao_nome)

        return jsonify({
            'resultado': resultado,
            'cardinalidade': len(resultado),
            'imagem': img_base64
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
