import csv
from django.conf import settings
from cmpsc431w import settings as app_settings

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES)

import django

django.setup()

from django.db.models import ForeignKey, ManyToOneRel
from django.contrib.auth.models import User
from NittanyPathApp.models import *


def load_data(model_to_load, csv_file_path):
    with open(csv_file_path) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            arg_dict = {}

            for field in model_to_load._meta.get_fields(include_parents=False):
                print(field)
                if isinstance(field, ManyToOneRel):
                    continue

                field_name = field.name
                fk_object = model_to_load._meta.get_field(field_name)

                if isinstance(fk_object, ForeignKey):
                    # print(field, field_name, fk_object.related_model._meta.get_fields(include_parents=False))
                    print(row)
                    # print(fk_object.related_model.objects.get({'course_id_id':row[field_name]}))
                    arg_dict[field_name] = fk_object.related_model.objects.get(**{field_name: row[field_name]})

                    # try:
                    #     arg_dict[field_name] = fk_object.related_model.objects.get(**{field_name: row[field_name]})
                    # except:
                    #     pass

                    # if field_name == "email":
                    #     arg_dict[field_name] = fk_object.related_model.objects.get(**{"username": row[field_name]})
                    #
                    # else:
                    #     arg_dict[field_name] = fk_object.related_model.objects.get(**{field_name: row[field_name]})

                else:
                    if field_name != 'id':
                        arg_dict[field_name] = row[field_name]

            # print(json.dumps(arg_dict, indent=4, sort_keys=True))
            model_to_load.objects.get_or_create(**arg_dict)


def create_user(csv_path):
    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            user = User.objects.create_user(**row)
            user.save()


if __name__ == "__main__":
    path = "/Users/semideum_zepodesgan01/PycharmProjects/cmpsc431w/NittanyPathApp/Data/"
    # load_data(Zipcodes, path + "Zipcodes.csv")
    # load_data(Students, path + "Students.csv")
    # load_data(Professors, path + "Professors.csv")
    # load_data(Departments, path + "Departments.csv")
    # load_data(Courses, path + "Courses.csv")
    # load_data(Sections, path + "sections.csv")
    # load_data(Enrolls, path + "Enrolls.csv")
    # load_data(TA_teaching_teams, path + "TA_teaching_teams.csv")
    # load_data(ProfTeachingTeams, path + "Prof_teaching_teams.csv")
    # load_data(Homeworks, path + "Homeworks.csv")
    # load_data(HomeworkGrades, path + "HomeworkGrades.csv")
    # load_data(Exams, path + "Exams.csv")
    # load_data(ExamGrades, path + "ExamGrades.csv")
    # load_data(Posts, path + "posts.csv")
    load_data(Comments, path + "comments.csv")

    # Create User
    # create_user(path + "User.csv")
