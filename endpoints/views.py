from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from endpoints.permissions import IsAppUserOrReadOnly
import endpoints.models as models
import endpoints.serializers as serializers

# Create your views here.

# API
# TODO - move to documentation
# GET /user/<username>
#   returns all apps used by user <username>
# POST /user/<username>
#   with payload: <app>
#   with auth
#   adds <app> for user <username>
# GET /app/<app>
#   returns app <app> global stats
# POST /app
#   with payload: {name: <app_name>}
#   with auth
#   adds new app
# GET /user/<username>/<app>
#   returns user <username>'s stats concerning <app> usage
# POST /user/<username>/<app>
#   with auth
#   creates new session
#   returns session id
# PUT /user/<username>/<app>
#   with payload: {finished: <has_finished>}
#   session heartbeat
#   if (<has_finished>) stops current session


class UserView(APIView):
    permission_classes = (IsAppUserOrReadOnly, )

    def get(self, request, username):
        user = User.objects.get(username=username)
        used_apps = models.UsedApp.objects.filter(user=user)
        serializer = serializers.UsedAppSerializer(used_apps, many=True)
        return Response(serializer.data)


class AppView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        serializer = serializers.AppSerializer(data=request.data)
        serializer.save(creator=request.user)
        return Response(serializer.data)
