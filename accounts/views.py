from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


def start(request):
    return render(request, 'intro.html')
# Create your views here.


def about_us(request):
    print('you are ', request.session.get('username'))
    return render(request, 'about-us.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = auth.authenticate( username=username, password=password)

        if user is not None:
            auth.login(request, user)

            request.session['user_id'] = user.id
            request.session['username'] = user.username

            return redirect('/products')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/login')
    else:
        return render(request, 'login.html')


from django.core.mail import send_mail
from django.utils.html import strip_tags

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already Taken')
                return redirect('/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already Taken')
                return redirect('/register')
            else:
                # Create the user
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()

                # Send registration confirmation email
                subject = 'Welcome to A1 Tech Store!'
                message = f"Dear {username},\n\nThank you for registering with A1 Tech! We're delighted to have you as a valued member of our online store.\n\nAt A1 Tech, we strive to provide high-quality products and excellent customer service.\n\nFeel free to explore our wide range of products and enjoy a seamless shopping experience.\n\nIf you have any questions or need assistance, don't hesitate to contact our support team.\n\nBest regards,\nThe A1 Tech Team"
                from_email = 'A1 Tech <joannabedella@gmail.com>'
                to_email = email

                send_mail(subject, message, from_email, [to_email])

                # Redirect to login page
                print('user created')
                return redirect('/login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('/register')

    else:
        return render(request, 'register.html')



