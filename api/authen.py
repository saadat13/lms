import jwt
from django.contrib.auth import user_logged_in
from rest_framework import status, authentication, exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_jwt.serializers import jwt_payload_handler
from .models import User


class IsFirstAuthenticate:
    @staticmethod
    def authenticate_user(request):
        try:
            username = request.data.get['username']
            password = request.data.get['password']
            user = User.objects.get(username=username, password=password)
            if user:
                try:
                    secret_key = "strange secret key"
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
                    user_details = {}
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or cant find the account'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a username and a password'}
            return Response(res)


# class IsSecondAuthenticated(BasicAuthentication):
#     @staticmethod
#     def second_authenticate(request):
#         json_data = json.loads(request.body)
#         token = json_data['token']
#         data = User.objects.filter(token=token)
#         if len(data) == 0:
#             flag = True
#         else:
#             flag = False
#         return flag


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        json_data = json.loads(request.body)
        # username = json_data['username']
        token = json_data['token']
        data = User.objects.filter(token=token)
        if len(data) == 0:
            return None
        try:
            user = User.objects.get(token=token) # get the user
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist

        return (user, None) # authentication successful