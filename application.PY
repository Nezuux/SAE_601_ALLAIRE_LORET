import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


# Configurer la page Streamlit
st.set_page_config(page_title="🧑‍💻 Analyse des Salaires en Data Science", layout="wide")

st.text("ALLAIRE Mathis & LORET Martin, Groupe D")

# Charger les données
df = pd.read_csv("ds_salaries.csv")

# Titre de l'application
st.title("📊 Visualisation des Salaires en Data Science")

# Afficher un aperçu des données
if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head())

# Statistiques descriptives
st.subheader("📌 Statistiques générales")
st.write(df.describe())

with st.expander("💭 Analyse des statistiques générales"):
    st.markdown("""
    - Le jeu de données contient 3,755 entrées
    - Les années couvertes vont de 2020 à 2023
    - La majorité des données sont de 2022-2023
    - Les données sont bien distribuées sur la période
    """)

# Distribution des salaires
df_france = df[df["company_location"] == "FR"]
fig1 = px.box(df_france, x="experience_level", y="salary_in_usd", color="experience_level", 
              title="Distribution des salaires par niveau d'expérience en France")
st.plotly_chart(fig1)


with st.expander("💭 Analyse de la distribution des salaires en France"):
    st.markdown("""
    - Les salaires augmentent avec le niveau d'expérience
    - Les seniors (SE) ont les salaires les plus élevés
    - On observe une grande dispersion pour les niveaux expérimentés
    - Quelques valeurs atypiques sont présentes
    """)

# Salaire moyen par catégorie
st.subheader("📊 Salaire moyen par catégorie")
category = st.selectbox("Choisir une catégorie", ['experience_level', 'employment_type', 'job_title', 'company_location'])
avg_salary = df.groupby(category)['salary_in_usd'].mean()
st.bar_chart(avg_salary)

with st.expander("💭 Analyse des tendances de salaires"):
    st.markdown("""
    - Les salaires varient significativement selon les catégories
    - Les postes à temps plein sont mieux rémunérés
    - Certains pays offrent des salaires nettement supérieurs
    - Les Data Scientists seniors sont les mieux payés
    """)

# Corrélation entre variables numériques
st.subheader("🔗 Corrélations entre variables numériques")
numeric_df = df.select_dtypes(include=[np.number])
correlation_matrix = numeric_df.corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

with st.expander("💭 Analyse des corrélations"):
    st.markdown("""
    - Certaines variables montrent des corrélations fortes
    - Le salaire est fortement corrélé avec le niveau d'expérience
    - La taille de l'entreprise a un impact modéré sur les salaires
    """)

# Analyse interactive des variations de salaire
st.subheader("📈 Évolution des salaires par poste")

top_jobs = df["job_title"].value_counts().head(10).index
df_top_jobs = df[df["job_title"].isin(top_jobs)]
salary_trend = df_top_jobs.groupby(["work_year", "job_title"])["salary_in_usd"].mean().reset_index()

fig4 = px.line(salary_trend, x="work_year", y="salary_in_usd", color="job_title", 
               title="Tendance des salaires pour les 10 postes les plus courants")
fig4.update_xaxes(dtick=1, tickformat="d")
st.plotly_chart(fig4)

with st.expander("💭 Analyse des variations de salaire"):
    st.markdown("""
    - Les salaires ont tendance à augmenter au fil des années
    - Certains postes montrent une croissance plus rapide
    - La disparité entre les postes s'accentue avec le temps
    """)

# Salaire médian par expérience et taille d'entreprise
st.subheader("📊 Salaire médian par expérience et taille d'entreprise")

median_salary = df.groupby(["experience_level", "company_size"])["salary_in_usd"].median().reset_index()

fig5 = px.bar(median_salary, x="experience_level", y="salary_in_usd", color="company_size",
              title="Salaire médian par niveau d'expérience et taille d'entreprise")
st.plotly_chart(fig5)

with st.expander("💭 Analyse des salaires médians"):
    st.markdown("""
    - Les grandes entreprises offrent généralement de meilleurs salaires
    - L'écart de salaire entre les niveaux d'expérience est plus marqué dans les grandes entreprises
    - Les petites entreprises montrent moins de variation entre les niveaux
    """)

# Ajout de filtres dynamiques
st.subheader("🎛️ Filtrage dynamique des salaires")

salary_range = st.slider("Sélectionnez la plage de salaire", min_value=25000, max_value=175000, value=(25000, 175000))
df_filtered = df[(df["salary_in_usd"] >= salary_range[0]) & (df["salary_in_usd"] <= salary_range[1])]

st.write(f"Nombre d'observations après filtrage : {len(df_filtered)}")
st.write(df_filtered.head())

with st.expander("💭 Analyse du filtrage"):
    st.markdown("""
    - Le filtrage permet d'identifier les segments spécifiques
    - La majorité des salaires se situe dans une plage moyenne
    - Certains postes sortent des plages habituelles
    """)

# Impact du télétravail sur le salaire selon le pays
st.subheader("🏡 Impact du télétravail sur le salaire selon le pays")

telework_impact = df.groupby(["remote_ratio", "company_location"])["salary_in_usd"].mean().reset_index()

fig6 = px.bar(telework_impact, x="company_location", y="salary_in_usd", color="remote_ratio",
              title="Impact du télétravail sur les salaires")
st.plotly_chart(fig6)

with st.expander("💭 Analyse de l'impact du télétravail"):
    st.markdown("""
    - Le télétravail complet offre souvent des salaires plus élevés
    - L'impact varie selon les pays
    - Certains pays privilégient le travail hybride
    """)

# Filtrage avancé des données
st.subheader("🔍 Filtrage avancé")

exp_levels = st.multiselect("Sélectionnez le niveau d'expérience", df["experience_level"].unique())
company_sizes = st.multiselect("Sélectionnez la taille d'entreprise", df["company_size"].unique())

df_filtered_advanced = df
if exp_levels:
    df_filtered_advanced = df_filtered_advanced[df_filtered_advanced["experience_level"].isin(exp_levels)]
if company_sizes:
    df_filtered_advanced = df_filtered_advanced[df_filtered_advanced["company_size"].isin(company_sizes)]

st.write(f"Nombre d'observations après filtrage avancé : {len(df_filtered_advanced)}")
st.write(df_filtered_advanced.head())


with st.expander("💭 Analyse des statistiques générales"):
    st.markdown("""
    - Le jeu de données contient exactement 3,755 entrées
    - Les années couvertes vont de 2020 à 2023
    - La moyenne des années est d'environ 2022.37, indiquant que la majorité des données sont récentes
    - 50% des données se situent en 2022
    - Les données sont principalement concentrées sur 2022-2023
    - On observe une forte présence de profils seniors (SE) dans les données récentes
    """)

# Top 5 des jobs les mieux payés
# Grouper par titre de poste et calculer le salaire moyen
job_salaries = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)

# Sélectionner le top 5
top_5_jobs = job_salaries.head(5)

# Créer un DataFrame pour l'affichage
top_5_df = pd.DataFrame({
    'Job Title': top_5_jobs.index,
    'Average Salary (USD)': top_5_jobs.values
})

# Afficher le tableau dans Streamlit
st.subheader("Top 5 des jobs les mieux payés")
st.table(top_5_df)

with st.expander("💭 Analyse des jobs les mieux payés"):
    st.markdown("""
    - On retrouve le job Data Science Tech Lead qui est le mieux payé
    - Le job Data Science Tech Lead est 1,9 fois plus payé que Principal Data Scientist
    - Il y a beaucoup de différence entre les salaires
    """)