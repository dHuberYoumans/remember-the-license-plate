import numpy as np
import time
import os
from sys import platform

# TO DO: 
# documentation
# proper error handlng in usr input
# GUI
# more modes:
# sudden-death: go until first miss
# free practice: go on as long as you want to (maybe option to simply train 1,2 or mixed)
# survival: ends after 3 misses also gain life after 5 correct in a row?


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
    
def get_answer_one():
    return input('Kfz-Kennz.: ')

def get_answer_two():
    kfz_one = input('Kfz-Kennz. 1/2: ')
    kfz_two = input('Kfz-Kennz. 2/2: ')

    return [kfz_one,kfz_two]

def weiter_machen(score,t):
    global miss
    global total

    b = True
    while b:
        weiter = input('Möchtest Du weiter machen? ja/nein/score/highscore [j/n/s/h]\n')

        if weiter.lower() == 'j':
            score.append(test(t))
        elif weiter.lower() == 'n':
            clear_prompt()
            print(f'Score: {total-miss}/{total}')
            print(f'Highscore: {max(score)}')
            print('Bis zum nächsten Mal!')
            b = False
        elif weiter.lower() == 'h':
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
    print('\nFertig?')
    pause(1)
    print('Los!')
    pause(1)
    clear_prompt()

    lp = license_plate()
    print(lp)
    pause(t)
    clear_prompt()

    kfz = get_answer_one().lower().replace('-','').replace(' ','')

    if kfz == lp.lower().replace('-','').replace(' ',''):
        run += 1
        print('Korrekt!')
        print(f'Score: {total-miss}/{total}\n')
        pause(1)
        return run, True
    else:
        miss += 1
        print('Versuch es nochmal!')
        print(f'Score: {total-miss}/{total}')
        return run, False
    
def test_two(t,run):
    global total
    global miss

    total += 2

    clear_prompt()
    print('\nFertig?')
    pause(1)
    print('Los!')
    pause(1)
    clear_prompt()

    lp = [license_plate(),license_plate()]
    print(lp[0])
    print(lp[1])
    lpp = [s.lower().replace('-','').replace(' ','') for s in lp]
    pause(t)
    clear_prompt()

    kfz = [s.lower().replace('-','').replace(' ','') for s in get_answer_two()]

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
        print(f'Score: {total-miss}/{total}\n')
        pause(1)
        
        return run, True
    else:
        miss += 2
        print('Schade. Gleich nochmal!')
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

def main(): 
    score = []
    t = int(input('Hi! Wie wie viele Sekunden möchtest Du Zeit haben?\n\n'))
    b = True
    global miss
    global total
    miss = 0
    total = 0

 
    score.append(test(t))
        
    weiter_machen(score,t)
        
  

main()
# WHY DOES THIS NOT WORK?
    
# if __name__ == "__main__ ":
#     main()

