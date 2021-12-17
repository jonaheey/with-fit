from django.shortcuts import render

# Create your views here.
def signup(request):
    if request.method == 'POST':
        # 회원정보 저장
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')

        # user = User(email=email, password=PasswordHasher().hash(password), name=name, user_create=timezone.now())
        # user = User(email=email, password=password, name=name, user_create=timezone.now())
        # user.save()

        return HttpResponseRedirect('/signin/')

    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        # # 회원정보 저장
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # name = request.POST.get('name')

        # user = User(email=email, password=PasswordHasher().hash(password), name=name, user_create=timezone.now())
        # user = User(email=email, password=password, name=name, user_create=timezone.now())
        # user.save()

        return HttpResponseRedirect('/')

    return render(request, 'signin.html')

def signout(request):
    return render(request, 'signout.html')
