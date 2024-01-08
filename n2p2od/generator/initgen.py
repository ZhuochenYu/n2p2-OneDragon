import os

class InitGen:
    def __init__(self):
        pass
    def generate_init(self):

        directories = ['nnp-scaling', 'nnp-train', 'nnp-checkf', 'nnp-predict', 'nnp-data']
        
        for dir_name in directories:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(f"directory {dir_name} has been created.")
            else:
                print(f"directory {dir_name} exists")
        
