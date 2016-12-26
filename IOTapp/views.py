from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from IOTapp.models import Device
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required()
def get_index(request):

    list = []
    userid = request.session['userid']
    devices = Device.objects.filter(user=userid)

    for dev in devices:
        if dev.cur_temp > dev.threshold:
            is_warning = True
        else:
            is_warning = False
        print(dev.last_updated)
        temp_dev = {"id": dev.id, "SN": dev.SN, "name": dev.name, "temp": dev.cur_temp, "is_warning": is_warning,
                    "last_updated": dev.last_updated}
        list.append(temp_dev)

    return render(request, 'index.html', {'deviceList': list})


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
                request.session['username'] = user.username
                request.session['userid'] = user.id
            else:
                print("user is not active")
        else:
            print("user is None")
        print(request.session.keys())
        # resp = serialize(response);
        return JsonResponse(response, safe=False)


def get_logout(request):
    logout(request)


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


# API Method
@login_required()
def get_list(request):
    list = []
    devices = Device.objects.all()

    for dev in devices:
        if dev.cur_temp > dev.threshold:
            is_warning = True
        else:
            is_warning = False
        print(dev.last_updated)
        temp_dev = {"id": dev.id, "SN": dev.SN, "name": dev.name, "temp": dev.cur_temp, "is_warning": is_warning,
                    "last_updated": str(dev.last_updated)}
        list.append(temp_dev)

    res = {"deviceList": list}
    return JsonResponse(res)


def get_form(request):
    return render(request, 'static/form.html')


