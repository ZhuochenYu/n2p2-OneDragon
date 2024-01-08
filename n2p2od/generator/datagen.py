import os
import sys
import argparse
from ase.io import read
import numpy as np
from tqdm import tqdm
class DataGen:
    def __init__(self, pos_path, frc_path, cell_para_info, software='cp2k'):
        self.pos_path = pos_path
        self.frc_path = frc_path
        self.cell_para_info = cell_para_info
        self.software = software

    def read_cell_from_inp(self, file_path):
        cell = []
        start_reading = False
        with open(file_path, 'r') as file:
            for line in file:
                line_lower = line.lower()
                if '&cell' in line_lower:
                    start_reading = True
                    continue
                if '&end cell' in line_lower:
                    break
                if start_reading and line.strip():
                    parts = line.split()
                    if parts[0].upper() in ['A', 'B', 'C']:
                        cell.append([float(parts[i]) for i in range(1, 4)])
        return np.array(cell)

    def generate_data(self):
        cell = self.read_cell_from_inp(self.cell_para_info)
        pos = read(self.pos_path, index=":")
        frc = read(self.frc_path, index=":")

        out_path = os.path.join(os.getcwd(), "input.data")
        with open(out_path, "w") as fw:
            #for frame_idx in range(len(pos)):
            for frame_idx in tqdm(range(len(pos)), desc="Generating input.data"):
                fw.write("begin\n")
                for i in range(3):
                    fw.write("lattice{:10.4f}{:10.4f}{:10.4f}\n".format(cell[i][0], cell[i][1], cell[i][2]))
                for atom in zip(pos[frame_idx], frc[frame_idx]):
                    fw.write("atom{:12.5f}{:12.5f}{:12.5f}".format(atom[0].position[0], atom[0].position[1], atom[0].position[2]))
                    fw.write("     {}".format(atom[0].symbol))
                    fw.write("{:10.4f}{:10.4f}".format(0.0, 0.0))
                    fw.write("{:12.5f}{:12.5f}{:12.5f}\n".format(atom[1].position[0], atom[1].position[1], atom[1].position[2]))
                fw.write("energy{:20.4f}\n".format(pos[frame_idx].info['E']))
                fw.write("charge{:20.4f}\n".format(0.0))
                fw.write("end\n")
        print("Finish generating input.data")

if __name__ == '__main__':
    pos_path = 'path/to/coords.xyz'
    frc_path = 'path/to/forces.xyz'
    cell_para_info = 'path/to/cp2k.inp'

    generator = DataGenerator(pos_path, frc_path, cell_para_info)
    generator.generate_data()

