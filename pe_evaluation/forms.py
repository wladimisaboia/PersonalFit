from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .models import Student, TrainingPlan, Appointment
from django.utils import timezone

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput())

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")
    age = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1, message="A idade deve ser maior que zero")],
        label="Idade"
    )
    height = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0.1, message="A altura deve ser maior que zero")],
        label="Altura (m)"
    )
    weight = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0.1, message="O peso deve ser maior que zero")],
        label="Peso (kg)"
    )
    goal = forms.ChoiceField(
        choices=[
            ('Condicionamento Físico', 'Condicionamento Físico'),
            ('Emagrecimento', 'Emagrecimento'),
            ('Ganho de Massa Muscular', 'Ganho de Massa Muscular'),
        ],
        required=True,
        label="Objetivo"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'height', 'weight', 'goal']
        labels = {
            'username': 'Usuário',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação de senha'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['plan_details']
        widgets = {
            'plan_details': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'plan_details': 'Detalhes do Plano de Treino'
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'date': 'Data',
            'time': 'Hora',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%d/%m/%Y']