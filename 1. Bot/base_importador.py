import pandas as pd
from pathlib import Path
import base64

config_path = Path(r"C:\Scripts_e_Automacoes\Questor_Farmacias\2. Config\Config.xlsx")
empresas_path = Path(r"C:\Scripts_e_Automacoes\Questor_Farmacias\3. Empresas\GRUPO UNIPRECO.xlsx")

df_config = pd.read_excel(config_path)
df_empresas = pd.read_excel(empresas_path)

data_inicio = df_config.iloc[0, 0]
data_fim = df_config.iloc[0, 1]

def carregar_zips_corrigidos_por_nome_vetorfarma(nome_vetorfarma):
    from pathlib import Path
    import base64

    pasta_corrigida = Path(r"\\192.168.100.233\5. Outputs\XML\Corrigidos")
    zips = []

    # Busca arquivos com sufixo -parte*.zip
    arquivos_partes = list(pasta_corrigida.glob(f"{nome_vetorfarma}-parte*.zip"))

    # Se não houver partes, tenta buscar um zip único
    if not arquivos_partes:
        arquivo_unico = pasta_corrigida / f"{nome_vetorfarma}.zip"
        if arquivo_unico.exists():
            arquivos_partes = [arquivo_unico]

    for zip_path in sorted(arquivos_partes):
        with open(zip_path, "rb") as f:
            conteudo_base64 = base64.b64encode(f.read()).decode("utf-8")
        zips.append((zip_path.name, conteudo_base64))

    return zips