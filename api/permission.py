from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission


def group_user(user):
    role = user.roles.get().__str__()
    permissions = Permission.objects.all()
    for p in permissions:
        print(p)
        user.user_permissions.remove(p)
    user.save(update_fields=['user_permission'])
    # if role == "admin":
    #     permissions = Permission.objects.all()
    #     for p in permissions:
    #         user.user_permissions.add(p)
    #
    # elif role == "student":
    #     user.user_permissions.add(Permission.objects.filter(name="Can see Homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view building").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view college").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view building").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view course").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view department").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view message").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view video").first())
    #     print(user.get_all_permissions())
    # elif role == "staff":
    #     user.user_permissions.add(Permission.objects.filter(name="Can add course").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete course").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change course").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view course").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change field").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view field").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add field").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add message").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view message").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view video").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add video").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change video").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete video").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add session").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view session").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change session").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete session").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add session").first())
    # elif role== "professor":
    #     user.user_permissions.add(Permission.objects.filter(name="Can add document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete homework").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can add message").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view message").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can delete document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can change document").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view section").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view solution").first())
    #     user.user_permissions.add(Permission.objects.filter(name="Can view video").first())
    # else:
    #     pass
    # # user.save()




# class permission_enroll(Permission):
#     permission = Permission.objects.create(codename='enroll',
#                                            name='enroll to the course')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_enroll(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.enroll'):
#             return True
#         else:
#             return False
#
#
# class has_permission_seeHomework(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.seeHomework'):
#             return True
#         else:
#             return False
#
#
# class permission_uploadHomework(Permission):
#     permission = Permission.objects.create(codename='uploadHomework',
#                                            name='upload Homework')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_uploadHomework(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.uploadHomework'):
#             return True
#         else:
#             return False
#
#
# class permission_uploadSolution(Permission):
#     permission = Permission.objects.create(codename='uploadSolution',
#                                            name='upload Solution')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_uploadSolution(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.uploadSolution'):
#             return True
#         else:
#             return False
#
#
# class permission_addCourse(Permission):
#     permission = Permission.objects.create(codename='addCourse',
#                                            name='add Course')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addCourse(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addCourse'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteHomework(Permission):
#     permission = Permission.objects.create(codename='deleteHomework',
#                                            name='see Homework')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteHomework(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteHomework'):
#             return True
#         else:
#             return False
#
#
# class permission_seeDoc(Permission):
#     permission = Permission.objects.create(codename='seeDoc',
#                                            name='see Doc')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_seeDoc(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.seeDoc'):
#             return True
#         else:
#             return False
#
#
# class permission_uploadDoc(Permission):
#     permission = Permission.objects.create(coedename='uploadDoC',
#                                            name='upload Doc')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_uploadDoc(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.uploadDoC'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteDoc(Permission):
#     permission = Permission.objects.create(coedename='deleteDoC',
#                                            name='delete Doc')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteDoc(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteDoC'):
#             return True
#         else:
#             return False
#
#
# class permission_changeDoc(Permission):
#     permission = Permission.objects.create(coedename='changeDoC',
#                                            name='change Doc')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeDoc(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeDoC'):
#             return True
#         else:
#             return False
#
#
# class permission_seeSolution(Permission):
#     permission = Permission.objects.create(codename='seeSolution',
#                                            name='see Solution')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_seeSolution(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.seeSolution'):
#             return True
#         else:
#             return False
#
#
# class permission_sendMessage(Permission):
#     permission = Permission.objects.create(codename='sendMessage',
#                                            name='send Massage')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_sendMessage(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.sendMessage'):
#             return True
#         else:
#             return False
#
#
# class permission_changeDep(Permission):
#     permission = Permission.objects.create(codename='changeDep',
#                                            name='change Department')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeDep(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeDep'):
#             return True
#         else:
#             return False
#
#
# class permission_addDep(Permission):
#     permission = Permission.objects.create(codename='addDep',
#                                            name='add Department')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addDep(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addDep'):
#             return True
#         else:
#             return False
#
#
# class permission_removeDep(Permission):
#     permission = Permission.objects.create(codename='removeDep',
#                                            name='remove Department')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_removeDep(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.removeDep'):
#             return True
#         else:
#             return False
#
#
# class permission_changeRole(Permission):
#     permission = Permission.objects.create(codename='changeRole',
#                                            name='change Role')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeRole(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeRole'):
#             return True
#         else:
#             return False
#
#
# class permission_changeField(Permission):
#     permission = Permission.objects.create(codename='changeField',
#                                            name='change Field')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeField(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeField'):
#             return True
#         else:
#             return False
#
#
# class permission_addField(Permission):
#     permission = Permission.objects.create(codename='addField',
#                                            name='add Field')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addField(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addField'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteField(Permission):
#     permission = Permission.objects.create(codename='deleteField',
#                                            name='delete Field')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteField(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteField'):
#             return True
#         else:
#             return False
#
#
# class permission_addUser(Permission):
#     permission = Permission.objects.create(codename='addUser',
#                                            name='add User')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addUser(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addUser'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteUser(Permission):
#     permission = Permission.objects.create(codename='deleteUser',
#                                            name='delete User')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteUser(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteUser'):
#             return True
#         else:
#             return False
#
#
# class permission_addCollege(Permission):
#     permission = Permission.objects.create(codename='addCollege',
#                                            name='add College')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addCollege(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addCollege'):
#             return True
#         else:
#             return False
#
#
# class permission_changeCollege(Permission):
#     permission = Permission.objects.create(codename='changeCollege',
#                                            name='change College')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeCollege(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeCollege'):
#             return True
#         else:
#             return False
#
#
# class permission_removeCollege(Permission):
#     permission = Permission.objects.create(codename='removeCollege',
#                                            name='remove College')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_removeCollege(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.removeCollege'):
#             return True
#         else:
#             return False
#
#
# class permission_addCourse(Permission):
#     permission = Permission.objects.create(codename='addCourse',
#                                            name='add Course')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addCourse(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addCourse'):
#             return True
#         else:
#             return False
#
#
# class permission_changeCourse(Permission):
#     permission = Permission.objects.create(codename='changeCourse',
#                                            name='change Course')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeCourse(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeCourse'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteCourse(Permission):
#     permission = Permission.objects.create(codename='deleteCourse',
#                                            name='delete Course')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteCourse(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteCourse'):
#             return True
#         else:
#             return False
#
#
# class permission_addHomeworkGrade(Permission):
#     permission = Permission.objects.create(codename='addGrade',
#                                            name='add Grade')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_addHomeworkGrade(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.addGrade'):
#             return True
#         else:
#             return False
#
#
# class permission_changeHomeworkGrade(Permission):
#     permission = Permission.objects.create(codename='changeGrade',
#                                            name='change Grade')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_changeHomeworkGrade(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.changeGrade'):
#             return True
#         else:
#             return False
#
#
# class permission_deleteHomeworkGrade(Permission):
#     permission = Permission.objects.create(codename='deleteGrade',
#                                            name='delete Grade')
#
#     def get_permission(self):
#         return self.permission
#
#
# class has_permission_deleteHomeworkGrade(Permission):
#     @staticmethod
#     def has_permission(request):
#         if request.user.has_perm('app_name.deleteGrade'):
#             return True
#         else:
#             return False
