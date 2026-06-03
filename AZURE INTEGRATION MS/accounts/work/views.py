import msal
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import SharedFile
from .forms import SharedFileForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def build_msal_app():
    return msal.ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=settings.AUTHORITY,
        client_credential=settings.AZURE_CLIENT_SECRET,
    )

def login_view(request):
    return render(request, 'template.html')

def microsoft_login(request):
    msal_app = build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=settings.SCOPE,
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )
    return redirect(auth_url)

def auth_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Login failed: no code returned", status=400)

    msal_app = build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=settings.SCOPE,
        redirect_uri=settings.AZURE_REDIRECT_URI,
    )

    if "error" in result:
        return HttpResponse(f"Login error: {result.get('error_description')}", status=400)

    # Get user info from Microsoft Graph
    access_token = result['access_token']
    graph_response = requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile = graph_response.json()

    # Get or create Django user
    email = profile.get("mail") or profile.get("userPrincipalName")
    username = email.split("@")[0]
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email, "first_name": profile.get("displayName", "")}
    )

    # Store token in session
    request.session['access_token'] = access_token
    request.session['user_name'] = profile.get("displayName", username)
    request.session['user_email'] = email

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('dashboard')

# def dashboard_view(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     return render(request, 'dashboard.html', {
#         'user_name': request.session.get('user_name'),
#         'user_email': request.session.get('user_email'),
#     })

# ── REPLACE your existing dashboard_view with this ──

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    my_files   = SharedFile.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    received   = SharedFile.objects.filter(shared_with=request.user).order_by('-uploaded_at')

    # files shared out by me = my files that have at least 1 shared_with user
    shared_out = my_files.filter(shared_with__isnull=False).distinct()

    return render(request, 'dashboard.html', {
        'user_name':      request.session.get('user_name'),
        'user_email':     request.session.get('user_email'),
        # stat counts
        'my_files_count': my_files.count(),
        'shared_count':   shared_out.count(),
        'received_count': received.count(),
        # tables (5 most recent each)
        'recent_files':    my_files[:5],
        'recent_received': received[:5],
    })

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required
def file_list(request):
    my_files       = SharedFile.objects.filter(uploaded_by=request.user)
    shared_with_me = SharedFile.objects.filter(shared_with=request.user)
    return render(request, 'files.html', {
        'my_files':       my_files,
        'shared_with_me': shared_with_me,
        'user_name':      request.session.get('user_name'),
        'user_email':     request.session.get('user_email'),
    })

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = SharedFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.uploaded_by = request.user
            f.save()
            return redirect('file_list')
    else:
        form = SharedFileForm()
    return render(request, 'upload_file.html', {
        'form':       form,
        'user_name':  request.session.get('user_name'),
        'user_email': request.session.get('user_email'),
    })

# @login_required
# def share_file(request, pk):
#     file_obj = get_object_or_404(SharedFile, pk=pk, uploaded_by=request.user)
#     error = None
def share_file(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    file_obj = get_object_or_404(SharedFile, pk=pk, uploaded_by=request.user)
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = email.split("@")[0]
        target, _ = User.objects.get_or_create(email=email, defaults={'username': username})
        file_obj.shared_with.add(target)
        return redirect('file_list')
        # try:
        #     target = User.objects.get(email=email)
        #     file_obj.shared_with.add(target)
        #     return redirect('file_list')
        # except User.DoesNotExist:
        #     error = f'No user found with email: {email}'
    return render(request, 'share_file.html', {
        'file':       file_obj,
        'error':      error,
        'user_name':  request.session.get('user_name'),
        'user_email': request.session.get('user_email'),
    })

@login_required
def delete_file(request, pk):
    file_obj = get_object_or_404(SharedFile, pk=pk, uploaded_by=request.user)
    file_obj.file.delete()
    file_obj.delete()
    return redirect('file_list')