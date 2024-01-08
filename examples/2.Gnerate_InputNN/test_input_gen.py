import sys
sys.path.append('/home3/zcyu2/n2p2-one_dragon_package')
import n2p2od
#1 Initialize
#初始化包括建立一个文件夹存放后续的训练数据，复制必须的模板文件到当前目录，以及根据目标元素生成对称函数等。
#init_gen = n2p2od.generator.InitGen()
#init_gen.generate_init()
#2 Generate input.data
#data_gen = n2p2od.generator.DataGen("cp2k-pos-1.xyz","cp2k-frc-1.xyz","cp2k-1.restart")
#data_gen.generate_data()
#3 Generate input.nn
nn_gen = n2p2od.generator.NNGen("cp2k-1.restart")
nn_gen.generate_nn()
#4 Generate SymFunc and auto-modify the input.nn
#symfunc_gen = n2p2od.generator.SymFuncGen()
#symfunc_gen.generate_symfunc('radial angular_narrow angular_wide')
#5 Run n2p2
#n2p2_run = n2p2od.run.Run(np=16)  #initialize object
#n2p2_run.scailing()              #nnp-scailing, para1:number Default:number=500
#n2p2_run.train(np=8)             #nnp-train, para1: np Default:np=self.np
#n2p2_run.generate_combinations() #Before auto-checkf, we need to generate this file.
#n2p2_run.auto_checkf(max=2)       #nnp-checkf, para1: np=self.np; para2:max=4

