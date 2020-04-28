
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# TODO: Change email to student_email and prof_email
# TODOL Is blank required?
class Students(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Non-Binary'),
    )
    email = models.EmailField(primary_key=True)
    # email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # password = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=3, choices=GENDER, null=True, blank=True)
    major = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    zipcode = models.ForeignKey('Zipcodes', on_delete=models.DO_NOTHING)


class Zipcodes(models.Model):
    zipcode = models.PositiveSmallIntegerField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


class Professors(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Non-Binary'),
    )
    email = models.EmailField(primary_key=True)
    # email = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # password = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=3, choices=GENDER, null=True, blank=True)
    office_addr = models.CharField("office_address", max_length=60)
    dept_id = models.ForeignKey("Departments", on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=60)


class Departments(models.Model):
    dept_id = models.CharField(max_length=8, primary_key=True)
    dept_name = models.CharField(max_length=50)
    email = models.ForeignKey(Professors, on_delete=models.DO_NOTHING, null=True, blank=True)


# TODO: Change late_drop to Date field
class Courses(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=80)
    course_desc = models.CharField("course_description", max_length=200)
    late_drop = models.DateField(max_length=30)


class Sections(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    limit = models.PositiveSmallIntegerField()
    ta_id = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (("course_id", "sec_no"),)  # Unique together might be deprecated


class Enrolls(models.Model):
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField(null=True)

    class Meta:
        unique_together = (("email", "course_id", "sec_no"),)


class ProfTeachingTeams(models.Model):
    email = models.ForeignKey(Professors, on_delete=models.CASCADE)
    ta_id = models.PositiveSmallIntegerField()


class TA_teaching_teams(models.Model):
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    ta_id = models.PositiveSmallIntegerField()


class Homeworks(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    hw_no = models.PositiveSmallIntegerField()
    hw_details = models.CharField(max_length=200)

    class Meta:
        unique_together = (("course_id", "sec_no", "hw_no"),)


class HomeworkGrades(models.Model):
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    hw_no = models.PositiveSmallIntegerField()
    grades = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (("email", "course_id", "sec_no", "hw_no"),)


class Exams(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    exam_no = models.PositiveSmallIntegerField()
    exam_details = models.CharField(max_length=100)

    class Meta:
        unique_together = (("course_id", "sec_no", "exam_no"),)


# TODO: Check why unique_together is not working
class ExamGrades(models.Model):
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    sec_no = models.PositiveSmallIntegerField()
    exam_no = models.PositiveSmallIntegerField()
    grades = models.PositiveSmallIntegerField()

    # class Meta:
    #     unique_together = (("email", "course_id", "sec_no", "exam_no"),)


class Posts(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    post_no = models.PositiveSmallIntegerField()
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    post_info = models.CharField(max_length=500)

    class Meta:
        unique_together = (("email", "course_id", "post_no"),)


# TODO: unique_together?
class Comments(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    post_no = models.PositiveSmallIntegerField()
    comment_no = models.PositiveSmallIntegerField()
    email = models.ForeignKey(Students, on_delete=models.CASCADE)
    comment_info = models.CharField(max_length=500)


class Announcements(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    announcement_no = models.PositiveSmallIntegerField()
    email = models.ForeignKey(Professors, on_delete=models.CASCADE)
    announcement_info = models.CharField(max_length=500)

    class Meta:
        unique_together = (("email", "course_id", "announcement_no"),)