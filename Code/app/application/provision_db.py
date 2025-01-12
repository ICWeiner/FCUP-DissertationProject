from . import db
from .models import User, Exercise, TemplateVm
from datetime import datetime as dt

def provision_data():
    # Provides the database with a small amount of data if empty
    user1 = User.query.filter_by(username='Alice').first()
    if not user1:
        user1 = User(username = 'Alice',
                    email = 'alice@mail.com',
                    created_on = dt.now(),
                    )
        user1.set_password('testpass')
        db.session.add(user1)
        user2 = User(username = 'Bob',
                    email = 'bob@mail.com',
                    created_on = dt.now(),
                    )
        user2.set_password('testpass')
        db.session.add(user2)
        templatevm = TemplateVm(templatevm_proxmox_id=110,
                                created_on = dt.now())
        exercise = Exercise(name = 'exercise',
                            description = 'Lorem ipsum',
                            templatevm = templatevm,
                            created_on = dt.now()
                            )
        db.session.add(exercise)

    db.session.commit()