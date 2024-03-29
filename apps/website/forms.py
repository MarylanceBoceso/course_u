from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Email Address'}),max_length=100, required=True)
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'First Name'}),max_length=100, required=True)
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Last Name'}),max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["username"].widget.attrs['placeholder'] = 'Username'
        self.fields["username"].label = ""
        self.fields["username"].help_text = ""

        self.fields["password1"].widget.attrs['class'] = 'form-control'
        self.fields["password1"].widget.attrs['placeholder'] = 'Password'
        self.fields["password1"].label = ""
        self.fields["password1"].help_text = ""

        self.fields["password2"].widget.attrs['class'] = 'form-control'
        self.fields["password2"].widget.attrs['placeholder'] = 'Re-Password'
        self.fields["password2"].label = ""
        self.fields["password2"].help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)

        # Check the email of the user
        if '@admin' in user.email:
            user.is_superuser = True
            user.is_staff = True
        elif '@instructor' in user.email:
            user.is_staff = True

        if commit:
            user.save()

        return user


class StudentScoreForm(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Username'}),max_length=100, required=True)
    max_score = forms.IntegerField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Max Score'}),required=True)
    min_score = forms.IntegerField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Min Score'}),required=True)

    class Meta:
        model = User
        fields = ('username', 'max_score', 'min_score')
    
    def __init__(self, *args, **kwargs):
        super(StudentScoreForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs['class'] = 'form-control'
        self.fields["username"].widget.attrs['placeholder'] = 'Username'
        self.fields["username"].label = ""

        self.fields["max_score"].widget.attrs['class'] = 'form-control'
        self.fields["max_score"].widget.attrs['placeholder'] = 'Max Score'
        self.fields["max_score"].label = ""

        self.fields["min_score"].widget.attrs['class'] = 'form-control'
        self.fields["min_score"].widget.attrs['placeholder'] = 'Min Score'
        self.fields["min_score"].label = ""