# Projeto de Inteligência Artificial — Exploring Mental Health Data

## 1. Definição do Problema
- **Objetivo:** Prever se uma pessoa sofre de depressão.
- **Tipo de problema:** Classificação binária.
- **Variável alvo (target):** `Depression` (0 = Não, 1 = Sim).

## 2. Descrição do Dataset
- Dados relacionados com fatores acadêmicos, profissionais, estresse financeiro, hábitos de sono e alimentação.
- **Variáveis numéricas:**
  - Age
  - Academic Pressure
  - Work Pressure
  - CGPA
  - Study Satisfaction
  - Job Satisfaction
  - Work/Study Hours
  - Financial Stress
- **Variáveis categóricas:**
  - Gender
  - City
  - Profession
  - Degree
  - Sleep Duration
  - Dietary Habits, entre outras.

## 3. Principais Observações da Análise Exploratória
- **Missing values:**
  - Muitas colunas com valores ausentes significativos (`Study Satisfaction`, `Academic Pressure`, `CGPA`).
- **Correlações:**
  - `Financial Stress` apresenta uma correlação positiva moderada (~0.31) com `Depression`.
  - `Academic Pressure` e `Job Satisfaction` mostram correlações leves.
- **Outliers:**
  - Identificados em `Age`, `Work/Study Hours` e `CGPA`.
- **Distribuição da variável alvo:**
  - Leve desequilíbrio entre classes (0 e 1).

## 4. Pipeline de Machine Learning
- **Carregamento e limpeza de dados:**
  - Imputação de valores nulos (mediana para numéricos, moda para categóricos).
  - Encoding das variáveis categóricas (Label Encoding).
  - Normalização das variáveis numéricas (StandardScaler).
- **Separar features e target:**
  - Divisão em treino e teste (80/20).

## 5. Modelos Aplicados
- **Decision Tree Classifier**
- **k-Nearest Neighbors (k-NN)**
- **Support Vector Machine (SVM)**

## 6. Avaliação dos Modelos
- **Métricas usadas:**
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - Matriz de Confusão
- **Análises adicionais (opcionais):**
  - ROC Curves
  - Learning Curves

## 7. Tecnologias Utilizadas
- Python 3
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

## 8. Execução do Projeto
### Instalar dependências:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Executar:
- Abrir o ficheiro `projeto_mental_health.ipynb` num ambiente Jupyter Notebook.
- Seguir as instruções célula a célula para reproduzir o projeto.

---

_Projeto desenvolvido no âmbito da UC de Inteligência Artificial 2024/25._