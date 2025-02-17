from . import db
from .models import User, Exercise, TemplateVm, WorkVm
from datetime import datetime as dt

def provision_data(): #creates 10 users and 1 exercise
    # Creates a database with a small amount of data if empty
    user1 = User.query.filter_by(username='user1').first()
    if not user1:
        users_data = [#generate user data
            {"username": f'user{i}', "email": f'user{i}@mail.com'}
            for i in range(1, 11)
        ]

        #insert templatevm
        templatevm = TemplateVm(proxmox_id=10000,
                                created_on = dt.now())
        db.session.add(templatevm)
        #insert exercise
        exercise = Exercise(name = 'exercise',#NOTE: this exercise does not have any workvm assigned
                            description = 'Lorem ipsum',
                            templatevm = templatevm,
                            created_on = dt.now()
                            )
        db.session.add(exercise)

        i = 1

        for user_data in users_data:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                created_on=dt.now()
            )
            user.set_password('123123')
            db.session.add(user)

            workvm = WorkVm(proxmox_id = i,
                            user = user,
                            templatevm = templatevm,
                            created_on = dt.now()
                            )
            db.session.add(workvm)
            i+=1

    db.session.commit()
