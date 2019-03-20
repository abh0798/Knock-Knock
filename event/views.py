from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Questions, Event, CustomUser, Special
from .forms import CustomUserSignupForm, EventAnswerForm, SpecialAnswerForm
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import datetime
import pytz
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .tokens import account_activation_token


utc = pytz.UTC


# Create your views here.
def main(request):
    return render(request, 'Knock_Knock.html', {})

@login_required
@csrf_protect
def event(request, ID):
    user = CustomUser.objects.get(username=request.user.username)
    answered = user.answered
    ls = ["query1", "query2","query3","query4","query5","query6","query7","query8","query9","query10","query11"]
    answers=[]
    for i in range(1,12):
        globals()[ls[i-1]] = int(answered[i-1])
        answers.append(answered[i-1])
    event_details = Event.objects.all()
    queries = Questions.objects.get(number=ID)
    starting = event_details[0].start
    ending = event_details[0].end
    now = utc.localize(datetime.datetime.now())
    if starting < now and ending > now:
        if answers[ID-1] == '0':
            if request.method == 'POST':
                form = EventAnswerForm(request.POST)
                if form.is_valid():
                    add = EventAnswerForm.validate(form,ID)
                    #Validating the form, if answer
                    if add == 1:
                        answers[ID-1] = 1
                        user.answered=""
                        for i in range(1,12):
                            user.answered = user.answered+str(answers[i-1])
                        user.score += 10
                        user.time_submission = utc.localize(datetime.datetime.now())
                        user.save()
                        user.publish()
                        if ID<10:
                            return redirect('../' + str(ID + 1))
                        else:
                            return redirect('../../special/')
                    else:
                        answers[ID-1] = 1
                        user.answered = ""
                        for i in range(1, 12):
                            user.answered = user.answered + str(answers[i-1])
                        user.save()
                        user.publish()
                        if ID<10:
                            return redirect('../' + str(ID + 1))
                        else:
                            return redirect('../../special/')
            else:
                form = EventAnswerForm()
            return render(request, 'questions.html', {'queries': queries, 'form': form, 'ID': ID, 'query1': query1, 'query2': query2, 'query3': query3, 'query4': query4, 'query5': query5, 'query6': query6, 'query7': query7, 'query8': query8, 'query9': query9, 'query10': query10, 'query11': query11})
        else:
            if ID <10:
                return redirect('../' + str(ID + 1))
            else:
                return redirect('../../special/')
    else:
        return render(request, 'notstarted.html', {})


def winners(request):
    toppers = CustomUser.objects.all().order_by('-score', 'time_submission')[:11]
    return render(request, 'winners.html', {'participants' : toppers})


def leader(request):
    event_details = Event.objects.all()
    now = utc.localize(datetime.datetime.now())
    ending = event_details[0].end
    if request.user.is_superuser:
        everyone = CustomUser.objects.all().order_by('-score', 'time_submission')
        return render(request, 'leaderboard.html', {'everyone': everyone})
    if now>ending:
        everyone = CustomUser.objects.all().order_by('-score', 'time_submission')
        return render(request, 'leaderboard.html', {'everyone' : everyone})
    else:
        return HttpResponse("Contest ranks will only be displayed after the contest")

@login_required
def rules(request):
    event = Event.objects.all()
    start = event[0].start
    now = utc.localize(datetime.datetime.now())
    link = ""
    if start < now:
        link = "../event/1/"
    else:
        link = "#"
    return render(request, 'rules.html', {'start': start, 'now': now, 'link': link})


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your MNTC account.'
            message = render_to_string('mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(
                mail_subject, message,'mntcnitd@gmail.com' ,[to_email], fail_silently=False
            )
            return HttpResponse('Please confirm your email address to complete the registration.Check your spam folder if you have not received the mail')
    else:
        form = CustomUserSignupForm()
    return render(request, 'signup.html', {'form' : form,})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')



def special(request):
    user = CustomUser.objects.get(username=request.user.username)
    answered = user.answered
    ls = ["query1", "query2", "query3", "query4", "query5", "query6", "query7", "query8", "query9", "query10",
          "query11"]
    answers = []
    for i in range(1, 12):
        globals()[ls[i - 1]] = int(answered[i - 1])
        answers.append(answered[i - 1])
    event_details = Event.objects.all()
    queries = Special.objects.all()
    queries = queries[0]
    starting = event_details[0].start
    ending = event_details[0].end
    now = utc.localize(datetime.datetime.now())
    if starting < now and ending > now:
        if answers[10] == '0':
            if request.method == 'POST':
                form = SpecialAnswerForm(request.POST)
                if form.is_valid():
                    add = SpecialAnswerForm.validate(form)
                    #Validating the form for correct answer
                    if add ==1:
                        answers[10] = 1
                        user.answered=""
                        for i in range(1,12):
                            user.answered = user.answered+str(answers[i-1])
                        user.score +=50
                        user.time_submission = utc.localize(datetime.datetime.now())
                        user.save()
                        user.publish()
                        return redirect('/')
                    else:
                        answers[10] = 1
                        user.answered = ""
                        for i in range(1, 12):
                            user.answered = user.answered + str(answers[i - 1])
                        user.save()
                        user.publish()
                        return redirect('/')
            else:
                form = SpecialAnswerForm()
            return render(request, 'special.html', {'queries': queries, 'form': form, 'query1': query1, 'query2': query2, 'query3': query3, 'query4': query4, 'query5': query5, 'query6': query6, 'query7': query7, 'query8': query8, 'query9': query9, 'query10': query10, 'query11': query11})
        else:
            return redirect('/')
    else:
        return render(request, 'notstarted.html', {})


def reset_done(request):
    return redirect('../../login/')
