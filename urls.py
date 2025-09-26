from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from appdata.views import *
urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', Login),
    path('degreeAdd/', degreeAdd),
    path('degreeDelete/<int:id>', degreeDelete),
    path('degreeUpdate/<int:id>', degreeUpdate),
    path('departmentAdd/', departmentAdd),
    path('departmentUpdate/<int:id>/', departmentUpdate ),
    path('departmentDelete/<int:id>', departmentDelete),
    path('degreeList/', degreeList),
    path('departmentList/', departmentList,name='department_list'),
    path('checkCourse/', checkCourse),
    path('admissionAdd/', admissionAdd),
    path('checkDegree/', checkDegree),
    path('admissionUpdate/<int:id>', admissionUpdate),
    path('admissionList/', admissionList),
    path('admissionDelete/<int:id>', admissionDelete),
    
    path('', index),
    path('attendanceList/', attendanceList),
    path('attendanceDelete/<int:id>', attendanceDelete),
    path('attendanceList/', attendanceList),
    path('timeAdd/', timeAdd),
    path('timeList/', timeList),
    path('timeDelete/<int:id>', timeDelete),
    path('timeList/', timeList),
    path('timeList/', timeList),
    
   
]
if settings.DEBUG:
        urlpatterns+= static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)