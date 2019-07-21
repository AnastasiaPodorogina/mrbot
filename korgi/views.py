from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

from .models import CustomUser
# Create your views here.


@csrf_exempt
def registration(request):
    if request.method == 'POST':
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


@csrf_exempt
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            try:
                user = CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                return HttpResponse('Such user does not exist', status=404)

            if user.check_password(password):
                login(request, user)
                return HttpResponse("You're logged in.")
            else:
                return HttpResponse("Your username and password didn't match.", status=400)
    else:
        return HttpResponse('You are already logged in')


def logout_view(request):
    try:
        logout(request)
    except KeyError:
        pass
    return HttpResponse("You're logged out.")


@csrf_exempt
def count_view(request):
    if request.user.is_authenticated:
        username = request.user.get_username()
        user = CustomUser.objects.get(username=username)

        if request.method == 'POST':
            user.count += 1
            user.save()
            return HttpResponse(f'Count update {user.count} for {username}')

        if request.method == 'GET':
            return HttpResponse(f'For user {username} count = {user.count}')

        if request.method == 'DELETE':
            user.count -= 1
            user.save()
            return HttpResponse(f'Count update {user.count} for {username}')
    else:
        return HttpResponse('Permission denied. You have to login')
