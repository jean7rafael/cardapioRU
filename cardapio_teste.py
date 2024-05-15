import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obter_cardapio(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Garantir codificação correta
    if response.status_code == 200:
        # Decodificar o conteúdo da resposta explicitamente como UTF-8
        content = response.content.decode('utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html.parser')
        
        # Seleciona a div com id 'post'
        cardapio_div = soup.select_one('div#post')
        if cardapio_div:
            # Obter a data e hora atual
            data_atual = datetime.now().strftime('%d/%m/%y')
            hora_atual = datetime.now().time()

            # Extrair as datas e verificar se coincidem com a data atual
            dias = cardapio_div.find_all('p', string=lambda x: x and data_atual in x)
            if not dias:
                return "Não foi possível encontrar as datas."

            # Extrair todas as figures com a classe 'wp-block-table'
            figuras = cardapio_div.select('figure.wp-block-table')
            if not figuras:
                return "Não foi possível encontrar figuras com a classe 'wp-block-table'."

            # Variável para armazenar a refeição desejada
            refeicao_desejada = None

            for dia, fig in zip(dias, figuras):
                dia_texto = dia.get_text()
                if data_atual in dia_texto:
                    # Encontrar linhas logo abaixo do ALMOÇO e do JANTAR
                    lines = fig.get_text(separator='\n').split('\n')
                    almoco_index = lines.index('ALMOÇO')
                    jantar_index = lines.index('JANTAR')
                    almoco_linha = lines[almoco_index + 1]
                    jantar_linha = lines[jantar_index + 1]
                    
                    if hora_atual < datetime.strptime('14:00', '%H:%M').time():
                        refeicao_desejada = f"Hoje para almoçar tem {almoco_linha}"
                    else:
                        refeicao_desejada = f"Hoje para jantar tem {jantar_linha}"
                    break

            return refeicao_desejada if refeicao_desejada else "Não foi possível encontrar o cardápio para hoje."
        else:
            return "Não foi possível encontrar a seção do cardápio."
    else:
        return f"Falha ao acessar a página: {response.status_code}"

url = 'https://pra.ufpr.br/ru/ru-centro-politecnico/'
cardapio = obter_cardapio(url)
print(cardapio)

