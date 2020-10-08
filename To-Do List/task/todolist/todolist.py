from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
is_running = True
while is_running:
    print("""
1) Today's tasks
2) Add task
0) Exit
    """)
    choose_action = int(input())

    if choose_action == 1:
        rows = session.query(Table).all()
        print("Today:")
        if len(rows) != 0:
            for i in rows:
                print(f"{i.id}. {i.task}")
        else:
            print("Nothing to do!")
    elif choose_action == 2:
        print("Enter task")
        add_task = input()
        new_row = Table(task = add_task)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif choose_action == 0:
        is_running = False

print("Bye!")