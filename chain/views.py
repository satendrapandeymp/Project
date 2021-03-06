from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.contrib.auth import authenticate,login, logout
from .forms import UserForm
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response

# For adding a user Profile
def AddUser(request):
    if request.method == "POST":
        form = ProfileForm(request.POST or None )
        if form.is_valid():
            temp_node = form.save(commit=False)
            temp_node.owner = request.user
            temp_node.save()
            mynodes = Node.objects.filter(owner=request.user)
            return render(request, 'chain/index.html' , { 'mynodes' : mynodes})
        else:
            form = ProfileForm(initial={'owner': request.user})
            return render(request, 'chain/profile_form.html', {'form': form})
    else:
        form = ProfileForm()
        return render(request, 'chain/profile_form.html', {'form': form})

# For updating the User
class UpdateUser(UpdateView):
        model= Profile
        fields = ['first_name','last_name','about', 'image']


# It's the homepage
def index(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/index.html' , { 'mynodes' : mynodes})

# It's for testing some new things
def test(request):
        return render(request, 'chain/base1.html' )

# it's for registering new user
class Register_User(View):
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

# For user login
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

# For logout user
def logout_user(request):
        logout(request)
        return render(request, 'chain/login.html')

# For updating node
class UpdateNode(UpdateView):
        model= Node
        fields = ['gateway_name','name','description','image']

# For Deleting Node
class DeleteNode(DeleteView):
        model= Node
        success_url = reverse_lazy('chain:index')

# For Updating Sensor
class UpdateSensor(UpdateView):
        model= Sensor
        fields = ['name' ,'description','image']

# For Deleting Sensor
class DeleteSensor(DeleteView):
        model= Sensor
        success_url = reverse_lazy('chain:index')

# To find all Sensors att One place
def sensors(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/sensors.html' , { 'mynodes' : mynodes})

# To Find all sensors attached to a Node
def sensor(request,pk):
        mynodes = Node.objects.filter(pk=pk)
        return render(request, 'chain/sensor.html' , { 'mynodes' : mynodes})

# To find data of a sensor
def data(request,pk):
        mysensors = Sensor.objects.filter(pk=pk)
        return render(request, 'chain/data.html' , { 'mysensors' : mysensors})

# To find all data From all sensors
def datas(request):
        mynodes = Node.objects.filter(owner=request.user)
        return render(request, 'chain/datas.html' , { 'mynodes' : mynodes})

# For adding data Manualy -- Remove later for automatically updating data
class AddData(CreateView):
        model= Data
        fields = ['sensor_name','data' ]

# For deleting data
class DeleteData(DeleteView):
        model= Data
        success_url = reverse_lazy('chain:index')

# Adding a New Node
def new_node(request):
    if request.method == "POST":
        form = NodeForm(request.POST or None )
        if form.is_valid():
            temp_node = form.save(commit=False)
            temp_node.owner = request.user
            temp_node.save()
            mynodes = Node.objects.filter(owner=request.user)
            return render(request, 'chain/index.html' , { 'mynodes' : mynodes})
        else:
            form = NodeForm(initial={'owner': request.user})
            return render(request, 'chain/node_form.html', {'form': form})
    else:
        form = NodeForm()
        return render(request, 'chain/node_form.html', {'form': form})

# For Adding A new sensor
def new_sensor(request):
    if request.method == "POST":
        form = SensorForm(request.user, request.POST or None )
        if form.is_valid():
            temp_sensor = form.save(commit=False)
            # For checking if someone is try to add sensor to someone elses node.
            if temp_sensor.node_name.owner == request.user:
                temp_sensor.save()
                mynodes = Node.objects.filter(owner=request.user)
                return render(request, 'chain/index.html' , { 'mynodes' : mynodes})
            else:
                form = SensorForm( request.user)
                return render(request, 'chain/sensor_form.html', {'form': form ,'error_message': 'Not your node'})
        else:
            form = SensorForm( request.user)
            return render(request, 'chain/sensor_form.html', {'form': form})
    else:
        form = SensorForm( request.user)
        return render(request, 'chain/sensor_form.html', {'form': form})
