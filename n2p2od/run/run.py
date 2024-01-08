import subprocess
import os
import shutil
import glob
import itertools
from tqdm import tqdm
import random
class Run():
    def __init__(self,np=16):
        self.np = np
    def scailing(self, number=500):
        self.number = number
        shutil.copy('input.nn','nnp-scaling')
        shutil.copy('input.data', 'nnp-scaling')
        os.chdir("nnp-scaling")
        command_scaling = ['mpirun', '-np', str(self.np), 'nnp-scaling', str(number)]
        print('Running command: ' + ' '.join(command_scaling))
        with open('n2p2od-nnp-scaling.log', 'w') as log_file:
            subprocess.run(command_scaling, stdout=log_file, text=True)
        os.chdir("..")
        print('Running command-----Done.')
    
    def train(self,np=None):
        if np == None:
            np = self.np
        shutil.copy('input.nn','nnp-train')
        shutil.copy('input.data', 'nnp-train')
        shutil.copy("./nnp-scaling/scaling.data", 'nnp-train')
        os.chdir("nnp-train")        
        command_train = ['mpirun', '-np', str(np), 'nnp-train']
        print(' '.join(command_train))
        #with open('n2p2od-nnp-train.log', 'w') as log_file:
        subprocess.run(command_train, text=True)
        os.chdir("..")
        print('Running command-----Done.')
  
  
    def generate_combinations(self):
        os.chdir("nnp-train")
        weights_file_pattern = "weights*.out"
        weights_file_list = glob.glob(weights_file_pattern)
        # classification
        class_files = {}
        for file in weights_file_list:
            parts = file.split('.')
            if len(parts) == 4:
                element_type = parts[1].lstrip('0')
                number = parts[2].lstrip('0') or '0'
                if element_type not in class_files:
                    class_files[element_type] = {}

                if number not in class_files[element_type]:
                    class_files[element_type][number] = []

                class_files[element_type][number].append(file)

        #print(class_files)
        with open('weights_combinations.txt','w') as f:
           f.write(f"combination file1 file2 ...\n")
        number_combinations = [class_files[etype].keys() for etype in class_files]
        # 使用 itertools.product 生成所有可能的 element_type 和 number 的组合
        for combo in itertools.product(*number_combinations):
            combined_names = []
            files_for_combo = []
            for etype, number in zip(class_files.keys(), combo):
                combined_names.append(f"{etype}_{number}")
                files_for_combo.extend(class_files[etype][number])
        
            combined_name = '-'.join(combined_names)
            
            with open('weights_combinations.txt','a') as f:
                f.write(f"{combined_name} {' '.join(files_for_combo)}\n")
            #print(combined_name, files_for_combo)        
        if os.path.exists('../weights_combinations.txt'):
            os.remove('../weights_combinations.txt')
        shutil.move('weights_combinations.txt', "../")            
        os.chdir("..")
        
    def checkf(self, np=None, error='10E-03'):
        if np == None:
            np = self.np
        #os.chdir("nnp-checkf")
        command_checkf = ['mpirun', '-np', str(self.np), 'nnp-checkf', str(error)]
        print('Running command: ' + ' '.join(command_checkf))
        with open('n2p2od-nnp-checkf.log', 'w') as log_file:
            subprocess.run(command_checkf, stdout=log_file, text=True)
        #os.chdir("..")
    def auto_checkf(self,np=None, max=4):
        if np==None:
           np = self.np
        def rename_files(folder_name):
            pattern = f"./nnp-checkf/{folder_name}/*.out"
            for filepath in glob.glob(pattern):
                new_filepath = filepath.rsplit('.', 2)[0] + '.data'
                shutil.copy(filepath, new_filepath)
        self.max = max
        combinations = self.get_random_lines()
        #print(combinations)
        for comb in combinations:
            folder_name = comb.split()[0]
            if not os.path.exists(f"./nnp-checkf/{folder_name}"):
                os.mkdir(f"./nnp-checkf/{folder_name}")
            files = comb.split()[1:]
            for file in files:
                shutil.copy(f"./nnp-train/{file}",f"./nnp-checkf/{folder_name}")
                shutil.copy(f"./nnp-train/input.nn",f"./nnp-checkf/{folder_name}")
                shutil.copy(f"./nnp-train/input.data",f"./nnp-checkf/{folder_name}")
                shutil.copy(f"./nnp-train/scaling.data",f"./nnp-checkf/{folder_name}")
                rename_files(folder_name)
            os.chdir(f"./nnp-checkf/{folder_name}")
            self.checkf(np=np)
            os.chdir("cd -")
        #print(files)
    def get_random_lines(self):
        filename = 'weights_combinations.txt'
        with open(filename, 'r') as f:
            lines = f.readlines()

        line_count = len(lines)
        random_line_numbers = random.sample(range(2, line_count), self.max)
        #print(random_line_numbers)
        selected_lines = [lines[i-1].strip() for i in random_line_numbers]
        return selected_lines
