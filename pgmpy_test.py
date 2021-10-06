from pgmpy.readwrite import BIFReader
from pgmpy.inference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD
LOCA_Bayesian_model = BIFReader("./models/LOCA.bif").get_model() #read LOCA Bayesian model
LOCA_inference_model = BeliefPropagation(LOCA_Bayesian_model) #construct inference model
hard_evidence = {'AP':"higher"}
virtual_evidence = TabularCPD(variable='RP', variable_card=3, values=[[0.1],[0.3],[0.6]])
diagnosis_result = LOCA_inference_model.query(variables=['LLOCA'],evidence=hard_evidence,virtual_evidence=[virtual_evidence]) #go to inference
print(diagnosis_result)

