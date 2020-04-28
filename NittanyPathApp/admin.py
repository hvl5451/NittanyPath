from django.contrib import admin

# Register your models here.
from . import models

# Register your models here.
admin.site.register(models.Students)
admin.site.register(models.Zipcodes)
admin.site.register(models.Professors)
admin.site.register(models.Departments)
admin.site.register(models.Courses)
admin.site.register(models.Sections)
admin.site.register(models.Enrolls)
admin.site.register(models.ProfTeachingTeams)
admin.site.register(models.TA_teaching_teams)
admin.site.register(models.Homeworks)
admin.site.register(models.HomeworkGrades)
admin.site.register(models.Exams)
admin.site.register(models.ExamGrades)
admin.site.register(models.Posts)
admin.site.register(models.Comments)
