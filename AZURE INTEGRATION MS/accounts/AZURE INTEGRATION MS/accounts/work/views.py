import msal
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

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

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html', {
        'user_name': request.session.get('user_name'),
        'user_email': request.session.get('user_email'),
    })

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')