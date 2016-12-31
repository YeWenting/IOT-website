from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from IOTapp.models import Device, DeviceLog
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required()
def get_index(request):
    list = []
    userid = request.session['userid']
    devices = Device.objects.filter(user=userid)

    for dev in devices:
        if dev.temperature > dev.threshold:
            is_warning = True
        else:
            is_warning = False

        if dev.is_open:
            status = "Active"
        else:
            status = "Inactive"

        print(dev.last_updated)
        temp_dev = {"id": dev.id, "SN": dev.SN, "name": dev.name, "temp": dev.temperature, "is_warning": is_warning,
                    "last_updated": dev.last_updated, "status": status}
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
    userid = request.session['userid']
    user = User.objects.get(id=userid)
    devices = Device.objects.filter(user=user)

    for dev in devices:
        if dev.temperature > dev.threshold:
            is_warning = True
        else:
            is_warning = False

        if dev.is_open:
            status = "Active"
        else:
            status = "Inactive"

        print(dev.last_updated)
        temp_dev = [dev.SN, dev.name, dev.temperature, dev.last_updated, is_warning, status, dev.threshold]
        list.append(temp_dev)

    res = {"data": list}
    return JsonResponse(res)

@login_required()
def add_device(request):

    # Get info
    SN = request.POST['SN']
    name = request.POST['name']
    last_updated = request.POST['last_updated']
    temperature = int(request.POST['temperature'])
    threshold = int(request.POST['threshold'])
    userid = request.session['userid']

    # Process the request
    if len(Device.objects.filter(user=userid, SN=SN)) > 0:
        resp = {"status": "existed"}
        print("repeat")
    else:
        try:
            user = User.objects.get(id=userid)
            Device.objects.create(SN=SN, name=name, last_updated=last_updated,
                                  temperature=temperature, threshold=threshold, user=user, is_open=True)
            resp = {"status": "success"}
            print("success")
        except:
            resp = {"status": "invalid"}
            print("fail")

    return JsonResponse(resp)


@login_required()
def delete_device(request):

    print(request.POST['device_SN'])
    device_SN = request.POST['device_SN']
    devices = Device.objects.filter(SN=device_SN)

    if len(devices) <= 0:
        resp = False
    else:
        resp = True
        devices.delete()

    return JsonResponse(resp, safe=False)


@login_required()
def update_device(request):

    # Get info
    SN = request.POST['SN']
    name = request.POST['name']
    last_updated = request.POST['last_updated']
    temperature = int(request.POST['temperature'])
    threshold = int(request.POST['threshold'])
    userid = request.session['userid']

    # Process the request
    try:
        user = User.objects.get(id=userid)
        Device.objects.filter(user=user, SN=SN).update(name=name, last_updated=last_updated,
                                                       temperature=temperature, threshold=threshold);
        resp = {"status": "success"}
        print("success")
    except:
        resp = {"status": "invalid"}
        print("fail")

    return JsonResponse(resp)


@login_required()
def get_log(request):
    userid = request.session['userid']
    logs = DeviceLog.objects.filter(user=userid)

    res = {"data": logs}
    return JsonResponse(res)