""" This will create a list of all the different jobs based on the config files in the jobs directory """
import os
from random import choice
import configparser
from Job import Job

JOB_DIR = "jobs"
DIR_PATH = os.path.join(os.getcwd(), JOB_DIR)
FILES_IN_DIR = os.listdir(DIR_PATH)
FILE_LIST = []
for filename in FILES_IN_DIR:
    FILE_LIST.append(os.path.join(DIR_PATH, filename))


class JobList:
    """Job list creator Class"""

    def __init__(self):
        self.job_list = []
        for item in FILE_LIST:
            config = configparser.ConfigParser()
            config.read_file(open(item))
            job_name = config.get("job", "job_name")
            attack_bonus = config.get("job", "attack_bonus")
            defense_bonus = config.get("job", "defense_bonus")
            view_range_bonus = config.get("job", "view_range_bonus")
            damage = config.getint("job", "damage")
            description = config.get("job", "description")
            hit_dice = config.getint("job", "hit_dice")
            job = Job(
                job_name,
                attack_bonus,
                defense_bonus,
                view_range_bonus,
                damage,
                hit_dice,
                description,
            )
            self.job_list.append(job)

    def pick_a_random_job(self):
        """picks a job at random useful for generating monsters with different jobs"""
        return choice(self.job_list)

    def generate_job_for(self, job_name):
        for job in self.job_list:
            if job.job_name == job_name:
                return Job(
                    job_name,
                    job.attack_bonus,
                    job.defense_bonus,
                    job.view_range_bonus,
                    job.damage,
                    job.hit_dice,
                    job.description,
                )
        return choice(self.job_list)  # if no job is found choose a random one

    def get_list(self):
        """return the whole list, used by the character creator"""
        return self.job_list


if __name__ == "__main__":
    # debugging
    JL = JobList()
    job1 = JL.pick_a_random_job()
    job2 = JL.pick_a_random_job()
    print(f"{job1}, {job2}")
