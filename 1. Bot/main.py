import json

with open("api.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

response = requests.post(
    url="http://192.168.100.234:1102/TnWebDMProcesso/ProcessoExecutar?_AActionName=TnArqDPImportarLctoFisNFEXML",
    headers={
        "Content-Type": "application/json",
        "x-access-token": "79ba467c45f2fe74ac14627045fa117f"
    },
    json=dados
)

print(response.status_code)
print(response.text)
