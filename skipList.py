from random import randint
import sys
#index of the pointer = level of the pointer
class Node:
    def __init__(self, value):
        self.value = value
        self.pointers = {}
        self.index = None


    def set_pointer(self,pointer, level):
        self.pointers[level] = pointer




class SkipList:
    def __init__(self):
        self.firstNode = Node(None)
        self.firstNode.set_pointer(None,0)
        self.elements = 0

    def max_level(self):
        return len(list(self.firstNode.pointers))

    def get_random(self):
        lvl = 0
        while randint(1,100) > 50:
            lvl = lvl+1
            if lvl == self.max_level():
                self.firstNode.set_pointer(None,self.max_level() )
                break

        return lvl 


    def get_first(self):
        return self.firstNode.pointers[0]




    def add_value(self, value):
        
        self.elements += 1

        new_node = Node(value)
        node_to_insert_after, pointers_to_break = self.search(value)
        max_lvl = self.get_random()

        for level in node_to_insert_after.pointers:
            pointers_to_break[level] = node_to_insert_after

        for lvl in pointers_to_break:
            if lvl <=max_lvl:
                forward_to = pointers_to_break[lvl].pointers[lvl]
                pointers_to_break[lvl].set_pointer(new_node,lvl)
                new_node.set_pointer(forward_to,lvl)
            else:
                break
        for i in range(0, max_lvl+1):
            if i not in pointers_to_break:
                new_node.set_pointer(None, i)
                self.firstNode.set_pointer(new_node,i)




    def remove_value(self,value):
        # current node is the one we need to delete if value is found
        maybe_delete_node, pointers_to_break = self.search(value)
        if maybe_delete_node.value == value:
            #print("a")
            for lvl in pointers_to_break:
                if lvl in maybe_delete_node.pointers:
                    forward_to = maybe_delete_node.pointers[lvl]
                    pointers_to_break[lvl].set_pointer(forward_to,lvl)
            self.elements -= 1
            return value
        else:
            return None

    def print_list(self):
        for i in range (self.max_level()-1, -1,-1 ):
            sys.stdout.write("lvl " + str(i) +" :::")
            node = self.firstNode.pointers[i]
            while node is not None:
                try:
                    sys.stdout.write(" -> " + str(node.value))
                except:
                    sys.stdout.write("first one")
                node = node.pointers[i]
            print("\n")



    def search(self, value):
        raise Exception("SHould be never called")



class SkipListIncr(SkipList):
    def __init__(self):
        super().__init__()

    def search(self, value):
        current_node = self.firstNode
        lvl = self.max_level()-1
        prev_pointers = {}
        # while the level is not -1
        while lvl >= 0:
            # keep going down levels till we find pointer to a smaller value
            if current_node.pointers[lvl] == None or current_node.pointers[lvl].value > value:
                lvl -= 1
            # if we found the pointer, go there and loop again
            else:
                # save in prev_pointers previous pointers that'll be interupted
                for level in current_node.pointers:
                    prev_pointers[level] = current_node
                if current_node.pointers[lvl].value < value:
                    current_node = current_node.pointers[lvl]
                elif lvl >0:
                    lvl = lvl-1
                else:
                    current_node = current_node.pointers[lvl]
        # if we looped till here, nothing found
        return (current_node, prev_pointers)




class SkipListDecr(SkipList):
    def __init__(self):
        super().__init__()


    def search(self, value):
        current_node = self.firstNode
        lvl = self.max_level()-1
        prev_pointers = {}
        # while the level is not -1
        while lvl >= 0:
            # keep going down levels till we find pointer to a smaller value
            if current_node.pointers[lvl] == None or current_node.pointers[lvl].value < value:
                lvl -= 1
            # if we found the pointer, go there and loop again
            else:
                # save in prev_pointers previous pointers that'll be interupted
                for level in current_node.pointers:
                    prev_pointers[level] = current_node
                if current_node.pointers[lvl].value > value:
                    current_node = current_node.pointers[lvl]
                elif lvl >0:
                    lvl = lvl-1
                else:
                    current_node = current_node.pointers[lvl]
        # if we looped till here, nothing found
        return (current_node, prev_pointers)


class SkipListMedian:
    def __init__(self):
        self.lstLessThnMedian = SkipListDecr()
        self.greaterThnMedian = SkipListIncr()
        self.skip = False
    def median(self):
        if (self.lstLessThnMedian.elements + self.greaterThnMedian.elements) == 0:
           # print("Wrong!")
            return None
        if self.lstLessThnMedian.elements > self.greaterThnMedian.elements:
            #print("less:")
           # print(self.lstLessThnMedian.get_first().value)
            return self.lstLessThnMedian.get_first().value
        elif self.lstLessThnMedian.elements < self.greaterThnMedian.elements:
            #print("greater:")
            #print(self.greaterThnMedian.get_first().value)
            return self.greaterThnMedian.get_first().value  
        else:
            #print("median:")
            #print(float ((self.lstLessThnMedian.get_first().value +  self.greaterThnMedian.get_first().value) )/2  )
            return float ((self.lstLessThnMedian.get_first().value +  self.greaterThnMedian.get_first().value) )/2         

    def print_median(self):
        if not self.skip:
            if (self.lstLessThnMedian.elements + self.greaterThnMedian.elements) == 0 :
                print("Wrong!")
            else:
                if str(self.median())[-2:] == '.0':
                    print(str(self.median())[:-2])
                else:
                    print(self.median())
        else:
            self.skip = False

            
    def add(self, new_val):
        if  self.median() is None or new_val >= self.median():
            #print("adding {} to greater than median".format(new_val))
            self.greaterThnMedian.add_value(new_val)
        else:
            #print("adding {} to less than median".format(new_val))
            self.lstLessThnMedian.add_value(new_val)
        self.balanceIfNeeded()

    def remove(self, val_remove):
        if self.median() is None:
           # print("Wrong!")
            return
        if  val_remove >= self.median():
            #print("removing {} from greater than median".format(val_remove))
            result = self.greaterThnMedian.remove_value(val_remove)
            if result is None:
                #print(" {} not found in greater than median, removing from less".format(val_remove))
                result = self.lstLessThnMedian.remove_value(val_remove) 
                if result == None:
                    self.skip = True
                    print("Wrong!")
        else:
            #print("removing {} from less than median".format(val_remove))
            result = self.lstLessThnMedian.remove_value(val_remove)   
            if result is None:
                #print(" {} not found in less than median, removing from greater".format(val_remove))
                result = self.greaterThnMedian.remove_value(val_remove) 
                if result == None:
                    self.skip = True
                    print("Wrong!")
        self.balanceIfNeeded()

    def balanceIfNeeded(self):
        if  self.lstLessThnMedian.elements > self.greaterThnMedian.elements+1:
            #print("b")
            el_to_move = self.lstLessThnMedian.get_first().value
            self.lstLessThnMedian.remove_value(el_to_move)
            self.greaterThnMedian.add_value(el_to_move)
            #print("moved {} from less to greater ".format(el_to_move))
            #print("greater")
            #self.greaterThnMedian.print_list()
            #print("less")
            #self.lstLessThnMedian.print_list()
        elif self.lstLessThnMedian.elements +1 < self.greaterThnMedian.elements:
            #print("a")
            el_to_move = self.greaterThnMedian.get_first().value
            self.greaterThnMedian.remove_value(el_to_move)
            self.lstLessThnMedian.add_value(el_to_move)
            #print("moved {} from greater to less ".format(el_to_move))
            #print("greater")
            #self.greaterThnMedian.print_list()
            #print("less")
            #self.lstLessThnMedian.print_list()

if __name__ == "__main__":
    skipLst = SkipListMedian()


    skipLst.add( -2147483648)
    skipLst.print_median()
    skipLst.add( -2147483648)
    skipLst.print_median()
    skipLst.add( -2147483647)
    skipLst.print_median()
    skipLst.remove(  -2147483648)
    skipLst.print_median()
    skipLst.add( 2147483647)
    skipLst.print_median()
    skipLst.remove(  -2147483648)
    skipLst.print_median()
    skipLst.add( 10)
    skipLst.print_median()
    skipLst.add( 10)
    skipLst.print_median()
    skipLst.add( 10)
    skipLst.print_median()
    skipLst.remove(  10)
    skipLst.print_median()
    skipLst.remove(  10)
    skipLst.print_median()
    skipLst.remove(  10)
    skipLst.print_median()
    skipLst.remove(  100)
    skipLst.print_median()
    skipLst.remove(  100)
    skipLst.print_median()
    skipLst.remove(  100)
    skipLst.print_median()
    skipLst.remove(  -2147483648)
    skipLst.print_median()
    skipLst.remove(  2147483647)
    skipLst.print_median()
    skipLst.remove(  10)
    skipLst.print_median()
    skipLst.add( 1)
    skipLst.print_median()
    skipLst.add( -1)
    skipLst.print_median()
    skipLst.add( 1)
    skipLst.print_median()
    skipLst.add( -1)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.remove(  -1)
    skipLst.print_median()
    skipLst.remove(  -1)
    skipLst.print_median()
    skipLst.remove(  -1)
    skipLst.print_median()
    skipLst.remove(  -1)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.remove(  0)
    skipLst.print_median()
    skipLst.add( 0)
    skipLst.print_median()
    skipLst.add( 1)
    skipLst.print_median()
    skipLst.add( 2147483647)
    skipLst.print_median()
    skipLst.add( 2)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.add( 2147483646)
    skipLst.print_median()
    skipLst.remove(  2)
    skipLst.print_median()
    skipLst.add( 2147483640)
    skipLst.print_median()
    skipLst.add( 10)
    skipLst.print_median()
    skipLst.remove(  2)
    skipLst.print_median()
    skipLst.remove(  2)
    skipLst.print_median()
    skipLst.remove(  2)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.remove(  1)
    skipLst.print_median()
    skipLst.add( 2147483640)
    skipLst.print_median()
    skipLst.add( 2147483640)
    skipLst.print_median()
    skipLst.add( -2147483648)
    skipLst.print_median()
    skipLst.add( -2147483640)
    skipLst.print_median()
    skipLst.remove(  2147483640)
    skipLst.print_median()


