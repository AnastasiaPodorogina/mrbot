import json

from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views import View

from .models import CustomUser


# Create your views here.


class RegistrationView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            user = CustomUser(username=username)
            user.set_password(password)

            user.save()
            return HttpResponse("Registery successful", status=201)
        except KeyError:
            HttpResponse('expected fields "username", "password"')



class LoginView(View):

    def post(self, request):
        if not request.user.is_authenticated:

            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            try:
                user = CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponse('Such user does not exist', status=404)

            if user.check_password(password):
                login(request, user)
                return HttpResponse("You're logged in.", status=200)
            else:
                return HttpResponse("Your username and password didn't match.", status=400)
        else:
            return HttpResponse('You are already logged in')


class LogoutView(View):

    def get(self, request):
        try:
            logout(request)
        except KeyError:
            pass
        return HttpResponse("You're logged out.")


class CountView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Permission denied. You have to login')
        username = request.user.get_username()
        user = CustomUser.objects.get(username=username)
        return HttpResponse(f'For user {username} count = {user.count}')

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Permission denied. You have to login')
        username = request.user.get_username()
        user = CustomUser.objects.get(username=username)
        user.count += 1
        user.save()
        return HttpResponse(f'Count update {user.count} for {username}')

    def delete(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Permission denied. You have to login')
        username = request.user.get_username()
        user = CustomUser.objects.get(username=username)
        user.count -= 1
        user.save()
        return HttpResponse(f'Count update {user.count} for {username}')
