from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from classroom.views import classroom, students, teachers, parents, adminV

urlpatterns = [
    path('', include('classroom.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/student/', students.StudentSignUpView, name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView, name='teacher_signup'),
    path('accounts/signup/parent/', parents.ParentSignUpView, name='parent_signup'),
    path('accounts/signup/admin/', adminV.AdminSignUpView.as_view(), name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
