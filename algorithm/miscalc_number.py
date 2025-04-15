class MiscalcNumber:

    def __init__(self, number, miscalc=None):
        self.number = number
        if miscalc is None:
            self.miscalc = (0.5 if len(str(number).split('.')) < 2 
                            else 10**(-len(str(number).split('.')[1])) / 2)
        else:
            self.miscalc = miscalc

    def __add__(self, other):
        return MiscalcNumber(self.number + other.number, self.miscalc + other.miscalc)
    
    def __sub__(self, other):
        return MiscalcNumber(self.number - other.number, self.miscalc + other.miscalc)
    
    def __iadd__(self, other):
        self.number += other.number
        self.miscalc += other.miscalc
        return self
    
    def __isub__(self, other):
        self.number -= other.number
        self.miscalc += other.miscalc
        return self
    
    def __mul__(self, other):
        if self.number == 0 or other.number == 0:
            return MiscalcNumber(0, 0)
        res = self.number * other.number
        return MiscalcNumber(res, abs(res) * (self.miscalc / abs(self.number) 
                                         + other.miscalc / abs(other.number)))
    
    def __truediv__(self, other):
        if self.number == 0:
            return self
        res = self.number / other.number
        return MiscalcNumber(res, abs(res) * (self.miscalc / abs(self.number) 
                                         + other.miscalc / abs(other.number)))
    
    def __imul__(self, other):
        if self.number == 0 or other.number == 0:
            self.number = 0
            self.miscalc = 0
            return self
        self.number *= other.number
        self.miscalc = abs(self.number) * (self.miscalc / abs(self.number) 
                                    + other.miscalc / abs(other.number))
        return self
        
    def __itruediv__(self, other):
        if self.number == 0:
            return self
        self.number /= other.number
        self.miscalc = abs(self.number) * (self.miscalc / abs(self.number) 
                                    + other.miscalc / abs(other.number))
        return self
    
    def __repr__(self):
        return f"{self.number} +- {self.miscalc}"