import os
import turtle 
import argparse
import numpy as np
from PIL import Image


class hilb:
    def __init__(self, input:np.array, scrWid=720) -> None: #input array
        self.count = int(0)
        self.pltCount = int(0)

        self.input = input # 512*512 px
        self.output = input.flatten()
         # traversal order in terms of coordinate(x,y) 
        self.coord_ord = [(i,i) for i in range(len(input.flatten()))] 
        self.wid_order = int(np.log2(len(input))) # input image width (px) convert to power of 2  
        self.path = [(0,0), (0,1), (1,1), (1,0)]
        
        self.t = turtle.Turtle()
        self.scr = turtle.Screen()
        self.dotWid = scrWid//len(input) # dot width
        self.scrWid = scrWid
        self.scr.setup(width=scrWid, height=scrWid)

        
    def set_init(self, order):
        self.count = int(0)
        self.pltCount = int(0)
        self.step = self.dotWid/(2**(order)) # length of each line within each curve

    '''Convert 2d Array By Hilbert traversal'''
    def hilbArr(self, start_pt=(0,0), **kwargs) -> np.array: # ordered array
        order = kwargs.get('order', self.wid_order)
        path = kwargs.get('path', self.path)
        if order == 1:
            for i in range(4): 
                update = (start_pt[0]+path[i][0], start_pt[1]+path[i][1])
                self.output[self.count] = self.input[update]
                self.coord_ord[self.count] = update
                self.count+=1
        else:
            for i in range(4):

                new_start_pt = (start_pt[0] + path[i][0]*(2**(order-1)),
                                 start_pt[1] + path[i][1]*(2**(order-1)))
                new_path=self.bit_st(self.count, order, path)
                self.hilbArr(order=order-1, start_pt=new_start_pt, path=new_path)

    '''Draw Hilbert Curve'''
    def hilbCur(self, order: int, **kwargs):

        start_pt = kwargs.get("start_pt", (0,0))
        path = kwargs.get("path", self.path)
        step = kwargs.get("step", self.step)
        first_px = kwargs.get("first_px", False)

        if ((self.pltCount==0) & first_px):
            self.t.clear()
            self.t.penup()
            self.t.setpos(start_pt) # shift start point
            self.t.pendown()

        if order == 1:
            for i in range(4):  
                update = (start_pt[0] + path[i][0]*step,
                           start_pt[1] + path[i][1]*step)
                self.t.setpos(update)
                self.pltCount+=1
        else:
            for i in range(4):
                new_start_pt = (start_pt[0] + path[i][0]*(2**(order-1)*step),
                                 start_pt[1] + path[i][1]*(2**(order-1))*step)
                new_path=self.bit_st(self.pltCount, order, path)
                self.hilbCur(order-1, start_pt=new_start_pt, path=new_path)
        

    '''bit masking'''
    def bit_st(self, count, order, path): # path swithching
        sft_path = path.copy()
        bit_stat = count//(4**(order-1)) & 3 
        if bit_stat == 0:
            tmp = sft_path[1]
            sft_path[1] = sft_path[3]
            sft_path[3] = tmp 
        elif bit_stat == 3:
            tmp = sft_path[0]
            sft_path[0] = sft_path[2]
            sft_path[2] = tmp 
        else: # path = [(0,0), (0,1), (1,1), (1,0)]
            pass
        return(sft_path) #
    

    def main(self, fname, convert=False):
        self.t.speed(0)
        self.hilbArr() # order input -img- array
        self.output = np.where(self.output > self.output.mean(), 1, 2) # change px to order
        for idx, px in enumerate(self.output):
            # print(px)       
            self.set_init(order=px)   # update param in each px
            '''set which path pass to hilbCur function'''
            for odr in range(1,self.wid_order+1):
                if odr == 1:
                    new_path = self.bit_st(count = idx, order = odr, path = self.path)
                else: 
                    new_path = self.bit_st(count = idx, order = odr, path = new_path)
            '''set starting point of each px'''
            if idx ==0:
                self.sxy = (-self.scrWid//2 + self.step,
                            -self.scrWid//2 + self.step)                
                new_start_pt = self.sxy
            else:
                new_start_pt = (self.sxy[0] + self.dotWid * self.coord_ord[idx][0],
                                self.sxy[1] + self.dotWid * self.coord_ord[idx][1])
            self.hilbCur(order = px, start_pt = new_start_pt, path = new_path, first_px = (idx==0))
        fname = fname+'_art'
        canvas = self.scr.getcanvas()
        canvas.postscript(file= fname+'.eps', width=720, height=720)
        if convert:
            img=Image.open(fname+'.eps')
            img.save(fname+'.png')
            img.close()
            os.remove(fname+'.eps')

        # self.scr.exitonclick()
        

    

def main(fname, convert=False):
    img = Image.open(fname) # imput image
    out = img.resize((32,32)).rotate(270) # rotation to make correct direction
    a = hilb(np.array(out)) 
    a.main(fname, convert)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", type=str, help="The input Image file")
    parser.add_argument("-c","--convert", action="store_true",
                         help="convert .eps to .png")
    args = parser.parse_args()
    main(args.file, args.convert)


