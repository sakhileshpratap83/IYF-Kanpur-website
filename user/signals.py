from django.db.models.signals import post_save#after an object is saved
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_signed_up


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)    


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# #https://stackoverflow.com/questions/14523224/how-to-populate-user-profile-with-django-allauth-provider-information?answertab=votes#tab-top
# @receiver(user_signed_up)
# def create_profile_(request, user, sociallogin=None, **kwargs):
#     if sociallogin:
#         # Extract first / last names from social nets and store on User record
#         if sociallogin.account.provider == 'twitter':
#             name = sociallogin.account.extra_data['name']
#             user.first_name = name.split()[0]
#             user.last_name = name.split()[1]
 
#         if sociallogin.account.provider == 'facebook':
#             user.first_name = sociallogin.account.extra_data['first_name']
#             user.last_name = sociallogin.account.extra_data['last_name']
 
#         if sociallogin.account.provider == 'google':
#             user.profile.user = sociallogin.account.extra_data['given_name']
#             user.last_name = sociallogin.account.extra_data['family_name']
 
#         user.save()

# @receiver(user_signed_up)
# def populate_profile(request, user, sociallogin, **kwargs):
# 	print(user)    
# 	user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
# 	Profile.objects.create(user = user)
#     # user.picture_url = user_data['picture']
#     # user.profile.user = user
# 	user.profile.image = user_data['picture']
#     # user.profile.email_address = email
#     # user.profile.first_name = first_name
# 	user.profile.save() 


# @receiver(social_account_added)
# def create_profile1(request, sociallogin, **kwargs):
#     user1 = sociallogin.account.user
#     Profile.objects.create(user = user1)

# @receiver(social_account_added)
# def save_profile1(request, sociallogin, **kwargs):
#     user1.profile.save()
