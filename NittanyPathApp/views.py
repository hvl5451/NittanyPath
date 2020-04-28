from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from collections import defaultdict
from datetime import date

from .forms import PostForm, CommentsForm
from .models import *


# Create your views here.
# TODO: Check if Prof or Student is available first?
@login_required()
def home(request):
    is_TA, TA_course_list = False, []

    # Determine the type of user and get the appropriate user object
    try:
        user = Students.objects.get(pk=request.user.username)
        request.session['isStudent'] = True
    except Students.DoesNotExist:
        user = Professors.objects.get(pk=request.user.username)
        request.session['isStudent'] = False

    # Fill the courses list depending on the type of the user
    courses_list = []
    if request.session['isStudent']:
        courses_list = [(obj.course_id_id, obj.sec_no, obj.course_id.course_name, obj.course_id.course_desc) for obj in
                        user.enrolls_set.all()]
        print(courses_list)

        # Check if the student is a TA
        print("USER-TA-SET: ", user.ta_teaching_teams_set.count())
        if user.ta_teaching_teams_set.count():
            print("HERE")
            print(TA_teaching_teams.objects.get(email=request.user.username))
            is_TA = True
            section_obj = Sections.objects.filter(
                ta_id=TA_teaching_teams.objects.get(email=request.user.username).ta_id).order_by('sec_no')
            print(section_obj.all())
            TA_course_list = [(section.course_id_id, section.sec_no, section.course_id.course_name,
                               section.course_id.course_desc) for section in section_obj]

    else:
        section_obj = [Sections.objects.filter(ta_id=obj.ta_id).order_by('sec_no') for obj in
                       user.profteachingteams_set.all()]
        courses_list = []
        print(section_obj)
        for item in section_obj:
            for section in item:
                courses_list.append((section.course_id_id, section.sec_no, section.course_id.course_name,
                                     section.course_id.course_desc))

    request.session['name'] = user.name
    context = {
        'course_list': courses_list,
        'user_name': user.name,
        'is_TA': is_TA,
        'TA_course_list': TA_course_list,
    }

    return render(request, "courses.html", context)


@login_required()
def course(request, course_id, sec_no):
    # Display the course info
    prof_email = ''
    course_obj = Courses.objects.get(pk=course_id)
    if request.session['isStudent']:
        section_obj = Sections.objects.get(course_id=course_id, sec_no=sec_no)
        print(section_obj.ta_id)
        prof_email = ProfTeachingTeams.objects.get(ta_id=section_obj.ta_id).email_id
    else:
        prof_email = request.user.username

    print(prof_email)
    prof_obj = Professors.objects.get(pk=prof_email)
    context = {
        'course': course_id,
        'sec_no': sec_no,
        'course_name': course_obj.course_name,
        'course_desc': course_obj.course_desc,
        'late_drop': course_obj.late_drop,
        'prof_name': prof_obj.name,
        'prof_email': prof_email,
        'prof_office': prof_obj.office_addr
    }
    return render(request, "course_home.html", context)
    # return HttpResponse(course_id + ';Sec no:' + sec_no)


@login_required()
def account(request):
    context = {}
    if request.session.get('isStudent', False):
        user = Students.objects.get(pk=request.user.username)
        context['Major'] = user.major
        context['Address'] = user.street + user.zipcode.city + ", " + user.zipcode.state + ", " + str(user.zipcode_id)
        context['user_type'] = "Student"
    else:
        user = Professors.objects.get(pk=request.user.username)
        context['Address'] = user.office_addr
        context['Department'] = user.dept_id_id
        context['Title'] = user.title
        context['user_type'] = "Prof"

    context.update({'Name': user.name,
                    'Email': user.email,
                    'Age': user.age,
                    'Gender': user.get_gender_display(),
                    })
    return render(request, "account.html", context)


@login_required()
def announcements(request, course_id, sec_no):
    # Query all the announcement and display it
    announcement_obj = Announcements.objects.filter(course_id=course_id).order_by('id')

    if request.method == "POST":
        announcement_desc = request.POST.get('announcement_desc', "")
        print(announcement_desc)
        if announcement_desc:
            announcement = Announcements(course_id=Courses.objects.get(pk=course_id),
                                         email=get_user(request.user.username), announcement_no=0,
                                         announcement_info=announcement_desc)
            announcement.save()
            announcement.announcement_no = announcement.id
            announcement.save()
            print(announcement)

    context = {
        'announcement_list': [(obj.email.name, obj.announcement_info) for obj in announcement_obj],
        'course': course_id,
        'sec_no': sec_no,
        'isStudent': request.session['isStudent'],
    }

    print(announcement_obj)
    return render(request, "announcement.html", context)

@login_required()
def assignments(request, course_id, sec_no):
    # Handle new assignment_creating by the prof
    if request.method == "POST":
        new_hw_no, new_hw_info = request.POST.get('hw_no', ""), request.POST.get('hw_details', "")
        if new_hw_no and new_hw_info:
            new_hw_obj = Homeworks(course_id=Courses.objects.get(pk=course_id), sec_no=sec_no, hw_no=new_hw_no,
                                   hw_details=new_hw_info)
            new_hw_obj.save()

    # Retrieve all the homeworks
    hw_obj = Homeworks.objects.filter(course_id=course_id, sec_no=sec_no).order_by('hw_no')
    context = {
        'hw_list': [(obj.hw_no, obj.hw_details) for obj in hw_obj],
        'course': course_id,
        'sec_no': sec_no,
        'isStudent': request.session['isStudent'],
    }
    print(context['hw_list'])
    return render(request, "assignments.html", context)


@login_required()
def exams(request, course_id, sec_no):
    # Handle new assignment_creating by the prof
    if request.method == "POST":
        new_exam_no, new_exam_info = request.POST.get('exam_no', ""), request.POST.get('exam_details', "")
        if new_exam_no and new_exam_info:
            new_exam_obj = Exams(course_id=Courses.objects.get(pk=course_id), sec_no=sec_no, exam_no=new_exam_no,
                               exam_details=new_exam_info)
            new_exam_obj.save()

    exam_obj = Exams.objects.filter(course_id=course_id, sec_no=sec_no).order_by('exam_no')
    context = {
        "exam_list": [(obj.exam_no, obj.exam_details) for obj in exam_obj],
        'course': course_id,
        'sec_no': sec_no,
        'isStudent': request.session['isStudent'],
    }
    print(context['exam_list'])
    return render(request, "exams.html", context)


@login_required()
def grades(request, course_id, sec_no):
    if request.session['isStudent']:
        exam_grade_obj = ExamGrades.objects.filter(email=request.user.username, course_id=course_id,
                                                   sec_no=sec_no).order_by('exam_no')
        hw_grade_obj = HomeworkGrades.objects.filter(email=request.user.username, course_id=course_id,
                                                     sec_no=sec_no).order_by('hw_no')
        context = {
            'exam_grades_list': [(obj.exam_no, obj.grades) for obj in exam_grade_obj],
            'hw_grades_list': [(obj.hw_no, obj.grades) for obj in hw_grade_obj],
            'course': course_id,
            'sec_no': sec_no,
            'isStudent': request.session['isStudent']
        }
        print(context['hw_grades_list'], context['exam_grades_list'])
        return render(request, 'grades.html', context)

    # if professor, query the HW and exams
    exam_obj = Exams.objects.filter(course_id=course_id, sec_no=sec_no).order_by('exam_no')
    hw_obj = Homeworks.objects.filter(course_id=course_id, sec_no=sec_no).order_by('hw_no')
    context = {
        "exam_grades_list": [(obj.exam_no, obj.exam_details) for obj in exam_obj],
        'hw_grades_list': [(obj.hw_no, obj.hw_details) for obj in hw_obj],
        'course': course_id,
        'sec_no': sec_no,
        'isStudent': request.session['isStudent'],
    }
    print(context['exam_grades_list'])
    print(context['hw_grades_list'])
    return render(request, 'grades.html', context)


@login_required()
def discussion(request, course_id, sec_no):
    # Query all the discussion post and display it
    post_obj = Posts.objects.filter(course_id=course_id).order_by('id')
    # print(request.POST.get('post_desc'), "")

    if request.method == "POST":
        post_desc = request.POST.get('post_desc', "")
        print(post_desc)
        if post_desc:
            post = Posts(course_id=Courses.objects.get(pk=course_id), email=get_user(request.user.username), post_no=0, post_info=post_desc)
            post.save()
            post.post_no = post.id
            post.save()
            print(post)

    form = PostForm()
    context = {
        'post_list': [(obj.email.name, obj.post_no, obj.post_info, obj.id) for obj in post_obj],
        'course': course_id,
        'sec_no': sec_no,
        'form': form,
    }

    print(post_obj)
    return render(request, "discussion.html", context)


@login_required()
def post(request, course_id, sec_no, post_id):
    if request.method == "POST":
        comment_desc = request.POST.get('comment_desc', "")
        print(comment_desc)
        if comment_desc:
            comment = Comments(course_id=Courses.objects.get(pk=course_id), post_no=post_id,
                               email=get_user(request.user.username), comment_info=comment_desc, comment_no=0)
            comment.save()
            comment.comment_no = comment.id
            post_obj = Posts.objects.get(course_id=course_id, id=post_id)
            if post_obj.post_no == 1:
                comment.post_no = post_obj.post_no
            comment.save()
            print(comment.post_no, post_id)
    post_obj = Posts.objects.get(course_id=course_id, id=post_id)
    print(post_obj.post_no)
    comments_obj = Comments.objects.filter(course_id=course_id, post_no=post_obj.post_no).order_by('id')
    context = {
        'post_user': post_obj.email.name,
        'post_info': post_obj.post_info,
        'comment_list': [(obj.email.name, obj.comment_info) for obj in comments_obj],
        'course': course_id,
        'sec_no': sec_no,
        'post_id': post_id,
    }
    return render(request, "post.html", context)



@login_required()
def grade_assignment(request, course_id, sec_no, type, hw_no):
    student_enrolled = Enrolls.objects.filter(course_id=course_id, sec_no=sec_no).order_by('email')

    # If the request is post, handle it
    if request.method == "POST":
        for student_obj in student_enrolled:
            # Grade not changed
            new_grade = request.POST.get(student_obj.email.name, "")
            if new_grade == "":
                continue

            # Update the student's grade
            if type == "Homework":
                try:
                    new_hw_grade = HomeworkGrades.objects.get(email=student_obj.email,
                                                          course_id=Courses.objects.get(pk=course_id), sec_no=sec_no,
                                                          hw_no=hw_no)
                    new_hw_grade.grades = new_grade
                    new_hw_grade.save()
                except HomeworkGrades.DoesNotExist:
                    new_hw_grade = HomeworkGrades(email=student_obj.email, course_id=Courses.objects.get(pk=course_id),
                                              sec_no=sec_no, hw_no=hw_no, grades=new_grade)
                    new_hw_grade.save()

            else:
                try:
                    new_exam_grade = ExamGrades.objects.get(email=student_obj.email,
                                                          course_id=Courses.objects.get(pk=course_id), sec_no=sec_no,
                                                          exam_no=hw_no)
                    new_exam_grade.grades = new_grade
                    new_exam_grade.save()
                except ExamGrades.DoesNotExist:
                    new_exam_grade = ExamGrades(email=student_obj.email, course_id=Courses.objects.get(pk=course_id),
                                                sec_no=sec_no, exam_no=hw_no, grades=new_grade)
                    new_exam_grade.save()

    # Retrieve all the students and their grades for the hw/exam
    if type == "Homework":
        grade_obj = HomeworkGrades.objects.filter(course_id=course_id, sec_no=sec_no, hw_no=hw_no)
    else:
        grade_obj = ExamGrades.objects.filter(course_id=course_id, sec_no=sec_no, exam_no=hw_no)

    grades = defaultdict(str)
    grades.update({obj.email_id: obj.grades for obj in grade_obj})

    context = {
        'student_grades': [(obj.email.name, grades[obj.email_id]) for obj in student_enrolled],
        'type': type,
        'hw_no': hw_no,
        'course': course_id,
        'sec_no': sec_no,
        'isStudent': request.session['isStudent']
    }
    print(context['student_grades'])

    return render(request, 'gradebook.html', context)


@login_required()
def late_drop(request, course_id, sec_no):
    # Get late_drop date and check if it's valid to late_drop
    late_drop_date = Courses.objects.get(pk=course_id).late_drop
    if date.today() > late_drop_date:
        print("LATE DROP UNSUCCESSFUL")
        return redirect('course', course_id=course_id, sec_no=sec_no)

    # Delete the obj in enroll, hw_grade, exam_grade, post and comment
    user = get_user(request.user.username)
    enroll_obj = Enrolls.objects.get(email=user, course_id=course_id, sec_no=sec_no)
    enroll_obj.delete()

    hw_grade_obj = HomeworkGrades.objects.filter(email=user, course_id=course_id, sec_no=sec_no)
    for items in hw_grade_obj:
        items.delete()

    exam_grade_obj = ExamGrades.objects.filter(email=user, course_id=course_id, sec_no=sec_no)
    for items in exam_grade_obj:
        items.delete()

    post_obj = Posts.objects.filter(email=user, course_id=course_id)
    for items in post_obj:
        items.delete()

    comments_obj = Comments.objects.filter(email=user, course_id=course_id)
    for items in comments_obj:
        items.delete()

    return redirect('login-landing')


def get_user(email):
    try:
        user = Students.objects.get(pk=email)
    except Students.DoesNotExist:
        user = Professors.objects.get(pk=email)

    return user