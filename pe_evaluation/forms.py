from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .models import Student, TrainingPlan, Appointment

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1, message="A idade deve ser maior que zero")]
    )
    height = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0.1, message="A altura deve ser maior que zero")]
    )
    weight = forms.FloatField(
        required=False,
        validators=[MinValueValidator(0.1, message="O peso deve ser maior que zero")]
    )
    goal = forms.ChoiceField(
        choices=[
            ('Condicionamento Físico', 'Condicionamento Físico'),
            ('Emagrecimento', 'Emagrecimento'),
            ('Ganho de Massa Muscular', 'Ganho de Massa Muscular'),
            ('Melhora da Postura', 'Melhora da Postura'),
            ('Preparação para Testes Físicos', 'Preparação para Testes Físicos'),
            ('Melhoria da Resistência Cardiovascular', 'Melhoria da Resistência Cardiovascular'),
        ],
        required=True,
        label="Objetivo"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'height', 'weight', 'goal']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
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
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'date': 'Data',
            'time': 'Hora',
        }