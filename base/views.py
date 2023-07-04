from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import *

# login view
class CustomLoginView(LoginView):
     template_name = 'base/login.html'
     fields = '__all__'
     redirect_authenticated_user = True
     
     def get_success_url(self):
          return reverse_lazy('tasklist')
     
class RegisterPage(FormView):
     template_name = 'base/register.html'
     form_class = UserCreationForm
     redirect_authenticated_user = True
     success_url = reverse_lazy('tasklist')
     
     def form_valid(self,form):
          user= form.save()
          if user is not None:
               login(self.request,user)
          return super(RegisterPage,self).form_valid(form)
     
     # prevent login user to register page
     def get(self,*args,**kwargs):
          if self.request.user.is_authenticated:
               return redirect('tasklist')
          return super(RegisterPage,self).get(*args,**kwargs)       
          
     
     
          
          

# lists the task
class TaskList(LoginRequiredMixin,ListView):
     # getting model of name Task
     model = Task
     # creating the variable to store Task data as object
     context_object_name = 'tasks'
     
     # get the data according to userloggedin 
     def get_context_data(self,**kwargs):
          # inheriting the context data
          context = super().get_context_data(**kwargs)
          # getting original context data that is in user value
          context['tasks'] = context['tasks'].filter(user=self.request.user)
          # count the incomplete items and store in count vairable
          context['count'] = context['tasks'].filter(complete=False).count()
          
          # getting the search value
          search_input = self.request.GET.get('search-area') or ''
          if search_input:
               # search context with title
               # context['tasks'] = context['tasks'].filter(title__icontains = search_input)
               
               # search context with the letters and words
               context['tasks'] = context['tasks'].filter(title__startswith = search_input )
               
          # storing the data in variable name "search_input" to transfer value in template
          context['search_input'] = search_input
               
          return context

# return the detail of task
class TaskDetail(DetailView):
     model = Task
     context_object_name = 'task'
     # giving the template name to classview
     template_name = 'base/task.html'
     
# create the task through form
class TaskCreate(LoginRequiredMixin,CreateView):
     model = Task
     # getting the all fields of model Task
     # fields = '__all__'
     fields = ['title','description','complete']
     # redirecting to tasklist after adding task
     success_url = reverse_lazy('tasklist')
     
     # function to create task to logged user automatically
     def form_valid(self,form):
          # making sure that user is logged in 
          form.instance.user = self.request.user
          return super(TaskCreate,self).form_valid(form)
     
class TaskUpdate(LoginRequiredMixin,UpdateView):
     model = Task
     fields = ['title','description','complete']
     success_url = reverse_lazy('tasklist')
     
class TaskDelete(LoginRequiredMixin,DeleteView):
     model = Task
     context_object_name = 'task'
     success_url =  reverse_lazy('tasklist')
     template_name = 'base/task_conform_delete.html'
     

     
     
     
     
     
     
       
