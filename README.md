# Analyse du Churn & Prédictions ML – Projet Décisionnel (BI) & analyse dedonnées

## 1. Objectif du Projet & Contexte Business
Dans le secteur ultra-concurrentiel des télécommunications, acquérir un nouveau client coûte **5 fois plus cher** que d'en retenir un existant. La perte de clients (le Churn) détruit directement la rentabilité d'une entreprise.

L'objectif de ce projet est d'analyser le comportement des clients d'une entreprise de télécoms (Données certifiées IBM), d'identifier précisément pourquoi les abonnés à forte valeur partent, et de déployer un **modèle de Machine Learning** automatisé pour cibler les profils à risque avant qu'ils ne résilient.

**En combinant la Business Intelligence (BI) et la Data analysis et Science, ce projet apporte des solutions pour :**
*    **Réduire l'attrition (Churn) :** Intercepter les comptes fragiles avant la rupture.
*    **Améliorer la satisfaction :** Cibler les irritants techniques et de facturation.
*    **Sécuriser le Chiffre d'Affaires :** Concentrer les efforts marketing sur les clients les plus rentables.

---

## 2. Architecture des Données & Compréhension
Le projet s'appuie sur le dataset standardisé **Telco Customer Churn d'IBM**  regroupant le profil démographique, les types de contrats, les indicateurs financiers et le statut de résiliation des utilisateurs.

### Principaux indicateurs de la base :
*   **Identifiants :** `Customer ID` (Identifiant unique du client).
*   **Démographie :** `Gender` (Genre), `Senior Citizen`, `Partner`, `Dependents`.
*   **Abonnement & Usage :** `Tenure` (Ancienneté en mois), `Contract Type` (Mois par mois, 1 an, 2 ans), `Payment Method` (Mode de paiement).
*   **Services :** `Internet Service` (Fibre optique, DSL), `Tech Support` (Assistance technique), etc.
*   **Finances :** `Monthly Charges` (Frais mensuels), `Total Charges` (dépenses totales).
*   **Cibles d'analyse :** `Churn Value` (1 = Parti, 0 = Resté), `Churn Score` (Indice de risque), `CLTV` (Valeur long terme du client).

---

## 3. Pipeline ETL & Nettoyage des Données
Les données brutes ont été nettoyées et préparées via **Python (Pandas)** et **Power BI (Power Query)** pour garantir une intégrité totale avant l'analyse :

1.  **Suppression des doublons :** Vérification stricte et suppression de toute ligne dupliquée basée sur le `Customer ID`.
2.  **Correction des types de données :** Conversion des frais financiers textuels en **Décimaux** et de l'ancienneté (`Tenure`) en **Entiers**.
3.  **Traitement des valeurs manquantes :** Résolution des valeurs vides dans la colonne `Total Charges` (qui arrivaient principalement lorsque `Tenure = 0`) en les initialisant à 0 pour éviter les erreurs de calcul.


---

## 4. Indicateurs Clés de Performance BI (Mesures DAX)
Pour calculer des métriques précises et dynamiques, les mesures **DAX** suivantes ont été créées dans le modèle :

$$CustomerCount = COUNT(Fact_Client[CustomerID])$$

$$ChurnedCustomers = CALCULATE(COUNT(Fact_Client[CustomerID]), Fact_Client[Churn Value] = 1)$$

$$Churn Rate = DIVIDE([ChurnedCustomers], [CustomerCount], 0)$$

$$ARPU (average revenue per user) = AVERAGE(Fact_Client[Monthly Charges])$$

---

## 5. Modélisation Power BI & Dashboard Interactif
Plutôt que de charger une seule table plate, un modèle performant en **Schéma en Étoile** a été conçu pour séparer les faits transactionnels des dimensions métier :

*   **Table de Faits :** `Fact_Client` (Contient les enregistrements financiers et les scores de risque).
*   **Tables de Dimensions :** `Dimension_Service` (Configurations des abonnements) et `Dimension_Profil` (Données démographiques) et `Dimension_Geographie` (Données de localisation du client).

*   **Gestion des relations :** Liaisons actives par le `CustomerID` avec un filtrage adapté pour une navigation fluide.

###  Structure Visuelle du Dashboard
Le tableau de bord a été pensé pour offrir une lecture rapide et interactive , en incluant des visualisations telles que:
*   **Cartes d'en-tête (KPIs) :** Affichage des indicateurs globaux (`Total Clients`, `Taux de Churn`, `Score moyen de Churn` et `CLTV moyenne`).
*   **Histogramme groupé :** colonnes visuelles affichant le taux d'attrition (churn rate) en fonction du type de contrat des clients.
*   **Graphique en Courbes :** Visualisation du nombre de clients partis par groupe d'ancienneté, illustrant la perte critique de clients durant les premiers mois.

---

## 6. Analyse Prédictive & Machine Learning (Modèle V1)
Pour passer d'une analyse historique à une stratégie préventive, un modèle de classification **Random Forest** a été entraîné sous Python.

### Logique de découpage (La règle des 80/20)
Sur les **7 043 lignes** du fichier, un découpage strict a été appliqué (`test_size=0.20`) :
*   **80 % (5 634 clients) :** Réservés à l'entraînement de l'IA pour lui apprendre les comportements de Churn.
*   **20 % (1 409 clients) :** Conservés comme un "examen à l'aveugle". Le modèle n'a jamais vu ces clients durant son apprentissage. La matrice de confusion et les scores finaux sont calculés **uniquement** sur ces 1 409 clients pour simuler des prédictions réelles.

### Performances Réelles du Modèle
*   **Accuracy :** `75,00 %` – L'IA classe correctement 3 clients sur 4.
*   **Precision :** `57,00 %` – Lorsqu'une alerte est levée, elle est fiable dans plus de la moitié des cas (limite le gaspillage du budget marketing).
*   **Recall:** `46,00 %` – Le modèle parvient à intercepter à lui seul près de la moitié des départs réels dès cette première version.

### Pistes d'améliorationpour les performances :
Ce modèle sert de base de référence. Pour aller plus loin, les pistes techniques suivantes sont planifiées :
*  **Gestion du déséquilibre des classes (SMOTE) :** Le sur-échantillonnage synthétique permettra de créer des profils virtuels de "churners" pour booster le score de **Rappel**.
*  **Ajustement du seuil de classification :** Abaisser le seuil d'alerte par défaut (de 50 % à 35 %). En télécom, générer une fausse alerte (envoyer un mail de promo à un client heureux) coûte bien moins cher que de rater un client premium.

---

## 7. Analyses Métier
*   **Le probléme des hauts revenus :** L'analyse montre que le Churn ne touche pas les petits budgets. Il culmine sévèrement chez les clients payant entre **60 $ et 80 $ par mois**. L'entreprise réussit à garder ses petits clients mais perd sa base la plus rentable.
*   **L'échec de la phase d'accueil :** On observe une concentration massive de Churn chez les clients ayant **0 mois d'ancienneté** avec une facture de 80 $/mois. L'entreprise vend des abonnements premium très chers sans engagement (Mois par mois) ; au moindre problème le premier mois, le client s'en va immédiatement.
*   **La fragilité du sans engagement :** Les contrats au mois par mois représentent la quasi-totalité des clients perdus, face à la grande stabilité des abonnés engagés sur 1 ou 2 ans.

---

## 8. Remarques et solutions pour le churn:

### 1. Qu'est-ce qui cause la perte de clients
 Le Churn est principalement causé par le manque d'engagement contractuel associé à des prix élevés. Les clients qui prennent des abonnements "Fibre Optique" coûteux sans engagement se désabonnent très vite s'ils ne sont pas accompagnés par une assistance technique ou un suivi dès le départ.


### 2. Comment réduire le Churn :
 *   **Campagne de bascule contractuelle :** Il faut cibler les clients sans engagement à 60 et80 $ par mois en leur offrant un avantage financier s'ils passent sur un contrat stable d'un an.
 *   **Programme "Onboarding safe" :** Déclencher un appel automatique du service client au 15ème jour pour tous les nouveaux clients Premium afin de valider que l'installation technique fonctionne parfaitement.
 *  **Programme de fidélité pour les contrats "Mois par Mois" :** Plus les clients restent, moins ca devient cher pour eux, au bout d'un nombre de mois d'ancienneté, leur facture pourrait baisser ou ils peuvent avoir des options gratuite (streaming etc.)
