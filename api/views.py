from json.decoder import JSONDecoder
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer,TodoCompleteSerializer
from todo.models import Todo
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
# Create your views here.

@csrf_exempt
def signup(request):
    if request.method=="POST":
        try:
            data=JSONParser().parse(request)
            user=User.objects.create_user(data['username'],password=data['password'])
            user.save()
            token=Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)





@csrf_exempt
def login(request):
    if request.method == 'POST':
        data=JSONParser().parse(request.data)
        user = User.objects.authenticate(username = data['username'], password= data['password'])
        if user is None:
            return JsonResponse({'error':'Could not login! please check your username and password'})
        else:
            try:
                token = Token.objects.get(user = user)
            except:
                token = Token.objects.create(user = user)
            return JsonResponse({'token': str(token)}, status = 201)
# def loginuser(request):
#     if request.method == "POST":
#         data = JSONParser().parse(request)
#         user = authenticate(request, username=data['username'], password=data['password'])
#         if user is None:
#             return JsonResponse({'error':'Could not login. Please check username and password'}, status=400)
#         else:
#             try:
#                 token = Token.objects.get(user=user)
#             except:
#                 token = Token.objects.create(user=user)
#             return JsonResponse({'token':str(token)}, status=201)


class TodoCompleteList(generics.ListAPIView):
    serializer_class= TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user,datecompleted__isnull=False).order_by("-datecompleted")

class TodoCreate(generics.ListCreateAPIView):
    serializer_class= TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user,datecompleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= TodoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)

        
class TodoUpdate(generics.UpdateAPIView):
    serializer_class= TodoCompleteSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted=timezone.now()
        serializer.save()