from pgmpy.readwrite import BIFReader
from pgmpy.inference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD


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
class Fuzzy_function:
    def __init__(self, real_time_value,lower_limit,upper_limit):
        self.real_time_value = real_time_value
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.middle_value = 1/2*(self.upper_limit + self.lower_limit)
    def low_probablity(self):
        if self.real_time_value < self.upper_limit:
            p_low = 1
        elif self.lower_limit <= self.real_time_value <= self.middle_value:
            p_low = (self.middle_value - self.real_time_value) / (self.middle_value - self.lower_limit)
        else:
            p_low = 0
        return p_low
    def normal_probablity(self):
        if self.real_time_value < self.upper_limit:
            p_normal = 0
        elif self.lower_limit <= self.real_time_value <= self.middle_value:
            p_normal = (self.real_time_value - self.lower_limit) / (self.middle_value - self.lower_limit)
        elif self.middle_value < self.real_time_value <= self.upper_limit
            p_normal = (self.upper_limit - self.real_time_value) / (self.upper_limit - self.middle_value)
        else:
            p_normal = 0
        return p_normal
    def high_probablity(self):
        if self.real_time_value < self.middle_value:
            p_high = 0
        elif self.middle_value <= self.real_time_value <= self.upper_limit:
            p_high = (self.real_time_value - self.middle_value) / (self.upper_limit - self.middle_value)
        else:
            p_high = 1
        return p_high
    def return_result(self):
LOCA = Accient_diagnosis(path="./models/WU_LOCA.bif", hard_evidence={'CP':"higher"},
                         virtual_evidence=TabularCPD(variable='RP', variable_card=3, values=[[0.9],[0.1],[0]]),
                         pre_diagnostic_accident="LOCA")
result = LOCA.inference()
print(result)


