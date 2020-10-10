from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
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
2) Week's tasks
3) All tasks
4) Add task
0) Exit
""")
    choose_action = input()

    if choose_action == '1':
        today = datetime.today()
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(f"Today {today.day} {today.strftime('%b')}:")
        if len(rows) != 0:
            for i in rows:
                print(f"{i.id}. {i.task}")
        else:
            print("Nothing to do!")
    elif choose_action == '2':
        today = datetime.today()
        last_day = today + timedelta(days=7)
        week_tasks = session.query(Table).filter(Table.deadline >=today.date(),Table.deadline <= last_day.date()).order_by(Table.deadline).all()
        week_days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        for i in range(0,7):
            print(f'{week_days[(today + timedelta(days=i)).weekday()]} {(today + timedelta(days=i)).day} {(today + timedelta(days=i)).strftime("%b")}:')
            cnt = 1
            for task in week_tasks:
                if (today + timedelta(days=i)).date() == task.deadline:
                    print(f'{cnt}. {task}')
                    cnt += 1
            else:
                print("Nothing to do!")
            print()
    elif choose_action == '3':
        all_tasks = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        cnt = 1
        for task in all_tasks:
            print(f"{cnt}. {task.task}. {task.deadline.day} {task.deadline.strftime('%b')}")
            cnt += 1
    elif choose_action == '4':
        print("Enter task")
        add_task = input()
        print("Enter deadline")
        add_deadline = input()
        new_row = Table(task=add_task, deadline=datetime.strptime(add_deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif choose_action == '0':
        is_running = False
print("Bye!")
