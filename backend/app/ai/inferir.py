# moved from project root
import joblib
import os
import numpy as np

# --- 1. Carregar o Modelo (Deve estar no escopo global) ---
# Esta parte deve ser executada UMA VEZ quando seu script iniciar.

nome_arquivo_modelo = os.path.join(os.path.dirname(__file__), 'sentiment_model.joblib')
model = None
model_classes = None # Ex: ['negative', 'neutral', 'positive']

try:
	model = joblib.load(nome_arquivo_modelo)
	model_classes = model.classes_
	print(f"Modelo '{nome_arquivo_modelo}' carregado. Classes: {model_classes}")
except FileNotFoundError:
	print(f"AVISO: Arquivo do modelo '{nome_arquivo_modelo}' não encontrado.")
	print("AVISO: Rode o script de treino primeiro. A função não funcionará.")
except Exception as e:
	print(f"AVISO: Erro ao carregar o modelo: {e}")
# -----------------------------------------------------------


def get_negativity_gradient(message: str) -> float:
	"""
	Returns sentiment score: 0.0 (positive) to 1.0 (negative).
	Returns 0.5 (neutral) if model fails.
	"""
	if model is None or model_classes is None:
		return 0.5
	
	try:
		probabilities = model.predict_proba([message])[0]
		score_dict = dict(zip(model_classes, probabilities))
		
		p_neg = score_dict.get('negative', 0.0)
		p_neu = score_dict.get('neutral', 0.0)
		
		# Formula: (p_neu * 0.5) + (p_neg * 1.0)
		return (p_neu * 0.5) + p_neg
	except:
		return 0.5


