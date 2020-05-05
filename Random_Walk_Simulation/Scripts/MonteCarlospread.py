# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:27:46 2020

@author: johnw
"""

#monte carlo simulation for disease spread
import random
import math
import matplotlib.pyplot as plt


class Individual:
    def __init__(self,infected,asymptomatic,current_location,home_location,time,alive):
        self.i = infected
        self.a = asymptomatic
        self.currloc = current_location
        self.homeloc = home_location
        self.time = time
        self.alive = alive
        
#tunable parameters
population_size = 100
social_distance = 20
length_of_walk = 100
recovery_time = 14
initial_mortality_rate = 0.01
dist_for_contact = 10
time_to_quarantine = 3
pat_0_asymp = True
chance_asymp = 0.2
chance_immun = 0.01
chance_of_walk = 1
chance_of_infection = 1
capacity_of_quarantine = 5

#initializing necessary arrays       
population = []
inf_line = []
noninf_line = []
rem_line = []
t_line = []
recov_line = []
mort_line = []
mortality_rate = initial_mortality_rate

#initialize the general population
for i in range(1,population_size):
    check_asymp = random.uniform(0,1)
    check_immun = random.uniform(0,1)
    if check_asymp <= chance_asymp and check_immun > chance_immun: 
        population.append(Individual(False,True,social_distance*i,social_distance*i,0,True))
    elif check_asymp > chance_asymp and check_immun > chance_immun:
        population.append(Individual(False,False,social_distance*i,social_distance*i,0,True))
    elif check_immun <= chance_immun:
        population.append(Individual(False,False,social_distance*i,social_distance*i,100,True))

#initialize patient zero       
pat_0 = Individual(True,pat_0_asymp,social_distance*(population_size),social_distance*(population_size),0,True)

#add patient zero to the population
population.append(pat_0)

#time step loop
for t in range(0,population_size):
    num_of_infected = 0
    num_of_noninfected = 0
    num_of_removed = 0
    num_of_recovered = 0
    num_of_fatalities = 0

    for i in range(0,population_size): #loop for determining infection
        if population[i].i:
            for j in range(0,population_size):
                infection = random.uniform(0,1)
                location_difference = population[i].currloc - population[j].currloc
                if abs(location_difference) < dist_for_contact and infection <= chance_of_infection and population[j].time == 0:
                    population[j].i = True
    check_for_walk = t % (1/chance_of_walk) 
    
    if check_for_walk == 0: #loop for random 1-D walk
        for i in range(0,population_size):
            if population[i].currloc >= population_size - length_of_walk:
                population[i].currloc = population[i].currloc - random.uniform(0,1)*length_of_walk
            elif population[i].currloc <= length_of_walk:
                population[i].currloc = population[i].currloc + random.uniform(0,1)*length_of_walk
            else:
                direction = random.uniform(0,1)
                if direction > 0.5:
                    population[i].currloc = population[i].currloc + random.uniform(0,1)*length_of_walk
                else:
                    population[i].currloc = population[i].currloc - random.uniform(0,1)*length_of_walk
    else: #if there is no walk, sends everyone to their home location
        for i in range(0,population_size):
            population[i].currloc = population[i].homeloc
    for i in range(0,population_size): #loop for managing recovery and quarantine of infected people
        if population[i].i:
            population[i].time = population[i].time + 1
        if population[i].a and population[i].time == recovery_time:
            population[i].i = False
        if population[i].a == False and population[i].time >= time_to_quarantine and population[i].time < recovery_time:
            population[i].currloc = population_size*length_of_walk
        if population[i].a ==False and population[i].time == recovery_time:
            mort = random.uniform(0,1) #determines if infected, symptomatic patient recovers or not.
            if mort > mortality_rate:
                population[i].i = False
                population[i].currloc = population[i].homeloc
                population[i].time = population[i].time + 1
            else:
                population[i].i = False
                population[i].alive = False
                population[i].time = population[i].time + 1

    
    print(mortality_rate)
    mortality_rate = initial_mortality_rate
    print(mortality_rate)
    for i in range(0,population_size): #checks the number of infected, quarantined, recovered, fatalities, and noninfected
        if population[i].i and population[i].time < recovery_time and population[i].alive: #checks number of infected
            num_of_infected = num_of_infected + 1
        if population[i].currloc == population_size*length_of_walk:#checks number of quarantined
            num_of_removed = num_of_removed + 1
        if population[i].time >= recovery_time and population[i].alive and population[i].i == False:#checks number of recovered
            num_of_recovered = num_of_recovered + 1
        if population[i].alive == False: #checks number of fatalitities
            num_of_fatalities = num_of_fatalities + 1
        if population[i].time == 0: #checks number of noninfected
            num_of_noninfected = num_of_noninfected + 1
    if num_of_removed >= capacity_of_quarantine:
            mortality_rate = math.floor(num_of_removed/capacity_of_quarantine)*mortality_rate #mortality begins to increase when capacity if reached or exceeded  
        
        
 #adding the data for the plots
    inf_line.append(num_of_infected)
    noninf_line.append(num_of_noninfected)
    rem_line.append(num_of_removed)
    recov_line.append(num_of_recovered)
    mort_line.append(num_of_fatalities)
    t_line.append(t)

    #creating the plots
plt.plot(t_line,inf_line,'r-',label='infected')
plt.plot(t_line,noninf_line,'b-',label='non-infected')
plt.plot(t_line,rem_line,'g-',label='quarantined')
plt.plot(t_line,recov_line,'k-',label='recovered')
plt.plot(t_line,mort_line,'c-',label='fatalities')
plt.legend()
plt.show()


        
    