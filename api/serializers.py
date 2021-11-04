from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import PackageRelease, Project
from .pypi import version_exists, latest_version
import json
from rest_framework.renderers import JSONRenderer

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}   
    
    # Validar o pacote, checar se ele existe na versão especificada.
    def validate(self, data):
        nome_pacote = data.get('name', '')
        versao_pacote = data.get('version', '')

        if versao_pacote:
            existente = version_exists(nome_pacote, versao_pacote)
            
            if existente:
                return data
            else:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        
        ultima_versao = latest_version(nome_pacote)

        if ultima_versao:
            data['version'] = ultima_versao
            return data
        else:
            raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        packages = validated_data["packages"]

        projeto =  Project.objects.create(name=validated_data["name"])

        for package in packages:
            PackageRelease.objects.create(project=projeto, name=package["name"], version=package["version"])

        return projeto
