

class Box:
    def __init__(self, data, arr='xywh'):
        self.xi = data[0]
        self.yi = data[1]
        self.w = data[2]
        self.h = data[3]
        self.xf = self.xi + self.w
        self.yf = self.yi + self.h
        self.area = self.w * self.h
    
    def get_sPoint(self):   #get star point
        return (self.xi, self.yi)
    
    def get_ePoint(self):   #get end point
        return (self.xf, self.yf)
    
    def get_x(self):
        return (self.xi, self.xf)
    
    def get_y(self):
        return (self.yi, self.yf)
    
    def get_points(self):
        return ((self.xi,self.xf),(self.yi,self.yf))

    def get_amplify(self, amp):
        x_amp = self.w * amp/100
        y_amp = self.h * amp/100
        self.xi = int(self.xi - x_amp/2)
        self.yi = int(self.yi - y_amp/2)
        self.xf = int(self.xf + x_amp/2)
        self.yf = int(self.yf + y_amp/2)

    def intercepts(self,boxB):
        if self.xf < boxB.xi or self.xi > boxB.xf:      # the boxes doesnt cross on axis x
            return False
        if self.yf < boxB.yi or self.yi > boxB.yf:      # the boxes doesnt cross on axis y
            return False
        return True