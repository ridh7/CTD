from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from .serializers import QuestionSerializers, UserSerializers
from .models import UserProfileInfo, Submissions, Questions

# Create your views here.


class QuestionsList(generics.ListCreateAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializers


class QuestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializers


class UserList(generics.ListCreateAPIView):
    queryset = UserProfileInfo.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfileInfo.objects.all()
    serializer_class = UserSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = (BasicAuthentication, SessionAuthentication)


class SubmissionList(generics.ListCreateAPIView):
    queryset = Submissions.objects.all()
    serializer_class = QuestionSerializers


class SubmissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submissions.objects.all()
    serializer_class = QuestionSerializers
