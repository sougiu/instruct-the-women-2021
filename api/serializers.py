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

        especificada = False
        
        # Checar se a versão foi especificada
        for chave in data:
            if chave == 'version':
                versao_pacote = data[chave]
                especificada = True
        
        # Checar se número da versão é válido
        if especificada:
            existente = version_exists(data["name"], versao_pacote)
            if existente == True:
                return data
            else:
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
        
        # Se a versão não for especificada, procurar a última versão
        else:
            ultima_versao = latest_version(data["name"])
            
            # Subir a exceção `serializers.ValidationError()` se o pacote não
            # for válido
            if ultima_versao == "None":
                raise serializers.ValidationError({"error": "One or more packages doesn't exist"})
            
            # Retornar os dados atualizados e completos
            else:
                data['version'] = ultima_versao
                return data

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def create(self, validated_data):
        # Algumas referência para uso de models do Django:
        # - https://docs.djangoproject.com/en/3.2/topics/db/models/
        # - https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        
        packages = validated_data["packages"]

        # Definir nome do projeto (qualquer nome)
        projeto = Project.objects.create(name=validated_data["name"])

        # Iterar por todos pacotes
        for i in range(len(packages)):
            package = PackageRelease.objects.create(name=packages[i]['name'], version=packages[i]['version'], project=projeto)

        # Salvar o projeto e seus pacotes associados.
        projeto.save()

        return projeto
