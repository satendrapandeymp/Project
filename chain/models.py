from django.db import models
from django.contrib.auth.models import Permission, User
from django.core.urlresolvers import reverse
from django.forms import ModelForm

# Create your models here.

class Gateway(models.Model):
    name = models.CharField(max_length = 40)
    def __str__(self):
        return self.name

class Node(models.Model):
    gateway_name = models.ForeignKey(Gateway,on_delete = models.CASCADE)
    name = models.CharField(max_length = 40)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    def get_absolute_url(self):
        return reverse(request , 'chain/test.html')
    def __str__(self):
        str1 = str(self.owner) + ' -- ' + self.name
        return str1

class Sensor(models.Model):
    node_name = models.ForeignKey(Node,on_delete = models.CASCADE)
    name = models.CharField(max_length = 40)
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
        return self.name

class Data(models.Model):
    sensor_name = models.ForeignKey(Sensor,on_delete = models.CASCADE)
    data = models.CharField(max_length = 40)
    def get_absolute_url(self):
        return reverse('chain:index')
    def __str__(self):
        return self.data

class NodeForm(ModelForm):
    class Meta:
        model = Node
        exclude = ('owner',)

class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        exclude = ()
