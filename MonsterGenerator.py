""" This will allow adding monster dynamically from a set of configuration files
    in the 'mobs' directory, images for the monsters should be put in the images directory.
    Eventually the images will get restructured into better locations, but for now thats where its going. """
import ConfigParser
from Mob import Mob
import os
from molecular import Molecule
from random import choice
from JobList import JobList

# load up the mobs into a list of config files, will be read by the __init__ of the MonsterGenerator class
MOB_DIR = 'mobs'
DIR_PATH = os.path.join(os.getcwd(), MOB_DIR)
FILES_IN_DIR = os.listdir(DIR_PATH)
FILE_LIST = []
for filename in FILES_IN_DIR:
    FILE_LIST.append(os.path.join(DIR_PATH, filename))

def namegen_orc_first():
    name = Molecule()
    name.load("namefiles/orcs_t.nam")
    return name.name()
    
def namegen_orc_second():
    name = Molecule()
    name.load("namefiles/orcs_wh.nam")
    return name.name()

class MonsterGenerator():
    """ MonsterGenerator Class """
    def __init__(self):
        self.monster_list = []
        self.JL = JobList()
        self.job_list = self.JL.get_list() 
        for item in FILE_LIST:
            config = ConfigParser.ConfigParser()
            #config.readfp(open(os.path.join('mobs', item)))
            config.readfp(open(item))
            name = config.get('mob', 'name')
            image = config.get('mob', 'image')
            portrait = config.get('mob', 'portrait')
            dead_image = config.get('mob', 'dead_image')
            job = config.get('mob', 'job')
            level = config.getint('mob', 'level')
            max_hp = config.getint('mob', 'max_hp')
            strength = config.getint('mob', 'strength')
            defense = config.getint('mob', 'defense')
            view_range = config.getint('mob', 'view_range')
            experience = config.getint('mob', 'experience')
            mob_dict = {
                        'name': name, 'image': image, 'portrait': portrait, 'dead_image': dead_image, 
                        'job': job, 'level': level, 'max_hp': max_hp, 
                        'strength': strength, 'defense': defense, 
                        'view_range': view_range, 'experience': experience
                        }    
            self.monster_list.append(mob_dict)
        #load the list of different types of monsters on init
        
    
    def generate_monster(self, mob_level, name = None, job = None):
        """ This is the function thats called and will generate the specified monster, 2 optional params (name and job) """
        temp_list = []
        for monster in self.monster_list:
            if name:
                pass
            else:
                name = monster['name']
                
            if job:
                pass
            else:
                job = monster['job']
            if monster['level'] == mob_level:
                if name == "generate":
                    name = namegen_orc_first() + " " + namegen_orc_second()
                if job == "generate":
                    job = choice(self.job_list)
                else:
                    job = self.JL.generate_job_for(job)
                mob = Mob(name, monster['image'], monster['portrait'], monster['dead_image'])
                mob.job = job
                mob.level = monster['level']
                mob.max_hp = monster['max_hp']
                mob.str = monster['strength']
                mob.defense = monster['defense']
                mob.view_range = monster['view_range']
                mob.experience = monster['experience']
                temp_list.append(mob)
        #pick one of the monsters from the list randomly
        return choice(temp_list)
    
    def __str__(self):
        return self.monster_list
    
    
if __name__ == '__main__':
    #debugging
    MG = MonsterGenerator()
    mob_test = MG.generate_monster(1)
    mob_test2 = MG.generate_monster(1, 'testname')
    mob_test3 = MG.generate_monster(1, 'testname2', 'testjob')
    print mob_test.name
    print mob_test.job
    print mob_test2.name
    print mob_test2.job
    print mob_test3.name
    print mob_test3.job
    
    