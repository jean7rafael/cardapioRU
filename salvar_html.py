import http.client
import ssl

def salvar_html(url, arquivo_saida):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    conn = http.client.HTTPSConnection("pra.ufpr.br", context=context)
    conn.request("GET", "/ru/ru-centro-politecnico/")
    response = conn.getresponse()
    
    if response.status == 200:
        content = response.read().decode('utf-8')
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Conteúdo salvo em {arquivo_saida}")
    else:
        print(f"Falha ao acessar a página: {response.status}")

url = 'https://pra.ufpr.br/ru/ru-centro-politecnico/'
arquivo_saida = 'conteudo_pagina.html'
salvar_html(url, arquivo_saida)
