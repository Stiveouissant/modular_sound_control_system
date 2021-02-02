# -*- coding: utf-8 -*-

from peewee import *
from datetime import datetime

base = SqliteDatabase('profiles.db')
fields = ['Id', 'Description', 'Function', 'Trigger', 'Bonus Data', 'Active', 'Delete']


class DataModel(Model):

    class Meta:
        database = base


class Profile(DataModel):
    login = CharField(null=False, unique=True)

    class Meta:
        order_by = ('login',)


class RecognitionTask(DataModel):
    desc = TextField(null=False)
    func = TextField(null=False)
    trigger = TextField(null=False)
    triggerType = IntegerField(null=False)
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
    tasks = (('Default speech recognition task', 'Write Text', 'Test', 0, 'Speech works!'),
             ('Default sound recognition task', 'Write Text', 'lt;lt;lt;', 1, 'Sound works!'),
             ('Default pitch recognition task', 'Write Text', 'A4', 2, 'Pitch works!'))
    o = Profile(login='profile1')
    o.save()
    for task in tasks:
        z = RecognitionTask(desc=task[0], func=task[1], trigger=task[2], triggerType=task[3], bonusData=task[4], profile=o)
        z.save()
    base.commit()
    base.close()


def read_profiles():
    """ Reads all existing profiles names """
    profiles = []
    records = Profile.select()
    for z in records:
        profiles.append(z.login)
    return profiles


def read_profiles_full():
    """ Reads all existing profiles with id's and adds deletion field """
    profiles = []
    records = Profile.select()
    for z in records:
        profiles.append([z.id, z.login, False])
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
            z.bonusData,
            z.active,
            False])
    return tasks


def read_mode_tasks(profile, mode):
    """ Reads all tasks of the given profile of the given trigger type """
    tasks = []
    records = RecognitionTask.select().where(RecognitionTask.profile == profile, RecognitionTask.triggerType == mode)
    for z in records:
        tasks.append([
            z.id,
            z.desc,
            z.func,
            z.trigger,
            z.bonusData,
            z.active,
            False])
    return tasks


def add_profile(login):
    """ Adds new profile """
    profile = Profile(login=login)
    profile.save()
    return [
        profile.id,
        profile.login,
        False]


def add_task(desc, func, trigger, trigger_type, data, profile):
    """ Adds new task """
    task = RecognitionTask(desc=desc, func=func, trigger=trigger, triggerType=trigger_type, bonusData=data, profile=profile)
    task.save()
    return [
        task.id,
        task.desc,
        task.func,
        task.trigger,
        task.bonusData,
        task.active,
        False]


def save_profiles(profiles):
    """ Saves changes in manage profiles window """
    for i, z in enumerate(profiles):
        # creates profile instance
        profile = Profile.select().where(Profile.id == z[0]).get()
        if z[2]:  # if profile is selected for deletion
            delete_profile_tasks(profile)  # deletes all tasks belonging to a profile
            profile.delete_instance()  # delete profile from database
            del profiles[i]  # delete from data model
        else:
            profile.login = z[1]
            profile.save()


def delete_profile_tasks(profile):
    """ Deletes all tasks belonging to given profile """
    records = RecognitionTask.select().where(RecognitionTask.profile == profile)
    for v in records:
        v.delete_instance()


def saveData(tasks):
    """ Saves changes in tasks """
    for i, z in enumerate(tasks):
        # creates tasks instance
        task = RecognitionTask.select().where(RecognitionTask.id == z[0]).get()
        if z[6]:  # if tasks is selected for deletion
            task.delete_instance()  # delete from database
            del tasks[i]  # delete from data model
        else:
            task.desc = z[1]
            task.active = z[5]
            task.save()
