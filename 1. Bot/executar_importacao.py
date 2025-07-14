from base_importador import df_empresas, data_inicio, data_fim, carregar_zips_corrigidos_por_nome_vetorfarma
import requests
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor

url_api = "http://192.168.100.234:1102/TnWebDMProcesso/ProcessoExecutar?_AActionName=TnArqDPImportarLctoFisNFEXML"
log_resultados = []

def importar_empresa(row):
    resultados = []

    cd_empresa = row['cd_empresa']
    cd_estab = row['cd_estab']
    nome_vetorfarma = row['Nome_VetorFarma']

    zips_corrigidos = carregar_zips_corrigidos_por_nome_vetorfarma(nome_vetorfarma)
    if not zips_corrigidos:
        resultados.append({
            'empresa': nome_vetorfarma,
            'codigo': cd_empresa,
            'filial': cd_estab,
            'arquivo': '',
            'status': 'ERRO: Nenhum .zip corrigido encontrado',
            'tempo': ''
        })
        return resultados

    for nome_zip, zip_base64 in zips_corrigidos:
        payload = {
            "pCodigoEmpresa": int(cd_empresa),
            "pCodigoEstab": int(cd_estab),
            "pDataInicial": data_inicio.strftime('%d/%m/%Y'),
            "pDataFinal": data_fim.strftime('%d/%m/%Y'),
            "pNomeArquivo": nome_vetorfarma,
            "pNomePasta_DIRABRIR": {
                "filename": nome_zip,
                "data": zip_base64
            }
        }

        try:
            inicio = time.time()
            response = requests.post(url_api, json=payload)
            duracao = round(time.time() - inicio, 2)
            status_msg = 'SUCESSO' if response.status_code == 200 else f"ERRO: Status {response.status_code}"
            print(f"[{status_msg}] {nome_vetorfarma} - {nome_zip} ({duracao}s)")
        except Exception as e:
            duracao = round(time.time() - inicio, 2)
            status_msg = f"EXCEÇÃO: {str(e)}"
            print(f"[FALHA] {nome_vetorfarma} - {nome_zip} ({duracao}s) - {status_msg}")

        resultados.append({
            'empresa': nome_vetorfarma,
            'codigo': cd_empresa,
            'filial': cd_estab,
            'arquivo': nome_zip,
            'status': status_msg,
            'tempo': f"{duracao}s"
        })

    return resultados

# Executar em paralelo
with ThreadPoolExecutor(max_workers=3) as executor:
    futuros = executor.map(importar_empresa, [row for _, row in df_empresas.iterrows()])
    for resultado_empresa in futuros:
        log_resultados.extend(resultado_empresa)

# Salva log
df_log = pd.DataFrame(log_resultados)
df_log.to_excel(r"C:\Scripts_e_Automacoes\Questor_Farmacias\4. Logs\log_importacao_api.xlsx", index=False)

print("Importação finalizada.")
