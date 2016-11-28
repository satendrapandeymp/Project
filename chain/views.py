from django.shortcuts import render,get_object_or_404,redirect
from .models import Gateway, Node, Sensor, Data
from django.contrib.auth import authenticate,login, logout
from .forms import UserForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/index.html' , { 'mynodes' : mynodes})

class UserFormView(View):
    form_class = UserForm
    template_name = 'chain/reg.html'

    def get(self,request):
        form = self.form_class(None)
        return render (request,self.template_name , {'form' :form })

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # normalised data_set
            username = form.cleaned_data ['username']
            password = form.cleaned_data ['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)
            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect ('chain:index')
        return render(request, self.template_name , {'form': form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                mynodes = Node.objects.filter(owner=request.user)
                return render(request, 'chain/index.html', {'mynodes' : mynodes})
            else:
                return render(request, 'chain/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'chain/login.html', {'error_message': 'Invalid login'})
    return render(request, 'chain/login.html')

def logout_user(request):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        logout(request)
        return render(request, 'chain/login.html')

class AddNode(CreateView):
        model= Node
        fields = ['gateway_name','name','owner']

class UpdateNode(UpdateView):
        model= Node
        fields = ['gateway_name','name','owner']

class DeleteNode(DeleteView):
        model= Node
        success_url = reverse_lazy('chain:index')


class AddSensor(CreateView):
        model= Sensor
        fields = ['node_name','name']

class UpdateSensor(UpdateView):
        model= Sensor
        fields = ['node_name','name']

class DeleteSensor(DeleteView):
        model= Sensor
        success_url = reverse_lazy('chain:index')

def sensors(request):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/sensors.html' , { 'mynodes' : mynodes})

def sensor(request,pk):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        mynodes = Node.objects.filter(pk=pk)
        return render(request, 'chain/sensor.html' , { 'mynodes' : mynodes})

def data(request,pk):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        mysensors = Sensor.objects.filter(pk=pk)
        return render(request, 'chain/data.html' , { 'mysensors' : mysensors})

def datas(request):
    if not request.user.is_authenticated():
        return render(request, 'chain/login.html')
    else:
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/datas.html' , { 'mynodes' : mynodes})



class AddData(CreateView):
        model= Data
        fields = ['sensor_name','data']

class DeleteData(DeleteView):
        model= Data
        success_url = reverse_lazy('chain:index')
