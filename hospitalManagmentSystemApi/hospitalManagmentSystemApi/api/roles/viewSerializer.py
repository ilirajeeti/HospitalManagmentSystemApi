from rest_framework import serializers
from .viewModel import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = ('id',) 
