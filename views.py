from django.shortcuts import render,redirect
from django.contrib import messages  
from .models import *
from .forms import *
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timezone import make_naive, now
def index(request):    
    
    return render(request,"index.html",locals())
def attendanceList(request):
    if request.method == 'POST': 
        course = request.POST.get('course', None)  # Use .get() to prevent KeyError
        deg = request.POST.get('deg', None)
        dept = request.POST.get('dept', None)
        bat = request.POST.get('bat', None)
        dt = request.POST.get('dt', None)
        
        frm=Attendance.objects.filter(course=course,deg=deg,dept=dept,batch=bat,dt1=dt)   
        if frm:
            pass
        else:
            messages.success(request,'Record Not Found')  
    return render(request,"attendance_list.html",locals())

    #     # Debugging: Print received data
    #     print("Received Data:", request.POST)

    #     # Check if any required field is missing
    #     if not all([course, deg, dept, bat, dt]):
    #         messages.error(request, "Missing required fields!")
    #         return render(request, "attendance_list.html")

    #     frm = Attendance.objects.filter(course=course, deg=deg, dept=dept, batch=bat, dt1=dt)   
    #     if not frm.exists():  # Use .exists() for better performance
    #         messages.warning(request, "Record Not Found")

    # return render(request, "attendance_list.html")

# def attendanceList(request):
#     if request.method=='POST': 
#         course=request.POST['course']
#         deg=request.POST['deg']
#         dept=request.POST['dept']
#         bat=request.POST['bat']
#         dt=request.POST['dt']
         
#         frm=Attendance.objects.filter(course=course,deg=deg,dept=dept,batch=bat,dt1=dt)   
#         if frm:
#             pass
#         else:
#             messages.success(request,'Record Not Found')  
#     return render(request,"attendance_list.html",locals())
def attendanceDelete(request,id):
    frm=Attendance.objects.get(id=id)
    frm.delete()  
    messages.success(request,'Attendance Delete Successfully')  
    return redirect('/attendanceList')

def Login(request):
    status="User Login"
    if request.method=='POST':        
        uname=request.POST['uname']       
        pass1=request.POST['pass1']
                
        if uname=="admin"  and pass1=="admin":                          
            return redirect('/degreeList')
        else:
            messages.success(request,'Login Failed')        
    return render(request,"login.html",locals())
def degreeAdd(request):
    if request.method=='POST': 
        frm = DegreeForm(request.POST)  
        if frm.is_valid():            
            messages.success(request,'Degree Save Successfully')
            frm.save()
        else:
            messages.success(request,'Please Fill all Field')
    return render(request,"degree_add.html",locals())
def degreeList(request):
    frm=Degree.objects.all()    
    return render(request,"degree_list.html",locals())
def degreeDelete(request,id):
    frm=Degree.objects.get(id=id)
    frm.delete()  
    messages.success(request,'Degree Delete Successfully')  
    return redirect('/degreeList')
def degreeUpdate(request, id):
    degree = Degree.objects.get(id=id)
    
    if request.method == "POST":
        original_dt = degree.dt  # Store the original Dt value

        frm = DegreeForm(request.POST, instance=degree)  
        if frm.is_valid():  
            updated_degree = frm.save(commit=False)  # Prevent auto-save

            updated_degree.dt = original_dt  # Ensure Dt remains unchanged
            updated_degree.save()  # Now save to DB
            
            messages.success(request, 'Degree Updated Successfully')
            return redirect('/degreeList')  # Redirect to degree list

        else:
            messages.error(request, 'Please Fill all Fields')

    else:
        frm = DegreeForm(instance=degree)

    return render(request, "degree_update.html", {"ob": degree, "form": frm})

def departmentAdd(request):
    if request.method=='POST': 
        frm = DepartmentForm(request.POST)  
        if frm.is_valid():            
            messages.success(request,'Department Save Successfully')
            frm.save()
        else:
            messages.success(request,'Please Fill all Field')
    
    return render(request,"department_add.html",locals())
def checkCourse(request):
    course=request.GET.get('course')
    frm=Degree.objects.filter(course=course)
    data=[]
    for k in frm:
        print(k.deg)
        data.append(k.deg)
    return JsonResponse({'data': data}, status=200)
def checkDegree(request):
    course=request.GET.get('course')
    deg=request.GET.get('deg')
    
    frm=Department.objects.filter(course=course,deg=deg)
    data=[]
    for k in frm:
        print(k.dept)
        data.append(k.dept)
    return JsonResponse({'data': data}, status=200)

def departmentList(request):
    frm=Department.objects.all()   
    if request.method=='POST':        
        course=request.POST['course']  
        deg=request.POST['deg']
        frm=Department.objects.filter(course=course,deg=deg)     

        
     
    return render(request,"Department_list.html",locals())
def departmentDelete(request,id):
    frm=Department.objects.get(id=id)
    frm.delete()  
    messages.success(request,'Department Delete Successfully')  
    return redirect('/departmentList')
def departmentUpdate(request, id):
    department = Department.objects.get( id=id)

    if request.method == "POST":
        original_dt = department.dt  # Store the original Dt value
        frm = DepartmentForm(request.POST, instance=department)  
        if frm.is_valid():  
            updated_department = frm.save(commit=False)  # Prevent auto-save

            updated_department.dt = original_dt  # Ensure Dt remains unchanged
            updated_department.save()  # Now save to DB
            
            messages.success(request, 'Department Updated Successfully')
            return redirect('/departmentList')  # Redirect to department list

        else:
            messages.error(request, 'Please Fill all Fields')

    else:
        frm = DepartmentForm(instance=department)

    return render(request, "department_update.html", {"ob": department, "form": frm})

def admissionAdd(request):
    if request.method=='POST': 
        frm = AdmissionForm(request.POST,request.FILES)  
        if frm.is_valid():            
            messages.success(request,'Admission Save Successfully')
            frm.save()
        else:
            messages.success(request,'Please Fill all Field')
    return render(request,"admission_add.html",locals())
def admissionList(request):
    if request.method=='POST': 
        course=request.POST['course']
        deg=request.POST['deg']
        dept=request.POST['dept']
        bat=request.POST['bat']         
        frm=Admission.objects.filter(course=course,deg=deg,dept=dept,bat=bat)    
    return render(request,"admission_list.html",locals())
def admissionDelete(request,id):
    frm=Admission.objects.get(id=id)
    frm.delete()  
    messages.success(request,'Admission Delete Successfully')  
    return redirect('/admissionList')
def admissionUpdate(request,id):
    ob=Admission.objects.get(id=id)
    if request.method=='POST': 
        original_dt = ob.dt  # Store original Dt value to preserve it
        frm = AdmissionForm(request.POST,request.FILES,instance=ob)  
        if frm.is_valid():            
           updated_admission = frm.save(commit=False)  # Prevent auto-save
            
           updated_admission.dt = original_dt  # Ensure Dt remains unchanged
           updated_admission.save()  # Now save to DB

           messages.success(request, 'Admission Updated Successfully')
           return redirect("/admissionList")  # Redirect to the list page
        else:
            messages.error(request, 'Please Fill all Fields')
    else:
        frm = AdmissionForm(instance=ob)  # Initialize the form for GET request
    return render(request, "admission_update.html", {"ob": ob, "form": frm})

def timeAdd(request):
    from datetime import datetime, timedelta
    if request.method=='POST': 
        SetTime.objects.all().delete()
        tm=request.POST['tm']
        tm = tm.split(":")
        print(int(tm[0]))
        print(int(tm[1]))
        print(int(datetime.now().year))
        yr=int(datetime.now().year)
        m=int(datetime.now().month)
        # d=int(datetime.now().)
        dt = str(datetime.now().date())
        dt = dt.split("-")
        print(dt[0])
        # tm = datetime(int(datetime.now().year), int(datetime.now().month), int(datetime.now().date), int(tm[0]), int(tm[1]), 0)
        tm = datetime(int(dt[0]), int(dt[1]), int(dt[2]), int(tm[0]), int(tm[1]), 0)
        # tm=datetime(2025, 2, 18, 14, 30, 0)
        print(tm)
        SetTime(tm=tm).save()
       
        messages.success(request,'Time Set  Successfully')
       
    return render(request,"set_time.html",locals())
def timeList(request):
    frm=SetTime.objects.all()    
    return render(request,"set_time_list.html",locals())
def timeDelete(request,id):
    frm=SetTime.objects.get(id=id)  
    frm.delete()  
    messages.success(request,'Set Date Delete Successfully')  
    return redirect('/timeList')

    


    