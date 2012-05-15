""" This will be the main job class, that the other jobs will fill out as a template """


class Job():
    def __init__(self, job_name, attack_bonus, defense_bonus, view_range_bonus, description):
        self.job_name = job_name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.view_range_bonus = view_range_bonus
        self.description = description
        
    def __repr__(self):
        return "job_name: " + self.job_name + " attack bonus: " + str(self.attack_bonus) + " defense bonus: " + str(self.defense_bonus) + " view range bonus: " + str(self.view_range_bonus) + " desc: " + self.description
        