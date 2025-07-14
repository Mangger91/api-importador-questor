import os
import base64
import requests
import pandas as pd

# Caminhos
planilha_empresas = r"C:\Scripts_e_Automacoes\Questor_Farmacias\3. Empresas\GRUPO UNIPRECO.xlsx"
pasta_nli = r"C:\Scripts_e_Automacoes\Questor_Farmacias\2. Config\201-Saidas"
pasta_xmls = r"\\192.168.100.233\5. Outputs\XML"
log_csv = r"C:\Scripts_e_Automacoes\Questor_Farmacias\4. Logs\importacao_log.csv"
url_api = "http://192.168.100.234:1102/integracao/importar" # "http://oej-vivo.ww0.com.br:1102/integracao/importar"

# Carregar empresas
df_empresas = pd.read_excel(planilha_empresas)
if not os.path.exists(os.path.dirname(log_csv)):
    os.makedirs(os.path.dirname(log_csv))
log = []

# Carregar e codificar todos os arquivos .nli
leiautes = []
for nome_arquivo in os.listdir(pasta_nli):
    if nome_arquivo.lower().endswith('.nli'):
        with open(os.path.join(pasta_nli, nome_arquivo), "rb") as f:
            leiautes.append({
                "nome": nome_arquivo,
                "arquivo": base64.b64encode(f.read()).decode("utf-8")
            })

# Processar cada empresa
for _, row in df_empresas.iterrows():
    cd_empresa = row["cd_empresa"]
    cd_estab = row["cd_estab"]
    nome_empresa = row["Nome Questor"]
    pasta_empresa = row["Nome VetorFarma"]
    caminho_xmls = os.path.join(pasta_xmls, str(pasta_empresa))

    if not os.path.exists(caminho_xmls):
        print(f"Pasta não encontrada para empresa {nome_empresa}: {caminho_xmls}")
        continue

    for nome_xml in os.listdir(caminho_xmls):
        if not nome_xml.lower().endswith(".xml"):
            continue
        caminho_xml = os.path.join(caminho_xmls, nome_xml)
        try:
            with open(caminho_xml, "rb") as f:
                xml_base64 = base64.b64encode(f.read()).decode("utf-8")

            payload = {
                "leiautes": leiautes,
                "filtro": "",
                "dados": xml_base64
            }

            response = requests.post(url_api, json=payload)
            status = response.status_code
            mensagem = response.text.strip()

            print(f"Enviado: {nome_xml} ({nome_empresa}) -> Status: {status}")
            log.append({
                "Empresa": nome_empresa,
                "XML": nome_xml,
                "cd_empresa": cd_empresa,
                "cd_estab": cd_estab,
                "Status HTTP": status,
                "Mensagem": mensagem[:500]  # Limita mensagem para o CSV
            })

        except Exception as e:
            print(f"Erro ao processar {nome_xml} da empresa {nome_empresa}: {e}")
            log.append({
                "Empresa": nome_empresa,
                "XML": nome_xml,
                "cd_empresa": cd_empresa,
                "cd_estab": cd_estab,
                "Status HTTP": "Erro",
                "Mensagem": str(e)
            })

# Salvar log
df_log = pd.DataFrame(log)
df_log.to_csv(log_csv, index=False, sep=";", encoding="utf-8-sig")
print(f"Log salvo em: {log_csv}")
