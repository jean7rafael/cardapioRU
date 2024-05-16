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

            dias = cardapio_div.find_all('p', string=lambda x: x and any(day in x for day in ['Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo', 'Segunda-feira', 'Terça-feira']))
            if not dias:
                return jsonify(message="Não foi possível encontrar as datas.")

            figuras = cardapio_div.select('figure.wp-block-table')
            if not figuras:
                return jsonify(message="Não foi possível encontrar figuras com a classe 'wp-block-table'.")

            # Função para obter a primeira linha não vazia após um índice dado
            def get_next_non_empty_line(lines, start_index):
                for i in range(start_index + 1, len(lines)):
                    if lines[i].strip():
                        return lines[i]
                return "Não foi possível encontrar a informação desejada."

            # Processar blocos de datas
            cardapio_blocos = []
            for dia, fig in zip(dias, figuras):
                dia_texto = dia.get_text()
                lines = fig.get_text(separator='\n').split('\n')
                almoco_index = lines.index('ALMOÇO')
                jantar_index = lines.index('JANTAR')

                almoco_linha = get_next_non_empty_line(lines, almoco_index)
                jantar_linha = get_next_non_empty_line(lines, jantar_index)
                
                bloco = {
                    'data': dia_texto,
                    'almoco': almoco_linha,
                    'jantar': jantar_linha
                }
                cardapio_blocos.append(bloco)

            # Descomente a linha abaixo se quiser retornar todos os blocos encontrados
            # return jsonify(cardapio_blocos=cardapio_blocos)
            
            # Lógica atual para retornar refeição desejada com base no horário
            for bloco in cardapio_blocos:
                if data_atual in bloco['data']:
                    if hora_atual < datetime.strptime('14:00', '%H:%M').time():
                        refeicao_desejada = f"Hoje para almoçar tem {bloco['almoco']}"
                    else:
                        refeicao_desejada = f"Hoje para jantar tem {bloco['jantar']}"
                    return jsonify(message=refeicao_desejada)

            return jsonify(message="Não foi possível encontrar o cardápio para hoje.")
        else:
            return jsonify(message="Não foi possível encontrar a seção do cardápio.")
    else:
        return jsonify(message=f"Falha ao acessar a página: {response.status_code}")

if __name__ == '__main__':
    app.run(debug=True)
