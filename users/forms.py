from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    # # user가 존재하지 않으면 error raise
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")
    # def clean_password(self):
    #     email = self.cleaned_data("email")

    #     return
    # 한개의 메서드로 에러가 정확한 위치에서 나타날 수 있게 작성
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()


# class SignupForm(forms.Form):

#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             # 이미있으면
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("User already exists with that email")
#         except models.User.DoesNotExist:
#             return email

#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")
#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#         user = models.User.objects.create_user(email, email, password)
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()


# class SignUpForm(UserCreationForm):
#     UserModel = get_user_model()

#     username = forms.EmailField(label="Email")

#     class Meta(UserCreationForm.Meta):
#         model = UserModel
#         fields = ("email",)