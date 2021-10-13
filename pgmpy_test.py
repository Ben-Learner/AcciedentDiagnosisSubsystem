from pgmpy.readwrite import BIFReader
from pgmpy.inference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD


class Accient_diagnosis:
    """

    this is for diagnosis of Bayesian models

    Examples
    --------
    >>> LOCA = Accient_diagnosis(path="./models/WU_LOCA.bif", hard_evidence={'CP':"higher"}, virtual_evidence=TabularCPD(variable='RP', variable_card=3, values=[[0.9],[0.1],[0]]),pre_diagnostic_accident="LOCA")
    >>> result = LOCA.inference()
    >>> print(result)
    0.9502762430939227
    """
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
    """

     Convert continous evidence into discrete evidence

     Examples
     --------
     >>> virtual_evidence = Fuzzy_function(6.8, 6.6, 7.4)
     >>> result = virtual_evidence.return_result()
     >>> print(result)
     [0.5, 0.5, 0]
     """
    def __init__(self, real_time_value,lower_limit,upper_limit):
        self.real_time_value = real_time_value
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.middle_value = 1/2*(self.upper_limit + self.lower_limit)
    def _low_probablity(self):
        if self.real_time_value < self.lower_limit:
            p_low = 1
        elif self.lower_limit <= self.real_time_value <= self.middle_value:
            p_low = (self.middle_value - self.real_time_value) / (self.middle_value - self.lower_limit)
        else:
            p_low = 0
        return p_low
    def _normal_probablity(self):
        if self.real_time_value < self.lower_limit:
            p_normal = 0
        elif self.lower_limit <= self.real_time_value <= self.middle_value:
            p_normal = (self.real_time_value - self.lower_limit) / (self.middle_value - self.lower_limit)
        elif self.middle_value < self.real_time_value <= self.upper_limit:
            p_normal = (self.upper_limit - self.real_time_value) / (self.upper_limit - self.middle_value)
        else:
            p_normal = 0
        return p_normal
    def _high_probablity(self):
        if self.real_time_value < self.middle_value:
            p_high = 0
        elif self.middle_value <= self.real_time_value <= self.upper_limit:
            p_high = (self.real_time_value - self.middle_value) / (self.upper_limit - self.middle_value)
        else:
            p_high = 1
        return p_high
    def return_result(self):
        p_low = self._low_probablity()
        p_normal = self._normal_probablity()
        p_high = self._high_probablity()
        result = [p_low, p_normal, p_high]
        return result

class data_fusion:
    """

     Convert multi-source evidence into single evidence.
     It is assumed that the database includes sensor number and status number


     Examples
     --------
     >>> data_fusion_evidence = data_fusion(4, 3, [0.82, 0.18, 0, 0.9, 0.1, 0, 0.7, 0.3, 0, 0.85, 0.15, 0])
     >>> result = data_fusion_evidence.combined_mass_function()
     >>> print(result)
     [0.9981587561374795, 0.0018412438625204585, 0.0]
     """
    def __init__(self, sensor_number, status_number, multi_source_evidence):
        """

        :param sensor_number:
        :param status_number:
        :param multi_source_evidence: list eg:[0, 0.05, 0.95, 0.01, 0.98, 0.01, 0.03, 0.96, 0.01]

        """
        self.sensor_number = sensor_number
        self.status_number = status_number
        self.multi_source_evidence = multi_source_evidence
    def _caculate_K(self):
        K = 0
        for i in range(self.status_number):
            sub_k = 1
            for j in range(self.sensor_number):
                sub_k *= self.multi_source_evidence[i + (j * self.status_number)]
            K += sub_k
        return K
    def combined_mass_function(self):
        K = self._caculate_K()
        result = []
        for i in range(self.status_number):
            sub_result = 1 / K
            for j in range(self.sensor_number):
                sub_result *= self.multi_source_evidence[i + (j * self.status_number)]
            result.append(sub_result)
        return result


