from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from .serializers import QuestionSerializers, UserSerializers
from .models import UserProfileInfo, Submissions, Questions
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

import datetime
import os


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


endtime = 0
_flag = False

starttime = ""

path = 'data/users_code'
path2 = 'data/standard'
path3 = 'data/standard/testcaseScore'


def start_Timer(request):
    if request.method == 'GET':
        return render(request, 'basic_app/timer.html')  # timer url known only to us
    else:
        adminpassword = '1'
        _password = request.POST.get('pass1')   # get admin password
        if _password == adminpassword:
            global _flag
            _flag = True    # flag True when you start the timer(used so he cannot go to register before waitin page# )
            now1 = datetime.datetime.now()  # cuurent time       ( by putting the url )
            min1 = now1.minute + 1  # 1 signifies time after hitting timer url
            hour1 = now1.hour
            time1 = str(hour1) + ':' + str(min1)    # makes the string of current time + 1 min

            time = now1.second+now1.minute*60+now1.hour*60*60
            global endtime
            global starttime
            starttime = time1
            endtime = time + 7200   # 7200 defines our event time

            return HttpResponse("Timer set go")
        else:
            return HttpResponse("Invalid login details supplied.")


def waiting(request):   # this view gets called every 5 seconds
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('question_panel'))
    else:
        now = datetime.datetime.now()
        min = now.minute
        hour = now.hour
        sec = min * 60 + hour * 60 * 60
        time = str(hour)+":" + str(min)

        global starttime    # has current time + 1 min time in string format

        if not starttime == "": # condition to handle if user types url of waiting page from register page
            _time_string = starttime.split(":")
            _min = int(_time_string[1]) # extract the hour and min for later use
            _hour = int(_time_string[0])
            _sec = _hour * 60 * 60 + _min * 60  # the hour and min in seconds
            if sec > _sec:  # if current time of hr:min in seconds greater than starttime ka seconds(hr:min conversion)
                            # so he should not go back to waiting page once he goes to register page
                return HttpResponseRedirect(reverse('register'))

        if time == starttime:   # since waiting page refreshes every 5 seconds when the current time equates to
                                # time defined when timer was hit i.e +1 the curr time then :
            return HttpResponseRedirect(reverse('register'))
        else:
            return render(request, 'basic_app/waiting.html')


def timer():
    now = datetime.datetime.now()
    time = now.second + now.minute * 60 + now.hour * 60 * 60
    global endtime  # defined once when timer was hit
    return endtime-time


def questions(request, id=1):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = UserProfileInfo.objects.get(user=request.user)
            user.question_id = int(id)

            username = request.user.username

            if not os.path.exists('{}/{}/'.format(path, username)): # make folders of user
                user.attempts = 0  # this line should be exceuted only once
                os.system('mkdir {}/{}'.format(path, username))

                for i in range(1, 7):
                    os.system('mkdir {}/{}/question{}'.format(path, username, i))

            user.save()

            return JsonResponse({})

        else:

            some_text = request.POST.get('editor')  # code to store in submission instance
            subb = Submissions(user=request.user, que=Questions.objects.get(pk=id))
            subb.sub = some_text
            time = timer()
            hour = time // (60 * 60)
            a = time % (60 * 60)
            if a < 60:
                sec = a
                min = 0
            else:
                min = a // 60
                sec = a % 60

            subb.subtime = '{}:{}:{}'.format(hour, min, sec)    # stores time of submission

            option = request.POST.get('lang')   # get c or cpp
            username = request.user.username
            user = UserProfileInfo.objects.get(user=request.user)
            user.option = option
            subb.qid = user.question_id     # submission quesion id
            subb.save()

            testlist = ['fail', 'fail', 'fail', 'fail', 'fail']

            user.attempts += 1

            fo = open('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option), 'w')
            fo.write(some_text)     # writes .c file
            fo.close()

            dictt = {}

            if os.path.exists('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option)):
                ans = os.popen("python data/main.py " + "{}/{}/question{}/{}{}.{}".format(path, username, user.question_id, username, user.attempts, option) + " " + username + " " + str(user.question_id) + " " + str(user.attempts)).read()
                # sandbox returns the 2 digit code of five testcases as a single integer of 10 digit number
                ans = int(ans)  # saves 99'99'89'99'50 as 9999899950 these ae sandbox returned codes of 5 testcases
                print("THE SANDBOX CODE IS", ans)
                data = [1, 2, 3, 4, 5]  # codes of each testcase for the question
                tcOut = [0, 1, 2, 3, 4] # switch case number for sandbox coode
                switch = {

                    10: 0,  # correct answer code
                    99: 1,  # wrong answer code
                    50: 2,  # System commands
                    89: 3,  # compile time error
                    70: 4,  # Abnormal termination
                    20: 5,  # custom error
                    60: 6,  # Run time error
                    40: 7   # Motherfucking code
                }

                user.score = 0
                for i in range(0, 5):
                    data[i] = ans % 100	# stores output for each case but in reverse order
                    ans = int(ans / 100)

                    tcOut[i] = switch.get(data[i], 2)
                    if tcOut[i] == 0:  # if data[i] is 10 i.e correct answer
                        testlist[4 - i] = 'pass'    # since data stored in reverse order

                testlistcopy = ['pass', 'pass', 'pass', 'pass', 'pass']

                if testlist == testlistcopy:
                    user.score = 100
                else:
                    user.score = 0

                cerror = ""

                tle_flag = False
                abt_flag = False
                rte_flag = False
                cte_flag = False

                status = ""

                if tcOut[4] == 3:   # if compiler error then store read it for error.txt which was made in main.py
                    cte_flag = True # and store it in strinf cerror to display on console
                    error = path + "/" + username + "/" + str("error{}.txt".format(user.question_id))
                    status = "CTE"
                    with open(error, 'r') as e:
                        cerror = e.read()
                        cerror1 = cerror.split('/')

                        cerror2 = cerror1[0]+'/'+cerror1[1]+'/'+cerror1[2]+'/'
                        cerror = cerror.replace(cerror2, '')    # scrape the file path of users

                if tcOut[0] == 2 or tcOut[1] == 2 or tcOut[2] == 2 or tcOut[3] == 2 or tcOut[4] == 2:
                    tle_flag = True
                    status = "TLE"

                if tcOut[0] == 4 or tcOut[1] == 4 or tcOut[2] == 4 or tcOut[3] == 4 or tcOut[4] == 4:
                    abt_flag = True
                    status = "W.A"

                if tcOut[0] == 5 or tcOut[1] == 5 or tcOut[2] == 5 or tcOut[3] == 5 or tcOut[4] == 5:
                    abt_flag = True
                    status = "RTE"

                if tcOut[0] == 6 or tcOut[1] == 6 or tcOut[2] == 6 or tcOut[3] == 6 or tcOut[4] == 6:
                    rte_flag = True
                    status = "RTE"   # strings to display on console

                if tcOut[0] == 7 or tcOut[1] == 7 or tcOut[2] == 7 or tcOut[3] == 7 or tcOut[4] == 7:
                    rte_flag = True
                    status = "RTE"   # strings to display on console

                user.QuestionDetails.objects.get(id=id).flag = True # flags to check if sumbitted(required for accuracy)
                if user.QuestionDetails.objects.get(id=id).score <= user.score:   # store the mac sccore
                    user.QuestionDetails.objects.get(id=id).score = user.score   # question1 marks

                for i in range(6):
                    user.totalScore += user.QuestionDetails.objects.get(id=i).score

                user.total = user.totalScore // 6
                user.save()

                Q = Questions.objects.get(id=id)    # current question object

                for_count = 0

                for i in testlist:
                    if i == 'pass':
                        for_count += 1

                if for_count == 5:
                    status = 'A.C'
                    Q.submission += 1      # if score 100 then increase successful subs for that question by 1
                    Q.save()

                else:
                    if not (tle_flag or rte_flag or abt_flag or cte_flag):
                        status = 'W.A'
                    for_count = 0

                subb.testCaseScore = (for_count / 5) * 100  # testcase % completion
                subb.save()

                dictt = {'e':cerror,'d':user.question_id,'t':timer(),'t1':testlist[0],'t2':testlist[1],'t3':testlist[2],'t4':testlist[3],'t5':testlist[4],'status':status}

            return JsonResponse(dictt)
    else:
        return HttpResponseRedirect(reverse('register'))


def question_panel(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            return register(request)

        user.flag = True    # once reaches question_panel do not enable user to go back
        user.save()

        all_user = UserProfileInfo.objects.all()

        accuracy_count = [0, 0, 0, 0, 0, 0] # number of users who have 100 score for each 6 questions
        user_sub_count = [0, 0, 0, 0, 0, 0] # number of users who have atleast one submissions
        percentage_accuracy = [0, 0, 0, 0, 0, 0] # stores accuracy of each question

        for user in all_user:
            user_ques = user.QuestionDetails.all()
            if user_ques[0].flag: # if even 1 submission then denominator +1
                user_sub_count[0] += 1
            if user_ques[1].flag:
                user_sub_count[1] += 1
            if user_ques[2].flag:
                user_sub_count[2] += 1
            if user_ques[3].flag:
                user_sub_count[3] += 1
            if user_ques[4].flag:
                user_sub_count[4] += 1
            if user_ques[5].flag:
                user_sub_count[5] += 1

        for user in all_user:
            user_ques = user.QuestionDetails.all()
            if user_ques[0].score == 100:  # if ques score 100 then numerator +1
                accuracy_count[0] += 1
            if user_ques[1].score == 100:
                accuracy_count[1] += 1
            if user_ques[2].score == 100:
                accuracy_count[2] += 1
            if user_ques[3].score == 100:
                accuracy_count[3] += 1
            if user_ques[4].score == 100:
                accuracy_count[4] += 1
            if user_ques[5].score == 100:
                accuracy_count[5] += 1

        for i in range(0, 6):
            try:
                percentage_accuracy[i] = int((accuracy_count[i] / user_sub_count[i]) * 100)
            except ZeroDivisionError:
                percentage_accuracy[i] = 0  # since for the first get request no submissions so 0/0 error

        all_question = Questions.objects.all()

        a1 = 0

        for i in all_question:
            i.accuracy = percentage_accuracy[a1]
            a1 += 1
            i.save()    # save the accuracy

        subs = []
        qtitle = []

        for i in range(0, 6):
            subs.append(all_question[i].submission)
            qtitle.append(all_question[i].questionTitle)

        dict = {'t': timer(), 'a0': percentage_accuracy[0], 'a1': percentage_accuracy[1], 'a2': percentage_accuracy[2],
                'a3': percentage_accuracy[3], 'a4': percentage_accuracy[4], 'a5': percentage_accuracy[5],
                'subs0': subs[0], 'subs1': subs[1], 'subs2': subs[2], 'subs3': subs[3], 'subs4': subs[4],
                'subs5': subs[5], 'qtitle0': qtitle[0], 'qtitle1': qtitle[1], 'qtitle2': qtitle[2],
                'qtitle3': qtitle[3], 'qtitle4': qtitle[4], 'qtitle5': qtitle[5]}

        return JsonResponse(dict)
    else:
        return HttpResponseRedirect(reverse('register'))


def leader(request):
    if request.user.is_authenticated:
        a=UserProfileInfo.objects.order_by("total")
        b=a.reverse()
        dict={'list': b, 't': timer()}
        return render(request, 'basic_app/Leaderboard.html', context=dict)

    else:
        return HttpResponseRedirect(reverse('register'))


def instructions(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            user = UserProfileInfo()
        if user.flag:   # if user has before visited question panel and tries to come back
            return HttpResponseRedirect(reverse('question_panel'))
        if request.method == "POST":
            return HttpResponseRedirect(reverse('question_panel'))
        return render(request, 'basic_app/instruction.html')
    else:
        return HttpResponseRedirect(reverse('register'))


def user_logout(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            return register(request)
        a = UserProfileInfo.objects.order_by("total")
        b = a.reverse()
        counter = 0
        for i in b:
            counter += 1
            if str(i.user) == str(request.user.username):
                break

        dict = {'count': counter, 'name': request.user.username, 'score': user.totalScore}

        logout(request)
        return render(request, 'basic_app/Result.htm', context=dict)
    else:
        return HttpResponseRedirect(reverse('register'))


def register(request):
    if request.user.is_authenticated:
        try:
            user = UserProfileInfo.objects.get(user=request.user)
        except UserProfileInfo.DoesNotExist:
            user = UserProfileInfo()
        if not user.flag:   # if not visited questions yet then:
            return HttpResponseRedirect(reverse('instructions'))
        return HttpResponseRedirect(reverse('question_panel'))
    else:
        try:
            global _flag
            if not _flag:   # if hits url for register in waiting page
                return HttpResponseRedirect(reverse('waiting'))
            if request.method == 'POST':
                username = request.POST.get('name')

                if username == "":  # back end verification
                    return render(request, 'basic_app/Loginn.html')
                password = request.POST.get('password')
                name1 = request.POST.get('name1')

                if name1 == "":
                    return render(request, 'basic_app/Loginn.html')
                name2 = request.POST.get('name2')
                phone1 = request.POST.get('phone1')

                if len(phone1) is not 10:
                    return render(request, 'basic_app/Loginn.html')
                phone2 = request.POST.get('phone2')
                email1 = request.POST.get('email1')

                if email1 == "":
                    return render(request, 'basic_app/Loginn.html')
                email2 = request.POST.get('email2')
                level = request.POST.get('level')

                b = UserProfileInfo()
                b.user = User.objects.create_user( username=username, password=password)
                b.name1 = name1
                b.name2 = name2
                b.phone1 = phone1
                b.phone2 = phone2
                b.email1 = email1
                b.email2 = email2
                b.level = level
                login(request, b.user)
                b.save()

                for i in range(1,7):
                    b.QuestionDetails.add(Questions.objects.get(id=i))

                b.save()

                return HttpResponseRedirect(reverse('instructions'))

        except IntegrityError:
            return HttpResponse("you have already been registered.")
        return render(request,'basic_app/Loginn.html')


def sub(request):
    user = UserProfileInfo.objects.get(user=request.user)
    a = Submissions.objects.filter(user=request.user, qid=user.question_id) # create sub for that question for that user
    b = a.reverse()                                                         # check models for clear picture

    dict={'loop': b, 't': timer()}
    return render(request, 'basic_app/Submissionn.html', context=dict)


def retry(request, id=1):
    if request.method == "GET":
        user = UserProfileInfo.objects.get(user=request.user)
        a = Submissions.objects.filter(user=request.user, qid=user.question_id) # create sub for that question for that user
        array = []  # all codes subs for that questions
        idd = []    # for qids

        for i in a:
            array.append(i.sub) # i.sub is code written by user
            idd.append(i.qid)
        var = Questions.objects.all()

        f = idd[int(id)-1]
        q = var[int(f)-1]   # extract question from the url id
        question = q.questions  # text of the question
        dict = {'sub': array[int(id)-1], 'question': question, 's': user.score, 't': timer()}

        return render(request, 'basic_app/Codingg.html', context=dict)
    if request.method == "POST":
        return questions(request)


def checkuser(request): # ajax validation of username
    response_data = {}
    uname = request.POST.get("name")
    check1 = User.objects.filter(username=uname)
    if not check1:
        response_data["is_success"] = True
    else:
        response_data["is_success"] = False
    return JsonResponse(response_data)


def loadbuff(request):
    response_data = {}
    username = request.user.username
    user = UserProfileInfo.objects.get(user=request.user)

    file = '{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts,
                                                           user.option)
    f = open(file, "r")
    text = f.read()

    if not text:
        data = ""
    response_data["text"] = text
    return JsonResponse(response_data)


def elogin(request):    # emergency login
    if request.method == 'POST':
        adminpassword = '1'
        username = request.POST.get('user')
        password = request.POST.get('pass')
        _password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)

        if user is not None and _password is adminpassword:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('question_panel'))

        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'basic_app/elogin.html', {})


# COMMENTS COURTESY OF SAUMITRA KULKARNI :P
