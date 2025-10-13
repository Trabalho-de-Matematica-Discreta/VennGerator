function parseSet(text) {
  if (!text) return [];
  return text
    .split(',')
    .map(s => s.trim())
    .filter(s => s !== '')
    .map(s => {
      const n = Number(s);
      return Number.isNaN(n) ? s : n;
    });
}

async function calcular(op) {
  const A = parseSet(document.getElementById('A').value);
  const B = parseSet(document.getElementById('B').value);

  try {
    const resp = await fetch('/operacao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ A, B, op }),
    });

    const data = await resp.json();

    if (data.erro) {
      document.getElementById('saida').innerText = 'Erro: ' + data.erro;
      document.getElementById('venn').src = '';
      return;
    }

    document.getElementById('saida').innerText = JSON.stringify(
      data.resultado,
      null,
      2
    );

    document.getElementById('venn').src =
      'data:image/png;base64,' + data.imagem;

    console.log('Dados recebidos:', data); 
  } catch (err) {
    console.error('Erro ao chamar o servidor:', err);
    document.getElementById('saida').innerText =
      'Erro de conexão com o servidor Flask.';
  }
}
