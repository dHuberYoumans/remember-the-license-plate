import numpy as np
import time
import os
from sys import platform

# TO DO: 
# implement 3-tier architecture Presentation, Logic, Data
# implement option to save score to a .txt file 
# documentation
# proper error handlng for usr input
# GUI
# more modes:
# sudden-death: go until first miss
# free practice: go on as long as you want to (maybe option to simply train 1,2 or mixed)
# survival: ends after 3 misses also gain life after 5 correct in a row?
# implement international license plates
# when wrong guess, not only show correct answer but also wrong guess

# PRESENTATION TIER
# string for clearing (console) cmd
class SysCmd:
    def __init__(self):
        if platform.startswith('darwin'):
            self.clear = 'clear'
        elif platform.startswith('win32'):
            self.clear = 'cls'

    def clear_prompt(self):
        """ clear the command line """
        os.system(self.clear)

    def pause(self,t):
        time.sleep(t)


class Babel:
    def __init__(self,char):
        if char == 'latin':
            self.script = dict(zip([i for i in range(1,27)],'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()))

    def rnd_letter(self):
        """ generate a random letter """
        return self.script[np.random.randint(1,len(self.script))]

def rnd_number():
    """ generate a random integer between 0 and 9 """
    return str(np.random.randint(0,10))

class LicensePlate:
    def __init__(self,alph):
        self.alphabet=alph

    def generate_rnd_plate(self):
        """ generate a random license plate according to the rules which apply in Germany """
        unit_one = []
        unit_two = []
        unit_three = []
            
        for i in range(1,np.random.randint(2,5)): #range and randint both work with half open intervals [a,b)
            unit_one.append(self.alphabet.rnd_letter()) 

        for i in range(1,np.random.randint(2,4)):
            unit_two.append(self.alphabet.rnd_letter())

        for i in range(1,np.random.randint(4,6)):
            unit_three.append(rnd_number())
        
        self.lp = ''.join(unit_one + ['-'] + unit_two + ['-'] + unit_three)
        if len(self.lp) <= 10 and len(self.lp) > 0:
            return self.lp
        else:
            return self.generate_rnd_plate()
        
    def generate_plate(self, u_one:int, u_two:int, u_three:int):
        """ 
        generates a license plate with 
        
        u_one = 1,2 or 3 (random) characters in unit 1

        u_two = 1 or 2 (random) charactrs in unit 2

        u_three = 1,2,3, or 4 (random) digits in unit 3
        """
        if not all(isinstance(x,int) for x in [u_one,u_two,u_three]):
             raise TypeError("TypeError: All parameters must be integers.")
        
        if u_one + u_two + u_three > 8:
            raise Exception("The values you provide do not generate a vaild license plate.")
        
        unit_one = []
        unit_two = []
        unit_three = []
            
        for i in range(1,u_one+1): #range and randint both work with half open intervals [a,b)
            unit_one.append(self.alphabet.rnd_letter()) 

        for i in range(1,u_two+1):
            unit_two.append(self.alphabet.rnd_letter())

        for i in range(1,u_three+1):
            unit_three.append(rnd_number())
        
        self.lp = ''.join(unit_one + ['-'] + unit_two + ['-'] + unit_three)
        if len(self.lp) <= 10 and len(self.lp) > 0:
            return self.lp
        
# initialize classes needed
sys_cmd = SysCmd()
alphabet = Babel('latin')      
license_plate = LicensePlate(alphabet)
    
def get_kfz(str):
    """ get a guess for a license plate from user """
    try:
        kfz = input(str).lower().replace('-','').replace(' ','')
    except AttributeError: # if one wants to skip the license plate, one is asked to  hit enter returning a NoneType objet. This raises an AttributeError in get_answer_one().lower()
        kfz = 'skipped'
    
    if len(kfz) < 4 and len(kfz) > 0 or len(kfz) > 8:
        print('\nBitte gib ein gültiges Kennzeichen ein.')
        print('Ein Kennzeichen muss mindestens 6 Zeichen beinhalten.')
        print('Wenn du dieses Kennzeichen überspringen möchtest, tippe Enter \n')
        return get_kfz(str)
    else:
        return kfz 
    
def get_answer_one():
    """ get user answer for 1 plate """
    return get_kfz('Kfz-Kennz.: ')

def get_answer_two():
    """ get user answer for 2 plates """
    kfz_one = get_kfz('Kfz-Kennz. 1/2: ')
    kfz_two = get_kfz('Kfz-Kennz. 2/2: ')

    return [kfz_one,kfz_two]

def weiter_machen(score,t):
    """ ask the user if they want to continue playing or if they want to see their current score  """
    global miss
    global total

    while True:
        weiter = input('Möchtest Du weiter machen? Ja/Nein/Score/Beenden [j/n/s/exit]: ')

        if weiter.lower() == 'j':
            score.append(test(t,score))
        elif weiter.lower()=='n':
            print(f'Score: {total-miss}/{total}')
            print(f'Highscore: {max(score)}')
            input()
            return False
            
        elif weiter.lower() == 's':
            sys_cmd.clear_prompt()
            print(f'Score: {total - miss}/{total}')
            print(f'Highscore: {max(score)}')
            return weiter_machen(score,t)
        elif weiter.lower() == 'exit':
            sys_cmd.clear_prompt()
            print(f'Score: {total-miss}/{total}')
            print(f'Highscore: {max(score)}')
            print('Bis zum nächsten Mal!')
            exit()
        
        
def test_one(t,run,score,mode):
    global miss
    global total

    total += 1

    sys_cmd.clear_prompt()
    print('Fertig?')
    sys_cmd.pause(1)
    print('Los!')
    sys_cmd.pause(1)
    
    lp = license_plate.generate_rnd_plate()
    sys_cmd.clear_prompt()

    # show license plate and remaining display time
    for i in range(0,t):
        print(f'{lp:<20}{t-i:02d}', end='\r')
        sys_cmd.pause(1)

    sys_cmd.clear_prompt()

    kfz = get_answer_one()
    
   
    if kfz == lp.lower().replace('-','').replace(' ',''):
        run += 1
        print('Korrekt!')
        print(f'Score: {total-miss}/{total}\n')
        if mode == 'training':
            return run
        elif mode == 'test':
            return run, True
    else:
        miss += 1
        print(f'Schade! Richtig wäre gewesen')
        print(f'\n{lp}\n')
        print('Versuch es nochmal!')
        print(f'Score: {total-miss}/{total}')
        print(f'Highscore: {max(score)}')

        if mode == 'training':
            return run
        elif mode == 'test':
            return run, False
    
def test_two(t,run,score):
    global total
    global miss

    total += 2

    sys_cmd.clear_prompt()
    print('Fertig?')
    sys_cmd.pause(1)
    print('Los!')
    sys_cmd.pause(1)
    sys_cmd.clear_prompt()

    lp = [license_plate.generate_rnd_plate(),license_plate.generate_rnd_plate()]
    for i in range(0,t): 
        print(lp[1] + '          {:02d}'.format(t-i))
        print(lp[0])
        sys_cmd.pause(1)
        sys_cmd.clear_prompt()
 
    lpp = [s.lower().replace('-','').replace(' ','') for s in lp]
    sys_cmd.pause(t)
    sys_cmd.clear_prompt()

    kfz = [s for s in get_answer_two()]

    if kfz[0] in lpp and kfz[1] in lpp:
        run += 2
        print('Stark! 2/2 korrekt!')
        print(f'Score: {run}\n')
        sys_cmd.pause(1)
        return run, True
    elif (kfz[0] in lpp and kfz[1] not in lpp) or (kfz[0] not in lpp and kfz[1] in lpp):
        run += 1
        miss += 1
        print('Fast! 1/2 richtig!')
        if kfz[1] not in lpp:
            print(f'Das zweite Kennzeichen wäre {kfz[0]} gewesen.')
        else:
            print(f'Das zweite Kennzeichen wäre {kfz[1]} gewesen.')
        print(f'Score: {total-miss}/{total}\n')
        sys_cmd.pause(1)
        
        return run, True
    else:
        miss += 2
        print('Schade. Die Kennzeichen waren')
        print('')
        print(lp[0])
        print(lp[1])
        print('')
        print('Gleich nochmal!')
        print(f'Score: {total-miss}/{total}')
        print(f'Highscore: {max(score)}')
        return run, False

 
def test(t,score):
    global total

    run = 0
    b = True

    while b:
        if run <10:
            run, b = test_one(t,run,score,'test')
            if run == 10:
                print('Sehr gut! 1 Kennzeichenn ist wohl zu einfach - wie wäre es mit 2?')
                sys_cmd.pause(2)
        else:
            sys_cmd.clear_prompt()
            run, b = test_two(t,run,score)
        

    return run

def get_time(str):
    try:
        return int(str)
    except ValueError:
        return get_time(input('Bitte gebe eine ganze Zahl ein: '))

def training(t,run,score,option):

    if option == 1:
        global total
        
        print('\nGo! (enter)')
        print('Hauptmenu (quit)')
        go_or_quit = input()
        if  go_or_quit == '':
            run = test_one(t,run,score,'training')
            training(t,run,score,1)

        elif go_or_quit == 'quit':
            return False
                

    if option == 2:
        # train_two(score,t)
        print('under construction')


def main(): 
    global miss
    global total
    

    while True:
        sys_cmd.clear_prompt()
        print('Hi! Warum bist Du hier?')
        print('1. Zum Üben')
        print('2. I mean Buisness')
        print('3. Ende\n')

        option = input()

        if option == '1':
            mode = 'training'
        elif option == '2':
            mode = 'test'
        else:
            sys_cmd.clear_prompt()
            print('Bis zum nächsten Mal!')
            exit()
        
        if mode == 'test':
            total = 0
            miss = 0
            run = 0
            score = [0]
            b = True

            while b:
                sys_cmd.clear_prompt()
                print('Du bist also für Buisness hier? Nagut!')
                t = get_time(input('Wie wie viele Sekunden möchtest Du Zeit haben? '))
                score.append(test(t,score))

                b = weiter_machen(score,t)

        elif mode == 'training':
            total = 0
            miss = 0
            run = 0
            score = [0]

            sys_cmd.clear_prompt()
            print('Willkommen im Übungslager.\n')
            print('Was würdest Du gerne Trainieren?')
            print('1. 1 Kfz-Kennzeichen')
            print('2. 2 Kfz-Kennzeichen\n')
            try:
                option = int(input('Option: '))
            except ValueError:
                print('Bitte gebe 1 oder 2 ein.')
            t = get_time(input('Wie wie viele Sekunden möchtest Du Zeit haben? '))

            training(t,run,score,option)
    
        
    
        
  

if __name__ == '__main__':
    main()

