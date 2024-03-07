# presentation tier
import buisness_logic_layer as bll
import time
import os
from sys import platform
from abc import ABC, abstractmethod


class SysCmd: # singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SysCmd, cls).__new__(cls)
        return cls.instance

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

sys_cmd = SysCmd()

class UserInterface:
    """ lass implements the user intereface """
    def __init__(self):
        self.menu = MainMenu()

    def run(self):
        alphabet = bll.Babel('latin')

        print('Wilkommen bei Remember the Plate!\n')

        while True:
            self.menu = MainMenu()
            self.menu.display() # show menu

            self.mode = self.menu.handle_usr_choice(input()) # get usr input and handle choice

            if self.mode == 'test':
                test_dummy = bll.TestLicenseplate()

                sys_cmd.clear_prompt()
                print('Buisness, huh? Nagut!\n')
                self.menu = TestMenu()
                self.menu.display()

                usr_choice = self.menu.handle_usr_choice(input())

                if usr_choice == '1':
                    test_dummy = bll.Survival(test_dummy)
                    self.menu = TestSurvivalMenu()
                    self.menu.display()
                    health = self.menu.handle_usr_choice(input('Mit vielen Leben möchtest Du starten? '))
                    print(f'\nDu startest mit {health} Leben.\n')
                    test_dummy.set_health(health)

                elif usr_choice == '2':
                    test_dummy = bll.SuddenDeath(test_dummy)
                    sys_cmd.clear_prompt()
                    self.menu = TestSuddenDeathMenu()
                    self.menu.display()
                    

                t = get_time(input('Wie wie viele Sekunden möchtest Du Zeit haben? '))

                print(f'\nVerstanden. Du hast {t} Sekunde(n) Zeit. Viel Glück Kadett!\n')
                time.sleep(2)
                sys_cmd.clear_prompt()

                alive = True
                while alive:
                    print('\nGo! (enter)')
                    print('Hauptmenu. (quit)')
                    usr_input = input()
                    if usr_input == '':
                        display_test = TestDisplay(test_dummy)
                        display_test.display_test(t,[test_dummy.generate_license_plate()])
                        alive = test_dummy.get_test_run().get_alive() 
                    elif usr_input == 'quit':
                        sys_cmd.clear_prompt()
                        break
                    

            elif self.mode == 'training':
                dummy_license_plate = bll.TrainLicensePlate() # instanciate a license platae as component

                sys_cmd.clear_prompt()
                self.menu = TrainingMenu()
                self.menu.display()

                option_rnd_or_specific = self.menu.handle_usr_choice(input('Option: ')) # checks if user wants to learn 1 or 2 license plates
                if option_rnd_or_specific == '1':
                    dummy_license_plate = bll.Random(dummy_license_plate) # wrap component as random
                if option_rnd_or_specific == '2':
                    dummy_license_plate = bll.Specific(dummy_license_plate)
                    try:
                        dummy_license_plate.set_unit_one(int(input('\nWie viele Buchstaben soll es in der ersten Einheit geben (1/2/3)? ')))
                    except TypeError:
                        print('Bitte einen integer Eingeben')

                    try:   
                        dummy_license_plate.set_unit_two(int(input('Wie viele Buchstaben soll es in der zweiten Einheit geben (1/2)? ')))
                    except TypeError:
                        print('Bitte einen integer Eingeben')

                    try:
                        dummy_license_plate.set_unit_three(int(input('Wie viele Ziffern soll das Kennzeichen haben (1/2/3/4)? ')))
                    except TypeError:
                        print('Bitte einen integer Eingeben')
                
                self.menu = TrainingSubMenu()
                self.menu.display()
                option_one_or_many = self.menu.handle_usr_choice(input('Option: '))
                if option_one_or_many == '1':
                    dummy_license_plate = bll.N(dummy_license_plate,1) # wrap component as N (number of license plates)
                if option_one_or_many == '2':
                    self.n = int(input('\nWie viele Kennzeichen möchtest du trainieren? X = '))
                    dummy_license_plate = bll.N(dummy_license_plate,self.n) # wrap component as N (number of license plates)

                t = get_time(input('\nWie wie viele Sekunden möchtest Du Zeit haben? ')) # errror handling? 

                while True:
                    print('\nGo! (enter)')
                    print('Hauptmenu (quit)\n')
                    usr_input = input()
                    if usr_input == '':
                        display_training = TrainingDisplay(dummy_license_plate)
                        display_training.display_training(t,dummy_license_plate.generate_license_plate())
                    elif usr_input == 'quit':
                        sys_cmd.clear_prompt()
                        break

        
def get_time(str):
    try:
        return int(str)
    except ValueError:
        return get_time(input('Bitte gebe eine ganze Zahl ein: '))

# use strategy design pattern for menus: 
class AbstractMenu(ABC): # abstract strategy
    """ this class is an abstract class serving as abstract stratgey """
    @staticmethod
    @abstractmethod 
    def display():
        pass

    @abstractmethod
    def handle_usr_choice(self, choice : str):
        pass

class MainMenu(AbstractMenu): # concrete strategy 
    """ this class is a concrete strategy for the main menu """
    def __init__(self):
        pass

    @staticmethod
    def display():
        print('(Hauptmenu)')
        print('Warum bist Du hier?')
        print('1. Zum Üben')
        print('2. I mean Buisness')
        print('3. Ende\n')

    def handle_usr_choice(self,choice : str):
        if choice == '1':
            return 'training'
        elif choice == '2':
            return 'test'
        elif choice == '3':
            sys_cmd.clear_prompt()
            print('Bis zum nächsten Mal!')
            exit()
 
class TrainingMenu(AbstractMenu): # concrete strategy 
    """ this class is a concrete strategy for sub training menu """
    def __init__(self):
        pass

    @staticmethod
    def display():
        print('\n(Übungslager)')
        print('Willkommen im Übungslager.\n')
        print('Was möchtest Du üben?')
        print('1. Zufällige Kennzeichen')
        print('2. Sepzifische Konfigurationen\n')

    def handle_usr_choice(self, choice : str):
        return choice        

class TrainingSubMenu(AbstractMenu): # concrete strategy 
    """ this class is a concrete strategy for the training menu """
    def __init__(self):
        pass

    @staticmethod
    def display():
        print('\nWas würdest Du gerne trainieren?')
        print('1. 1 Kfz-Kennzeichen')
        print('2. X Kfz-Kennzeichen\n')

    def handle_usr_choice(self, choice : str):
        return choice # need to handle error?

class TestMenu(AbstractMenu):
    def __init__(self):
        pass

    @staticmethod 
    def display():
        print('\nQual der Wahl!')
        print('1. Survival')
        print('2. Suddden Death\n')

    def handle_usr_choice(self, choice : str):
        return choice

class TestSurvivalMenu(AbstractMenu):
    def __init__(self):
        pass

    @staticmethod 
    def display():
        print('\nStarte Survival Modus',end='')
        time.sleep(0.3)
        for c in '.....':
            print(c,end='')
            time.sleep(0.3)

    def handle_usr_choice(self, choice : str) -> int:
        try:
             usr_input = int(choice)
        except ValueError:
            self.handle_usr_choice('Bitte gebe einie ganze Zahl ein: ')

        return usr_input


class TestSuddenDeathMenu(AbstractMenu):
    def __init__(self):
        pass

    @staticmethod 
    def display():
        print('\nStarte Sudden Death Modus',end='')
        time.sleep(0.3)
        for c in '.....':
            print(c,end='')
            time.sleep(0.3)
        
        for c in 'One life. One opportunity.':
            print(c,end='')
            time.sleep(0.1)

        print('\n') 

    def handle_usr_choice(self):
        pass

  
class ContinueMenu(AbstractMenu): # concrete strategy 
    """ this class is a concrete strategy for asking if the user wants to continue """
    def __init__(self):
        pass

    @staticmethod
    def display():
        print('Möchtest Du weiter machen? Ja/Nein/Score/Beenden [j/n/s/exit]: ')

    def handle_usr_choice(self,choice : str):
        if choice.lower() == 'j':
            print('continue')
            # bt.score.append(test(t,score))

        elif choice.lower()=='n':
            print('you stop')
            # print(f'Score: {total-miss}/{total}')
            # print(f'Highscore: {max(score)}')
            input()
            return False # how to go back to main menu?
            
        elif choice.lower() == 's':
            sys_cmd.clear_prompt()
            print('score')
            # print(f'Score: {total - miss}/{total}')
            # print(f'Highscore: {max(score)}')
            self.handle_usr_choice(input('Möchtest Du weiter machen? Ja/Nein/Score/Beenden [j/n/s/exit]: ')) 
        
        elif choice.lower() == 'exit':
            sys_cmd.clear_prompt()
            print('score')
            # print(f'Score: {total-miss}/{total}')
            # print(f'Highscore: {max(score)}')
            print('Bis zum nächsten Mal!')
            exit()
            
class TrainingDisplay:
    def __init__(self, train_dummy : bll.AbstractTrain):
        self.train_dummy = train_dummy

    def get_kfz(self, n : int) -> list[str]:
            """ this method gets the users guess for the license plate """
            kfz = []
            
            for i in range(0,n):
                try:
                    kfz.append(input(f'Kfz-Kennz. {i+1}: ').lower().replace('-','').replace(' ',''))
                except AttributeError: # if one wants to skip the license plate, one is asked to  hit enter returning a NoneType objet. This raises an AttributeError in get_answer_one().lower()
                    kfz.append('skipped')
            
            return kfz
            
    def evaluate_answer(self, kfz : list[str], license_plates : list[str]):
        """ this methods evaluates the answer given by the user """
        self.check_answers = self.train_dummy.train(kfz,license_plates)
        sys_cmd.clear_prompt()
        print(f'Du hast {sum(self.check_answers.values())} / {len(self.check_answers)} richtig erinnert!')
        print('Score: ' + self.train_dummy.get_trainings_run().get_total_score())
        print(f'Highscore: {self.train_dummy.get_trainings_run().get_highscore()}\n')

        print('Hier ist ein Überblick (falsch erinnerte sind mit * gekenntzeichnet):\n')
        print(f"{f'Original:':<20} {f'Deine Antwort:':<20}")
        for x in self.check_answers:
            if self.check_answers[x]:
                print(f"{x:<20} {kfz[license_plates.index(x)]:<20}")
            elif not self.check_answers[x]:
                print(f"{f'{x}*':<20} {kfz[license_plates.index(x)]:<20}")
        print('')

    def display_training(self, t : float, lp : list[bll.LicensePlate]):
        """ this method implements the actual training logic """

        sys_cmd.clear_prompt()
        print('Fertig?')
        time.sleep(1)
        print('Los!\n')
        time.sleep(1)
        sys_cmd.clear_prompt()

        # show license plate and remaining display time
        for i in range(0,t):
            print(f'{lp[0]:<20}{t-i:02d}')
            for x in lp[1:]:
                print(f'{x}')
            time.sleep(1)
            sys_cmd.clear_prompt()

        sys_cmd.clear_prompt() 
        kfz = self.get_kfz(len(lp)) 
        self.evaluate_answer(kfz,lp)      

class TestDisplay:
    def __init__(self, test_dummy : bll.AbstractTest):
        self.test_dummy = test_dummy

    def get_kfz(self, n : int) -> list[str]:
        """ this method gets the users guess for the license plate """
        kfz = []
        
        for i in range(0,n):
            try:
                kfz.append(input(f'Kfz-Kennz. {i+1}: ').lower().replace('-','').replace(' ',''))
            except AttributeError: # if one wants to skip the license plate, one is asked to  hit enter returning a NoneType objet. This raises an AttributeError in get_answer_one().lower()
                kfz.append('skipped')
        
        return kfz
            
    def evaluate_answer(self, kfz : list[str], license_plates : list[str]):
        """ this methods evaluates the answer given by the user depending on the chosen mode """

        self.check_answers = self.test_dummy.test(kfz,license_plates)
        if isinstance(self.test_dummy,bll.SuddenDeath):
            sys_cmd.clear_prompt()
            if all(self.check_answers.values()):
                print('Stark! Alles richtig erinnert! ')
                print(f'Highscore: {self.test_dummy.get_test_run().get_run()}')
            else:
                print('Aaarrghh .... ')
                print(f'Guter Run!')
                print(f'Highscore: {self.test_dummy.get_test_run().get_run()}')
                print('GAME OVER')
                input()
                sys_cmd.clear_prompt()

        elif isinstance(self.test_dummy,bll.Survival):
            if not all(self.check_answers.values()):
                print('Arrrrr ... Du wurdest getroffen!')
                print(f"{'verbleibende Leben:':<20}{self.test_dummy.get_test_run().get_health()}") 
                if self.test_dummy.get_test_run().get_health() == 0:
                    print('GAME OVER')
            else: 
                print('Stark! Alles richtig. Weiter so!')
            

    def display_test(self, t : float, lp : list[bll.LicensePlate]):
        """ this method implements the actual test logic """

        sys_cmd.clear_prompt()
        print('Fertig?')
        time.sleep(1)
        print('Los!\n')
        time.sleep(1)
        sys_cmd.clear_prompt()

        # show license plate and remaining display time
        for i in range(0,t):
            print(f'{lp[0]:<20}{t-i:02d}')
            for x in lp[1:]:
                print(f'{x}')
            time.sleep(1)
            sys_cmd.clear_prompt()

        sys_cmd.clear_prompt() 
        kfz = self.get_kfz(len(lp)) 
        self.evaluate_answer(kfz,lp)   