import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Charger le Dataset
script_dir = Path(__file__).resolve().parent

chemin = script_dir.parent / "Dataset" / "Telco_customer_churn.xlsx"

df = pd.read_excel(chemin)
df.head()

df.columns.tolist()

df.isna().sum()

df.info()

#Préparation des données 
df_churn = df.drop(columns=['Count', 'Country', 'State', 'Lat Long','Churn Label'], axis=1)

# Afficher le nouveau Dataset:
df_churn.head()

df_churn.info()

# Changer le type des données
colonnes_numeriques=['Zip Code','Latitude','Longitude','Tenure Months','Monthly Charges','Total Charges','Churn Value','Churn Score','CLTV']
colonnes_textuelles=['CustomerID','City','Gender','Senior Citizen','Partner','Dependents','Phone Service','Multiple Lines','Internet Service','Online Security','Online Backup','Device Protection','Tech Support','Streaming TV','Streaming Movies','Contract','Paperless Billing','Payment Method','Churn Reason']

df_churn[colonnes_numeriques]=df_churn[colonnes_numeriques].apply(pd.to_numeric, errors="coerce")
df_churn[colonnes_textuelles]=df_churn[colonnes_textuelles].astype(str)
df_churn['Churn Reason'] = df_churn['Churn Reason'].replace({'NaN': None, 'nan': None})
df_churn['Churn Reason']=df_churn['Churn Reason'].fillna("Client already with us")
df_churn['Total Charges']=df_churn['Total Charges'].fillna(0)

df_churn.isna().sum()

df_churn['CustomerID'].duplicated().sum()

# Visuels

#répartition des déaprts selon le genre
plt.figure(figsize=(8,5))
sns.countplot(data=df_churn, x='Gender', hue='Churn Value')

plt.title("répartition des déaprts selon le genre")
plt.xlabel("Genre")
plt.ylabel("Nombre de clients")
plt.legend(title="Statut", labels=["Resté (0)", "Parti (1)"])

plt.show()


#matrice de corrélation des variables numériques

colonnes_a_traiter=['Tenure Months', 'Monthly Charges', 'Total Charges', 'Churn Value', 'Churn Score', 'CLTV']
matrice_correlation= df_churn[colonnes_a_traiter].corr()
plt.figure(figsize=(10,5))

#heatmap pour la matrice
sns.heatmap(matrice_correlation, annot=True, cmap="coolwarm", linewidth =0.5)

plt.title("matrice de corrélation des variables numériques")
plt.show()

#Vérifications
df_churn[df_churn['Churn Value']== 0]

# Exporter les nouvelles données

df_churn.to_csv("Telco_customer_churn_clean.csv", index=False)
