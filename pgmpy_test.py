from pgmpy.readwrite import BIFReader
from pgmpy.inference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DynamicBayesianNetwork as DBN
# LOCA_Bayesian_model = BIFReader("./models/LOCA.bif").get_model() #read LOCA Bayesian model
# print(LOCA_Bayesian_model.get_cpds('CP'))
# LOCA_inference_model = BeliefPropagation(LOCA_Bayesian_model) #construct inference model
# hard_evidence = {'AP':"higher"}
# virtual_evidence = TabularCPD(variable='RP', variable_card=3, values=[[0.1],[0.3],[0.6]])
# diagnosis_result = LOCA_inference_model.query(variables=['LLOCA'],evidence=hard_evidence,virtual_evidence=[virtual_evidence]) #go to inference
# print((diagnosis_result.values)[1])
#第一步从静态网络中获取节点
#第二步从静态网络中获取边缘
#第三步从静态网络中获取条件概率表
#第四步组建动态贝叶斯网络
LOCA_Bayesian_model = BIFReader("./models/D_LOCA.bif")
print(LOCA_Bayesian_model.get_variables())
LOCA_Dynamic_Bayesian_model = DBN(LOCA_Bayesian_model)
print(LOCA_Dynamic_Bayesian_model.edges())