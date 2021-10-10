from pgmpy.readwrite import BIFReader
from pgmpy.inference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DynamicBayesianNetwork as DBN
from pgmpy.readwrite import BIFWriter

class Accient_diagnosis:
    def __init__(self, path, hard_evidence, virtual_evidence, pre_diagnostic_accident):
        self.path = path
        self.hard_evidence = hard_evidence
        self.virtual_evidence = virtual_evidence
        self.model = BIFReader(self.path).get_model()
        self.inference_model = BeliefPropagation(self.model)
        self.pre_diagnostic_accident = pre_diagnostic_accident
    def inference(self):
        diagnosis_process = self.inference_model.query(variables=[self.pre_diagnostic_accident],
                                                       evidence=self.hard_evidence, virtual_evidence=[self.virtual_evidence])
        return (diagnosis_process.values)[1]


LOCA = Accient_diagnosis(path="./models/WU_LOCA.bif", hard_evidence={'CP':"higher"},
                         virtual_evidence=TabularCPD(variable='RP', variable_card=3, values=[[0.9],[0.1],[0]]),
                         pre_diagnostic_accident="LOCA")
result = LOCA.inference()
print(result)



# LOCA_Bayesian_model = BIFReader("./models/WU_LOCA.bif").get_model() #read LOCA Bayesian model
# SGTR_Bayesian_model = BIFReader("./models/WU_SGTR.bif").get_model() #read LOCA Bayesian model
# LOCA_inference_model = BeliefPropagation(LOCA_Bayesian_model) #construct inference model
# SGTR_inference_model = BeliefPropagation(SGTR_Bayesian_model) #construct inference model
#
# LOCA_hard_evidence = {'CP':"higher"}
# LOCA_virtual_evidence = TabularCPD(variable='RP', variable_card=3, values=[[0.9],[0.1],[0]])
# LOCA_diagnosis_result = LOCA_inference_model.query(variables=['LOCA'],evidence=LOCA_hard_evidence,virtual_evidence=[LOCA_virtual_evidence]) #go to inference
# print((LOCA_diagnosis_result.values)[1])
# SGTR_hard_evidence = {'PSGR':"normal"}
# SGTR_virtual_evidence = TabularCPD(variable='RP', variable_card=3, values=[[0.9],[0.1],[0]])
# SGTR_diagnosis_result = SGTR_inference_model.query(variables=['SGTR'],evidence=SGTR_hard_evidence,virtual_evidence=[SGTR_virtual_evidence]) #go to inference
# print((SGTR_diagnosis_result.values)[1])


