# -*- coding: utf-8 -*-

############### References: https://github.com/marsja/stroopy/blob/master/stroopy.py

import os
import sys
from psychopy import event, core, data, gui, visual, sound
from fileHandling import *

mistake_sound = sound.Sound('negative-101682.mp3')
level1_file = 'stroop_task_2options.csv'
level1_numbers='stroop_task_4options_numbers.csv'


class Experiment:
    #def __init__(self, num_options, win_color, txt_color, completed_levels=None):
    def __init__(self, win_color, txt_color):
        # stimuli_positions 
        # [0, 0] is to show the question. Will be stored in stimuli_positions[-1]
        
        #if num_options == 2:
        #    self.stimuli_positions = [[-.4, 0], [.4, 0], [0, 0]]
        #if num_options == 4:
        #    self.stimuli_positions = [[-.4, 0], [.4, 0], [0, .4], [0, -.4], [0, 0]]
        self.win_color = win_color
        self.txt_color = txt_color
        #self.completed_levels = completed_levels

    def create_window(self, color=(1, 1, 1)):
        # type: (object, object) -> object
        color = self.win_color
        win = visual.Window(monitor="testMonitor",
                            color=color, fullscr=True)
        return win

    def settings(self, completed_levels):
        """
        completed_levels = levels that the subject has already completed
        """
        # getting current folder
        #_thisDir = os.path.dirname(os.path.abspath(__file__))
        
        remaining_sessions = ['practice', 'level1_2options', 'level1_numbers', 'level2_2options', 'level2_numbers']
        for i in completed_levels:
            remaining_sessions.remove(i)
        """
        if completed_levels is None:
            remaining_sessions = ['practice', 'level1_2options', 'level1_numbers', 'level2_2options', 'level2_numbers']
        elif completed_levels == 'practice':
            print ('practice completed')
            remaining_sessions = ['level1_2options', 'level1_numbers', 'level2_2options', 'level2_numbers']
        elif completed_levels == 'level1':
            remaining_sessions = ['level2']
        """

        experiment_info = {'User_ID': 'user_00x', 'Session': remaining_sessions, 
                           'Language': ['English'], u'date':
                               data.getDateStr(format="%Y-%m-%d_%H-%M-%S")}
                               #u'Saving directory': _thisDir+os.sep+'data_'+data.getDateStr(format="%Y-%m-%d")}
        info_dialog = gui.DlgFromDict(title='Stroop task', dictionary=experiment_info,
                                      fixed=['Experiment Version'])
        experiment_info[u'DataFile'] = 'Data' + os.path.sep + experiment_info['User_ID'] + os.path.sep + experiment_info['date']+'_'+ experiment_info['Session'] + '.csv'
        if info_dialog.OK:
            return experiment_info
        else:
            core.quit()
            return 'Cancelled'

    def create_text_stimuli(self, window, text=None, pos=[0.0, 0.0], name='', color=None):
        '''Creates a text stimulus,
        '''
        if color is None:
            color = self.txt_color
        text_stimuli = visual.TextStim(win=window, ori=0, name=name,
                                       text=text, font=u'Arial',
                                       pos=pos,
                                       color=color, colorSpace=u'rgb')
        return text_stimuli

    def create_trials(self, trial_file, randomization='random'):
        '''Doc string'''
        data_types = ['Response', 'Accuracy', 'RT', 'User_ID']
        with open(trial_file, 'r') as stimfile:
            _stims = csv.DictReader(stimfile)
            trials = data.TrialHandler(list(_stims), 1,
                                       method="sequential")                 #method: ['random', 'sequential', 'fullRandom']:
        [trials.data.addDataType(data_type) for data_type in data_types]

        return trials

    def present_stimuli(self, color, text, position, stim):
        _stimulus = stim
        color = color
        position = position
        #if settings['Language'] == "Swedish":
        #    text = swedish_task(text)
   
        text = text
        _stimulus.pos = position
        _stimulus.setColor(color)
        _stimulus.setText(text) 

    def running_experiment(self, trials, testtype, curr_window, key_list):
        _trials = trials

        # getting the number of alternatives we want to show
        trials_keys = trials.trialList[0].keys()
        num_options = 0
        for key in trials_keys:
            if "alt" in key:
                num_options = num_options +1
        print (num_options)

        testtype = testtype
        timer = core.Clock()

        # this will create "empty" text to show stimuli on main window
        #stimuli = [self.create_text_stimuli(curr_window) for _ in range(num_options+1)]

        for trial in _trials:
            # Fixation cross
            fixation = visual.TextStim(win=curr_window, ori=0, name='',text='+', font=u'Arial',pos=[0.0, 0.0],color="White", colorSpace=u'rgb')
            #fixation = self.present_stimuli(self.txt_color, '+', self.stimuli_positions[-1],
                                            #stimuli[3])
            fixation.draw()
            window.flip()
            core.wait(.6)
            timer.reset()

            # Target word (will occupy center of the screen)
            #target = visual.TextStim(win=curr_window, ori=0, name='',text=trial['stimulus'], 
            #                         font=u'Arial',pos=self.stimuli_positions[-1],color=trial['colour'], colorSpace=u'rgb')
            target_stimuli = visual.TextStim(win=window, ori=0, 
                        name='', text=trial['stimulus'], font=u'Arial',
                        pos=[0.0, 0.5], color=trial['colour'], colorSpace=u'rgb')

            target_stimuli.height = 0.5
            target_stimuli.draw()
            """
            for i in range(0, num_options):
                #print(trial['alt'+str(i+1)])
                #print (self.stimuli_positions[i])
                #print (stimuli[i+1])
                #alt=self.present_stimuli(self.txt_color, trial['alt'+str(i+1)],
                                        #self.stimuli_positions[i], stimuli[i+1])
                alt = visual.TextStim(win=curr_window, ori=0, name='',text=trial['alt'+str(i+1)], 
                                     font=u'Arial',pos=self.stimuli_positions[i], color=self.txt_color, colorSpace=u'rgb')
                alt.draw()
            """
            count = 1
            delta_horizontal = window.size[0] / (num_options //2)
            for i in range(-num_options //2, num_options//2):
                w_pos_pixel = delta_horizontal//2 + i*delta_horizontal
                w_pos_norm = w_pos_pixel / window.size[0]

                alt_stimuli = visual.TextStim(win=window, ori=0, 
                                    name='', text=trial['alt'+str(count)], font=u'Arial',
                                    pos=[w_pos_norm, -0.4], color="White", colorSpace=u'rgb')
                if num_options == 2:
                    alt_stimuli.height = target_stimuli.height / 2 
                elif num_options == 4:
                    alt_stimuli.height = target_stimuli.height / 4

                alt_stimuli.draw()
                count = count +1
            window.flip()

            
            # note: for now m == right
            #               x == left
            
            if testtype == 'practice':
                keys = event.waitKeys(keyList=key_list)
                resp_time = timer.getTime()
                absTimer= core.getAbsTime()                    #this returns the whole seconds elapsed since whole seconds elapsed since Jan 1, 1970
                if keys[0] != trial['correctresponse']:
                    text_stimuli = visual.TextStim(window,text='WRONG', wrapWidth=1.2,alignHoriz='center', color='White',
                    alignVert='center', height=0.06)
                    text_stimuli.draw()
                    #instruction_stimuli['incorrect'].draw()
                    trial['Accuracy'] = 0

                else:
                    text_stimuli = visual.TextStim(window,text='CORRECT', wrapWidth=1.2,alignHoriz='center', color='White',
                    alignVert='center', height=0.06)
                    text_stimuli.draw()
                    #instruction_stimuli['right'].draw()
                    trial['Accuracy'] = 1
                
                trial['RT'] = resp_time
                trial['TimeStamp'] = absTimer
                print (trial['RT'])
                trial['Response'] = keys[0]
                trial['User_ID'] = settings['User_ID']
                print ('saving')
                write_csv(settings[u'DataFile'], trial)

                window.flip()
                core.wait(2)

            if testtype == 'test':
                mistake_sound.stop()
                #keys = event.waitKeys(keyList=['left', 'right', 'up', 'down'])
                keys = event.waitKeys(keyList=key_list)
                resp_time = timer.getTime()
                absTimer= core.getAbsTime()
                if keys[0] != trial['correctresponse']:
                    text_stimuli = visual.TextStim(window,text='X', wrapWidth=1.2, alignHoriz='center', color='Red',
                    alignVert='center', height=2)
                    text_stimuli.draw()
                    mistake_sound.play()
                    #instruction_stimuli['incorrect'].draw()
                    trial['Accuracy'] = 0

                else:
                    text_stimuli = visual.TextStim(window,text='CORRECT', wrapWidth=1.2,alignHoriz='center', color='White',
                    alignVert='center', height=0.06)
                    text_stimuli.draw()
                    #instruction_stimuli['right'].draw()
                    trial['Accuracy'] = 1
                
                trial['RT'] = resp_time
                print (trial['RT'])
                trial['TimeStamp'] = absTimer
                trial['Response'] = keys[0]
                trial['User_ID'] = settings['User_ID']
                print ('saving')
                write_csv(settings[u'DataFile'], trial)

                window.flip()
                core.wait(2)

            if testtype == 'test2':
                mistake_sound.stop()
                keys = event.waitKeys(maxWait=1, keyList=key_list)
                resp_time = timer.getTime()
                absTimer= core.getAbsTime()
                if keys is None:
                    text_stimuli = visual.TextStim(window,text='X', wrapWidth=1.2, alignHoriz='center', color='Red',
                    alignVert='center', height=2)
                    text_stimuli.draw()
                    mistake_sound.play()
                    #instruction_stimuli['incorrect'].draw()
                    trial['Accuracy'] = 0
                
                elif keys[0] != trial['correctresponse']:
                    text_stimuli = visual.TextStim(window,text='X', wrapWidth=1.2, alignHoriz='center', color='Red',
                    alignVert='center', height=2)
                    text_stimuli.draw()
                    mistake_sound.play()
                    #instruction_stimuli['incorrect'].draw()
                    trial['Accuracy'] = 0

                else:
                    text_stimuli = visual.TextStim(window,text='CORRECT', wrapWidth=1.2,alignHoriz='center', color='White',
                    alignVert='center', height=0.06)
                    text_stimuli.draw()
                    #instruction_stimuli['right'].draw()
                    trial['Accuracy'] = 1
                
                trial['RT'] = resp_time
                trial['TimeStamp'] = absTimer
                print (trial['RT'])
                if keys is not None:
                    trial['Response'] = keys[0]
                else:
                    trial['Response'] = ['expired']
                trial['User_ID'] = settings['User_ID']
                print ('saving')
                write_csv(settings[u'DataFile'], trial)

                window.flip()
                core.wait(2)

            event.clearEvents()
            print(f"keys: {keys}")
            #if 'q' in keys:
                #print(f"breaking because keys: {keys}")
                #break


def create_instructions_dict(instr):
    start_n_end = [w for w in instr.split() if w.endswith('START') or w.endswith('END')]
    keys = {}

    for word in start_n_end:
        key = re.split("[END, START]", word)[0]

        if key not in keys.keys():
            keys[key] = []

        if word.startswith(key):
            keys[key].append(word)
    return keys


def create_instructions(input, START, END, color="Black"):
    instruction_text = parse_instructions(input, START, END)
    print(instruction_text)
    
    text_stimuli = visual.TextStim(window, text=instruction_text, wrapWidth=1.2,
                                   alignHoriz='center', color=color,
                                   alignVert='center', height=0.06)
    
    return text_stimuli


def display_instructions(start_instruction=''):
    # Display instructions

    if start_instruction == 'Practice':
        instruction_stimuli['instructions'].pos = (0.0, 0.5)
        instruction_stimuli['instructions'].draw()

        positions = [[-.2, 0], [.2, 0], [0, 0]]
        examples = [experiment.create_text_stimuli(window) for pos in positions]
        example_words = ['green', 'blue', 'green']
        #if settings['Language'] == 'Swedish':
        #    example_words = [swedish_task(word) for word in example_words]

        for i, pos in enumerate(positions):
            examples[i].pos = pos
            if i == 0:
                examples[0].setText(example_words[i])
            elif i == 1:
                examples[1].setText(example_words[i])
            elif i == 2:
                examples[2].setColor('Green')
                examples[2].setText(example_words[i])

        [example.draw() for example in examples]

        instruction_stimuli['practice'].pos = (0.0, -0.5)
        instruction_stimuli['practice'].draw()   

    if start_instruction == 'Practice_end':
        instruction_stimuli['donepractice'].draw()
    elif start_instruction == 'Test':
        instruction_stimuli['test'].draw()

    elif start_instruction == 'End':
        instruction_stimuli['done'].pos = (0.0, 0.5)
        instruction_stimuli['done'].draw()

    window.flip()
    key_pressed=event.waitKeys(keyList=['space'])
    event.clearEvents()

    return key_pressed



if __name__ == "__main__":
    completed_sessions = []
    possible_session = ['practice', 'level1_2options', 'level1_numbers', 'level2_2options', 'level2_numbers']


    _codeDir = os.path.dirname(os.path.abspath(__file__))

    instruction_file = _codeDir + os.sep + "INSTRUCTIONS.txt"

    practice_file = _codeDir + os.sep + "practice_list.csv"
    level_2options = _codeDir + os.sep + "stroop_task_2options.csv"
    level_4options = _codeDir + os.sep + "stroop_task_4options_numbers.csv"
    
    background = "Black"
    back_color = (0, 0, 0)
    textColor = "White"
    experiment = Experiment(win_color=background,txt_color=textColor)

    settings = experiment.settings(completed_levels=[])
    #session = print (settings['Session'])
    language = settings['Language']

    
    # Read the txt file
    instructions = read_instructions_file(instruction_file, language, language + "End")
    #Create a dictionary to store keywords in the txt file to distinguish between different phases
    instructions_dict = create_instructions_dict(instructions)
    instruction_stimuli = {}

    
    window = experiment.create_window(color=back_color)
    for inst in instructions_dict.keys():
        instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
        # instruction_stimuli will store the text to display for each phase
        instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)
    print ('instructions created')

    # We don't want the mouse to show:
    event.Mouse(visible=False)

    text_color = (1, 1, 1)
    
    if (settings['Session'] == 'practice'):
        # Display instructions for practice round
        key_pressed=display_instructions(start_instruction='Practice')
        #for i in key_pressed:
        #    while i != 'space':
        #        key_pressed = alert_for_wrong_key()
        #        print (key_pressed)

        practice = experiment.create_trials(practice_file)
        experiment.num_options = 2
        fixation = experiment.running_experiment(practice, testtype='practice', curr_window=window, key_list=['left', 'right'])

        key_pressed=display_instructions(start_instruction='End')
        #print(key_pressed)
        #for i in key_pressed:
        #    while i != 'space':
        #        key_pressed = alert_for_wrong_key()
        #        print (key_pressed)
        window.close()   

    
    # once this session has been completed, display again window to select new level

    settings = experiment.settings(completed_levels=['practice'])

    if (settings['Session'] == 'level1_2options'):
        window = experiment.create_window(color=back_color)
    
        for inst in instructions_dict.keys():
            instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
 
            instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)
        
        practice = experiment.create_trials(level_2options)
        experiment.running_experiment(practice, testtype='test', curr_window=window, key_list=['left', 'right'])
        key_pressed=display_instructions(start_instruction='End')
        window.close()
        settings = experiment.settings(completed_levels=['practice', 'level1_2options'])


    if (settings['Session'] == 'level1_numbers'):
        window = experiment.create_window(color=back_color)
    
        for inst in instructions_dict.keys():
            instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]

            instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)
        
        practice = experiment.create_trials(level_4options)
        experiment.running_experiment(practice, testtype='test', curr_window=window, key_list=['1', '2', '3', '4'])
        key_pressed=display_instructions(start_instruction='End')
        window.close()
        settings = experiment.settings(completed_levels=['practice', 'level1_2options', 'level1_numbers'])
        


    if (settings['Session'] == 'level2_2options'):
        window = experiment.create_window(color=back_color)
        for inst in instructions_dict.keys():
            instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]
            instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)
        practice = experiment.create_trials(level_2options)
        experiment.running_experiment(practice, testtype='test2', curr_window=window, key_list=['right', 'left'])
        window.close()
        settings = experiment.settings(completed_levels=['practice', 'level1_2options', 'level1_numbers', 'level2_2options'])
        
    if (settings['Session']=='level2_numbers'):
        window = experiment.create_window(color=back_color)
    
        for inst in instructions_dict.keys():
            instruction, START, END = inst, instructions_dict[inst][0], instructions_dict[inst][1]

            instruction_stimuli[instruction] = create_instructions(instructions, START, END, color=textColor)
        
        practice = experiment.create_trials(level_4options)
        experiment.running_experiment(practice, testtype='test2', curr_window=window, key_list=['1', '2', '3', '4'])
        key_pressed=display_instructions(start_instruction='End')
        window.close()


        
    key_pressed=display_instructions(start_instruction='End')
    window.close()
    
