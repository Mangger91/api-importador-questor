import requests
import base64
import pandas as pd
import re

# === CONFIGURAÇÕES ===
URL = (
    "http://192.168.100.234:1102/TnWebDMRelatorio/Executar"
    "?_AActionName=nFisRRTotalICMSNatureza"
    "&_ABase64=false"
    "&_ATipoRetorno=nrwexCSV"
)
TOKEN = "c153d325bc7a55f7258ef985e780c298"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# === PARÂMETROS DO RELATÓRIO ===
PARAMS = {
    "reportParameters": {
        "PMODELO": 1,
        "PQUEBRA": 1,
        "PDATAINICIAL": "01/05/2025",
        "PDATAFINAL": "01/05/2025",
        "PTIPOMOVIMENTO": 2,  # Saída
        "PTIPOTOTAL": 0,
        "PQUEBRAPORMOVIMENTO": 0,
        "PDETALHARNOESTADO": 0,
        "PCODIGOEMPRESA": 3301,
        "PCODIGOESTAB": 1,
        "PORDENAR": 1
    }
}

# === REQUISIÇÃO ===
response = requests.post(URL, json=PARAMS, headers=HEADERS, timeout=180)
response.raise_for_status()
texto = response.text

# === EXTRAIR O VALOR EXATO DO TOTAL ===
match = re.search(r'Total de Saídas.*?;([\d\.,]+);', texto)
if match:
    valor_contabil = float(match.group(1).replace('.', '').replace(',', '.'))
else:
    valor_contabil = 0.0

# === CRIAR PLANILHA COM RESULTADO ===
df = pd.DataFrame([{
    "Codigo Empresa": PARAMS['reportParameters']['PCODIGOEMPRESA'],
    "Filial": PARAMS['reportParameters']['PCODIGOESTAB'],
    "Periodo": f"{PARAMS['reportParameters']['PDATAINICIAL']} a {PARAMS['reportParameters']['PDATAFINAL']}",
    "Valor Contábil Total (Saídas)": valor_contabil
}])

# === SALVAR EXCEL ===
df.to_excel("valor_contabil_total.xlsx", index=False)
print("Relatório salvo com sucesso: valor_contabil_total.xlsx")
print(valor_contabil)