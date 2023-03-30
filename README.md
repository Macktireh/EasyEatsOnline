# API Ecommerce en Flask

Il s'agit de l'API backend d'un site de commerce électronique construit avec Flask.

Pour que ce projet soit opérationnel, vous devez commencer par installer `Python` sur votre ordinateur. Il est conseillé de créer un environnement virtuel pour stocker les dépendances de vos projets séparément.

Dans un terminal et exécuter les commandes suivantes:

### 1. Cloner le projet 

Si vous avez `Git` sur votre ordinateur utiliser les commandes ci-dessous sinon télécharger simplement le projet.

```bash
git clone https://github.com/Macktireh/ecommerce-backend-flask.git ecommerce-backend
```

```bash
cd ecommerce-backend
```

Si vous avez `Docker` installer sur vorte ordinateur, vous pouvez utilisez docker pour lancer le projet

### 2. Avec Docker

lancer la commande ci-dessous à la racine du projet :

```bash
docker-compose up --build -d
```

### 3. Sans Docker

#### 3.1 Créer l'environnement virtual

```bash
python -m venv .venv
```
#### 3.2 Activer l'environnement virtual

****Pour Windows :****

```bash
.venv\Scripts\activate
```

****Pour Linux ou Mac os :****

```bash
source .venv/bin/activate
```

#### 3.3 Installer les dépendances

```bash
pip install -r requirements.txt
```

#### 3.4 Configurer les variables d'environnement

Renommer le fichier `.env.example` en `.env` et renseigner vos informations. 

#### 3.5 Appliquer les migrations

```bash
flask db upgrade
```

#### 3.6 Lancer le server de développement :

```bash
flask run
```

C'est fait 🚀 
