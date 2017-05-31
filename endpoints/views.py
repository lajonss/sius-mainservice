from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from endpoints.permissions import IsAppUserOrReadOnly
import endpoints.models as models
import endpoints.serializers as serializers

# Create your views here.

# API
# TODO - move to documentation
# GET /user/<username>/
#   returns all apps used by user <username>
# POST /user/
#   with payload: <app>
#   with auth
#   adds <app> for user <username>
# GET /app/<app>/
#   returns app <app> global stats
# POST /app/
#   with payload: {name: <app_name>}
#   with auth
#   adds new app
# GET /user/<username>/<app>/
#   returns user <username>'s stats concerning <app> usage
# PUT /user/app/<app>/
#   with auth
#   updates user's app metadata (e.g. rating or notes)
# POST /user/app/<app>/
#   with auth
#   creates new session
#   returns session id
# PUT /user/app/<app>/session/
#   with auth
#   session heartbeat
# DELETE /user/app/<app>/session/
#   with auth
#   ends current session


class UserView(APIView):
    """
    GET /user/<username>/
    returns all apps used by user named <username>
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request):
        try:
            app = models.App.objects.filter(name=request.data).get()
            serializer = serializers.UsedAppSerializer(data={})
            if serializer.is_valid():
                serializer.save(user=request.user, app=app)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            used_apps = models.UsedApp.objects.filter(user=user)
            serializer = serializers.UsedAppSerializer(used_apps, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AppView(APIView):
    """
    GET /app/<app>/
    returns app named <app> global stats
    POST /app/
    with payload: {name: <app_name>}
    with auth
    creates new app named <app_name>
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request):
        serializer = serializers.AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, appname=None):
        try:
            app = models.App.objects.filter(name=appname).get()
            serializer = serializers.AppSerializer(app)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UsedAppView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def post(self, request, appname):
        try:
            app = models.App.objects.filter(name=appname).get()
            used_app = models.UsedApp.objects.filter(
                user=request.user, app=app).get()
            session_serializer = serializers.AppSessionSerializer(
                data={'used_app': used_app.id})
            if session_serializer.is_valid():
                session = session_serializer.save()
                used_app_serializer = serializers.UsedAppSerializer(
                    used_app, data={'current_session': session}, partial=True)
                if used_app_serializer.is_valid():
                    used_app_serializer.save()
                    return Response(session_serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, appname):
        try:
            app = models.App.objects.filter(name=appname).get()
            used_app = models.UsedApp.objects.filter(
                user=request.user, app=app).get()
            serializer = serializers.UsedAppSerializer(
                used_app, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
