from django.shortcuts import render
from. models import Seeker,Employer,CustomUser,ApprovedSeeker,ApprovedEmployer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .Serializers import EmployerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_protect


@csrf_exempt
def register_seeker(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        mobile = data.get('mobile')
        password = data.get('password')
        dob = data.get('dob')
        user_type = data.get('userType')
        
        # Create and save a new Seeker object
        seeker = Seeker(name=name, email=email, mobile=mobile, password=password, dob=dob,user_type=user_type)
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
        user_type = data.get('userType')

        # Create and save a new Employer object
        employer = Employer(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            logo=logo,
            website=website,
            address=address,
            user_type=user_type
        )
        employer.save()

        return JsonResponse({'message': 'Employer registered successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'success': True, 'usertype': user.user_type, 'token': token.key})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Username or password missing'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def get_seekers(request):
    if request.method == 'GET':
        seekers = Seeker.objects.all()
        seekers_data = []
        for seeker in seekers:
            seekers_data.append({
                'id': seeker.id,
                'name': seeker.name,
                'email': seeker.email,
                'mobile': seeker.mobile,
                'dob': seeker.dob
                # Add other fields as necessary
            })
        return JsonResponse(seekers_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def get_employers(request):
    if request.method == 'GET':
        employers = Employer.objects.all()
        employers_data = []
        for employer in employers:
            employers_data.append({
                'id': employer.id,
                'name': employer.name,
                'email': employer.email,
                'mobile': employer.mobile,
                'website': employer.website,
                'address':employer.address
                # Add other fields as necessary
            })
        return JsonResponse(employers_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def approve_seeker(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seeker_id = data.get('seeker_id')
            print(seeker_id)  # For debugging purposes
            if not seeker_id:
                return JsonResponse({'success': False, 'message': 'Seeker ID not provided'}, status=400)
            try:
                seeker = Seeker.objects.get(id=seeker_id)
                # Create a new ApprovedSeeker with the same details
                custom_seeker, created = CustomUser.objects.get_or_create(
                    username=seeker.name,
                    email=seeker.email,
                    password= make_password(seeker.password),
                    user_type=seeker.user_type
                )
                approved_seeker, created = ApprovedSeeker.objects.get_or_create(
                    name=seeker.name,
                    email=seeker.email,
                    mobile=seeker.mobile,
                    password=seeker.password,
                    dob=seeker.dob,
                    user_type=custom_seeker
                )
                
                if created:
                    # Delete the seeker from the Seeker table
                    seeker.delete()
                    return JsonResponse({'success': True, 'message': 'Seeker approved successfully'})
                else:
                    return JsonResponse({'success': False, 'message': 'Seeker is already approved'})
            except Seeker.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Seeker not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
@csrf_exempt
def approve_employer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employer_id = data.get('employer_id')
            print(employer_id)  # For debugging purposes
            if not employer_id:
                return JsonResponse({'success': False, 'message': 'Employer ID not provided'}, status=400)
            try:
                employer = Employer.objects.get(id=employer_id)
                # Create a new ApprovedEmployer with the same details
                custom_employer, created = CustomUser.objects.get_or_create(
                    username=employer.name,
                    email=employer.email,
                    password=employer.password,
                    user_type=employer.user_type
                )
                approved_employer, created = ApprovedEmployer.objects.get_or_create(
                    name=employer.name,
                    email=employer.email,
                    mobile=employer.mobile,
                    password=employer.password,
                    logo=employer.logo,
                    website=employer.website,
                    address=employer.address,
                    user_type= custom_employer
                )
                
                if created:
                    # Optionally, you can delete the original employer
                    employer.delete()
                    return JsonResponse({'success': True, 'message': 'Employer approved successfully'})
                else:
                    return JsonResponse({'success': False, 'message': 'Employer is already approved'})
            except Employer.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Employer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    


@csrf_exempt
def all_seekers(request):
    if request.method == 'GET':
        seekers = ApprovedSeeker.objects.all()
        seekers_data = []
        for seeker in seekers:
            seekers_data.append({
                'id': seeker.id,
                'name': seeker.name,
                'email': seeker.email,
                'mobile': seeker.mobile,
                'dob': seeker.dob
                # Add other fields as necessary
            })
        return JsonResponse(seekers_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def all_employers(request):
    if request.method == 'GET':
        employers = ApprovedEmployer.objects.all()
        employers_data = []
        for employer in employers:
            employers_data.append({
                'id': employer.id,
                'name': employer.name,
                'email': employer.email,
                'mobile': employer.mobile,
                'website': employer.website,
                'address':employer.address
                # Add other fields as necessary
            })
        return JsonResponse(employers_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def reject_seeker(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seeker_id = data.get('seeker_id')
            if not seeker_id:
                return JsonResponse({'success': False, 'message': 'Seeker ID not provided'}, status=400)
            try:
                seeker = Seeker.objects.get(id=seeker_id)
                seeker.delete()
                return JsonResponse({'success': True, 'message': 'Seeker rejected successfully'})
            except Seeker.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Seeker not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    

@csrf_exempt
def reject_employer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employer_id = data.get('employer_id')
            if not employer_id:
                return JsonResponse({'success': False, 'message': 'Employer ID not provided'}, status=400)
            try:
                employer = Employer.objects.get(id=employer_id)
                employer.delete()
                return JsonResponse({'success': True, 'message': 'employer rejected successfully'})
            except Seeker.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Employer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
@csrf_exempt
def remove_employer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employer_id = data.get('employer_id')
            if not employer_id:
                return JsonResponse({'success': False, 'message': 'Employer ID not provided'}, status=400)
            try:
                employer = ApprovedEmployer.objects.get(id=employer_id)
                user_type = employer.user_type
                employer.delete()
                user_type.delete()
                return JsonResponse({'success': True, 'message': 'employer deleted successfully'})
            except Seeker.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Employer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    

@csrf_exempt
def remove_seeker(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seeker_id = data.get('seeker_id')
            if not seeker_id:
                return JsonResponse({'success': False, 'message': 'Seeker ID not provided'}, status=400)
            try:
                seeker = ApprovedSeeker.objects.get(id=seeker_id)
                user_type = seeker.user_type
                seeker.delete()
                user_type.delete()
                return JsonResponse({'success': True, 'message': 'employer deleted successfully'})
            except Seeker.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Employer not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_details(request):
    user = request.user
    return Response({
        'username': user.username,
        'email': user.email if user.email else ''
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_admin_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            username = data.get('username')
            email = data.get('email')

            if username:
                user.username = username
            if email:
                user.email = email

            user.save()

            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            password = data.get('password')

            if password:
                user.password = make_password(password)

            user.save()

            return JsonResponse({'success': True, 'message': 'Password updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)