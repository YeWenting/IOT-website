from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from IOTapp.models import Device, DeviceLog
from django.contrib.auth.decorators import login_required
import django.utils.timezone as timezone


# Create your views here.

@login_required()
def get_index(request):
    return render(request, 'index.html')


def switch_index(request):
    return HttpResponseRedirect("/devices/")


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


@login_required()
def get_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required()
def get_history(request):
    return render(request, 'log.html')

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

        temp_dev = [dev.SN, dev.name, dev.temperature, dev.last_updated.strftime('%b %d, %Y  %H:%M'), is_warning, status, dev.threshold, dev.id]
        list.append(temp_dev)

    res = {"data": list}
    return JsonResponse(res)

@login_required()
def add_device(request):

    # Get info
    SN = request.POST['SN']
    name = request.POST['name']
    threshold = int(request.POST['threshold'])
    userid = request.session['userid']

    # Process the request
    if len(Device.objects.filter(user=userid, SN=SN)) > 0:
        resp = {"status": "existed"}
        print("repeat")
    else:
        try:
            user = User.objects.get(id=userid)
            Device.objects.create(SN=SN, name=name, threshold=threshold, user=user, is_open=True)
            DeviceLog.objects.create(SN=SN)
            resp = {"status": "success"}
            print("success")
        except:
            resp = {"status": "invalid"}
            print("fail")

    return JsonResponse(resp)


@login_required()
def delete_device(request):

    print(request.POST['device_id'])
    device_id = request.POST['device_id']
    devices = Device.objects.filter(id=device_id)

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
    threshold = int(request.POST['threshold'])
    userid = request.session['userid']

    # Process the request
    try:
        user = User.objects.get(id=userid)
        Device.objects.filter(user=user, SN=SN).update(name=name, threshold=threshold)
        resp = {"status": "success"}
        print("success")
    except:
        resp = {"status": "invalid"}
        print("fail")

    return JsonResponse(resp)


@login_required()
def get_log(request):

    logs = []
    list = []
    # Get the log HTML
    if 'SN' not in request.GET:
        logs = DeviceLog.objects.all()
    else:
        SN = request.GET['SN']
        logs = DeviceLog.objects.filter(SN=SN)

    for log in logs:
        userid = request.session['userid']
        devices = Device.objects.filter(SN=log.SN, user=userid)
        if len(devices) == 0:
            continue
        name = devices[0].name
        if log.is_open:
            status = "Active"
        else:
            status = "Inactive"
        temp_log = [log.SN, name, log.time.strftime('%b %d, %Y  %H:%M:%S'), log.temperature, status]
        list.append(temp_log)

    res = {"data": list}
    return JsonResponse(res)


def add_log(request):
    SN = 0
    resp = {}
    try:
        SN = request.POST['SN']
        working = Device.objects.filter(SN=SN)[0].is_open
        if working:
            temp = request.POST['temperature']
            Device.objects.filter(SN=SN).update(temperature=temp, last_updated=timezone.now())
            DeviceLog.objects.create(SN=SN, temperature=temp)
            resp['add'] = True


        # Give back the info
        resp['is_open'] = working
    except:
        resp['add'] = False
        resp['is_open'] = Device.objects.filter(SN=SN)[0].is_open
        print("add log fail")

    return JsonResponse(resp)

