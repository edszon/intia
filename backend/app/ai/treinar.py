import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib


def carregar_e_treinar_modelo(caminho_csv):
    try:
        df = pd.read_csv(caminho_csv)
        print(df['sentiment'].value_counts())
        if 'message' not in df.columns or 'sentiment' not in df.columns:
            print("Erro: O CSV deve conter as colunas 'message' e 'sentiment'.")
            return None
        df = df.dropna(subset=['message', 'sentiment'])
        X_train = df['message']
        y_train = df['sentiment']
        model = make_pipeline(CountVectorizer(), MultinomialNB())
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(f"Erro: {e}")
        return None


if __name__ == "__main__":
    csv_para_treinar = 'feelings.csv'
    nome_arquivo_modelo = 'sentiment_model.joblib'
    model = carregar_e_treinar_modelo(csv_para_treinar)
    if model:
        joblib.dump(model, nome_arquivo_modelo)
        print(f"Modelo salvo em '{nome_arquivo_modelo}'")


