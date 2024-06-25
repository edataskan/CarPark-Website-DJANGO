from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from carpark import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_protect
from . tokens import account_activation_tokens
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.html import strip_tags
from django.urls import reverse_lazy
from django.conf import settings

# Create your views here.
def home(request) :
    return render(request, "authentication/index.html")

@csrf_protect
def signup(request) :

    if request.method == "POST" :
        #username = request.POST.get['username']
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username) :
            messages.error(request, "Username already exist! Please try some other username" )
            return redirect('home')

        if User.objects.filter(email = email) :
            messages.error(request, "Email already registered! ")
            return redirect('home')
        
        if len(username) > 30 :
            messages.error(request, "Username must be under 10 characters")

        else :
            if pass1!= pass2 :
                messages.error(request, "Password didn't match!")

            if not username.isalnum() :
                messages.error(request, "Username must be Alpha-Numeric")
                return redirect('home')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account has been succesfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
        
        #send_activation_email(myuser)
        
        #Welcome Email

        subject = "Welcome to Car-Park Login "
        message = "Hello" + myuser.first_name + "\n"+"Welcome to Car-Park \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thankin You \n Car-Park "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently = True)


        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @Car-Park Login "
        message2 = render_to_string('email_confirmation.html',{
            'name' : myuser.first_name,
            'domain' :current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token' : account_activation_tokens.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        

        return redirect('signin')



    return render(request, "authentication/signup.html")

def signin(request) :

    if request.method == 'POST' :
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)

        if user is not None :
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname' : fname})

        else :
            messages.error(request, "Bad credentials ! ")
            return render(request, 'authentication/index.html')
        
    return render(request, "authentication/signin.html")

def signout(request) :
    logout(request)
    messages.success(request, "Logged Out Succesfully!")
    return redirect('home')


def activate(request, uidb64, token) :
    User = get_user_model()
    try :
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid) 
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) :
        myuser = None

    if myuser is not None and account_activation_tokens.check_token(myuser,token) :
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return render(request, 'authentication/index.html', {'fname': myuser.first_name})
        
    else :
        return render(request, "activation_failed.html")
    
"""def send_activation_email(user, activation_link):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    email.send()"""
    
class CustomLoginView(LoginView):
    template_name = 'templates/authentication/signin.html'

    def get_success_url(self):
        # Bu, kullanıcı giriş yaptıktan sonra yönlendirilecek URL'yi belirler
        # Burada, kullanıcının e-posta adresini alarak bir bağlantı oluşturuyoruz.
        # Bu bağlantı, kullanıcı e-posta üzerinden tıkladığında çalışacak olan bir URL olmalıdır.
        email = self.request.POST['username']  # Bu, kullanıcının e-posta adresini alır, bu örnekte kullanıcı adı olarak kullanıyoruz
        activation_link = reverse_lazy('activate', kwargs={'email': email})
        
        # Aktivasyon linkini e-posta ile gönder
        user = get_user_model().objects.get(email=email)
        #send_activation_email(user, activation_link)

        return activation_link

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/change_password.html', {'form': form})

@login_required
def send_login_notification(request):
    # E-posta gönderimi
    subject = 'Giriş Bildirimi'
    message = render_to_string('authentication/login_notification_email.html', {'user': request.user})
    plain_message = strip_tags(message)
    from_email = 'carpark-@outlook.com'  # Gönderen e-posta adresi
    to = [request.user.email]  # Kullanıcının e-posta adresi

    send_mail(subject, plain_message, from_email, to, html_message=message)

    return redirect('index')  # Kullanıcıyı yönlendirmek istediğiniz sayfanın adını girin

def send_login_notification(request):
    # E-posta gönderimi
    subject = 'Giriş Bildirimi'
    message = render(request, 'authentication/login_notification_email.html', {'user': request.user})
    plain_message = strip_tags(message)
    from_email = 'carpark-@outlook.com'  # Gönderen e-posta adresi
    to = [request.user.email]  # Kullanıcının e-posta adresi

    send_mail(subject, plain_message, from_email, to, html_message=message)

    return redirect('home')  # Kullanıcıyı yönlendirmek istediğiniz sayfanın adını girin