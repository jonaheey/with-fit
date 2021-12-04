from django.shortcuts import render

# 메인
def index(request):
    return render(
        request,
        'index.html'
    )

# 운동, 인원수 선택
def select(request):
    # 운동 선택 후
    if request.method == 'POST':
        # 선택된 운동 값
        exercise_name = request.POST.get('selected_e')

        if exercise_name == '푸시업':
            exercise_img = 'push_up'
        elif exercise_name == '사이드 런지':
            exercise_img = 'side_lunge'
        elif exercise_name == '스탠딩 니업':
            exercise_img = 'standing_knee_up'
        else:
            exercise_img = 'step_forward_lunge'
        print(exercise_img)
        
        # 인원 수 선택 화면으로 넘어감
        return render(
            request,
            'people.html',
            {'exercise_name' : exercise_name,
             'exercise_img' : exercise_img}
        )
    # 운동 선택 화면
    return render(
        request,
        'exercise.html'
    )

# 플레이
def play(request):
    # 선택된 운동
    exercise_name = request.POST.get('exercise')
    print(exercise_name)
    # 선택된 인원수
    num_people = request.POST.get('selected_p')
    print(num_people)
    # 플레이 화면
    return render(
        request,
        'play.html',
        {'num_people' : num_people}
    )