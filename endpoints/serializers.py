from rest_framework import serializers
from django.contrib.auth.models import User
import endpoints.models as models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class AppSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = models.App
        fields = '__all__'


class UsedAppSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    app = serializers.ReadOnlyField(source='app.name')

    class Meta:
        model = models.UsedApp
        fields = '__all__'


class AppSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AppSession
