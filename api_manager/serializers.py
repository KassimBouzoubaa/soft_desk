from rest_framework import serializers
from .models import Project, Contributor
from users.serializers import UserDetailSerializer

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'created_time']

class ProjectRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type'] 
        
class ProjectDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    contributors = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = ['title', 'description', 'project_type', 'created_time', 'author', 'contributors']  
