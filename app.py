from flask import Flask, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/cardapio', methods=['GET'])
def obter_cardapio():
    url = 'https://pra.ufpr.br/ru/ru-centro-politecnico/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Garantir codificação correta
    if response.status_code == 200:
        content = response.content.decode('utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html.parser')
        
        cardapio_div = soup.select_one('div#post')
        if cardapio_div:
            data_atual = datetime.now().strftime('%d/%m/%y')
            hora_atual = datetime.now().time()

            dias = cardapio_div.find_all('p', string=lambda x: x and data_atual in x)
            if not dias:
                return jsonify(message="Não foi possível encontrar as datas.")

            figuras = cardapio_div.select('figure.wp-block-table')
            if not figuras:
                return jsonify(message="Não foi possível encontrar figuras com a classe 'wp-block-table'.")

            for dia, fig in zip(dias, figuras):
                dia_texto = dia.get_text()
                if data_atual in dia_texto:
                    lines = fig.get_text(separator='\n').split('\n')
                    almoco_index = lines.index('ALMOÇO')
                    jantar_index = lines.index('JANTAR')
                    almoco_linha = lines[almoco_index + 1]
                    jantar_linha = lines[jantar_index + 1]
                    
                    if hora_atual < datetime.strptime('14:00', '%H:%M').time():
                        refeicao_desejada = f"Hoje para almoçar tem {almoco_linha}"
                    else:
                        refeicao_desejada = f"Hoje para jantar tem {jantar_linha}"
                    return jsonify(message=refeicao_desejada)

            return jsonify(message="Não foi possível encontrar o cardápio para hoje.")
        else:
            return jsonify(message="Não foi possível encontrar a seção do cardápio.")
    else:
        return jsonify(message=f"Falha ao acessar a página: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True)
