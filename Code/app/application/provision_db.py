from . import db
from sqlalchemy import select
from .models import User, Exercise, TemplateVm, WorkVm
from datetime import datetime as dt

def provision_data(): #creates 10 users and 1 exercise
    # Creates a database with a small amount of data if empty
    with db.bind.Session() as s:
        with s.begin():
            user1 = s.scalars(select(User)).one_or_none()
            if not user1:
            
                users_data = [#generate user data
                    {"username": f'user{i}', "email": f'user{i}@mail.com'}
                    for i in range(1, 11)
                ]

                #insert templatevm
                templatevm = TemplateVm(proxmox_id=10000)
                s.add(templatevm)
                #insert exercise
                exercise = Exercise(name = 'exercise',#NOTE: this exercise does not have any workvm assigned
                                    description = 'Lorem ipsum',
                                    templatevm = templatevm )
                s.add(exercise)

                i = 1

                for user_data in users_data:
                    user = User(
                        username=user_data["username"],
                        email=user_data["email"])
                    user.set_password('123123')
                    s.add(user)

                    workvm = WorkVm(proxmox_id = i,
                                    user = user,
                                    templatevm = templatevm )
                    s.add(workvm)
                    i+=1
                print(s.scalars(select(User)).all())
                s.commit()
                
