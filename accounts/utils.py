def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'admin'

def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'

def is_student(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'student'
