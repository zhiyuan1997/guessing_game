#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Helper functions
import time    
def unpack_file(file):
    '''
    This function read's a file's content that are separated by return and 
    returns a list of the file's raw content.
    
    param file:       .txt file containing raw data separated by the return key
    return file_list: list of file context
    rtype:            string
    '''
    file_list=[]
    count=0
    for line in file:
        #remove new space character
        file_list.append(line.lower().strip('\n'))
    #return cleaned lists    
    return file_list

def reset_variables(game_variables,possible_words):
    '''
    This function resets a user's game variables.
    param game_variables: Dictionary that contain's a user's past game variables. 
    param possible_words: Possible words that can be set at the right answer.
    return:                None
    '''
    #1.) Get random word
    random_number= random.randint(0, len(possible_words)-1)
    game_variables['answer']= possible_words[random_number]
    #print(game_variables['answer'])
    #2.) Reset user feedback 
    user_feedback=[]
    for i in range(len(game_variables['answer'])):
        user_feedback.append('_')
        game_variables['user_feedback']=user_feedback
    #3.) Reset past guesses
    game_variables['past_guess']=[]
    #4.) Reset game end status
    game_variables['game_end']=None
    #5.) Reset initial money to 1200
    game_variables['prize_money']= 1200
    
    return 0


def draw_progress_bar(game_variables):
    '''
    This function draws a progress bar based on the number of letters a user has guessed correctly'
    return: progress bar drawn using string elements
    rtype: string
    '''
    user_feedback=game_variables['user_feedback']
    dash_count=0
    loading_string='['
    #get number of unguessed letters
    for i in range(len(user_feedback)):
        if user_feedback[i] == '_':
            dash_count+=1
    #fill in progress bar for number of guessed letters
    for i in range(len(user_feedback)-dash_count):
        loading_string+='='
    #leave progress bar blank for number of unguessed letters
    for i in range(dash_count):
        loading_string+=" "
    loading_string+=']'

    return loading_string

def wheel_spin():
    '''
    This function imitates spinning a game wheel. 
    
    return: Result of the wheel spin
    rtype: string/int
    '''
    print('Wheel is spinning!')
    for i in range(3):
        print('.\n')
        time.sleep(0.2)
        
    wheel=[-1,100,100,100,100,100,-1,2,200,200,200,200,200,-1,4,400,400,400,-1,8,800,800,-1,10000,-1]
    random_number= random.randint(0, len(wheel)-1)

    return wheel[random_number]

def process_guess(game_variables):
    '''
    This function checks if a user's guess is a letter or word and compares the guess to the answer.
    Based on the result of the comparison, the function then sets the user visual, next game state, and number of
    remaining guesses.
    
    param game_variables: Dictionary that stores the game variables: number of guesses remaining, correct word to
                          guess, current guess, number of wins, number of losses.
                          
    return game_status : Next state of the game. 
    rtype:               int
    
    '''
    spin_result=wheel_spin()
    #print(spin_result)
    #check if user guess is word or letter
    if len(game_variables['guess']) > 1: #user guessed a word
        if str(game_variables['guess']) == str(game_variables['answer']): #correct word!
            is_correct=1
            next_state= 3 #end current game
            game_variables['game_end']=1
            game_variables['wins']+=1
            
            #update user feedback
            for i in range(len(game_variables['guess'])):
                game_variables['user_feedback'][i]= game_variables['guess'][i]
                
        else:#incorrect
            is_correct=0
            next_state=2
            #game_variables['guess_n']-=1 #incorrect guess, decrement remaining tries
      
    else: #user guessed a letter
        if game_variables['guess'] in game_variables['answer']:#user correctly guessed a letter in the word
            is_correct=1
            #update user response to display additional correct letter
            for i in range(len(game_variables['answer'])):
                if str(game_variables['guess']) == str(game_variables['answer'][i]):
                    game_variables['user_feedback'][i]= game_variables['guess']
            #check if word is complete 
            if '_' in game_variables['user_feedback']:#not complete
                next_state=2 #still in the middle of the game
            else:#complete
                next_state=3 #game over (winner)
                game_variables['game_end']=1
                game_variables['wins']+=1
                
        else: #incorrect 
            is_correct=0
            next_state=2
            #game_variables['guess_n']-=1
            
    '''
    if game_variables['guess_n'] == 0: #check if the user still has guesses available
        next_state=3 #game over (loser)
        game_variables['game_end']=0
        game_variables['losses']+=1
    elif next_state == 0: #game logic so far has not set game state
        next_state=2
    '''
    if spin_result>0:#+/- amount
        if is_correct:
            print("Congratulations. You guessed a correct letter and the wheel landed on : $%i" % spin_result)
            game_variables['prize_money']+=spin_result
        else:
            print("Probably not congratulations. The wheel landed on  : $%i" % spin_result,'but you guessed wrong!')
    else:#bankrunpt
        print('BANKRUPT!')
        game_variables['prize_money']=0
    return next_state


# In[5]:


#read file content into list
file= open('words_alpha.txt')
possible_words= unpack_file(file)
file.close()


# In[8]:


import random
'''
The guessing game uses a moore machine to keep track of the state of the game.
The game_status stores the value of the actual state machine. 
0 --> Terminate Script 
1 --> New Game
2 --> Middle of current game
3 --> End of current game 
'''
'''
#Ask for the number of players 
while 1:
    player_n= input('Enter the number of players playing:').strip().lower()
    #make sure user inputted number
    if player_n.isdigit():#valid
        break  
    else:#invalid
        print("Please enter a valid number.")
        
#initiliaze user variables dictionary for each user:
for i in range(player_n):
    name='Player'+str(i)
'''
#initialize game variables 
total_prize=0
game_status=1 #set game status to a new game
game_variables={} #intialize dictionary to store game variables
game_variables['wins']=0 #initialize wins to 0
game_variables['losses']=0 #initialize losses to 0


while game_status!=0:
    
    if game_status == 1: #New game
        #initialize game variables 
        reset_variables(game_variables, possible_words)
        #set next state
        game_status=2
         
    elif game_status == 2: #Middle of current game
        #Display the current game variables (user feedback, guesses remaining) after the last guess
        #print(f"\nYou have %i guesses left." % game_variables['guess_n'])
        print("\nPrize Money:",game_variables['prize_money'])
        print("Based on your past guesses, this is what the word looks like:")
        print(' '.join([char for char in game_variables['user_feedback']]))
        print(draw_progress_bar(game_variables))
        #1.) Get new valid user guess
        valid_guess = 0
        while valid_guess == 0:
            game_variables['guess']= input('Guess a letter in the word or the actual word to spin the wheel:').strip().lower()
            valid_guess=1 #first assume guess is valid
            for char in game_variables['guess']:#make sure all chars in word are letters
                if char.isdigit():
                    print('\nInvalid char inputted >:(')
                    valid_guess=0 #digit detected, guess isn't valid
                    break     
            if game_variables['guess'] in game_variables['past_guess']:#guess has already been made
                print('\nYou already guessed this word!')
                valid_guess=0
            
            else: #guess hasn't been made
                game_variables['past_guess'].append(game_variables['guess']) 

        #2.) Process the guess 
        game_status= process_guess(game_variables) 
        

    elif game_status == 3: #End of current game 
        if game_variables['game_end'] ==1: #winner!
            print("\nCongratulations you guessed the correct word: ", game_variables['answer'])
        else: #loser
            print("\nYou didn't guess the word. The correct word was: ",game_variables['answer'])
        #Display the final game variables 
        #print(f"You have %i guesses left." % game_variables['guess_n'])
        print("\nPrize Money:",game_variables['prize_money'])
        print("Based on your past guesses, this is what the word looks like:")
        print(' '.join([char for char in game_variables['user_feedback']]))
        print(draw_progress_bar(game_variables))
        #Ask if user wants to play again
        valid_response =0
        while valid_response == 0: 
            play_again = input("Do you want to play again? (y/n)").lower().strip()
            if play_again == 'y':
                total_prize+=game_variables['prize_money']
                valid_response = 1
                #set game status accordingly
                game_status=1
            elif play_again == 'n':
                total_prize+=game_variables['prize_money']
                valid_response = 1
                #set game status accordingly
                game_status=0
                print("\nThanks for playing you won %i time(s) for a total of  $%i dollars" % (game_variables['wins'],total_prize))
                
    else:
        print("The program should never reach here ")
        
        
        
        
    

