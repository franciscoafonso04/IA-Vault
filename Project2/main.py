import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("data/train.csv")

# Ver os primeiros dados
print(df.head())

# Ver informações gerais
print(df.info())

# Ver estatísticas básicas
print(df.describe())

# 1. Verificar valores nulos por coluna
missing_values = df.isnull().sum().sort_values(ascending=False)

# 2. Distribuição da variável alvo (Depression)
plt.figure(figsize=(6, 4))
sns.countplot(x='Depression', data=df)
plt.title("Distribuição da variável alvo: Depression")
plt.xlabel("Depression (0 = Não, 1 = Sim)")
plt.ylabel("Contagem")
plt.tight_layout()
plt.show()

# Selecionar colunas numéricas úteis (ignorando id e target)
numeric_cols = ['Age', 'Academic Pressure', 'Work Pressure', 'CGPA',
                'Study Satisfaction', 'Job Satisfaction', 'Work/Study Hours', 'Financial Stress']

# Histogramas das variáveis numéricas
df[numeric_cols].hist(bins=30, figsize=(15, 10), layout=(3, 3))
plt.suptitle("Distribuição das Variáveis Numéricas", fontsize=16)
plt.tight_layout()
plt.show()

# Boxplots para ver outliers
for col in numeric_cols:
    plt.figure(figsize=(6, 3))
    sns.boxplot(x=df[col])
    plt.title(f"Boxplot de {col}")
    plt.tight_layout()
    plt.show()


# Selecionar variáveis categóricas (excluindo target)
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Exibir até 6 gráficos por linha
for col in categorical_cols:
    plt.figure(figsize=(6, 3))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f"Distribuição da variável categórica: {col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Gerar o mapa de correlação entre as variáveis numéricas
plt.figure(figsize=(10, 8))
correlation_matrix = df[numeric_cols + ['Depression']].corr(numeric_only=True)

sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
plt.title("Mapa de Correlação (variáveis numéricas)")
plt.tight_layout()
plt.show()
