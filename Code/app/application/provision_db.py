from . import db
from .models import User, Exercise, TemplateVm
from datetime import datetime as dt

def provision_data(): #creates 20 users and 1 exercise
    # Provides the database with a small amount of data if empty
    user1 = User.query.filter_by(username='user1').first()
    if not user1:
        users_data = [
            {"username": f'user{i}', "email": f'user{i}@mail.com'}
            for i in range(1, 21)
        ]

        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                created_on=dt.now()
            )
            user.set_password('testpass')
            db.session.add(user)
        templatevm = TemplateVm(templatevm_proxmox_id=10000,
                                created_on = dt.now())
        exercise = Exercise(name = 'exercise',#NOTE: this exercise does not have any workvm assigned
                            description = 'Lorem ipsum',
                            templatevm = templatevm,
                            created_on = dt.now()
                            )
        db.session.add(exercise)

    db.session.commit()

def alt_provision_data(): #creates 1 user and 20 exercises
    # Provides the database with a small amount of data if empty
    user1 = User.query.filter_by(username='user1').first()
    if not user1:
        # Create 1 user
        user = User(
            username='user1',
            email='user1@mail.com',
            created_on=dt.now()
        )
        user.set_password('testpass')
        db.session.add(user)
        
        # Create 20 exercises
        templatevm = TemplateVm(templatevm_proxmox_id=10000,
                                 created_on=dt.now())
        for i in range(1, 21):
            exercise = Exercise(
                name=f'exercise_{i}',  # Unique exercise name
                description=f'Lorem ipsum for exercise {i}',
                templatevm=templatevm,  # Assuming all exercises share the same TemplateVm
                created_on=dt.now()
            )
            db.session.add(exercise)

    db.session.commit()