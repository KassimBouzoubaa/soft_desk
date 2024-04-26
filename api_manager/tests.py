from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken


class TestProjectViewSet(APITestCase):
    def setUp(self):
        # Crée un utilisateur pour les tests
        self.user = User.objects.create(username='testuser', password='ok', can_be_contacted=True, can_data_be_shared=True, age=18)
        # Génère un token JWT pour l'utilisateur
        self.token = str(AccessToken.for_user(self.user))

    def create_project(self, title, description, project_type):
        # Définir l'URL pour créer un projet
        url = '/api/project/'
        # Définir les données pour la création du projet
        data = {
            'title': title,
            'description': description,
            'project_type': project_type,
            'author': self.user.id  # Assurez-vous que l'utilisateur est correctement spécifié
        }
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Effectuer la requête POST pour créer un projet
        response = self.client.post(url, data, format='json')
        return response

    def test_create_project(self):
        # Effectuer la création du projet
        response = self.create_project('Nouveau projet', 'Description du nouveau projet', 'backend')
        # Vérifier que la création du projet a réussi (code de statut HTTP 201)
        self.assertEqual(response.status_code, 201)
        # Vérifier que le projet a été créé dans la base de données
        self.assertTrue(Project.objects.filter(title='Nouveau projet').exists())

    def test_update_project(self):
        # Effectuer la création du projet
        self.create_project('Nouveau projet', 'Description du nouveau projet', 'backend')
        # Récupérer le projet créé dans la base de données
        project = Project.objects.get(title='Nouveau projet')
        # Définir l'URL pour mettre à jour le projet
        url = f'/api/project/{project.id}/'
        # Définir les données pour la mise à jour du projet
        data = {
            'title': 'Projet mis à jour',
            'description': 'Nouvelle description du projet',
            'project_type': 'backend',
        }
        # Ajouter le token JWT à l'en-tête d'autorisation
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        # Effectuer la requête PUT pour mettre à jour le projet
        response = self.client.put(url, data)
        # Rafraîchir l'instance du projet depuis la base de données
        project.refresh_from_db()
        # Vérifier que la mise à jour du projet a réussi (code de statut HTTP 200)
        self.assertEqual(response.status_code, 200)
        # Vérifier que les données du projet ont été mises à jour correctement
        self.assertEqual(project.title, 'Projet mis à jour')
        self.assertEqual(project.description, 'Nouvelle description du projet')
        self.assertEqual(project.project_type, 'backend')
