import ConfigParser
from Mob import Mob
import os
from molecular import Molecule
""" Monster generator """
from random import choice

file_list = ['centaur.cfg', 'centaur2.cfg']

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
        for item in file_list:
            config = ConfigParser.ConfigParser()
            config.readfp(open(os.path.join('mobs', item)))
            name = config.get('mob', 'name')
            image = config.get('mob', 'image')
            portrait = config.get('mob', 'portrait')
            job = config.get('mob', 'job')
            level = config.getint('mob', 'level')
            max_hp = config.getint('mob', 'max_hp')
            strength = config.getint('mob', 'strength')
            defense = config.getint('mob', 'defense')
            view_range = config.getint('mob', 'view_range')
            experience = config.getint('mob', 'experience')
            mob_dict = {'name': name, 'image': image, 'portrait': portrait, 'job': job, 'level': level, 'max_hp': max_hp, 'strength': strength, 'defense': defense, 'view_range': view_range, 'experience': experience}    
            self.monster_list.append(mob_dict)
        #load the list of different types of monsters on init
        
    
    def generate_monster(self, mob_level, name = None, job = None):
        
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
                    job_list = ['gimp', 'gimpy', 'grunt', 'footsoldier', 'twirp', 'git']
                    job = choice(job_list)
                mob = Mob(name, monster['image'], monster['portrait'])
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
    
    
if __name__ == '__main__':
    MG = MonsterGenerator()
    mob = MG.generate_monster(1)
    mob2 = MG.generate_monster(1, 'testname')
    mob3 = MG.generate_monster(1, 'testname', 'testjob')
    print mob.name
    print mob.job
    print mob2.name
    print mob2.job
    print mob3.name
    print mob3.job
    
    