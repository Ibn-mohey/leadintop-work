from django.contrib.auth.forms import UserCreationForm, UserChangeForm  
from django.db.models import fields  
from django import forms  
from .models import CustomUser  
from django.contrib.auth import get_user_model  
from django.contrib.auth.password_validation import validate_password
User = get_user_model()  
  
class UserRegisterForm(UserCreationForm):  
    fields  = ['email','name','is_staff']
    password1 = forms.CharField(widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    # name = forms.CharField()
  
    class Meta:  
        model = CustomUser  
        fields = ('email','name','is_staff')  
      
    def clean_email(self):  
        email = self.cleaned_data.get('email')  
        qs = User.objects.filter(email=email)  
        if qs.exists():  
            raise forms.ValidationError("Email is taken")  
        return email  
  
    def clean(self):  
        '''  
        Verify both passwords match.  
        '''  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password1', error)
            
        password2 = cleaned_data.get("password2") 
          
        if password1 is not None and password1 != password2:  
            self.add_error("password2", "Your passwords must match")  
        return cleaned_data  
  
    def save(self, commit=True):  
        # Save the provided password in hashed format  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])
        # if user.type == 'moderator':
        #     print('here')
        #     # user.type == 'moderator'
        # staff = 
        if commit:  
            user.save()  
        return user          
      
  
  
# class UserChangeForm(UserChangeForm):  
#     # fields  = ['email','name','is_staff']
#     # password1 = forms.CharField(widget=forms.PasswordInput)  
#     # password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#     # name = forms.CharField()
  
#     class Meta:  
#         model = CustomUser  
#         fields = ('email','name','is_staff')  
      

#     def clean(self):  
#         '''  
#         Verify both passwords match.  
#         '''  
#         cleaned_data = super().clean()  
#         password1 = cleaned_data.get("password1")
#         try:
#             validate_password(password1, self.instance)
#         except forms.ValidationError as error:

#             # Method inherited from BaseForm
#             self.add_error('password1', error)
            
#         password2 = cleaned_data.get("password2") 
          
#         if password1 is not None and password1 != password2:  
#             self.add_error("password2", "Your passwords must match")  
#         return cleaned_data  
  
#     def save(self, commit=True):  
#         # Save the provided password in hashed format  
#         user = super().save(commit=False)  
#         user.set_password(self.cleaned_data["password1"])
#         # if user.type == 'moderator':
#         #     print('here')
#         #     # user.type == 'moderator'
#         # staff = 
#         if commit:  
#             user.save()  
#         return user          
# class UserChangeForm2(UserChangeForm):  
#     class Meta:  
#         model = CustomUser  
#         fields = ('email', 'name','is_staff')  
  
#     def clean_password(self):  
#         # Regardless of what the user provides, return the initial value.  
#         # This is done here, rather than on the field, because the  
#         # field does not have access to the initial value  
#         return self.initial["password1"]  