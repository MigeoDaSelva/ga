from dataclasses import dataclass
import math


@dataclass
class FunctionDeap:

    qtd_variables: int
    bounds: tuple
    function_name: str
    
    def objective_fxn(self, individual):     
        
        # decoding chromosome to get decoded x in a list
        x = self.decode_all_x(individual)
        
        decoded_x = x[0]
        decoded_y = x[1]

        # the himmelblau function
        if self.function_name == "himmelblau":
            obj_function_value = (((decoded_x)**2)+decoded_y-11)**2+(decoded_x+((decoded_y)**2)-7)**2
        
        elif self.function_name == "h1":
            obj_function_value = (math.sin(decoded_x - decoded_y/8)**2 + math.sin(decoded_y+decoded_x/8)**2) / (math.sqrt((decoded_x-8.6998)**2 + (decoded_y-6.7665)**2 + 1))

        elif self.function_name == "five_variables":
            decoded_z = x[2]
            decoded_a = x[3]
            decoded_b = x[4]
            obj_function_value = ((decoded_x)**2 + decoded_y - 11)**2 - (decoded_z + (decoded_a)**2 - 7)**2 + decoded_b
        elif self.function_name == "gradient descent":
            obj_function_value = 3 * (1 - decoded_x)**2 * math.exp((-decoded_x)**2 - (decoded_y+1)**2) - 10 * (decoded_x/5 - decoded_x**3 - decoded_y**5) * math.exp((-decoded_x)**2 - decoded_y**2) - 1/3 * math.exp(-(decoded_x+1)**2 - decoded_y**2)
        
        
        return [obj_function_value] 
    
    def decode_all_x(self, individual):
        len_chromosome = len(individual)
        len_chromosome_one_var = int(len_chromosome/self.qtd_variables)
        bound_index = 0
        x = []
        
        # one loop each for x(first 50 bits of individual) and y(next 50 of individual)
        for i in range(0,len_chromosome,len_chromosome_one_var):
            # converts binary to decimial using 2**place_value
            chromosome_string = ''.join((str(xi) for xi in  individual[i:i+len_chromosome_one_var]))
            binary_to_decimal = int(chromosome_string,2)
            
            lb = self.bounds[bound_index][0]
            ub = self.bounds[bound_index][1]
            precision = (ub-lb)/((2**len_chromosome_one_var)-1)
            decoded = (binary_to_decimal*precision)+lb
            x.append(decoded)
            bound_index +=1
        
        return x
    
    def check_feasiblity(self, individual):
        var_list = self.decode_all_x(individual)
        if sum(var_list) < 0:
            return True
        else:
            return False

    def penalty_fxn(self, individual):
        var_list = self.decode_all_x(individual)
        return sum(var_list)**2
