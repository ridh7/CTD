from django.urls import path
from . import views


urlpatterns =[
    path('api/submissionsList/', views.SubmissionList.as_view()),
    path('api/questionsList/', views.QuestionsList.as_view()),
    path('api/userList/', views.UserList.as_view()),
    path('api/question/<int:pk>/', views.QuestionsDetail.as_view()),
    path('api/submission/<int:pk>/', views.SubmissionDetail.as_view()),
    path('api/user/<int:pk>/', views.UserDetail.as_view()),
]