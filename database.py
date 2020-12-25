# -*- coding: utf-8 -*-

from peewee import *
from datetime import datetime

base = SqliteDatabase('profiles.db')
fields = ['Id', 'Description', 'Added', 'Done', 'Delete']


class DataModel(Model):

    class Meta:
        database = base


class Profile(DataModel):
    login = CharField(null=False, unique=True)
    password = CharField()

    class Meta:
        order_by = ('login',)


class RecognitionTask(DataModel):
    desc = TextField(null=True)
    # task = IntegerField(null=False)
    # fileAddress = TextField(null=True)
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


def logon(login, password):
    try:
        profile, created = Profile.get_or_create(login=login, password=password)
        return profile
    except IntegrityError:
        return None


def loadData():
    """ Prepares default profile and tasks if there are none """
    if Profile.select().count() > 0:
        return
    profiles = ('profile1', 'profile2')
    tasks = ('Default recognition task 1', 'Default recognition task 2')
    for login in profiles:
        o = Profile(login=login, password='123')
        o.save()
        for describer in tasks:
            z = RecognitionTask(desc=describer, profile=o)
            z.save()
    base.commit()
    base.close()


def readData(profile):
    """ Reads tasks of the given profile """
    tasks = []
    records = RecognitionTask.select().where(RecognitionTask.profile == profile)
    for z in records:
        tasks.append([
            z.id,
            z.desc,
            '{0:%Y-%m-%d %H:%M:%S}'.format(z.dateAdded),
            z.active,
            False])
    return tasks


def addTask(profile, description):
    """ Adds new task """
    task = RecognitionTask(desc=description, profile=profile)
    task.save()
    return [
        task.id,
        task.desc,
        '{0:%Y-%m-%d %H:%M:%S}'.format(task.dateAdded),
        task.active,
        False]


def saveData(tasks):
    """ Saves changes """
    for i, z in enumerate(tasks):
        # utworzenie instancji tasks
        task = RecognitionTask.select().where(RecognitionTask.id == z[0]).get()
        if z[4]:  # if tasks is selected for deletion
            task.delete_instance()  # delete from database
            del tasks[i]  # delete from data model
        else:
            task.desc = z[1]
            task.active = z[3]
            task.save()
