from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models import UserPreference, Activity, UserProfile
from .forms import UserPreferenceForm


def index(request):
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if profile.last_page:
            return redirect(profile.last_page)
        return redirect('welcome')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'planner/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('welcome')
            else:
                return render(request, 'planner/login.html', {'error_message': 'Your account is disabled.'})
        else:
            return render(request, 'planner/login.html', {'error_message': 'Invalid login details supplied.'})
    else:
        return render(request, 'planner/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def welcome(request):
    return render(request, 'planner/welcome.html', {'username': request.user.username})


@login_required
def user_preferences(request):
    UserProfile.objects.get_or_create(user=request.user)[0].__class__.objects.filter(user=request.user).update(last_page='preferences')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if request.method == 'POST':
        UserPreference.objects.filter(user=request.user).delete()
        for day in days:
            start = request.POST.get(f'start_{day}')
            end = request.POST.get(f'end_{day}')
            if start and end:
                UserPreference.objects.create(user=request.user, day_of_week=day, start_time=start, end_time=end)
        return redirect('activities')
    existing = {p.day_of_week: {'start': p.start_time.strftime('%H:%M'), 'end': p.end_time.strftime('%H:%M')} for p in UserPreference.objects.filter(user=request.user)}
    return render(request, 'planner/user_preferences.html', {'days': days, 'existing': existing})


@login_required
def activity_selection(request):
    UserProfile.objects.get_or_create(user=request.user)[0].__class__.objects.filter(user=request.user).update(last_page='activities')
    available_activities = [
        {'name': 'Studying'}, {'name': 'Workout'}, {'name': 'Reading'}, {'name': 'Meditation'},
        {'name': 'Coding'}, {'name': 'Walk'}, {'name': 'Cooking'}, {'name': 'Cleaning'},
        {'name': 'Jogging'}, {'name': 'Watching Movie'}, {'name': 'Prayer Time/Word Study'},
        {'name': 'Shopping'}, {'name': 'Working on Project'}, {'name': 'Gaming'}, {'name': 'Studying/Doing Homework'},
        {'name': 'Community Activities'}, {'name': 'Journaling'}, {'name': 'Writing'}, {'name': 'Listening to Music/Podcasts'}
    ]
    if request.method == 'POST':
        selected_names = request.POST.getlist('activities')
        if len(selected_names) > 10:
            return render(
                request,
                'planner/activity_selection.html',
                {'activities': available_activities, 'error_message': 'Please select up to ten activities only.'}
            )
        for name in selected_names:
            Activity.objects.get_or_create(user=request.user, name=name, defaults={'selected': True})
        return redirect('timetable')
    selected = set(Activity.objects.filter(user=request.user).values_list('name', flat=True))
    return render(request, 'planner/activity_selection.html', {'activities': available_activities, 'selected': selected})


@login_required
def final_timetable(request):
    UserProfile.objects.get_or_create(user=request.user)[0].__class__.objects.filter(user=request.user).update(last_page='timetable')
    import json
    preferences = UserPreference.objects.filter(user=request.user)
    activities = list(Activity.objects.filter(user=request.user).values_list('name', flat=True))
    activities_json = mark_safe(json.dumps(activities))
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    saved = profile.timetable_data or {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_json = mark_safe(json.dumps(days))
    return render(
        request,
        'planner/final_timetable.html',
        {'preferences': preferences, 'activities_json': activities_json, 'saved': saved, 'days': days, 'days_json': days_json}
    )


@login_required
def save_progress(request):
    if request.method == 'POST':
        import json
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        try:
            body = json.loads(request.body.decode('utf-8'))
        except Exception:
            return HttpResponse('Invalid JSON', status=400)
        profile.timetable_data = body
        profile.save()
        return HttpResponse('OK')
    return HttpResponse('Method Not Allowed', status=405)


@login_required
def export_ics(request):
    import datetime
    from uuid import uuid4

    preferences = UserPreference.objects.filter(user=request.user)
    activities = list(Activity.objects.filter(user=request.user).values_list('name', flat=True))
    if not activities:
        activities = ["Activity"]

    now = datetime.date.today()
    weeks = request.GET.get('weeks')
    try:
        weeks = int(weeks) if weeks is not None else 12
    except Exception:
        weeks = 12
    if weeks < 1:
        weeks = 1
    if weeks > 52:
        weeks = 52
    day_to_weekday = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }

    def next_weekday(base_date, target_weekday):
        days_ahead = target_weekday - base_date.weekday()
        if days_ahead < 0:
            days_ahead += 7
        return base_date + datetime.timedelta(days=days_ahead)

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Daily Planner//EN',
    ]

    for pref in preferences:
        weekday = day_to_weekday.get(pref.day_of_week)
        if weekday is None:
            continue
        first_date = next_weekday(now, weekday)
        for w in range(weeks):
            event_date = first_date + datetime.timedelta(days=7 * w)
            start_dt = datetime.datetime.combine(event_date, pref.start_time)
            end_dt = datetime.datetime.combine(event_date, pref.end_time)
            duration = (end_dt - start_dt)
            if duration.total_seconds() <= 0:
                continue
            slot_minutes = 60
            total_slots = int(duration.total_seconds() // (slot_minutes * 60))
            slot_starts = [start_dt + datetime.timedelta(minutes=slot_minutes * i) for i in range(total_slots)]
            activity_pool = []
            for a in activities:
                activity_pool.append(a)
                activity_pool.append(a)
            idx = 0
            for slot_start in slot_starts:
                if idx >= len(activity_pool):
                    break
                slot_end = slot_start + datetime.timedelta(minutes=slot_minutes)
                summary = activity_pool[idx]
                idx += 1
                uid = str(uuid4())
                lines.extend([
                    'BEGIN:VEVENT',
                    f'UID:{uid}',
                    f'DTSTAMP:{datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}',
                    f'DTSTART:{slot_start.strftime("%Y%m%dT%H%M%S")}',
                    f'DTEND:{slot_end.strftime("%Y%m%dT%H%M%S")}',
                    f'SUMMARY:{summary}',
                    'END:VEVENT',
                ])

    lines.append('END:VCALENDAR')
    ics_content = '\r\n'.join(lines)
    response = HttpResponse(ics_content, content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="timetable.ics"'
    return response
