import os
import pandas as pd

def rodar_pipeline():
    print("🚀 Iniciando o Pipeline de Qualidade de Dados...")

    # 1. Dados de exemplo simulando o Censo Escolar (INEP)
    dados = {
        'CO_ENTIDADE': [35000001, 35000002, 35000002, None, 35000004],
        'NO_ENTIDADE': ['Escola A ', 'escola b', 'escola b', 'Escola C', 'Escola D'],
        'SG_UF': ['SP', 'SP', 'SP', 'SP', 'SP'],
        'QT_MATRICULAS': [150, -10, -10, 200, 85]  # Contém erro de valor negativo e duplicado
    }
    
    df_bruto = pd.DataFrame(dados)
    print(f"\n1. Dados Brutos Carregados ({len(df_bruto)} registros)")

    # 2. Diagnóstico de Qualidade (Data Quality Check)
    duplicados = df_bruto.duplicated().sum()
    nulos = df_bruto['CO_ENTIDADE'].isnull().sum()
    negativos = (df_bruto['QT_MATRICULAS'] < 0).sum()

    print("\n🔍 Relatório de Problemas Encontrados:")
    print(f"   - Linhas duplicadas: {duplicados}")
    print(f"   - Escolas sem código ID: {nulos}")
    print(f"   - Matrículas negativas: {negativos}")

    # 3. Tratamento dos Dados (Limpeza)
    df_limpo = df_bruto.copy()
    df_limpo = df_limpo.drop_duplicates()                       # Remove duplicados
    df_limpo = df_limpo.dropna(subset=['CO_ENTIDADE'])           # Remove sem ID
    df_limpo['QT_MATRICULAS'] = df_limpo['QT_MATRICULAS'].clip(lower=0) # Corrige negativos para 0
    df_limpo['NO_ENTIDADE'] = df_limpo['NO_ENTIDADE'].str.strip().str.upper() # Padroniza nome

    print(f"\n2. Limpeza Concluída! Registros válidos restantes: {len(df_limpo)}")

    # 4. Salvar resultado
    os.makedirs('resultado', exist_ok=True)
    df_limpo.to_csv('resultado/dados_censo_tratados.csv', index=False)
    print("\n✅ Sucesso! Dados limpos salvos em 'resultado/dados_censo_tratados.csv'")

if __name__ == "__main__":
    rodar_pipeline()
