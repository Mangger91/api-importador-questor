import os
import pandas as pd

# Caminho da planilha
caminho_planilha = r"C:\Scripts_e_Automacoes\Questor_Farmacias\3. Empresas\GRUPO UNIPRECO.xlsx"

# Caminho da rede onde estão os XMLs
caminho_base_xml = r"\\192.168.100.233\5. Outputs\XML"

# Carregar planilha
df = pd.read_excel(caminho_planilha)

# Normalizar nome da coluna
df.columns = df.columns.str.strip().str.lower()

# Percorrer as empresas
for _, linha in df.iterrows():
    nome_pasta = linha["nome no grupo spn"]  # <- Nome da subpasta
    nome_empresa = linha["nome no grupo spn"]
    cnpj = str(linha["cnpj"]).zfill(14)

    pasta_xml = os.path.join(caminho_base_xml, nome_pasta)
    
    if os.path.isdir(pasta_xml):
        arquivos = [f for f in os.listdir(pasta_xml) if f.lower().endswith(".xml")]
        print(f"\n📁 {nome_empresa} ({cnpj})")
        if arquivos:
            for xml in arquivos:
                print(f"  - {xml}")
        else:
            print("  ⚠️ Nenhum XML encontrado.")
    else:
        print(f"\n🚫 Pasta não encontrada para {nome_empresa} ({cnpj})")
        print(f"  ↳ Tentado acessar: {pasta_xml}")
