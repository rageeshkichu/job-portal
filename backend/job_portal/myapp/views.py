from django.shortcuts import render
from. models import Seeker,Employer,CustomUser
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Serializers import EmployerSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login


@csrf_exempt
def register_seeker(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        dob = data.get('dob')
        
        # Create and save a new Seeker object
        seeker = Seeker(name=name, email=email, mobile=mobile, password=password, dob=dob)
        seeker.save()
        
        return JsonResponse({'message': 'Seeker registered successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def register_employer(request):
    if request.method == 'POST':
        data = request.POST  # If form data is submitted via POST
        # Or use request.body if data is submitted via JSON

        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        logo = request.FILES.get('logo')  # If you're uploading a file
        website = data.get('website')
        address = data.get('address')

        # Create and save a new Employer object
        employer = Employer(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            logo=logo,
            website=website,
            address=address
        )
        employer.save()

        return JsonResponse({'message': 'Employer registered successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        # For JSON data
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        # For form data
        # username = request.POST.get('username')
        # password = request.POST.get('password')

        # Your authentication logic here
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Authentication successful
                login(request, user)
                return JsonResponse({'success': True, 'usertype': user.user_type})
            else:
                # Authentication failed
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Username or password missing'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
