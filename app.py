from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import io, base64

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/operacao', methods=['POST'])
def operacao():
    data = request.get_json() or {}
    A = set(data.get('A', []))
    B = set(data.get('B', []))
    op = data.get('op', 'uniao')

    if op == 'uniao':
        resultado = sorted(list(A | B))
    elif op == 'intersecao':
        resultado = sorted(list(A & B))
    elif op == 'diferenca':
        resultado = sorted(list(A - B))
    else:
        return jsonify({'erro': 'Operação inválida'}), 400

    fig, ax = plt.subplots(figsize=(5, 5))
    v = venn2([A, B], set_labels=("A", "B"))

    if v.get_label_by_id('10'):
        v.get_label_by_id('10').set_text(','.join(map(str, A - B)))
    if v.get_label_by_id('01'):
        v.get_label_by_id('01').set_text(','.join(map(str, B - A)))
    if v.get_label_by_id('11'):
        v.get_label_by_id('11').set_text(','.join(map(str, A & B)))

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')

    return jsonify({'resultado': resultado, 'imagem': img_b64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
