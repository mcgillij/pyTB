""" This will create a list of all the different jobs based on the config files in the jobs directory """
import ConfigParser
from Job import Job
import os
from random import choice

JOB_DIR = 'jobs'
DIR_PATH = os.path.join(os.getcwd(), JOB_DIR)
FILES_IN_DIR = os.listdir(DIR_PATH)
FILE_LIST = []
for filename in FILES_IN_DIR:
    FILE_LIST.append(os.path.join(DIR_PATH, filename))

class JobList():
    """ Job list creator Class """
    def __init__(self):
        self.job_list = []
        for item in FILE_LIST:
            config = ConfigParser.ConfigParser()
            config.readfp(open(item))
            job_name = config.get('job', 'job_name')
            attack_bonus = config.get('job', 'attack_bonus')
            defense_bonus = config.get('job', 'defense_bonus')
            view_range_bonus = config.get('job', 'view_range_bonus')
            description = config.get('job', 'description')
            job = Job(job_name, attack_bonus, defense_bonus, view_range_bonus, description)
            self.job_list.append(job)
    
    def pick_a_random_job(self):
        """ picks a job at random useful for generating monsters with different jobs """
        return choice(self.job_list)
    
    def generate_job_for(self, job_name):
        for job in self.job_list:
            if job.job_name == job_name:
                return Job(job_name, job.attack_bonus, job.defense_bonus, job.view_range_bonus, job.description)
        return None # no job by this description
    
    def get_list(self):
        """ return the whole list, used by the character creator """
        return self.job_list
    
if __name__ == '__main__':
    #debugging
    JL = JobList()
    job1 = JL.pick_a_random_job()
    job2 = JL.pick_a_random_job()
    print (job1, job2)
    