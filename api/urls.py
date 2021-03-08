from django.urls import path
from .import views



urlpatterns = [
    path('todo/completed',views.TodoCompleteList.as_view()),
    path('todo/',views.TodoCreate.as_view()),
    path('todo/<int:pk>',views.TodoRetrieveUpdateDestroy.as_view()),
    path('todo/<int:pk>/complete',views.TodoUpdate.as_view()),
    path('signup/',views.signup),
    path('login/',views.login),

]