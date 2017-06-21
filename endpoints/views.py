from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from endpoints.permissions import IsAppUserOrReadOnly
import endpoints.models as models
import endpoints.serializers as serializers


class UserView(APIView):
    """
    GET /user/
    returns list of users
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

    def get(self, request, username=None):
        if username is None:
            users = User.objects.all()
            serializer = serializers.UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            try:
                user = User.objects.get(username=username)
                used_apps = models.UsedApp.objects.filter(user=user)
                serializer = serializers.UsedAppSerializer(
                    used_apps, many=True)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class AppView(APIView):
    """
    GET /app/
    returns list of apps
    GET /app/<appname>/
    returns app named <appname> global stats
    POST /app/
    with payload: {name: <appname>}
    with auth
    creates new app named <appname>
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
        if appname is None:
            apps = models.App.objects.all()
            serializer = serializers.AppSerializer(apps, many=True)
            return Response(serializer.data)
        else:
            try:
                app = models.App.objects.filter(name=appname).get()
                serializer = serializers.AppSerializer(app)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class UsedAppView(APIView):
    """
    GET /user/<username>/<appname>/
    returns user <username>'s <appname> sessions
    POST /user/<username>/<appname>/
    with payload: {"start_time": <time>}
    with auth
    starts new session
    PUT /user/<username>/<appname>/
    with payload: {"notes"(optional): <notes>, "rating"(optional): <rating>}
    with auth
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, username, appname):
        try:
            app = models.App.objects.filter(name=appname).get()
            user = User.objects.filter(username=username).get()
            used_app = models.UsedApp.objects.filter(
                user=user, app=app).get()
            sessions = models.AppSession.objects.filter(used_app=used_app)
            serializer = serializers.AppSessionSerializer(sessions, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, username, appname):
        try:
            if username != request.user.username:
                return Response("User authorization failed.", status=status.HTTP_403_FORBIDDEN)
            app = models.App.objects.filter(name=appname).get()
            used_app = models.UsedApp.objects.filter(
                user=request.user, app=app).get()
            session_serializer = serializers.AppSessionSerializer(
                data=request.data)
            if session_serializer.is_valid():
                session = session_serializer.save(used_app=used_app)
                used_app.current_session = session
                used_app.save()
                return Response(session_serializer.data)
            else:
                return Response(session_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username, appname):
        try:
            if username != request.user.username:
                return Response("User authorization failed.", status=status.HTTP_403_FORBIDDEN)
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


class AppSessionView(APIView):
    """
    PUT /user/<username>/<appname>/session/
    with auth
    with payload: {"end_time": <time>}
    updates current session
    DELETE /user/<username>/<appname>/session/
    with auth
    with payload: {"end_time"(optional): <time>}
    ends current session
    """
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, username, appname):
        try:
            if username != request.user.username:
                return Response("User authorization failed.", status=status.HTTP_403_FORBIDDEN)
            app = models.App.objects.filter(name=appname).get()
            used_app = models.UsedApp.objects.filter(
                user=request.user, app=app).get()
            session = used_app.current_session
            print(session)
            if session is None or session.finished == True:
                return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
            else:
                serializer = serializers.AppSessionSerializer(
                    session, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, username, appname):
        try:
            if username != request.user.username:
                return Response("User authorization failed.", status=status.HTTP_403_FORBIDDEN)
            app = models.App.objects.filter(name=appname).get()
            used_app = models.UsedApp.objects.filter(
                user=request.user, app=app).get()
            session = used_app.current_session
            if session is None or session.finished:
                return Response(session, status=status.HTTP_408_REQUEST_TIMEOUT)
            else:
                data = {
                    'finished': True
                }
                if 'end_time' in request.data:
                    data['end_time'] = request.data['end_time']
                serializer = serializers.AppSessionSerializer(
                    session, data=data, partial=True)
                if serializer.is_valid():
                    saved_session = serializer.save()
                    used_app.time_summary += saved_session.end_time - saved_session.start_time
                    used_app.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
