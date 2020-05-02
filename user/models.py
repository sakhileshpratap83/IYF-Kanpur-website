from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import RegexValidator
from PIL import Image
# from phone_field import PhoneField
# from django.utils.encoding import python_2_unicode_compatible
# from six import python_2_unicode_compatible
# from django.db import models

# from django.contrib.auth.models import User

##Remember to use this command to create the tables you need in your database
##python manage.py migrate





BLOODGROUPS = (
	('A+', 'A+'),
	('A-', 'A-'),
	('B+', 'B+'),
	('B-', 'B-'),
	('O+', 'O+'),
	('O-', 'O-'),
	('AB+', 'AB+'),
	('AB-', 'AB-'),
	('NA', 'Do not know'), 
)

GENDER = (
	('M', 'Male'),
	('F', 'Female'),
	('O', 'Others'),
)

MARITALSTATUS = (
	('BRA', 'Brahmachari'),
	('GRA', 'Grahastha'),
	('VAN', 'Vanaprastha'),
	('SAN', 'Sannyasi'),
)

GRADUATION = (
	('btech', 'B.Tech'),
	('Be', 'BE'),
	('Bsc', 'B.Sc.'),
	('Dip', 'Diploma'),
	)

COLLEGE = (
	('iitbhu', 'IIT BHU'),
	('iitk', 'IIT Kanpur'),
	('bhu', 'BHU'),
	('nit', 'NIT ALD'),
	('iiit', 'IIIT ALD'),
	('hbtu','HBTU'),
	('iet','IET'),
	('csjm','CSJM'),
	('aith','AITH'),
	('gcti','GCTI'),
	('psit','PSIT'),
	('rec','REC-Bijnore'),
	('other', 'Other'),
	)



# class State(models.Model):
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name

# class City(models.Model):
#     state = models.ForeignKey(State, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.name



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE) #CASCADE delete the user and profile will be deleted
	# full_name = models.CharField(null = True, max_length=100)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	blood_group = models.CharField(default = 'NA', max_length=3, choices =BLOODGROUPS)
	dob = models.DateField(default = datetime.now)
	gender = models.CharField(default= 'Male', max_length=6, choices=GENDER)
	marital_status = models.CharField(default='BRA', max_length=12, choices=MARITALSTATUS)
	# state = models.ForeignKey(State,  on_delete=models.SET_NULL, null=True)
	# city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
	
	# communication
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 12 digits allowed.")
	mobile = models.CharField(validators=[phone_regex], max_length=12, null=True) # validators should be a list
	whatsapp = models.CharField(validators=[phone_regex], max_length=12, null=True) # validators should be a list
	

	# #address
	present_address = models.CharField(max_length=250, null=True)
	permanent_address = models.CharField(max_length=250, null=True)

	# #family information
	father_name = models.CharField(max_length=100, null=True)
	father_mobile_no = models.CharField(validators=[phone_regex], max_length=12, null=True) # validators should be a list
	# father_mobile_no = models.CharField(max_length=10,, help_text="Please enter 10 digit phone number")
	mother_name = models.CharField(max_length=100, null=True)
	mother_mobile_no = models.CharField(validators=[phone_regex], max_length=12, null=True) # validators should be a list
	# mother_mobile_no = models.CharField(max_length=10,default = '1234567890', help_text="Please enter 10 digit phone number")
	name_of_brother = models.CharField(max_length=100, null=True)
	age_of_brother = models.IntegerField(null=True)
	name_of_sister = models.CharField(max_length=100, null=True)
	age_of_sister = models.IntegerField(null=True)

	# #Education
	
	# graduation = models.CharField(max_length=10,default='btech', choices = GRADUATION)
	# stream = models.CharField(max_length=50)
	# year_of_passout = models.IntegerField()
	# college = models.CharField(max_length=15,default='iitbhu', choices = COLLEGE)
	


	def __str__(self):
		return f'{self.user.username} Profile'
# Create your models here.

	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)