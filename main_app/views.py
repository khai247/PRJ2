from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.user_type == '1':
                return redirect('main_app:admin_home')
            elif user.user_type == '2':  
                return redirect('main_app:staff_home')
            else:
                return redirect('main_app:student_home')
        else:
            error_message = 'Invalid username or password. Please try again.'
            return render(request, 'main/login.html', {'error_message': error_message})
        
    return render(request, 'main/login.html')
        
def logout_user(request):
    if request.user != None:
        logout(request)
    
    return redirect("/")

