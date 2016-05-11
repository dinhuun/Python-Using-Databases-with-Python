'''
Create a class and its instance
Create a subclass and its instance
Created on May 7, 2016
@author: course
@author: dinh
'''

class canine:
    sounds = 0
    name = ""
    def __init__(self, n):
        self.name = n
        print 'I am alive with name', self.name
    def bark(self):
        self.sounds = self.sounds + 1
        print 'barked', self.sounds, 'times'
    def __del__(self):
        print 'I am dead with name', self.name, self.sounds

dog = canine('Macki')
dog.bark()
dog.bark()
dog.bark()

class husky(canine):
    miles = 0
    def pull(self):
        self.miles = self.miles + 10
        print 'pulled', self.miles, 'miles'
        
wolf = husky('Buck')
wolf.bark()
wolf.pull()