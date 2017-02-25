# -*- coding: utf-8 -*-

class Course():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.teacher = kwargs.get('teacher')
        self.room = kwargs.get('room')
        self.weeks = kwargs.get('weeks')
        self.start_time = kwargs.get('start_time')
        self.end_time = kwargs.get('end_time')
