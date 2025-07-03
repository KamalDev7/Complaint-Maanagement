from django.shortcuts import render, redirect
from .forms import ComplaintForm
from .models import Complaint
from users.models import User
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages




def submit_complaint(request):
    if request.session.get('user_role') != 'user':
        return redirect('login')

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.submitted_by = User.objects.get(id=request.session['user_id'])
            complaint.save()
            return redirect('my_complaints')
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})



def my_complaints(request):
    if request.session.get('user_role') != 'user':
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    complaints = Complaint.objects.filter(submitted_by=user)
    return render(request, 'my_complaints.html', {'complaints': complaints})


def admin_complaint_list(request):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    status_filter = request.GET.get('status')
    complaints = Complaint.objects.all().order_by('-created_at')

    if status_filter:
        complaints = complaints.filter(status=status_filter)

    staff_users = User.objects.filter(role='staff')
    return render(request, 'admin_complaints.html', {
        'complaints': complaints,
        'staff_users': staff_users,
        'status_filter': status_filter,
    })


@require_POST
def assign_complaint(request, complaint_id):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    staff_id = request.POST.get('staff_id')
    complaint = Complaint.objects.get(id=complaint_id)
    staff_user = User.objects.get(id=staff_id)

    complaint.assigned_to = staff_user
    complaint.status = 'in_progress'
    complaint.save()
    return redirect('admin_complaints')


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_complaint(request, complaint_id):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        staff_id = request.POST.get('assigned_to')
        status = request.POST.get('status')

        if staff_id:
            staff_user = User.objects.get(id=staff_id)
            complaint.assigned_to = staff_user

        if status:
            complaint.status = status

        complaint.save()
        return redirect('admin_complaints')

    return redirect('admin_complaints')


from django.shortcuts import render
from .models import Complaint

def user_history_view(request):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    
    users = Complaint.objects.values('submitted_by__name').distinct()

    return render(request, 'user_history.html', {'users': users})


from django.shortcuts import render, redirect
from .models import Complaint
from django.views.decorators.csrf import csrf_exempt

def staff_dashboard_view(request):
    if request.session.get('user_role') != 'staff':
        return redirect('login')

    staff_id = request.session.get('user_id')
    complaints = Complaint.objects.filter(assigned_to_id=staff_id).order_by('-created_at')

    return render(request, 'staff_complaints.html', {
        'complaints': complaints
    })


@csrf_exempt
def staff_update_complaint(request, complaint_id):
    if request.session.get('user_role') != 'staff':
        return redirect('login')

    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        mark_resolved = request.POST.get('mark_resolved')

        if comment:
            complaint.staff_response = comment

        if mark_resolved == 'yes':
            complaint.status = 'resolved'

        complaint.save()
        return redirect('staff_complaint')

    return redirect('staff_complaint')



def mark_complaint_resolved(request):
    if request.session.get('user_role') != 'staff':
        messages.error(request, "Access denied.")
        return redirect('login')

    staff_id = request.session.get('user_id')

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        try:
            complaint = Complaint.objects.get(id=complaint_id, assigned_to_id=staff_id)
            complaint.status = 'Resolved'
            complaint.save()
            messages.success(request, "Complaint marked as resolved.")
        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found or not assigned to you.")

        return redirect('mark_resolved')

    
    assigned_complaints = Complaint.objects.filter(assigned_to_id=staff_id).exclude(status='Resolved')
    return render(request, 'mark_resolved.html', {'complaints': assigned_complaints})
