from rest_framework import serializers
from django.contrib.auth.models import User
import endpoints.models as models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.App


class UsedAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UsedApp


class AppEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppEvent
