from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .models import Student, TrainingPlan, WeightHistory, Appointment
from .forms import StudentRegistrationForm, TrainingPlanForm, AppointmentForm, LoginForm

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Student.objects.create(
                user=user,
                age=form.cleaned_data.get('age'),
                height=form.cleaned_data.get('height'),
                weight=form.cleaned_data.get('weight'),
                goal=form.cleaned_data.get('goal')
            )
            
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def student_dashboard(request):
    student = request.user.student
    weight_history = student.weight_history.order_by('date_recorded')

    # Calcular a evolução do peso
    if weight_history.exists():
        initial_weight = weight_history.first().weight
        current_weight = weight_history.last().weight
        weight_change = current_weight - initial_weight
        percentage_change = (weight_change / initial_weight) * 100
        weight_trend = f"{'↑' if weight_change > 0 else '↓'} {abs(weight_change):.1f} kg desde o início"
    else:
        initial_weight = current_weight = percentage_change = weight_trend = None

    # Calcular o IMC
    height = student.height
    if height and current_weight:
        bmi = current_weight / (height ** 2)
        if bmi < 18.5:
            bmi_category = "Abaixo do peso"
        elif 18.5 <= bmi < 24.9:
            bmi_category = "Peso normal"
        elif 25 <= bmi < 29.9:
            bmi_category = "Sobrepeso"
        else:
            bmi_category = "Obesidade"
    else:
        bmi = bmi_category = None

    context = {
        'student': student,
        'current_weight': current_weight,
        'initial_weight': initial_weight,
        'percentage_change': percentage_change,
        'weight_trend': weight_trend,
        'bmi': bmi,
        'bmi_category': bmi_category,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def student_training_plans(request):
    student = request.user.student
    training_plans = TrainingPlan.objects.filter(student=student)
    return render(request, 'student_training_plans.html', {'training_plans': training_plans})

@login_required
def student_update(request):
    student = request.user.student
    if request.method == 'POST':
        # Capturar os dados do formulário
        new_weight = float(request.POST.get('new_weight'))
        age = request.POST.get('age')
        height = request.POST.get('height')
        goal = request.POST.get('goal')

        # Salvar o novo peso no histórico
        WeightHistory.objects.create(student=student, weight=new_weight)

        # Atualizar as informações do aluno
        student.age = age
        student.height = height
        student.weight = new_weight
        student.goal = goal
        student.save()

        # Calcular o desempenho de peso
        weight_history = student.weight_history.order_by('date_recorded')
        if weight_history.exists():
            initial_weight = weight_history.first().weight
            weight_change = new_weight - initial_weight
            percentage_change = (weight_change / initial_weight) * 100
            message = f"Seu peso mudou em {percentage_change:.2f}% desde o início."
        else:
            message = "Este é o seu primeiro registro de peso."

        return render(request, 'student_update.html', {'student': student, 'message': message})
    
    return render(request, 'student_update.html', {'student': student})

def is_teacher(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
@user_passes_test(is_teacher)
def teacher_students(request):
    students = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'teacher_students.html', {'students': students})

@login_required
@user_passes_test(is_teacher)
def teacher_appointments(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'teacher_appointments.html', {'appointments': appointments})

@login_required
@user_passes_test(is_teacher)
def assign_training_plan(request, user_id):
    user = get_object_or_404(User, id=user_id)
    student, created = Student.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.student = student
            plan.save()
            messages.success(request, 'Plano de treino atribuído com sucesso!')
            return redirect('teacher_dashboard')
    else:
        form = TrainingPlanForm()
    
    return render(request, 'assign_training_plan.html', {'form': form, 'student': student})

def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')

@login_required
def schedule_appointment(request):
    student = request.user.student
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = student
            appointment.save()
            return redirect('student_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'schedule_appointment.html', {'form': form})