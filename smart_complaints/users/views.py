from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User
from django.http import HttpResponseForbidden,HttpResponse

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = form.cleaned_data['password']  
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                request.session['user_id'] = user.id
                request.session['user_role'] = user.role

                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'staff':
                    return redirect('staff_dashboard')
                else:
                    return redirect('user_dashboard')

            except User.DoesNotExist:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    return redirect('login')


def role_required(required_role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            role = request.session.get('user_role')
            if role != required_role:
                return HttpResponseForbidden("Access Denied: Insufficient Permissions")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


@role_required('user')  
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


@role_required('staff')
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')


@role_required('admin')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')



def home_redirect(request):
    role = request.session.get('user_role')
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'staff':
        return redirect('staff_dashboard')
    elif role == 'user':
        return redirect('user_dashboard')
    return redirect('login')




# def delete(request,id):
#     id = User.objects.get(id=id)
#     id.delete()
#     return HttpResponse("User Deleted",id)