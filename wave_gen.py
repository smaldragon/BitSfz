#TODO: Port this code to C
import math
import os

import wave
import struct

#import matplotlib.pyplot as plt
class bw_low_pass():
    def __init__(self,order,s,f):
        self.n = int(order/2)
        self.A = [0] * self.n
        self.d1 = [0] * self.n
        self.d2 = [0] * self.n

        self.w0 = [0] * self.n
        self.w1 = [0] * self.n
        self.w2 = [0] * self.n

        # Calc
        a = math.tan(math.pi * f/s)
        a2 = a*a
        for i in range(self.n):
            r = math.sin(math.pi*(2.0*i+1.0)/(4.0*self.n))
            s = a2 + 2.0*a*r + 1.0
            self.A[i] = a2/s
            self.d1[i] = 2.0*(1-a2)/s
            self.d2[i] = -(a2 - 2.0*a*r + 1.0)/s

    def filter(self,x):
        for i in range(self.n):
            self.w0[i] = self.d1[i]*self.w1[i] + self.d2[i]*self.w2[i] + x
            x = self.A[i]*(self.w0[i] + 2.0*self.w1[i] + self.w2[i])
            self.w2[i] = self.w1[i]
            self.w1[i] = self.w0[i]
        return x

def generate_tables(filename,directory,source,depth,layer):
    table = []
    for sample in source:
        table.append(sample/depth)
    LEN = 256
    HARM = 8
    ORDER = 16

    tabl = [[0]*LEN]*HARM

    ofi = [int(ORDER/4)]
    for i in range(1,HARM):
        ofi.append(int((ofi[i-1]*2)%(LEN)))

    for hi in range(HARM):
        h = hi+1
        fil = bw_low_pass(ORDER,LEN,LEN/(2**h))
        ar = []

        of = ofi[hi]-4

        min = 1000.0
        max = -1000.0
        for i in range(LEN*8):
            l = LEN/len(table)
            p = int((i%LEN)/l)
            v = table[p]       
            
            # Apply Filter
            vf = fil.filter(v)
            ar.append(vf)

            if i > LEN*6:
                if vf < min:
                    min = vf
                if vf > max:
                    max = vf
            
        #print("LEVEL",h,min,max,max-min)
        dif = (max+min)/2
        for i in range(LEN*8):
            ar[i] = (ar[i] - dif)*(1-0.1*hi)
        
        #print(of)
        tabl[hi] = ar[LEN*6+of:LEN*7+of]
        #plt.plot(tabl[hi])
        #plt.show()

    for i,table in enumerate(tabl):
        if directory != "":
            save_path=f'{directory}/samples/'
        else:
            save_path=f'samples/'
        os.makedirs(save_path, exist_ok=True) 
        obj = wave.open(f'{save_path}{filename[:-4]}_{"ABCD"[layer]}_{i}.wav','w')
        obj.setnchannels(1) # mono
        obj.setsampwidth(2)
        obj.setframerate(56320.0)
        for sample in table:
            data = struct.pack('<h',int(sample*0x8FFF))
            obj.writeframesraw( data )  
        obj.close()
