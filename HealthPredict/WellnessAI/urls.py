from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about,name = 'about'),
    path('symptomChecker/', views.symptomChecker,name = 'symptomChecker'),
    path('contact/', views.contact_view,name = 'contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('make-appointment/', views.make_appointment, name='make_appointment'),
    path('contact/', views.contact_view, name='contact'),
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('save-user-details/', views.save_user_details, name='save_user_details'),
    path('get-prediction/', views.get_prediction, name='get_prediction'),
    path('add-doctor/', views.add_doctor, name='add_doctor'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/', views.user_dashboard, name='profile'),
    path('update-profile/', views.update_profile_data, name='update_profile_data'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),  # Blog detail page
    path('update_/', views.update_basic_details, name='update_user_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
