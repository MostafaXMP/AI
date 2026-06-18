import random

#you can also see that the output explains the steps of the genetic algorithm
#beside that the variable names are clear

#first thing is to generate an individuals with 9 bits (9 chromosomes)
def generate_individual():
    individual = ""
    for x in range(0,9):
        individual += str(random.randint(0,1))
    return individual

#2nd thing is to see the fitness of all the generated individuals
#sort them in a dictionary so user can see the fitness of each one of them and make it easier for the discard step
def fitness(*x):
    fitness ={}
    for individual in x:
        fitness[individual] = (individual.count("010"))
    sorted_fitness = dict(sorted(fitness.items(), key=lambda item: item[1]))
    return sorted_fitness

#4th thing is to make crossover between them
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

#5th thing is to mutate one of the offspring
def mutate(new_generation):
    index = random.randint(0, len(new_generation) - 1)
    mutated = list(new_generation)
    mutated[index] = '1' if mutated[index] == '0' else '0'
    return ''.join(mutated)


###################1st: generate random individuals
x1 = generate_individual()
x2 = generate_individual()
x3 = generate_individual()
x4 = generate_individual()
# make them in a list so it is easier to deal with them
random_individuals = [x1,x2,x3,x4]
##########################################print and make setup

#6th thing is to make the number of the iterations = 2
for z in range (0,2):
    print(f"this is the {z+1} iteration")
    print()
    #print the individuals
    print(f"x1 = {random_individuals[0]},  x2= {random_individuals[1]}, x3 = {random_individuals[2]}, x4 = {random_individuals[3]}")
    ################2nd: see the fittness of the generated code
    evaluation = fitness(random_individuals[0],random_individuals[1],random_individuals[2],random_individuals[3])

    #################3rd discard is to discard the least 2 by making the dictionary take index 2 and 3 because it is sorted
    after_discard = dict(list(evaluation.items())[2:])
    print("the random individuals and their fitness")
    print(evaluation)

    print("after discarding the least 2 with respect to fitness")
    print(after_discard)

    ####################4th: crossover and generating the new generation
    print("making crossover between the above parents")
    parents = list(after_discard.keys())
    child1, child2 = crossover(parents[0],parents[1])

    print("Child 1:", child1)
    print("Child 2:", child2)
    new_generation = [child1,child2]

    ####################5th: make the mutation randomly at one offspring of the new generation which is chosen also randomly
    x = random.randint(0,1)
    mutate(new_generation[x])
    new_generation_with_one_mutated = [mutate(new_generation[x]),new_generation[x-1]]
    print("new generation is with one of the children mutated \n",new_generation_with_one_mutated)
    last_generation = []

    #make the 2 children and their parents of the new generation constitute the next generation
    last_generation.extend(parents)
    last_generation.extend(new_generation_with_one_mutated)
    print("the generation that will continue\n",last_generation)

    #make the list of the random individuals to be equal to the last_generation
    #that we will continue with it to make other generations
    counter = 0
    for x in random_individuals:
        random_individuals[counter] = last_generation[counter]
        counter += 1

    print()
