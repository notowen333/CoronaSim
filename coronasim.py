from random import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go

"""
defines a virus by the following:
        1) duration
        2) symptom delay 
        3) chance of infection upon exposure
"""

class Virus:

    def __init__(self, infection_chance, duration = 14, symptom_delay = 10):
        self.duration = duration
        self.symptom_delay = symptom_delay
        self.infection_chance = infection_chance


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
    defines a person by the following:
        1) alive or not
        2) interactions per day
        3) infected or not
        4) recovered or not        
"""

class Person:

    def __init__(self, interactions_per_day,is_infected,length_of_infection,is_isolated):
        self.interactions_per_day = interactions_per_day
        self.alive = True
        self.is_infected = is_infected
        self.recovered = False
        self.length_of_infection = length_of_infection
        self.is_isolated = is_isolated
    
class Adolescent(Person):

    def __init__(self, interactions_per_day, mortality_rate,length_of_infection,is_isolated,is_infected):
        Person.__init__(self,interactions_per_day,is_infected,length_of_infection,is_isolated)
        self.mortality_rate = mortality_rate

class Youth(Person):

   def __init__(self, interactions_per_day, mortality_rate,length_of_infection,is_isolated,is_infected):
        Person.__init__(self,interactions_per_day,is_infected,length_of_infection,is_isolated)
        self.mortality_rate = mortality_rate

class MiddleAged(Person):

   def __init__(self, interactions_per_day, mortality_rate,length_of_infection,is_isolated,is_infected):
        Person.__init__(self,interactions_per_day,is_infected,length_of_infection,is_isolated)
        self.mortality_rate = mortality_rate

class Elderly(Person):

    def __init__(self, interactions_per_day, mortality_rate,length_of_infection,is_isolated,is_infected):
        Person.__init__(self,interactions_per_day,is_infected,length_of_infection,is_isolated)
        self.mortality_rate = mortality_rate

class VeryElderly(Person):

    def __init__(self, interactions_per_day, mortality_rate,length_of_infection,is_isolated,is_infected):
        Person.__init__(self,interactions_per_day,is_infected,length_of_infection,is_isolated)
        self.mortality_rate = mortality_rate

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def count_positive(community):
    ctr = 0
    for person in community:
        if person.is_infected:
            ctr += 1
    return ctr

def count_negative(community):
    return len(community) - count_positive(community)

def count_dead(community):
    ctr = 0
    for person in community:
        if not person.alive:
            ctr += 1
    return ctr

def count_alive(community):
    return len(community) - count_dead(community)

def count_recovered(community):
    ctr = 0
    for person in community:
        if person.recovered:
            ctr += 1
    return ctr
    
def randint(n):
    a = random()
    b = int((a*n))
    return b



def create_adolescent_community (demographic_size, proportion_isolated = .45, interactions = 6, mortality_rate = 0):

    community = []

    for i in range(demographic_size):
        a = random()
        if a > proportion_isolated:
            community.append(Adolescent(interactions,mortality_rate,0,False,False))
        else:
            community.append(Adolescent(interactions,mortality_rate,0,True,False))
    
    return community
    


#all of the following take the previous community as a param for effeciency

def create_youth_community(prev,demographic_size, proportion_isolated = .45,interactions = 10, mortality_rate = .0018/2):

    community = prev

    for i in range(demographic_size):
        
        if random() > proportion_isolated:
            community.append(Youth(interactions,mortality_rate,0,False,False))
        else:
            community.append(Youth(interactions,mortality_rate,0,True,False))

    return community

def create_middle_community(prev, demographic_size, proportion_isolated = .45, interactions = 12, mortality_rate = .008):

    community = prev

    for i in range(demographic_size):
    
        if random() > proportion_isolated:
            community.append(MiddleAged(interactions,mortality_rate,0,False,False))
        else:
            community.append(MiddleAged(interactions,mortality_rate,0,True,False))

    return community

def create_elderly_community(prev, demographic_size, proportion_isolated = .45, interactions = 6, mortality_rate = .05):

    community = prev

    for i in range(demographic_size):

        if random() > proportion_isolated:
            community.append(Elderly(interactions,mortality_rate,0,False,False))
        else:
            community.append(Elderly(interactions,mortality_rate,0,True,False))

    return community

def create_very_elderly_community(prev, demographic_size, proportion_isolated = .45, interactions = 5, mortality_rate = .15):

    community = prev

    for i in range(demographic_size):

        if random() > proportion_isolated:
            community.append(VeryElderly(interactions,mortality_rate,0,False,False))
        else:
            community.append(VeryElderly(interactions,mortality_rate,0,True,False))

    
    return community




""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""
    takes a list of people as its argument and
    defines a community by the following:
    1) size
    2) positive cases
    3) negative cases
    4) dead
    5) alive
    6) time (days)
"""

class Community:

    def __init__(self, community, virus):
        self.community = community
        self.virus = virus
        self.size = len(community)
        self.number_positive = count_positive(community)
        self.number_negative = count_negative(community)
        self.number_dead = count_dead(community)
        self.number_alive = count_alive(community)
        self.number_recovered = count_recovered(community)
        self.time = 0
        self.time_list = [str(0)]
        self.positive_list = [self.number_positive]
        self.negative_list = [self.number_negative]
        self.alive_list = [self.number_alive]
        self.dead_list = [self.number_dead]
        self.recovered_list = [self.number_recovered]
        self.adolescent_deaths = 0
        self.youth_deaths = 0
        self.middle_deaths = 0
        self.elderly_deaths = 0
        self.very_elderly_deaths = 0
    
    def step_time(self):

        self.time += 1


        for person in self.community:
            if person.is_infected and person.alive:
                i = 0

                #given person infects proportional to infection_probability
                while i < person.interactions_per_day and not person.is_isolated:
                    j = randint(self.size)
                    interacted_person = self.community[j]
                    infection_chance = self.virus.infection_chance
                    sneeze = random()
                    if (sneeze < infection_chance) and (not interacted_person.recovered) and (not interacted_person.is_infected) and (not interacted_person.is_isolated):
                        interacted_person.is_infected = True
                        self.number_positive += 1
                        self.number_negative -= 1
                    i += 1
                
                #now infected people die proportional to mortality rate
                angel_of_death = random()
                if angel_of_death < (person.mortality_rate/self.virus.duration):

                    #person dies
                    person.alive = False
                    self.number_dead += 1
                    self.number_alive -= 1

                    #death count recorded in right demographic
                    if isinstance(person,Adolescent):
                        self.adolescent_deaths += 1
                    if isinstance(person,Youth):
                        self.youth_deaths += 1
                    if isinstance(person,MiddleAged):
                        self.middle_deaths += 1
                    if isinstance(person,Elderly):
                        self.elderly_deaths += 1
                    if isinstance(person,VeryElderly):
                        self.very_elderly_deaths += 1
                else:
                    person.length_of_infection += 1
                
                #now people recover if they have completed the duration
                if person.alive and person.length_of_infection == self.virus.duration:
                    person.is_infected = False
                    person.recovered = True
                    self.number_recovered += 1
                    self.number_positive -= 1
                    self.number_negative += 1
                
        #store results
        self.time_list.append(str(self.time))
        self.positive_list.append(self.number_positive)
        self.negative_list.append(self.number_negative)
        self.alive_list.append(self.number_alive)
        self.dead_list.append(self.number_dead)
        self.recovered_list.append(self.number_recovered)



#run sim

#demographics are: 13% adolescent, 37% youth, 31% middle, 17% elderly, 3% very elderly (https://censusreporter.org/profiles/06000US3401347500-montclair-township-essex-county-nj/)



def run(n, f1, f2, num_steps,mortality_list):

    if n == -1:
        f2.update_layout(
        title = "Mortality Rates With Various Social Distancing Measures",
        xaxis_title = 'Days Since Origin',
        yaxis_title = "Number of People",
        legend_title='<b> Measure </b>',
        legend=dict(font=dict(
            size=16,
            color="black"
        )))
        f1.show()
        f2.show()
        print(mortality_list)
        return


    demo = [.13,.37,.31,.17,.03]
    pop = 40000



    social_distance_prop = [.60,.5,.35,.10,0]

    a = create_adolescent_community(int(demo[0]*pop), social_distance_prop[n])
    b = create_youth_community(a,int(demo[1]*pop), social_distance_prop[n])
    c = create_middle_community(b,int(demo[2]*pop), social_distance_prop[n])
    d = create_elderly_community(c,int(demo[3]*pop), social_distance_prop[n])
    e = create_very_elderly_community(d,int(demo[4]*pop), social_distance_prop[n])
    e.append(MiddleAged(10,.008,0,False,True))

    coronavirus = Virus(.03)

    montclair = Community(e,coronavirus)

    for i in range(num_steps):
        montclair.step_time()


    #store mortality rates
    mortality_list.append([montclair.adolescent_deaths,montclair.youth_deaths,montclair.middle_deaths,montclair.elderly_deaths,montclair.very_elderly_deaths])

 #graph sim
    
    title_library = ["no",
                     "light",
                     "moderate",
                     "strong",
                     "severe"]
    
    



 # Create and style traces

    f1.add_trace(go.Scatter(x = montclair.time_list, y = montclair.positive_list, name=f"# positive cases with {title_library[4-n]} social distancing",
    line=dict(width = 4)))
    

    
    f2.add_trace(go.Scatter(x = montclair.time_list, y = montclair.dead_list, name=f"# deceased with {title_library[4-n]} social distancing",
    line=dict(width = 4)))
    
        


 # Edit the layout
    f1.update_layout(title = "Montclair, NJ Coronavirus Simulation",
                   xaxis_title='Days Since Origin',
                   yaxis_title='Number of People',
                   legend = dict(font_size = 16)
    )

    run(n-1,f1,f2,num_steps,mortality_list)




f1 = go.Figure()
f2 = go.Figure()            
            

run(4,f1,f2,220,[])

        




        













