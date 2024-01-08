import os
import shutil
from tqdm import tqdm

class NNGen():
    def __init__(self, cell_para_info, cutoff_type="6.0 0"):
        self.cell_para_info = cell_para_info
        self.cutoff_type = cutoff_type
        self.n2p2od_path = os.path.dirname((os.path.dirname(__file__))) #locate n2p2od library 
        self.template_path = os.path.join(self.n2p2od_path, "template", "input.nn.recommended") #get inpu.nn_template path.
        shutil.copy(self.template_path, "./input.nn")
        self.elements = []
        with open(self.cell_para_info,'r') as cell_f:
            for line in cell_f:
                if line.strip().upper().startswith('&KIND'):
                    self.elements.append(line.strip().split(' ')[1])  
        #print(len(self.elements))
        #print(self.template_path,self.n2p2od_path)
    def generate_nn(self):
        # read
        with open('input.nn', 'r') as nn_f:
            lines = nn_f.readlines()
    
        # change
        #for i in range(len(lines)):
        for i in tqdm(range(len(lines)), desc="Gnerating input.nn"):
            if lines[i].startswith('number_of_elements'):
                lines[i] = 'number_of_elements ' + str(len(self.elements)) + ' # Number of elements.\n'
            elif lines[i].startswith('elements'):
                lines[i] = 'elements ' + ' '.join(self.elements) + ' # Specification of elements.\n'
            elif lines[i].startswith('cutoff_type'):
                lines[i] = 'cutoff_type ' + str(self.cutoff_type) + '# Cutoff type (optional argument: shift parameter alpha).' + '\n'
    
        # write
        with open('input.nn', 'w') as nn_f:
            nn_f.writelines(lines)
        print("Finish generating input.nn")
                    
