# FILE USED TO GENERATE .txt file for trials


import random
import csv 

################################ to generate 2 pairs ##################################
NUM_STIMULI= 30

# Define the list of colors
color_list = ["red", "green", "blue", "yellow", "orange", "purple"]

# Define the list of congruent word-color pairs
congruent_pairs = [(color, color) for color in color_list]

# Define the list of incongruent word-color pairs
incongruent_pairs = [(color, other_color) for color in color_list for other_color in color_list if color != other_color]

# Combine congruent and incongruent pairs
word_color_pairs = congruent_pairs + incongruent_pairs

# Randomize the word-color pairs
random.shuffle(word_color_pairs)

# Create a list to store the stimuli
stimuli = []

data = []
# Generate the stimuli sequence without sequential repetitions
for i in range(NUM_STIMULI):
    # Get a random word-color pair from the list
    word_color = random.choice(word_color_pairs)

    # Add the word-color pair to the stimuli list
    stimuli.append(word_color)

    # Remove the selected word-color pair from the list to avoid repetitions
    word_color_pairs.remove(word_color)

    # Add the reversed word-color pair to the list to ensure both congruent and incongruent trials
    word_color_pairs.append((word_color[1], word_color[0]))
    word_color_list = list(word_color)
    # select randomly if alternative has to be displayed on right or left

    alt1= random.choice(word_color)                 # to be displayed on the left
    word_color_list.remove(alt1)
    alt2=word_color_list[0]
    if alt1==word_color[1]:                 # this is the color (correct answer)
        correct_response = 'left'
    else:
        correct_response = 'right'
    data.append([word_color[0].upper(), word_color[1], alt1.upper(), alt2.upper(), correct_response, word_color[0]==word_color[1]])

header = ["stimulus", "colour", "alt1", "alt2", "correctresponse", "congruent"]


filename = "stroop_task_2options.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)





################################ to generate 4 pairs ##################################
data = []
filename = "stroop_task_4options_numbers.csv"
for i in range(NUM_STIMULI):
    # Get a random word-color pair from the list
    word_color = random.choice(word_color_pairs)

    # Add the word-color pair to the stimuli list
    stimuli.append(word_color)

    # Remove the selected word-color pair from the list to avoid repetitions
    word_color_pairs.remove(word_color)

    # Add the reversed word-color pair to the list to ensure both congruent and incongruent trials
    word_color_pairs.append((word_color[1], word_color[0]))

    word_color_list = list(word_color)
    # select randomly if alternative has to be displayed on right or left
    
    for i in range(0, 2):
        added_word = random.choice(color_list)
        while added_word in word_color:
            added_word = random.choice(color_list)
        word_color_list.append(added_word)

    alt1= random.choice(word_color_list)                 # to be displayed on the left
    word_color_list.remove(alt1)

    alt2=random.choice(word_color_list)
    word_color_list.remove(alt2)

    
    alt3=random.choice(word_color_list)
    word_color_list.remove(alt3)


    alt4=word_color_list[0]

    if alt1 == word_color[1]:
        correct_response = '1'
    elif alt2 == word_color[1]:
        correct_response = '2'
    elif alt3 == word_color[1]:
        correct_response = '3'
    else:
        if alt4 == word_color[1]:
            correct_response = '4'

    data.append([word_color[0].upper(), word_color[1], alt1.upper(), alt2.upper(), alt3.upper(), alt4.upper(), correct_response, word_color[0]==word_color[1]])

header = ["stimulus", "colour", "alt1", "alt2", "alt3", "alt4" "correctresponse", "congruent"]



with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(data)
