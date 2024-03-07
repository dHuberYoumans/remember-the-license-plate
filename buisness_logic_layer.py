# buisness logic layer 
import numpy as np
from abc import ABC, abstractmethod

class Babel:
    """ the Babel class defines an alphabet and provides the rnd_letter method which generates a random character form the alphabet """
    def __init__(self,char):
        if char == 'latin':
            self.script = dict(zip([i for i in range(1,27)],'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()))

    def rnd_letter(self):
        """ generate a random letter """
        return self.script[np.random.randint(1,len(self.script))]
    
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
            unit_three.append(str(np.random.randint(0,10)))
        
        self.lp = ''.join(unit_one + ['-'] + unit_two + ['-'] + unit_three)
        if len(self.lp) <= 10 and len(self.lp) > 0:
            return self.lp
        else:
            return self.generate_rnd_plate()
        
    def generate_spc_plate(self, u_one:int, u_two:int, u_three:int):
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
            unit_three.append(str(np.random.randint(0,10)))
        
        self.lp = ''.join(unit_one + ['-'] + unit_two + ['-'] + unit_three)
        if len(self.lp) <= 10 and len(self.lp) > 0:
            return self.lp
        

# train license plate logic using decorators
        
class TrainingsRun():
    def __init__(self):
        self.score_list = [0]
        self.total = 0
        self.miss = 0
        self.run = 0
        
    def set_score_list(self, score_list : list[int]):
        self.score_list = score_list

    def set_total(self, total : int):
        self.total = total

    def set_miss(self, miss : int):
        self.miss = miss

    def set_run(self, run : int):
        self.run = run

    def get_score_list(self):
        return self.score_list
    
    def get_total_score(self):
        return f'{self.total-self.miss} / {self.total}'
    
    def get_highscore(self):
        if len(self.score_list) == 1:
            return self.run
        else:
            return max(self.score_list)
    
    def get_total(self):
        return self.total
    
    def get_miss(self):
        return self.miss
    
    def get_run(self):
        return self.run

    def reset(self):
        self.score_list = [0]
        self.total = 0
        self.miss = 0

    def append_score_list(self, x : int):
        self.score_list.append(x) 

    def update_run(self, n:int):
        self.run += n

    def update_total(self, n:int):
        self.total += n   

    def update_miss(self, n:int):
        self.miss += n        

    def check_usr_answer(self, kfz : list[str], license_plates : list[str]) -> dict:
        n = len(license_plates)
        correct_answers = [False]*n
        list_of_license_plates = [lp.lower().replace('-','').replace(' ','') for lp in license_plates]
        for x in kfz:
            if x in list_of_license_plates:
                self.update_run(1) 
                correct_answers[list_of_license_plates.index(x)] = True
            else:
                self.update_miss(1)
                self.append_score_list(self.get_run())
        
        return dict(zip(license_plates,correct_answers))
    
class AbstractTrain(ABC): # abstrct component
    """ abstract component for training classes """
    def __init__(self):
        pass

    @abstractmethod
    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        pass 

    @abstractmethod
    def get_trainings_run(self) -> TrainingsRun:
        pass

class TrainLicensePlate(AbstractTrain): # concrete (training) component 
    """ concrete training component """
    def __init__(self):
        self.trainings_run = TrainingsRun() 

    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        """ this method implements the actual training logic """
        self.trainings_run.update_total(len(license_plates))

        return self.trainings_run.check_usr_answer(kfz,license_plates)
    
    def get_trainings_run(self) -> TrainingsRun:
        return self.trainings_run

class AbstractTrainDecorator(AbstractTrain): # abstract decorators
    def __init__(self, dummy_license_plate : AbstractTrain):
        self.alphabet = Babel('latin')
        self.dummy_lp = dummy_license_plate 

    @abstractmethod
    def generate_license_plate():
        pass

    @abstractmethod
    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        pass 

    @abstractmethod
    def get_trainings_run(self) -> TrainingsRun:
        pass

class Random(AbstractTrainDecorator): # concrete decorator
    def __init__(self, dummy_license_plate : AbstractTrain):
        super().__init__(dummy_license_plate)

    def generate_license_plate(self) -> str:        
        return LicensePlate(self.alphabet).generate_rnd_plate() # create random license plate
    
    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        return self.dummy_lp.train(kfz, license_plates)

    def get_trainings_run(self) -> TrainingsRun:
        return self.dummy_lp.get_trainings_run()

class Specific(AbstractTrainDecorator): # concrete decorator
    def __init__(self, dummy_license_plate : AbstractTrain):
        super().__init__(dummy_license_plate)
        self.unit_one = None
        self.unit_two = None
        self.unit_three = None

    def generate_license_plate(self):        
        return LicensePlate(self.alphabet).generate_spc_plate(self.unit_one,self.unit_two,self.unit_three) # create random license plate
    
    def get_trainings_run(self) -> TrainingsRun:
        return self.dummy_lp.get_trainings_run()

    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        return self.dummy_lp.train(kfz, license_plates)

    def set_unit_one(self, unit_one : int):
        self.unit_one = unit_one

    def set_unit_two(self, unit_two : int):
        self.unit_two = unit_two

    def set_unit_three(self, unit_three : int):
        self.unit_three = unit_three

class N(AbstractTrainDecorator): # concrete decorator
    def __init__(self, dummy_license_plate, n : int):
        super().__init__(dummy_license_plate)
        self.n = n

    def generate_license_plate(self) -> list[str]:
        return [self.dummy_lp.generate_license_plate() for i in range(self.n)]

    def get_trainings_run(self) -> TrainingsRun:
        return self.dummy_lp.get_trainings_run()

    def train(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        return self.dummy_lp.train(kfz, license_plates)

    def set_unit_one(self, unit_one : int):
        if isinstance(self.dummy_lp, Specific):
            self.dummy_lp.set_unit_one(unit_one)
        else: 
            raise AttributeError("set_unit_one is only available when Specific is wrapped")

    def set_unit_two(self, unit_two : int):
        if isinstance(self.dummy_lp, Specific):
            self.dummy_lp.set_unit_two(unit_two)
        else: 
            raise AttributeError("set_unit_one is only available when Specific is wrapped")

    def set_unit_three(self, unit_three : int):
        if isinstance(self.dummy_lp, Specific):
            self.dummy_lp.set_unit_three(unit_three)
        else: 
            raise AttributeError("set_unit_three is only available when Specific is wrapped")

# test license plate logic using decorators 
        
class TestRun():
    def __init__(self):
        self.alive = True
        self.score_list = [0]
        self.total = 0
        self.miss = 0
        self.run = 0
        self.health = 0

    def set_alive(self, alive : bool):
        self.alive = alive

    def set_score(self, score_list : list[int]):
        self.score_list = score_list

    def set_total(self, total : int):
        self.total = total

    def set_miss(self, miss : int):
        self.miss = miss

    def set_run(self, run : int):
        self.run = run

    def set_health(self, health : int):
        self.health = health

    def get_alive(self) -> bool:
        return self.alive

    def get_score(self) -> list[int]:
        return self.score_list

    def get_total(self) -> int:
        return self.total

    def get_miss(self) -> int:
        return self.miss

    def get_run(self) -> int:
        return self.run

    def get_health(self) -> int:
        return self.health
    
    def append_score_list(self, x : int):
        self.score_list.append(x) 

    def update_run(self, n:int):
        self.run += n

    def update_total(self, n:int):
        self.total += n   

    def update_miss(self, n:int):
        self.miss += n    

    def add_health(self, n:int):
        self.health += n 

    def sub_health(self, n:int):
        self.health -= n   

    def check_usr_answer(self, kfz : list[str], license_plates : list[str]) -> dict:
        n = len(license_plates)
        correct_answers = [False]*n
        list_of_license_plates = [lp.lower().replace('-','').replace(' ','') for lp in license_plates]
        for x in kfz:
            if x in list_of_license_plates:
                self.update_run(1) 
                correct_answers[list_of_license_plates.index(x)] = True
            else:
                self.update_miss(1)
                self.append_score_list(self.get_run())
        
        return dict(zip(license_plates,correct_answers))

class AbstractTest(ABC): # abstract component
    """ abstract component for decoration of test classes """
    def __init__(self):
        pass

    @abstractmethod
    def test(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        pass 

    @abstractmethod
    def get_test_run(self) -> TestRun:
        pass

class TestLicenseplate(AbstractTest): # concrete component
    """ concrete test component """
    def __init__(self):
        self.test_run = TestRun()

    def test(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        """ this method implements the actual training logic """
        self.test_run.update_total(len(license_plates))

        return self.test_run.check_usr_answer(kfz,license_plates)
    
    def get_test_run(self) -> TrainingsRun:
        return self.test_run
    
class AbstractTestDecorator(ABC): # abstract decorator (test) class 
    """ abstract decorator class for test decorators of classees """
    def __init__(self, test_license_plate : AbstractTest):
        self.alphabet = Babel('latin')
        self.test_dummy = test_license_plate 

    @abstractmethod
    def generate_license_plate():
        pass

    @abstractmethod
    def test(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        pass 

    @abstractmethod
    def get_test_run(self) -> TestRun:
        pass

class SuddenDeath(AbstractTestDecorator): # concrete decorator of test class
    def __init__(self, test_license_plate : AbstractTest):
        super().__init__(test_license_plate)
    
    def test(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        self.test_results = self.test_dummy.test(kfz, license_plates) 
        self.test_dummy.get_test_run().set_alive(all(self.test_results))
        return self.test_results

    def generate_license_plate(self) -> str:
        return LicensePlate(self.alphabet).generate_rnd_plate()
    
    def get_test_run(self) -> TestRun:
        return self.test_dummy.get_test_run()
    

class Survival(AbstractTestDecorator): # concrete decorator of test class
    def __init__(self, test_license_plate : AbstractTest):
        super().__init__(test_license_plate)

    def set_health(self, health : int):
        self.test_dummy.get_test_run().set_health(health)

    def get_health(self) -> int:
        return self.test_dummy.get_test_run().get_health()
    
    def test(self, kfz : list[str], license_plates : list[LicensePlate]) -> dict:
        self.test_results = self.test_dummy.test(kfz, license_plates) 
        self.wrong = [b for b in self.test_results.values() if b == False]
        self.test_dummy.get_test_run().sub_health(len(self.wrong))
        if self.test_dummy.get_test_run().get_health() == 0:
            self.test_dummy.get_test_run().set_alive(False)
        
        return self.test_results

    def generate_license_plate(self) -> str:
        return LicensePlate(self.alphabet).generate_rnd_plate()
    
    def get_test_run(self) -> TestRun:
        return self.test_dummy.get_test_run()
    

