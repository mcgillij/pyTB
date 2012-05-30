""" This will be the main job class, that the other jobs will fill out as a template """

class Job():
    """ Main Job class that will be plugged into players / monsters to adjust stats """
    def __init__(self, job_name, attack_bonus, defense_bonus, view_range_bonus, damage, description):
        self.job_name = job_name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.view_range_bonus = view_range_bonus
        self.damage = damage
        self.description = description

    def __str__(self):
        return self.job_name + ", A: " + str(self.attack_bonus) + ", D: " + str(self.defense_bonus) + ", VR: " + str(self.view_range_bonus) + " D:" + str(self.damage) + " desc: " + self.description
