from django.contrib import admin
from django.urls import path
from main import views
from main.views import ContactAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', ContactAPIView.as_view(), name='contact'),
    path('resume/download/', views.download_resume, name='download_resume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
