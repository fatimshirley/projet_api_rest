# Tasks API

API REST de gestion de tâches avec authentification JWT.

## Technologies

* Python 3.12+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* JWT
* bcrypt
* Bruno

## Fonctionnalités

### Authentification

* Inscription des utilisateurs
* Email unique
* Mot de passe sécurisé avec hash bcrypt
* Connexion avec génération d'un JWT
* Protection des endpoints avec Bearer Token

### Gestion des tâches

Un utilisateur peut :

* créer une tâche ;
* consulter ses tâches ;
* consulter une tâche précise ;
* modifier une tâche ;
* marquer une tâche comme terminée ;
* supprimer une tâche.

Chaque utilisateur ne peut accéder qu'à ses propres tâches.

## Endpoints

### Authentification

| Méthode | Endpoint         | Description |
| ------- | ---------------- | ----------- |
| POST    | `/auth/register` | Inscription |
| POST    | `/auth/login`    | Connexion   |

### Tâches

| Méthode | Endpoint                    | Description         |
| ------- | --------------------------- | ------------------- |
| POST    | `/tasks`                    | Créer une tâche     |
| GET     | `/tasks`                    | Lister mes tâches   |
| GET     | `/tasks/{task_id}`          | Récupérer une tâche |
| PUT     | `/tasks/{task_id}`          | Modifier une tâche  |
| PATCH   | `/tasks/{task_id}/complete` | Terminer une tâche  |
| DELETE  | `/tasks/{task_id}`          | Supprimer une tâche |

## Filtres

L'API permet de filtrer les tâches :

* `/tasks?completed=true`
* `/tasks?completed=false`
* `/tasks?priority=high`
* `/tasks?priority=medium`
* `/tasks?priority=low`

Les priorités disponibles sont :

* `low`
* `medium`
* `high`

## Validation

L'API vérifie notamment :

* nom utilisateur obligatoire ;
* adresse email valide ;
* adresse email unique ;
* mot de passe d'au moins 8 caractères ;
* titre de tâche obligatoire ;
* priorité valide ;
* champ `completed` booléen.

Les données invalides retournent une erreur `422 Unprocessable Entity`.

Une adresse email déjà utilisée retourne une erreur `409 Conflict`.

Une tâche inexistante ou appartenant à un autre utilisateur retourne une erreur `404 Not Found`.

## Installation

Créer et activer l'environnement virtuel :


python -m venv .venv
source .venv/bin/activate


Installer les dépendances :


pip install -e .


## Configuration

Créer un fichier `.env` à la racine du projet :


DATABASE_URL=postgresql+psycopg2://USER:PASSWORD@localhost:5432/tasks_api
JWT_SECRET=votre_secret_jwt


Adapter les valeurs à votre installation PostgreSQL.

Le fichier `.env` ne doit pas être versionné.

## Base de données

Le projet utilise PostgreSQL avec SQLAlchemy.

La relation entre les entités est :


User 1 ---- N Task


Chaque tâche possède un `user_id` correspondant à son propriétaire.

## Lancement

Lancer l'API avec :


uvicorn src.projet_api_rest.main:app --reload


L'API est accessible à :


http://127.0.0.1:8000


Documentation Swagger :


http://127.0.0.1:8000/docs


Documentation ReDoc :


http://127.0.0.1:8000/redoc


Health check :


http://127.0.0.1:8000/health


## Authentification JWT

Après une connexion réussie sur `/auth/login`, l'API retourne un token JWT.

Les endpoints protégés nécessitent :


Authorization: Bearer VOTRE_TOKEN


Le propriétaire de la tâche est automatiquement déterminé à partir de l'utilisateur authentifié.

Le client ne peut pas choisir le `user_id` lors de la création d'une tâche.

## Tests

Les fonctionnalités de l'API ont été vérifiées avec des requêtes HTTP et Bruno.

Les tests couvrent notamment :

* inscription ;
* email déjà utilisé ;
* connexion avec identifiants corrects ;
* mot de passe incorrect ;
* accès à un endpoint protégé sans token ;
* accès avec un token valide ;
* création d'une tâche ;
* récupération de la liste des tâches ;
* récupération d'une tâche ;
* récupération d'une tâche inexistante ;
* modification d'une tâche ;
* complétion d'une tâche ;
* suppression d'une tâche ;
* filtrage des tâches ;
* validation des données ;
* isolation des utilisateurs.

## Bruno

La collection Bruno se trouve dans le dossier :


Tasks API/


Structure :


Tasks API/
├── Register.yml
├── Login.yml
└── Tasks/
    ├── Create task.yml
    ├── Get my tasks.yml
    ├── Get task by ID.yml
    ├── Filter tasks.yml
    ├── Update task.yml
    ├── Complete task.yml
    └── Delete task.yml


## Structure du projet

projet_api_rest/
├── src/
│   └── projet_api_rest/
│       ├── auth/
│       ├── core/
│       ├── database/
│       ├── models/
│       ├── routers/
│       ├── schemas/
│       └── services/
├── Tasks API/
├── .env
├── .gitignore
├── main.py
├── pyproject.toml
└── README.md


## Sécurité

Les mots de passe sont stockés sous forme de hash et ne sont jamais enregistrés en clair.

Les endpoints de gestion des tâches sont protégés par authentification JWT.

Les tâches sont systématiquement associées à l'utilisateur authentifié.

Un utilisateur ne peut pas consulter, modifier ou supprimer la tâche d'un autre utilisateur.

## Auteur

Projet pratique — API REST Gestion de tâches
