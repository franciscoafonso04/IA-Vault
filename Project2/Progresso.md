Total de linhas: 140.700

Total de colunas: 20

Coluna alvo (target): Depression (0 = não, 1 = sim)

Tipo de problema: Classificação binária

Variáveis numéricas: Age, Academic Pressure, Work Pressure, CGPA, Study Satisfaction, Job Satisfaction, Work/Study Hours, Financial Stress

Variáveis categóricas: Gender, City, Profession, Degree, Sleep Duration, Dietary Habits, etc.

Coluna alvo: Depression (nosso target)

Algumas colunas com muitos valores nulos:

Academic Pressure, CGPA, Study Satisfaction → só têm ~27k valores

Profession, Work Pressure, Job Satisfaction → também têm bastantes valores ausentes

Valores nulos (top 10 colunas com mais missing):

Study Satisfaction - 112.803
Academic Pressure - 112.803
CGPA - 112.802
Profession - 36.630
Work Pressure - 27.918
Job Satisfaction - 27.910
Dietary Habits -4
Financial Stress -4
Degree -2
Family History of Mental Illness - 0

Distribuição da variável alvo Depression:
Há um desequilíbrio leve ou moderado nas classes. Podemos considerar isso ao avaliar os modelos

---

Outliers visíveis em Age, Work/Study Hours e CGPA.

Muitas variáveis têm valores concentrados em faixas específicas (ex: Job Satisfaction, Financial Stress).

Algumas distribuições são assimétricas, o que pode impactar certos modelos (como SVM ou KNN).

Algumas colunas estão bastante afetadas por valores nulos, como vimos antes.

---

Principais correlações com Depression:
Financial Stress e Depression: positiva moderada (~0.31) → faz sentido, estresse financeiro pode influenciar.

Study Satisfaction, Academic Pressure e Job Satisfaction também têm correlação leve com Depression (entre 0.1 e 0.25).

Age, CGPA, Work/Study Hours têm baixa ou quase nenhuma correlação com a variável alvo.

Variáveis como estresse financeiro, pressão acadêmica, satisfação no trabalho/estudo devem ser consideradas no modelo.

Algumas variáveis com baixa correlação podem ainda ser úteis combinadas ou em modelos não luneares.