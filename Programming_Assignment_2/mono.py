import argparse
import numpy as np
import time

class mono_routing():
    def __init__(self, args):
        pass
    def parser(self): #You can modify it by yourself.
        with open("%s" % args.input, 'r', newline='') as file_in:
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("BoundaryIndex"):
                    value_list = lines.split(' ')
                    self.Bx1 = int(value_list[1])
                    self.By1 = int(value_list[2])
                    self.Bx2 = int(value_list[3])
                    self.By2 = int(value_list[4])
                if lines.startswith("DefaultCost"):
                    value_list = lines.split(' ')
                    self.default_cost = int(value_list[-1])
                if lines.startswith("NumNonDefaultCost"):
                    value_list = lines.split(' ')
                    self.size = int(value_list[-1])
                    break
            
            source_list = list(f[-2].split(' '))
            target_list = list(f[-1].split(' '))
            self.sx = source_list[1]
            self.sy = source_list[2]
            self.tx = target_list[1]
            self.ty = target_list[2]
            """Saving cost"""
            self.NDcost = {}
            for x in range(self.Bx2+1):
                for y in range(self.By2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x,y+1)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x,y+1)] = self.default_cost
            for y in range(self.By2+1):
                for x in range(self.Bx2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x+1,y)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x+1,y)] = self.default_cost
            num_cost = f[3:3+int(self.size)] # line4 to last
            for NDcost in num_cost:
                NDcost_list = NDcost.split(' ')
                if(NDcost_list[4] == 'x'):
                    self.NDcost[(int(NDcost_list[0]), int(NDcost_list[1]), int(NDcost_list[2]), int(NDcost_list[3]))] = np.inf # cost = Infinity
                else:
                    self.NDcost[(int(NDcost_list[0]), int(NDcost_list[1]), int(NDcost_list[2]), int(NDcost_list[3]))] += int(NDcost_list[4])
        
            print(self.NDcost)
        """Print parameters"""
        print('BoundaryIndex:',self.Bx1,self.By1,self.Bx2,self.By2)
        print('DefaultCost:',self.default_cost)
        print('NumNonDefaultCost:',self.size)
        for i in range(len(num_cost)):
            print(num_cost[i])
        print('Source:',self.sx, self.sy)
        print('Target:',self.tx, self.ty)
    def routing(self):
        self.routing_path = np.zeros((self.Bx2+self.By2+1,2),dtype=int) # total steps
        self.grid_cost = np.empty((self.By2+1,self.Bx2+1), dtype='object')
        self.grid_cost[0][0] = 0

        # ---TODO:
        # fill the min travel cost in self.grid_cost: O(N^2)
        for i in range(self.Bx1, self.Bx2+1):
            for j in range(self.By1, self.By2+1):
                if (i==self.Bx1):
                    if (j==self.By1): # [(0,0)]
                        pass
                    else:
                        self.grid_cost[i][j] = self.grid_cost[i][j-1]+self.NDcost[i,j-1,i,j]
                elif (j==self.By1):
                    self.grid_cost[i][j] = self.grid_cost[i-1][j]+self.NDcost[i-1,j,i,j]
                else:
                    from_left = self.grid_cost[i-1][j]+self.NDcost[i-1,j,i,j]
                    from_below = self.grid_cost[i][j-1]+self.NDcost[i,j-1,i,j]
                    if (from_left <= from_below):
                        self.grid_cost[i][j] = from_left
                    else: 
                        self.grid_cost[i][j] = from_below
        
        # fill Routing Path
        for step in range(1,len(self.routing_path)):
            if step == 1:
                self.routing_path[-1] = [self.Bx2,self.By2]
            else:
                lx, ly = self.routing_path[-step+1] #last spot
                if self.grid_cost[lx-1, ly] <= self.grid_cost[lx, ly-1]:
                    self.routing_path[-step] = [lx-1,ly]
                else:
                    self.routing_path[-step] = [lx,ly-1]
        # ---

    def output(self): # You can modify it by yourself, but the output format should be correct.
        with open("%s" % args.output, 'w', newline='') as file_out:
            file_out.writelines('RoutingCost %d'% self.grid_cost[self.By2][self.Bx2])
            file_out.writelines('\nRoutingPath %d'% len(self.routing_path))
            for i in range(len(self.routing_path)):
                file_out.writelines('\n%d %d'% (self.routing_path[i][0], self.routing_path[i][1]))
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './5x5.in',help="Input file root.")
    parser.add_argument("--output", type=str, default = './5x5.out',help="Output file root.")
    args = parser.parse_args()

    print('#################################################')
    print('#              Monotonic Routing                #')
    print('################################################# \n')

    routing = mono_routing(args)
    """Parser"""
    routing.parser()
    print('################ Parser Down ####################')
    """monotonic route"""
    start = time.time()
    routing.routing()
    print('run time:', round(time.time()-start,3))
    """output"""
    routing.output()
