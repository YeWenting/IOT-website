from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.


def get_index(request):
    return HttpResponseRedirect('/static/index.html')


def switch_index(request):
    return HttpResponseRedirect("home/")


def get_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        response = False
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response = True
            else:
                print("user is not active")
        else:
            print("user is None")
        print(request.session.keys())
        # resp = serialize(response);
        return JsonResponse(response, safe=False)


def get_sign_up(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html')
    elif request.method == 'POST':
        response = True
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        # user, created = User.objects.get_or_create(username=username)
        # if created == True:
        #     response = True
        #     user.
        try:
            User.objects.create_user(username=username, password=password, email=email)
        except:
            response = False
        return JsonResponse(response, safe=False)


def get_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

