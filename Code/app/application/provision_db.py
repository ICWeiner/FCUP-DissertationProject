from . import db
from .models import User, Exercise, TemplateVm
from datetime import datetime as dt

def provision_data():
    # Provides the database with a small amount of data if empty
    user1 = User.query.filter_by(username='Alice').first()
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
        templatevm = TemplateVm(templatevm_proxmox_id=110,
                                created_on = dt.now())
        exercise = Exercise(name = 'exercise',#NOTE: this exercise does not have any workvm assigned
                            description = 'Lorem ipsum',
                            templatevm = templatevm,
                            created_on = dt.now()
                            )
        db.session.add(exercise)

    db.session.commit()