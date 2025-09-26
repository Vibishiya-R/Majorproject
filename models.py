from django.db import models
from django.utils import timezone

class Admission(models.Model):
    ano = models.IntegerField(unique=True, blank=True, null=True)
    bat = models.TextField(blank=True, null=True)
    sname = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    fname = models.TextField(blank=True, null=True)
    dob = models.TextField(blank=True, null=True)
    addr = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    cno = models.TextField(blank=True, null=True)
    pgroup = models.TextField(blank=True, null=True)
    course = models.TextField(blank=True, null=True)
    deg = models.TextField(blank=True, null=True)
    
    dept = models.TextField(blank=True, null=True)
    caste = models.TextField(blank=True, null=True)
    rel = models.TextField(blank=True, null=True)     
    img = models.FileField(upload_to='upload/')    
    # dt = models.DateTimeField(default=timezone.now)  
    created_dt = models.DateTimeField(default=timezone.now, editable=False)  # Original creation time
    dt = models.DateTimeField(auto_now=True)  # Auto-update on modification
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  
    def __str__(self):
        return self.sname
    def save(self, *args, **kwargs):
        if not self.ano:
            last_entry = Admission.objects.all().order_by('ano').last()
            if last_entry:
                self.ano = last_entry.ano + 1
            else:
                self.ano = 1000  # Starting value
        super(Admission, self).save(*args, **kwargs)
class Degree(models.Model):
    course = models.TextField(blank=True, null=True) 
    deg = models.TextField(blank=True, null=True)     
    # dt = models.DateTimeField(default=timezone.now) 
    created_dt = models.DateTimeField(default=timezone.now, editable=False)  # Original creation time
    dt = models.DateTimeField(auto_now=True)  # Auto-update on modification
class Department(models.Model):
    course = models.TextField(blank=True, null=True) 
    deg = models.TextField(blank=True, null=True)    
    dept = models.TextField(blank=True, null=True)     
    # dt = models.DateTimeField(default=timezone.now)
    created_dt = models.DateTimeField(default=timezone.now, editable=False)  # Original creation time
    dt = models.DateTimeField(auto_now=True)  # Auto-update on modification


class Attendance(models.Model):
    course = models.TextField(blank=True, null=True) 
    deg = models.TextField(blank=True, null=True)    
    dept = models.TextField(blank=True, null=True) 
    batch = models.TextField(blank=True, null=True) 
    
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    dt = models.DateTimeField(default=timezone.now)  
    dt1 = models.TextField(blank=True, null=True) 
    

class SetTime(models.Model):
    tm = models.TextField(blank=True, null=True)    
    

    
      
      
    

 


    
    
    
