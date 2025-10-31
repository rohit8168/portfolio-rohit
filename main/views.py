from django.shortcuts import render, redirect
from .models import Project, Contact,Experience,Resume
from django.core.mail import send_mail
from django.conf import settings
from .Serializer import ContactSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import response,FileResponse,Http404
from rest_framework import status
import os
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    experiences=Experience.objects.all().order_by("-created_at")
    return render(request, 'main/index.html', {'projects': projects,'experiences': experiences,})

class ContactAPIView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Send email notification
            send_mail(
                subject="We received your message!",
                message=f"Hi {contact.name},\n\nThank you for reaching out. We will get back to you soon!\n\nYour Message:\n{contact.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact.email],  # send to user
                fail_silently=False,
            )

            # Optionally, send notification to yourself
            send_mail(
                subject="New Contact Form Submission",
                message=f"Name: {contact.name}\nEmail: {contact.email}\nMessage: {contact.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # your email
                fail_silently=False,
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def download_resume(request):
    try:
        resume = Resume.objects.first()  # Get the single resume
        if not resume:
            raise Http404("No resume uploaded yet.")
        file_path = resume.file.path
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename="My_Resume.pdf")
        else:
            raise Http404("File not found.")
    except Resume.DoesNotExist:
        raise Http404("Resume not found.")
