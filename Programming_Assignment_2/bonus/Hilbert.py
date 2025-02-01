import os
import turtle 
import argparse
from PIL import Image

class hilbt:
    def __init__(self, len=512) -> None:
        self.t = turtle.Turtle()
        self.scr = turtle.Screen()
        self.scr.setup(width=len, height=len)
        self.len = len

    def set_init(self, order):
        if order%2 == 1:
            self.cw = True # clockwise
            self.t.seth(90)
        else:
            self.cw = False
            self.t.seth(0)
        self.step = self.len/(2**(order))
        '''Set starting point'''
        self.t.clear()
        self.t.penup()
        self.t.setpos(-self.len/2 + self.len/(2**(order+1)), -self.len/2 + self.len/(2**(order+1))) #(0,0) shifted
        self.t.pendown()
        
    def plot(self, order, star_cw=None):
        if star_cw == None: # is starting clockwise
            star_cw = order%2==1 #default
        if order==1: 
            self.t.fd(self.step)
            for i in range(2):
                self.t.right(90 * (star_cw*2-1)) # clockwise: turn right
                self.t.fd(self.step)

        else:
            self.plot(order-1, star_cw=star_cw)
            if order%2==0:
                # first turn
                self.t.left(90 * (star_cw*2-1))
                self.t.fd(self.step)
                self.plot(order-1, star_cw = abs(star_cw-1)) # differ from begin
                # sec turn
                self.t.right(90 * (star_cw*2-1))
                self.t.fd(self.step)
                self.t.right(90 * (star_cw*2-1))
                self.plot(order-1, star_cw = abs(star_cw-1)) # differ from begin
                # 3rd turn
                self.t.fd(self.step)
                self.t.left(90 * (star_cw*2-1))
            else:
                # first turn
                self.t.fd(self.step)
                self.t.right(90 * (star_cw*2-1))
                self.plot(order-1, star_cw = abs(star_cw-1)) # differ from begin
                # sec turn
                self.t.fd(self.step)
                self.plot(order-1, star_cw = abs(star_cw-1)) # differ from begin
                #3rd turn
                self.t.right(90 * (star_cw*2-1))
                self.t.fd(self.step)

            self.plot(order-1, star_cw =star_cw)

            
    def main(self, order, speed=10, convert= False):
        self.t.speed(speed)
        self.set_init(order)
        self.plot(order)
        print(f'Order {order} Hilbert Curve is Done')
        fileName = f'h{order}'
        canvas = self.scr.getcanvas()
        canvas.postscript(file= fileName+'.eps', width=512, height=512)
        if convert:
            img=Image.open(fileName+'.eps')
            img.save(fileName+'.png')
            img.close()
            os.remove(fileName+'.eps')


def main(order, exec, convert = False):
    a = hilbt()
    if exec:
        for o in range(1,5):
            a.main(o, speed=5*o, convert = convert)
    else:
        a.main(order, convert = convert)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--order", type=int, help="The order of Hilbert Curve")
    parser.add_argument("-e","--exec", action="store_true",
                         help="To draw Hilbert Curve with order 1-4")
    parser.add_argument("-c","--convert", action="store_true",
                         help="convert .eps to .png")
    args = parser.parse_args()
    main(args.order, args.exec, args.convert)


