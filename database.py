# -*- coding: utf-8 -*-

from peewee import *
from datetime import datetime

base = SqliteDatabase('profiles.db')
fields = ['Id', 'Description', 'Function', 'Trigger', "Active", 'Delete']


class DataModel(Model):

    class Meta:
        database = base


class Profile(DataModel):
    login = CharField(null=False, unique=True)

    class Meta:
        order_by = ('login',)


class RecognitionTask(DataModel):
    desc = TextField(null=False)
    func = TextField(null=False, default="Open File")
    trigger = TextField(null=False, default="Open File")
    triggerType = IntegerField(null=False, default=0)
    bonusData = TextField(null=True, default="")
    dateAdded = DateTimeField(default=datetime.now)
    active = BooleanField(default=False)
    profile = ForeignKeyField(Profile, related_name='profiles')

    class Meta:
        order_by = ('dateAdded',)


def connect():
    base.connect()
    base.create_tables([Profile, RecognitionTask])
    loadData()
    return True


def logon(login):
    try:
        profile, created = Profile.get_or_create(login=login)
        return profile
    except IntegrityError:
        return None


def loadData():
    """ Prepares default profile and tasks if there are none """
    if Profile.select().count() > 0:
        return
    tasks = (('Default recognition task 1', 'Open File', 'Open File', 0, 'clap.mp3'),
             ('Default recognition task 2', 'Open File', 'Clap', 1, 'clap.mp3'),
             ('Default recognition task 3', 'Open File', 'A', 2, 'clap.mp3'))
    o = Profile(login='profile1')
    o.save()
    for task in tasks:
        z = RecognitionTask(desc=task[0], func=task[1], trigger=task[2], triggerType=task[3], bonusData=task[4], profile=o)
        z.save()
    base.commit()
    base.close()


def read_profiles():
    """ Reads all existing profiles """
    profiles = []
    records = Profile.select()
    for z in records:
        profiles.append(z.login)
    return profiles


def read_tasks(profile):
    """ Reads all tasks of the given profile """
    tasks = []
    records = RecognitionTask.select().where(RecognitionTask.profile == profile)
    for z in records:
        tasks.append([
            z.id,
            z.desc,
            z.func,
            z.trigger,
            z.active,
            False])
    return tasks


def add_task(desc, func, trigger, trigger_type, data, profile):
    """ Adds new task """
    task = RecognitionTask(desc=desc, func=func, trigger=trigger, triggerType=trigger_type, bonusData=data, profile=profile)
    task.save()
    return [
        task.id,
        task.desc,
        task.func,
        task.trigger,
        task.active,
        False]


def saveData(tasks):
    """ Saves changes """
    for i, z in enumerate(tasks):
        # creates tasks instance
        task = RecognitionTask.select().where(RecognitionTask.id == z[0]).get()
        if z[5]:  # if tasks is selected for deletion
            task.delete_instance()  # delete from database
            del tasks[i]  # delete from data model
        else:
            task.desc = z[1]
            task.active = z[4]
            task.save()
