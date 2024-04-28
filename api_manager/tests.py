from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project, Contributor, Issue
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken

# --- TEST PROJECT --- #

class TestProjectViewSet(APITestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create(
            username="testuser",
            password="ok",
            can_be_contacted=True,
            can_data_be_shared=True,
            age=18,
        )
        # Génère un token JWT pour l'utilisateur
        self.token = str(AccessToken.for_user(self.user))
        
    def create_project(self, title, description, project_type):
        # Définir l'URL pour créer un projet
        url = "/api/project/"
        # Définir les données pour la création du projet
        data = {
            "title": title,
            "description": description,
            "project_type": project_type,
            "author": self.user.id,  # Assurez-vous que l'utilisateur est correctement spécifié
        }
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectuer la requête POST pour créer un projet
        response = self.client.post(url, data, format="json")
        return response

    def test_create_project(self):
        # Effectuer la création du projet
        response = self.create_project(
            "Nouveau projet", "Description du nouveau projet", "backend"
        )
        # Vérifier que la création du projet a réussi (code de statut HTTP 201)
        self.assertEqual(response.status_code, 201)
        # Vérifier que le projet a été créé dans la base de données
        self.assertTrue(Project.objects.filter(title="Nouveau projet").exists())

    def test_update_project(self):
        # Effectuer la création du projet
        self.create_project(
            "Nouveau projet", "Description du nouveau projet", "backend"
        )
        # Récupérer le projet créé dans la base de données
        project = Project.objects.get(title="Nouveau projet")
        # Définir l'URL pour mettre à jour le projet
        url = f"/api/project/{project.id}/"
        # Définir les données pour la mise à jour du projet
        data = {
            "title": "Projet mis à jour",
            "description": "Nouvelle description du projet",
            "project_type": "backend",
        }
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectuer la requête PUT pour mettre à jour le projet
        response = self.client.put(url, data)
        # Rafraîchir l'instance du projet depuis la base de données
        project.refresh_from_db()
        # Vérifier que la mise à jour du projet a réussi (code de statut HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Vérifier que les données du projet ont été mises à jour correctement
        self.assertEqual(project.title, "Projet mis à jour")
        self.assertEqual(project.description, "Nouvelle description du projet")
        self.assertEqual(project.project_type, "backend")
        
    def test_read_project(self):
        self.create_project(
            "Nouveau projet", "Description du nouveau projet", "backend"
        )
        # Récupérer le projet créé dans la base de données
        project = Project.objects.get(title="Nouveau projet")
        # Définir l'URL pour lire les détails du projet
        url = f"/api/project/{project.id}/"
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectuer une requête GET pour lire les détails du projet
        response = self.client.get(url)
        # Vérifier que la requête a réussi (code de statut HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Vérifier que les détails du projet renvoyés correspondent aux données du projet créé
        self.assertEqual(response.data["title"], "Nouveau projet")
        self.assertEqual(response.data["description"], "Description du nouveau projet")
        self.assertEqual(response.data["project_type"], "backend")

    def test_delete_project(self):
        self.create_project(
            "Nouveau projet", "Description du nouveau projet", "backend"
        )
        # Récupérer le projet créé dans la base de données
        project = Project.objects.get(title="Nouveau projet")
        # Définir l'URL pour lire les détails du projet
        url = f"/api/project/{project.id}/"
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectuer une requête DELETE pour supprimer le projet
        response = self.client.delete(url)
        # Vérifier que la requête a réussi (code de statut HTTP 204)
        self.assertEqual(response.status_code, 204)
        # Vérifier que le projet a été supprimé de la base de données
        self.assertFalse(Project.objects.filter(id=project.id).exists())

# --- TEST ISSUE --- #

class IssueViewSetTests(APITestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create(
            username="testuser",
            password="ok",
            can_be_contacted=True,
            can_data_be_shared=True,
            age=18,
        )
        # Génère un token JWT pour l'utilisateur
        self.token = str(AccessToken.for_user(self.user))
        # Crée un projet pour les tests
        self.project = Project.objects.create(
            title="Test Project",
            description="Test description",
            project_type="Test",
            author=self.user,
        )
        # Associe l'utilisateur en tant que contributeur du projet
        self.contributor = Contributor.objects.create(
            user=self.user, project=self.project
        )

    def test_create_issue(self):
        # Crée les données pour la création de l'issue
        data = {
            "title": "Test Issue ",
            "description": "Description test",
            "statut": "in_progress",
            "priority": "low",
            "balise": "bug",
            "contributors": [
                self.contributor.id
            ],  # Ajoute le contributeur existant comme contributeur de l'issue
        }
        # Configure l'URL pour la création de l'issue avec l'ID du projet
        url = f"/api/project/{self.project.id}/issues/"

        # Authentifie l'utilisateur pour la requête
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectue une requête POST pour créer l'issue
        response = self.client.post(url, data, format="json")
        # Vérifie que la requête a réussi et l'issue a été créée
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Issue.objects.filter(title="Test Issue").exists())

    def test_update_issue(self):
             
        # Crée une issue pour les tests
        issue = Issue.objects.create(
            title="Issue de test",
            description="Description de l'issue de test",
            statut="to_do",
            priority="high",
            balise="feature",
            project=self.project,
            author=self.user,
            
        )
        issue.contributors.set([self.contributor])

        data = {
            "title": "Issue de test modifiée",
            "description": "Description modifiée de l'issue de test",
            "statut": "in_progress",
            "priority": "low",
            "balise": "bug",
            "contributors": [
                self.contributor.id
            ],  # Ajoute le contributeur existant comme contributeur de l'issue
        }
        # Configure l'URL pour la mise à jour de l'issue avec l'ID de l'issue
        url = f"/api/project/{self.project.id}/issues/{issue.id}/"

        # Authentifie l'utilisateur pour la requête
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectue une requête PUT pour mettre à jour l'issue
        response = self.client.put(url, data, format="json")
        # Rafraîchir l'instance de l'issue depuis la base de données
        issue.refresh_from_db()
        # Vérifie que la requête a réussi et l'issue a été mise à jour
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(issue.title, "Issue de test modifiée")
        
    def test_read_issue(self):
        
         # Crée une issue pour les tests
        issue = Issue.objects.create(
            title="Issue de test",
            description="Description de l'issue de test",
            statut="to_do",
            priority="high",
            balise="feature",
            project=self.project,
            author=self.user,
            
        )
        issue.contributors.set([self.contributor])
        
        url = f"/api/project/{self.project.id}/issues/{issue.id}/"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifier que les détails de l'issue renvoyés correspondent aux données de l'issue créée
        self.assertEqual(response.data["title"], "Issue de test")
        self.assertEqual(response.data["description"], "Description de l'issue de test")
        self.assertEqual(response.data["statut"], "to_do")
        self.assertEqual(response.data["priority"], "high")
        self.assertEqual(response.data["balise"], "feature")
        
    def test_delete_issue(self):
           # Crée une issue pour les tests
        issue = Issue.objects.create(
            title="Issue de test",
            description="Description de l'issue de test",
            statut="to_do",
            priority="high",
            balise="feature",
            project=self.project,
            author=self.user,
            
        )
        issue.contributors.set([self.contributor])
        # Définir l'URL pour lire les détails du projet
        url = f"/api/project/{self.project.id}/issues/{issue.id}/"
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Effectuer une requête DELETE pour supprimer le projet
        response = self.client.delete(url)
        # Vérifier que la requête a réussi (code de statut HTTP 204)
        self.assertEqual(response.status_code, 204)
        # Vérifier que le projet a été supprimé de la base de données
        self.assertFalse(Issue.objects.filter(id=issue.id).exists())
        
# --- TEST COMMENT --- #