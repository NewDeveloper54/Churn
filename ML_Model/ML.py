# Kit de préparation des données et d'analyse exploratoire pour le projet de churn client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

# Charger le Dataset nettoyé
df = pd.read_csv("Telco_customer_churn_clean.csv")
df.head()

df.columns.tolist()


sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


print("Graphique 1")

# Encodage automatique des variables textuelles catégorielles 
colonnes_encoder = [col for col in ['Contract', 'Internet Service', 'Payment Method'] if col in df.columns]
df_ml = pd.get_dummies(df, columns=colonnes_encoder, drop_first=True)

y = df_ml['Churn Value']

# Nottoyage de X
X = df_ml.select_dtypes(include=[np.number])

X = X.drop(columns=[col for col in ['Churn Value', 'Churn Score', 'CLTV','Latitude','Longitude','Zip Code'] if col in X.columns])

# 4. Entraînement du modèle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Calcul de l'importance des variables
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 6))
sns.barplot(x=importances[indices][:8], y=X.columns[indices][:8], palette="Reds_r")
plt.title("Facteurs prédictifs du Churn", fontsize=14, fontweight='bold')
plt.xlabel("Importance du modèle")
plt.ylabel("Variables")
plt.tight_layout()
plt.savefig('facteurs_predictifs.png', dpi=300)
plt.show()

#===================================
print("Graphique 2")

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

tn, fp, fn, tp = cm.ravel()

labels = np.array([
[f"TN (prédis et réellement resté)\n{tn}", f"FP (prédis churn mais réellement resté)\n{fp}"],
[f"FN (prédis resté mais réellement churn)\n{fn}", f"TP (prédis et réellement churn)\n{tp}"]])

plt.figure(figsize=(7, 5.5))
sns.heatmap(cm, annot=labels, fmt="", cmap='Blues', cbar=False, annot_kws={"size": 12},
xticklabels=['Prédit : Reste (0)', 'Prédit : Churn (1)'], 
yticklabels=['Réel : Reste (0)', 'Réel : Churn (1)'])

plt.title("Matrice de Confusion : Analyse des Erreurs ML", fontsize=14, fontweight='bold')
plt.xlabel("Prédictions du Modèle (IA)", fontsize=11, labelpad=10)
plt.ylabel("Réalité Terrain (Données Réelles)", fontsize=11, labelpad=10)
plt.tight_layout()
plt.savefig('matrice_confusion.png', dpi=300)
plt.show()

#==================================
print("Graphique 3")
features_scaled = StandardScaler().fit_transform(df[['Monthly Charges', 'Tenure Months']])
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Segment'] = kmeans.fit_predict(features_scaled)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Tenure Months', y='Monthly Charges', hue='Segment', palette='Set1', alpha=0.8, s=70)
plt.title("Segmentation Stratégique des Clients (K-Means Clustering)", fontsize=14, fontweight='bold')
plt.xlabel("Ancienneté (Mois)")
plt.ylabel("Frais Mensuels ($)")
plt.legend(title="Groupes de Clients")
plt.tight_layout()
plt.savefig('segmentation_clients.png', dpi=300)
plt.show()


# Precision
clients_count= tp+tn+fp+fn
precision = tp/ (tp+fp)
accuracy = (tp+tn)/ clients_count
recall = tp / (tp+fn)

print(f"Le Nombre de clients testés est : {clients_count}")
print(f"Accuracy  = (TP + TN) / Total  = {accuracy:.2%}")
print(f"Precision = TP / (TP + FP)     = {precision:.2%}")
print(f"Recall    = TP / (TP + FN)     = {recall:.2%}")
