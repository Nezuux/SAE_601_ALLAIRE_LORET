#https://github.com/Nezuux/SAE_601_ALLAIRE_LORET

# 📝 **Instructions** :
# - Installez toutes les bibliothèques nécessaires : conda create -n projet python pandas numpy matplotlib seaborn streamlit plotly
# - Complétez les sections en écrivant votre code où c'est indiqué.
# - Ajoutez des commentaires clairs pour expliquer vos choix.
# - Utilisez des emoji avec windows + ;
# - Interprétez les résultats de vos visualisations.

# Importation des bibliothèques nécessaires
import pandas as pd  # pour la manipulation des données
import numpy as np  # pour les calculs numériques
import matplotlib.pyplot as plt  # pour créer des graphiques statiques
import seaborn as sns  # pour la visualisation de données statistique (plus avancée que matplotlib)
import streamlit as st  # pour créer l'application web interactive
import plotly.express as px  # pour créer des graphiques interactifs

# Configurer la page Streamlit
st.set_page_config(page_title="🧑‍💻 Analyse des Salaires en Data Science", layout="wide")  # définir le titre de la page et son layout

st.text("ALLAIRE Mathis & LORET Martin, Groupe D")  # afficher un texte de présentation des auteurs

# Charger les données depuis un fichier CSV
df = pd.read_csv("ds_salaries.csv")  # lire le fichier CSV dans un DataFrame

# Titre de l'application Streamlit
st.title("📊 Visualisation des Salaires en Data Science")  # titre principal de l'application

# Afficher un aperçu des données
if st.checkbox("Afficher un aperçu des données"):  # créer une case à cocher
    st.write(df.head())  # afficher les 5 premières lignes du DataFrame

# Statistiques descriptives du DataFrame
st.subheader("📌 Statistiques générales")  # sous-titre de section
st.write(df.describe())  # afficher des statistiques comme la moyenne, écart-type, min, max, etc.

with st.expander("💭 Analyse des statistiques générales"):  # zone de texte extensible
    st.markdown("""
    - Le jeu de données contient 3,755 entrées
    - Les années couvertes vont de 2020 à 2023
    - La majorité des données sont de 2022-2023
    - Les données sont bien distribuées sur la période
    """)

# Distribution des salaires pour les personnes en France
df_france = df[df["company_location"] == "FR"]  # filtrer les données pour la France
fig1 = px.box(df_france, x="experience_level", y="salary_in_usd", color="experience_level", 
              title="Distribution des salaires par niveau d'expérience en France")  # graphique boxplot interactif
st.plotly_chart(fig1)  # afficher le graphique

with st.expander("💭 Analyse de la distribution des salaires en France"):  # zone de texte extensible
    st.markdown("""
    - Les salaires augmentent avec le niveau d'expérience
    - Les seniors (SE) ont les salaires les plus élevés
    - On observe une grande dispersion pour les niveaux expérimentés
    - Quelques valeurs atypiques sont présentes
    """)

# Salaire moyen par catégorie (ex : par expérience, type d'emploi, etc.)
st.subheader("📊 Salaire moyen par catégorie")  # sous-titre
category = st.selectbox("Choisir une catégorie", ['experience_level', 'employment_type', 'job_title', 'company_location'])  # menu déroulant pour sélectionner une catégorie
avg_salary = df.groupby(category)['salary_in_usd'].mean()  # calculer le salaire moyen par catégorie
st.bar_chart(avg_salary)  # afficher un graphique à barres

with st.expander("💭 Analyse des tendances de salaires"):  # zone de texte extensible
    st.markdown("""
    - Les salaires varient significativement selon les catégories
    - Les postes à temps plein sont mieux rémunérés
    - Certains pays offrent des salaires nettement supérieurs
    - Les Data Scientists seniors sont les mieux payés
    """)

# Calculer les corrélations entre les variables numériques
st.subheader("🔗 Corrélations entre variables numériques")  # sous-titre
numeric_df = df.select_dtypes(include=[np.number])  # sélectionner uniquement les colonnes numériques
correlation_matrix = numeric_df.corr()  # calculer la matrice de corrélation
fig, ax = plt.subplots(figsize=(10, 8))  # créer un graphique avec une taille définie
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)  # afficher la carte de chaleur des corrélations
st.pyplot(fig)  # afficher le graphique dans Streamlit

with st.expander("💭 Analyse des corrélations"):  # zone de texte extensible
    st.markdown("""
    - Certaines variables montrent des corrélations fortes
    - Le salaire est fortement corrélé avec le niveau d'expérience
    - La taille de l'entreprise a un impact modéré sur les salaires
    """)

# Analyse interactive de l'évolution des salaires par poste
st.subheader("📈 Évolution des salaires par poste")  # sous-titre
top_jobs = df["job_title"].value_counts().head(10).index  # obtenir les 10 titres de poste les plus fréquents
df_top_jobs = df[df["job_title"].isin(top_jobs)]  # filtrer les données pour ces 10 postes
salary_trend = df_top_jobs.groupby(["work_year", "job_title"])["salary_in_usd"].mean().reset_index()  # calculer le salaire moyen par année et poste

fig4 = px.line(salary_trend, x="work_year", y="salary_in_usd", color="job_title", 
               title="Tendance des salaires pour les 10 postes les plus courants")  # créer un graphique linéaire interactif
fig4.update_xaxes(dtick=1, tickformat="d")  # ajuster les axes x
st.plotly_chart(fig4)  # afficher le graphique interactif

with st.expander("💭 Analyse des variations de salaire"):  # zone de texte extensible
    st.markdown("""
    - Les salaires ont tendance à augmenter au fil des années
    - Certains postes montrent une croissance plus rapide
    - La disparité entre les postes s'accentue avec le temps
    """)

# Salaire médian par expérience et taille d'entreprise
st.subheader("📊 Salaire médian par expérience et taille d'entreprise")  # sous-titre

median_salary = df.groupby(["experience_level", "company_size"])["salary_in_usd"].median().reset_index()  # calculer le salaire médian

fig5 = px.bar(median_salary, x="experience_level", y="salary_in_usd", color="company_size",
              title="Salaire médian par niveau d'expérience et taille d'entreprise")  # créer un graphique en barres interactif
st.plotly_chart(fig5)  # afficher le graphique

with st.expander("💭 Analyse des salaires médians"):  # zone de texte extensible
    st.markdown("""
    - Les grandes entreprises offrent généralement de meilleurs salaires
    - L'écart de salaire entre les niveaux d'expérience est plus marqué dans les grandes entreprises
    - Les petites entreprises montrent moins de variation entre les niveaux
    """)

# Ajout de filtres dynamiques sur les salaires
st.subheader("🎛️ Filtrage dynamique des salaires")  # sous-titre

salary_range = st.slider("Sélectionnez la plage de salaire", min_value=25000, max_value=175000, value=(25000, 175000))  # créer un curseur pour filtrer par salaire
df_filtered = df[(df["salary_in_usd"] >= salary_range[0]) & (df["salary_in_usd"] <= salary_range[1])]  # filtrer les données en fonction du salaire sélectionné

st.write(f"Nombre d'observations après filtrage : {len(df_filtered)}")  # afficher le nombre de données restantes après filtrage
st.write(df_filtered.head())  # afficher les premières lignes du DataFrame filtré

with st.expander("💭 Analyse du filtrage"):  # zone de texte extensible
    st.markdown("""
    - Le filtrage permet d'identifier les segments spécifiques
    - La majorité des salaires se situe dans une plage moyenne
    - Certains postes sortent des plages habituelles
    """)

# Analyse de l'impact du télétravail sur les salaires selon le pays
st.subheader("🏡 Impact du télétravail sur le salaire selon le pays")  # sous-titre

telework_impact = df.groupby(["remote_ratio", "company_location"])["salary_in_usd"].mean().reset_index()  # calculer l'impact du télétravail par pays

fig6 = px.bar(telework_impact, x="company_location", y="salary_in_usd", color="remote_ratio",
              title="Impact du télétravail sur les salaires")  # créer un graphique en barres interactif
st.plotly_chart(fig6)  # afficher le graphique

with st.expander("💭 Analyse de l'impact du télétravail"):  # zone de texte extensible
    st.markdown("""
    - Le télétravail complet offre souvent des salaires plus élevés
    - L'impact varie selon les pays
    - Certains pays privilégient le travail hybride
    """)

# Filtrage avancé des données par niveau d'expérience et taille d'entreprise
st.subheader("🔍 Filtrage avancé")  # sous-titre

exp_levels = st.multiselect("Sélectionnez le niveau d'expérience", df["experience_level"].unique())  # multi-sélection pour le niveau d'expérience
company_sizes = st.multiselect("Sélectionnez la taille d'entreprise", df["company_size"].unique())  # multi-sélection pour la taille d'entreprise

df_filtered_advanced = df  # copie du DataFrame original
if exp_levels:  # si des niveaux d'expérience sont sélectionnés
    df_filtered_advanced = df_filtered_advanced[df_filtered_advanced["experience_level"].isin(exp_levels)]  # filtrer par niveaux
if company_sizes:  # si des tailles d'entreprise sont sélectionnées
    df_filtered_advanced = df_filtered_advanced[df_filtered_advanced["company_size"].isin(company_sizes)]  # filtrer par taille d'entreprise

st.write(f"Nombre d'observations après filtrage avancé : {len(df_filtered_advanced)}")  # afficher le nombre de données après filtrage avancé
st.write(df_filtered_advanced.head())  # afficher les premières lignes du DataFrame filtré

with st.expander("💭 Analyse des statistiques générales"):  # zone de texte extensible
    st.markdown("""
    - Le jeu de données contient exactement 3,755 entrées
    - Les années couvertes vont de 2020 à 2023
    - La moyenne des années est d'environ 2022.37, indiquant que la majorité des données sont récentes
    - 50% des données se situent en 2022
    - Les données sont principalement concentrées sur 2022-2023
    - On observe une forte présence de profils seniors (SE) dans les données récentes
    """)

# Afficher les 5 jobs les mieux payés
job_salaries = df.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending=False)  # calculer et trier par salaire moyen

# Sélectionner les top 5 jobs
top_5_jobs = job_salaries.head(5)  # obtenir les 5 meilleurs salaires

# Créer un DataFrame pour l'affichage
top_5_df = pd.DataFrame({
    'Job Title': top_5_jobs.index,  # titres des postes
    'Average Salary (USD)': top_5_jobs.values  # salaires moyens
})

# Afficher le tableau dans Streamlit
st.subheader("Top 5 des jobs les mieux payés")  # sous-titre
st.table(top_5_df)  # afficher le tableau des jobs et salaires

with st.expander("💭 Analyse des jobs les mieux payés"):  # zone de texte extensible
    st.markdown("""
    - On retrouve le job Data Science Tech Lead qui est le mieux payé
    - Le job Data Science Tech Lead est 1,9 fois plus payé que Principal Data Scientist
    - Il y a beaucoup de différence entre les salaires
    """)
