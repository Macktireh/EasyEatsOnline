# API Backend Ecommerce en Flask

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

### 2. Créer l'environnement virtual

```bash
python -m venv .venv
```
### 3. Activer l'environnement virtual

****Pour Windows :****

```bash
.venv\Scripts\activate
```

****Pour Linux ou Mac os :****

```bash
source .venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

Renommer le fichier `.env.example` en `.env` et renseigner vos informations. 

### 6. Appliquer les migrations

```bash
flask db upgrade
```

### 7. Lancer le server de développement :

```bash
flask run
```

C'est fait 🚀
