from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from .models import (
    Student, 
    TrainingPlan, 
    WeightHistory, 
    Availability, 
    Appointment, 
    PredefinedTraining,
    ExerciseStatus
)
from .forms import StudentRegistrationForm, TrainingPlanForm, LoginForm
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.urls import reverse

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
            
            student = Student.objects.create(
                user=user,
                age=form.cleaned_data.get('age'),
                height=form.cleaned_data.get('height'),
                weight=form.cleaned_data.get('weight'),
                goal=form.cleaned_data.get('goal')
            )
            
            if form.cleaned_data.get('weight'):
                WeightHistory.objects.create(
                    student=student,
                    weight=form.cleaned_data.get('weight')
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

    current_weight = student.weight
    
    if weight_history.exists():
        initial_weight = weight_history.first().weight
        weight_change = current_weight - initial_weight
        percentage_change = (weight_change / initial_weight) * 100
        weight_trend = f"{'↑' if weight_change > 0 else '↓'} {abs(weight_change):.1f} kg desde o início"
    else:
        initial_weight = current_weight
        percentage_change = 0
        weight_trend = "Peso inicial"

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
        bmi = None
        bmi_category = "Dados insuficientes"

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
    
    for plan in training_plans:
        exercises = [ex.strip() for ex in plan.plan_details.split(',') if ex.strip()]
        
        for exercise in exercises:
            ExerciseStatus.objects.get_or_create(
                training_plan=plan,
                exercise_description=exercise,
                defaults={'status': 'pending'}
            )
    
    return render(request, 'student_training_plans.html', {'training_plans': training_plans})

@login_required
def update_exercise_status(request):
    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        new_status = request.POST.get('status')

        if not exercise_id or not new_status:
            return JsonResponse({
                'status': 'error',
                'message': 'Dados inválidos fornecidos.'
            }, status=400)

        valid_statuses = ['pending', 'completed']
        if new_status not in valid_statuses:
            return JsonResponse({
                'status': 'error',
                'message': f'Status "{new_status}" não é válido.'
            }, status=400)

        try:
            exercise = ExerciseStatus.objects.select_related('training_plan__student').get(id=exercise_id)
            
            if exercise.training_plan.student != request.user.student:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Acesso não autorizado.'
                }, status=403)

            exercise.status = new_status
            exercise.save()

            total_exercises = exercise.training_plan.exercise_statuses.count()
            completed_exercises = exercise.training_plan.exercise_statuses.filter(status='completed').count()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Status atualizado com sucesso!',
                'statistics': {
                    'total': total_exercises,
                    'completed': completed_exercises,
                    'pending': total_exercises - completed_exercises
                }
            })

        except ExerciseStatus.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Exercício não encontrado.'
            }, status=404)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro inesperado: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Método inválido. Apenas POST é permitido.'
    }, status=405)


@login_required
def student_update(request):
    student = request.user.student
    if request.method == 'POST':
        new_weight = float(request.POST.get('new_weight'))
        age = request.POST.get('age')
        height = request.POST.get('height')
        goal = request.POST.get('goal')

        WeightHistory.objects.create(student=student, weight=new_weight)

        student.age = age
        student.height = height
        student.weight = new_weight
        student.goal = goal
        student.save()

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
        profile = request.POST.get('profile')
        level = request.POST.get('level')
        goal = request.POST.get('goal')

        training = get_object_or_404(PredefinedTraining, profile=profile, level=level, goal=goal)
        student.training_plans.create(plan_details=training.description)
        messages.success(request, 'Plano de treino atribuído com sucesso!')
        return redirect('teacher_dashboard')

    profiles = PredefinedTraining.PROFILE_CHOICES
    levels = PredefinedTraining.LEVEL_CHOICES
    goals = PredefinedTraining.objects.values_list('goal', flat=True).distinct()

    return render(request, 'assign_training_plan.html', {
        'student': student,
        'profiles': profiles,
        'levels': levels,
        'goals': goals,
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')

@login_required
@require_http_methods(["GET", "POST"])
def schedule_appointment(request):
    # Verificação adicional de AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    current_datetime = timezone.now()
    
    available_slots = Availability.objects.filter(
        is_booked=False,
        date__gte=current_datetime.date()
    ).order_by('date', 'time')
    
    if available_slots.filter(date=current_datetime.date()).exists():
        available_slots = available_slots.exclude(
            date=current_datetime.date(),
            time__lte=current_datetime.time()
        )
    
    if request.method == 'POST':
        if not is_ajax:
            return HttpResponseBadRequest(json.dumps({
                'status': 'error', 
                'message': 'Requisição inválida'
            }), content_type='application/json')
        
        slot_id = request.POST.get('slot_id')
        
        try:
            slot = Availability.objects.get(id=slot_id, is_booked=False)
            
            slot_datetime = timezone.make_aware(
                datetime.combine(slot.date, slot.time),
                timezone.get_current_timezone()
            )
            
            if slot_datetime <= timezone.now():
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Este horário não está mais disponível. Por favor, escolha outro horário.'
                }, status=400)
            
            if Appointment.objects.filter(
                student=request.user.student,
                date=slot.date,
                time=slot.time
            ).exists():
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Você já possui uma consulta agendada para este horário.'
                }, status=400)
            
            slot.is_booked = True
            slot.save()
            
            Appointment.objects.create(
                student=request.user.student,
                date=slot.date,
                time=slot.time
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': f'Consulta agendada com sucesso!',
                'redirect_url': reverse('student_dashboard')
            })
            
        except Availability.DoesNotExist:
            return JsonResponse({
                'status': 'error', 
                'message': 'O horário selecionado não está mais disponível. Por favor, escolha outro horário.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': 'Ocorreu um erro ao agendar a consulta. Por favor, tente novamente.'
            }, status=500)
    
    if is_ajax:
        return JsonResponse({
            'status': 'success',
            'available_slots': list(available_slots.values('id', 'date', 'time'))
        })
    
    return render(request, 'schedule_appointment.html', {
        'available_slots': available_slots
    })

@login_required
def cancel_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(
            id=appointment_id,
            student=request.user.student
        )
        
        availability = Availability.objects.get(
            date=appointment.date,
            time=appointment.time,
            is_booked=True
        )
        
        availability.is_booked = False
        availability.save()
        
        # Remove o agendamento
        appointment.delete()
        
        messages.success(request, 'Agendamento cancelado com sucesso.')
        return redirect('student_dashboard')
        
    except Appointment.DoesNotExist:
        messages.error(request, 'Agendamento não encontrado.')
        return redirect('student_dashboard')
    except Availability.DoesNotExist:
        Availability.objects.create(
            date=appointment.date,
            time=appointment.time,
            is_booked=False
        )
        appointment.delete()
        messages.success(request, 'Agendamento cancelado com sucesso.')
        return redirect('student_dashboard')
    except Exception as e:
        messages.error(request, 'Ocorreu um erro ao cancelar o agendamento.')
        return redirect('student_dashboard')

@login_required
@user_passes_test(is_teacher)
def delete_training_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, 'Plano de treino excluído com sucesso!')
        return redirect('teacher_dashboard')
    return render(request, 'confirm_delete_training.html', {'plan': plan, 'type': 'treino'})

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, student=request.user.student)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
        return redirect('student_dashboard')
    return render(request, 'confirm_delete_appointment.html', {'object': appointment, 'type': 'agendamento'})

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Sua conta foi excluída com sucesso!')
        return redirect('home')
    return render(request, 'confirm_delete_account.html', {'object': user, 'type': 'conta'})

@login_required
@user_passes_test(is_teacher)
def define_availability(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time, '%H:%M').time()
            
            slot_datetime = timezone.make_aware(
                datetime.combine(date_obj, time_obj),
                timezone.get_current_timezone()
            )
            
            if slot_datetime <= timezone.now():
                messages.error(request, 'Não é possível adicionar disponibilidade para uma data/hora que já passou.')
                return redirect('define_availability')
            
            if Availability.objects.filter(
                teacher=request.user,
                date=date_obj,
                time=time_obj
            ).exists():
                messages.error(request, 'Você já definiu disponibilidade para esta data e horário.')
                return redirect('define_availability')
            
            Availability.objects.create(
                teacher=request.user,
                date=date_obj,
                time=time_obj
            )
            messages.success(request, 'Disponibilidade adicionada com sucesso!')
            
        except ValueError:
            messages.error(request, 'Data ou hora em formato inválido.')
        
        return redirect('define_availability')
    
    current_datetime = timezone.now()
    availabilities = Availability.objects.filter(
        teacher=request.user,
        date__gte=current_datetime.date()
    ).order_by('date', 'time')
    
    if availabilities.filter(date=current_datetime.date()).exists():
        availabilities = availabilities.exclude(
            date=current_datetime.date(),
            time__lte=current_datetime.time()
        )
    
    return render(request, 'define_availability.html', {
        'availabilities': availabilities,
        'now': timezone.now()
    })

@login_required
@user_passes_test(is_teacher)
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id, teacher=request.user)
    if request.method == 'POST':
        if availability.is_booked:
            Appointment.objects.filter(date=availability.date, time=availability.time).delete()
        availability.delete()
        messages.success(request, 'Disponibilidade cancelada com sucesso!')
        return redirect('define_availability')
    return render(request, 'confirm_delete_availability.html', {'availability': availability})


@login_required
@user_passes_test(is_teacher)
def teacher_training_progress(request, student_id):
    student = get_object_or_404(User, id=student_id)
    training_plans = TrainingPlan.objects.filter(student=student.student).order_by('-created_at')

    for plan in training_plans:
        total_exercises = plan.exercise_statuses.count()
        completed_exercises = plan.exercise_statuses.filter(status='completed').count()
        plan.completion_percentage = int((completed_exercises / total_exercises * 100) if total_exercises > 0 else 0)

    return render(request, 'teacher_training_progress.html', {
        'student': student,
        'training_plans': training_plans
    })