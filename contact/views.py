
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
import os

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Save to database
            contact = Contact.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                address=data.get('address'),
                education=data.get('education'),
                skills=data.get('skills'),
                experience=data.get('experience'),
                salary=data.get('salary'),
                position=data.get('position'),
                dob=data.get('dob')
            )
            
            # Send email
            subject = f"New Bio-Data Submission from {data.get('name')}"
            message = f"""
            New bio-data submission:
            
            Name: {data.get('name')}
            Email: {data.get('email')}
            Phone: {data.get('phone')}
            Position: {data.get('position')}
            Experience: {data.get('experience')} years
            Expected Salary: {data.get('salary')}
            
            Full details saved in database.
            """
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            
            return JsonResponse({'message': 'Bio-data submitted successfully!'})
            
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=400)
    
    return JsonResponse({'message': 'Only POST method allowed'}, status=405)

def home(request):
    # Serve the index.html file from the root directory
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'index.html')
    with open(html_path, 'r') as f:
        return HttpResponse(f.read(), content_type='text/html')
