import numpy as np
import time
import os
from sys import platform

# TO DO: 
# documentation
# proper error handlng for usr input
# GUI
# more modes:
# sudden-death: go until first miss
# free practice: go on as long as you want to (maybe option to simply train 1,2 or mixed)
# survival: ends after 3 misses also gain life after 5 correct in a row?


# some error handling
# if wrong, show the correct license plate
# timer


alphabet = dict(zip([i for i in range(1,27)],'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()))

# string for clearing (console) cmd
if platform.startswith('darwin'):
    clear = 'clear'
elif platform.startswith('win32'):
    clear = 'cls'

def clear_prompt():
    os.system(clear)

def pause(t):
    time.sleep(t)

def rnd_letter():
    return alphabet[np.random.randint(1,26)]

def rnd_number():
    return str(np.random.randint(0,10))

def license_plate():
    lp = []
    for i in range(1,np.random.randint(2,5)): #range and randint both work with half open intervals [a,b)
        lp.append(rnd_letter())

    lp.append('-')

    for i in range(1,np.random.randint(2,4)):
        lp.append(rnd_letter())

    lp.append('-')

    for i in range(1,np.random.randint(4,6)):
        lp.append(rnd_number())
    
    lp = ''.join(lp)
    if len(lp) <= 10 and len(lp) > 0:
        return lp
    else:
        return license_plate()
    
def get_kfz(str):
    try:
        kfz = input(str).lower().replace('-','').replace(' ','')
    except AttributeError: # if one wants to skip the license plate, one is asked to  hit enter returning a NoneType objet. This raises an AttributeError in get_answer_one().lower()
        kfz = 'skipped'
    
    if len(kfz) < 6 and len(kfz) > 0 or len(kfz) > 8:
        print('\nBitte gib ein gültiges Kennzeichen ein.')
        print('Ein Kennzeichen muss mindestens 6 Zeichen beinhalten.')
        print('Wenn du aufhören möchtest, tippe Enter \n')
        return get_kfz(str)
    else:
        return kfz 
    
def get_answer_one():
    get_kfz('Kfz-Kennz.: ')

def get_answer_two():
    kfz_one = get_kfz('Kfz-Kennz. 1/2: ')
    kfz_two = get_kfz('Kfz-Kennz. 2/2: ')

    return [kfz_one,kfz_two]

def weiter_machen(score,t):
    global miss
    global total

    while True:
        weiter = input('Möchtest Du weiter machen? ja/nein/score/highscore [j/n/s/h]\n')

        if weiter.lower() == 'j':
            score.append(test(t))
        elif weiter.lower() == 'n':
            clear_prompt()
            print(f'Score: {total-miss}/{total}')
            print(f'Highscore: {max(score)}')
            print('Bis zum nächsten Mal!')
            exit()
        elif weiter.lower() == 's':
            print(f'Score: {total - miss}/{total}')
            return weiter_machen(score,t)
        elif weiter.lower() == 'h':
            print(f'Highscore: {max(score)}')
            return weiter_machen(score,t)
        
def test_one(t,run):
    global miss
    global total

    total += 1

    clear_prompt()
    print('Fertig?')
    pause(1)
    print('Los!')
    pause(1)
    
    
    lp = license_plate()
    clear_prompt()

    # show license plate and remaining display time
    for i in range(0,t):
        print(lp + '          {:02d}'.format(t-i), end='\r')
        pause(1)

   
    kfz = get_answer_one()
   
    if kfz == lp.lower().replace('-','').replace(' ',''):
        run += 1
        print('Korrekt!')
        print(f'Score: {total-miss}/{total}\n')
        pause(1)
        return run, True
    else:
        miss += 1
        print(f'Schade! Richtig wäre gewesen')
        print(f'\n{lp}\n')
        print('Versuch es nochmal!')
        print(f'Score: {total-miss}/{total}')
        return run, False
    
def test_two(t,run):
    global total
    global miss

    total += 2

    clear_prompt()
    print('Fertig?')
    pause(1)
    print('Los!')
    pause(1)
    clear_prompt()

    lp = [license_plate(),license_plate()]
    for i in range(0,t): 
        print(lp[1] + '          {:02d}'.format(t-i))
        print(lp[0])
        pause(1)
        clear_prompt()
 
    lpp = [s.lower().replace('-','').replace(' ','') for s in lp]
    pause(t)
    clear_prompt()

    kfz = [s for s in get_answer_two()]

    if kfz[0] in lpp and kfz[1] in lpp:
        run += 2
        print('Stark! 2/2 korrekt!')
        print(f'Score: {run}\n')
        pause(1)
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
        pause(1)
        
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
        return run, False

 
def test(t):
    global total

    run = 0
    b = True

    while b:
        if run <10:
            run, b = test_one(t,run)
            if run == 10:
                print('Sehr gut! 1 Kennzeichenn ist wohl zu einfach - wie wäre es mit 2?')
                pause(2)
        else:
            clear_prompt()
            run, b = test_two(t,run)
        

    return run

def get_time(str):
    try:
        return int(str)
    except ValueError:
        return get_time(input('Bitte gebe eine ganze Zahl ein: '))

def main(): 
    score = []

    t = get_time(input('Hi! Wie wie viele Sekunden möchtest Du Zeit haben?\n\n'))
    
    b = True
    global miss
    global total
    miss = 0
    total = 0

    score.append(test(t))
        
    weiter_machen(score,t)
        
  

if __name__ == '__main__':
    main()

