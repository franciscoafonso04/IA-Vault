# 📘 Projeto IART 2 – Mental Health Classification

Este repositório contém a submissão para o segundo trabalho de IART (2024/25), cujo objetivo foi treinar e avaliar modelos de aprendizagem automática para prever sintomas de depressão com base em dados pessoais, académicos e de estilo de vida.

## 📂 Ficheiros incluídos

- `mental_health_A2_77.ipynb` — Notebook completo com análise exploratória, treino, tuning e avaliação dos modelos.
- `IART2.pdf` — Apresentação em formato PDF (máximo 10 slides).
- `train.csv` — Conjunto de treino original.
- `test.csv` — Conjunto de teste original.
- `result.csv` — Resultado gerado com o modelo final (MLPClassifier Tuned).

## ▶️ Como correr

1. Abrir o notebook `mental_health_A2_77.ipynb` num ambiente como Jupyter Notebook ou VS Code.
2. Certificar-se de que todos os ficheiros `.csv` estão no mesmo diretório do notebook.
3. Correr todas as células sequencialmente:
   - O notebook inclui o pré-processamento, treino, tuning e avaliação.
   - A última secção aplica o modelo ao `test.csv` e gera o `result.csv`.

Não é necessário instalar bibliotecas adicionais para além das standard do `scikit-learn`, `pandas`, `numpy` e `matplotlib`.

## 🔗 Dataset

O dataset foi obtido a partir da competição [Kaggle Playground Series – S4E11](https://www.kaggle.com/competitions/playground-series-s4e11).

