from django.shortcuts import render
from. models import Seeker,Employer,CustomUser,ApprovedSeeker,ApprovedEmployer,JobPost,UserProfile,AppliedJobs
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
from django.core.files.base import ContentFile
import base64
from datetime import date
import logging
from django.views.decorators.http import require_http_methods


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
            print(username)
            print(password)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

        if username and password:
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print('user exist')
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
                    password= make_password(employer.password),
                    user_type=employer.user_type
                )
                approved_employer, created = ApprovedEmployer.objects.get_or_create(
                    name=employer.name,
                    email=employer.email,
                    mobile=employer.mobile,
                    password=make_password(employer.password),
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
    


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_job(request):
    try:
        data = request.data
        
        
        user = request.user
        

        job_designation = data.get('jobDesignation')
        description = data.get('description')
        posting_date = data.get('postingDate')
        last_date_to_apply = data.get('lastDateToApply')
        other_requirements = data.get('otherRequirements')
        
        image = data.get('image')
        image_format, image_str = image.split(';base64,') 
        ext = image_format.split('/')[-1] 
        image_data = ContentFile(base64.b64decode(image_str), name='temp.' + ext)
        

        job_post = JobPost(
            job_designation=job_designation,
            description=description,
            posting_date=posting_date,
            last_date_to_apply=last_date_to_apply,
            other_requirements=other_requirements,
            image=image_data,
            posted_by=user
        )
        
        job_post.save()
       

        return Response({'success': True, 'message': 'Job posted successfully'})
    except Exception as e:
        
        return Response({'success': False, 'message': str(e)}, status=500)
    



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_posted_jobs(request):
    try:
        user = request.user
        jobs = JobPost.objects.filter(posted_by=user)
        
        # Construct the response data manually
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'job_designation': job.job_designation,
                'description': job.description,
                'posting_date': job.posting_date,
                'last_date_to_apply': job.last_date_to_apply,
                'other_requirements': job.other_requirements,
                'status':job.status,
            })
        
        return JsonResponse(jobs_data, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_job_details(request, job_id):
    try:
        user = request.user
        job = JobPost.objects.get(id=job_id, posted_by=user)
        job_data = {
            'job_designation': job.job_designation,
            'description': job.description,
            'posting_date': job.posting_date,
            'last_date_to_apply': job.last_date_to_apply,
            'other_requirements': job.other_requirements,
        }
        return JsonResponse(job_data)
    except JobPost.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_job(request, job_id):
    try:
        user = request.user
        job = JobPost.objects.get(id=job_id, posted_by=user)
        data = json.loads(request.body)
        
        job.job_designation = data.get('job_designation', job.job_designation)
        job.description = data.get('description', job.description)
        job.posting_date = data.get('posting_date', job.posting_date)
        job.last_date_to_apply = data.get('last_date_to_apply', job.last_date_to_apply)
        job.other_requirements = data.get('other_requirements', job.other_requirements)
        
        job.save()
        return JsonResponse({'success': True, 'message': 'Job updated successfully'})
    except JobPost.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Job not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@require_http_methods(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def delete_job(request, job_id):
    try:
        # Check if the job exists and belongs to the logged-in user
        job = JobPost.objects.get(id=job_id)
        job.delete()
        return JsonResponse({'success': True, 'message': 'Job deleted successfully'})
    except JobPost.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@require_http_methods(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def posted_jobs(request):
    employer = request.user 
    jobs = JobPost.objects.filter(employer=employer)
    job_list = [
        {
            "id": job.id,
            "job_designation": job.job_designation,
            "description": job.description,
            "posting_date": job.posting_date,
            "last_date_to_apply": job.last_date_to_apply,
            "other_requirements": job.other_requirements
        }
        for job in jobs
    ]
    return JsonResponse(job_list, safe=False)

@api_view(['GET'])
def job_approvals(request):
    try:
        jobs = JobPost.objects.filter(status = 'pending')
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'job_designation': job.job_designation,
                'description': job.description,
                'posting_date': job.posting_date,
                'last_date_to_apply': job.last_date_to_apply,
                'other_requirements': job.other_requirements,
                'posted_by':job.posted_by.username
            })
        
        return JsonResponse(jobs_data, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@require_http_methods(["POST"])
@csrf_exempt
def approve_job(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        job = JobPost.objects.get(id=job_id)
        job.status = 'approved'
        job.save()
        return JsonResponse({"success": True})
    except JobPost.DoesNotExist:
        return JsonResponse({"success": False, "message": "Job not found"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    
@require_http_methods(["POST"])
@csrf_exempt
def reject_job(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        job = JobPost.objects.get(id=job_id)
        job.status = 'rejected'
        job.save()
        return JsonResponse({"success": True})
    except JobPost.DoesNotExist:
        return JsonResponse({"success": False, "message": "Job not found"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    

@api_view(['GET'])
def all_jobs(request):
    try:
        jobs = JobPost.objects.filter(status = 'approved')
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'job_designation': job.job_designation,
                'description': job.description,
                'posting_date': job.posting_date,
                'last_date_to_apply': job.last_date_to_apply,
                'other_requirements': job.other_requirements,
                'posted_by':job.posted_by.username
            })
        
        return JsonResponse(jobs_data, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

@api_view(['GET'])
def seeker_view_jobs(request):
    try:
        jobs = JobPost.objects.filter(status = 'approved')
        jobs_data = []
        for job in jobs:
            jobs_data.append({
                'id': job.id,
                'job_designation': job.job_designation,
                'description': job.description,
                'posting_date': job.posting_date,
                'last_date_to_apply': job.last_date_to_apply,
                'other_requirements': job.other_requirements,
                'posted_by':job.posted_by.username
            })
        
        return JsonResponse(jobs_data, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    profile_picture_url = ''
    if user_profile.profile_picture:
        profile_picture_url = request.build_absolute_uri(user_profile.profile_picture.url)
    
    profile_data = {
        'qualification': user_profile.qualification,
        'address': user_profile.address,
        'profile_picture': profile_picture_url
    }
    return Response(profile_data)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if 'qualification' in request.data:
        user_profile.qualification = request.data['qualification']
    if 'address' in request.data:
        user_profile.address = request.data['address']
    
    if 'profile_picture' in request.data and request.data['profile_picture']:
        format, imgstr = request.data['profile_picture'].split(';base64,')
        ext = format.split('/')[-1]
        user_profile.profile_picture = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}.{ext}')
    
    user_profile.save()
    
    return Response({"success": True})

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def apply_job(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_id = data.get('job_id')
            user = request.user
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        
        if job_id:
            try:
                job = JobPost.objects.get(id=job_id)
                user_profile = UserProfile.objects.get(user = user)
                AppliedJobs.objects.create(user=user, job=job,user_profile=user_profile)
                return JsonResponse({'success': True, 'message': 'Application submitted successfully'})
            except JobPost.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Job not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'message': 'Job ID missing'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_applied_jobs(request):
    if request.method == 'GET':
        user = request.user
        applied_jobs = AppliedJobs.objects.filter(user=user).select_related('job')
        applied_jobs_data = [
            {
                'id': applied_job.id,
                'job': {
                    'job_designation': applied_job.job.job_designation,
                    'description': applied_job.job.description,
                    'posting_date': applied_job.job.posting_date,
                    'last_date_to_apply': applied_job.job.last_date_to_apply,
                    'other_requirements': applied_job.job.other_requirements,
                    'posted_by': applied_job.job.posted_by.username, 
                },
                'applied_on': applied_job.applied_on,
                'status':applied_job.status
            }
            for applied_job in applied_jobs
        ]
        return JsonResponse(applied_jobs_data, safe=False)
    else:
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vieww_applied_jobs(request):
    user = request.user
    try:
        applied_jobs = AppliedJobs.objects.filter(user=user).select_related('job')
        job_list = [
            {
                'id': applied_job.job.id,
                'job_designation': applied_job.job.job_designation,
                'description': applied_job.job.description,
                'posting_date': applied_job.job.posting_date,
                'last_date_to_apply': applied_job.job.last_date_to_apply,
                'other_requirements': applied_job.job.other_requirements,
                'posted_by': applied_job.job.posted_by.username,
            }
            for applied_job in applied_jobs
        ]
        print(job_list)
        return JsonResponse(job_list, safe=False)
    except AppliedJobs.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No applied jobs found'}, status=404)
    except Exception as e:
        print(f"Error fetching applied jobs: {e}")
        return JsonResponse({'success': False, 'message': 'Error fetching applied jobs'}, status=500)
    

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def employer_view_applications(request):
    if request.method == 'GET':
        user = request.user
        job_posts = JobPost.objects.filter(posted_by=user)
        applied_jobs = AppliedJobs.objects.filter(job__in=job_posts).select_related('job', 'user')
        
        applications = []
        for application in applied_jobs:
            applications.append({
                'job_designation': application.job.job_designation,
                'job_description': application.job.description,
                'applicant_name': application.user.username,
                'application_date': application.applied_on,
                'id':application.id
            })

        return JsonResponse(applications, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_applicant_details(request, id):
    try:
        applied_job = AppliedJobs.objects.get(pk=id)
        applied_job.status = 'viewed'
        applied_job.save()
        applicant = {
            'applicant_name': applied_job.user.username,
            'applicant_qualification':applied_job.user_profile.qualification,
            'applicant_address':applied_job.user_profile.address,
            'application_date': applied_job.applied_on,
            'job_designation': applied_job.job.job_designation,
            'job_description': applied_job.job.description,
        }

        return JsonResponse(applicant)
    except AppliedJobs.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)