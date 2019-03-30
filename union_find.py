class Element:
    def __init__(self, val):
        self.parent = self
        self.value = val
        self.max_length = 0
        self.size = 1




class Union_find:
    def __init__(self, values):
        self.people = {}
        for i in range(1,values+1):
            self.people[i] = Element(i)


def union(root_one, root_two):
    print("call to union")
    if root_one.max_length > root_two.max_length:
        print("a")
        root_two.parent = root_one
        if root_two.size == root_one.size:
            print("c")
            root_one.max_length +=1
        root_one.size += root_two.size
        root_two.size = None
    else:
        print("b")
        root_one.parent = root_two
        if root_two.size == root_one.size:
            print("c")
            root_two.max_length +=1
        root_two.size += root_one.size
        root_one.size = None

def find_set(looked):
    elem = looked
    while elem != elem.parent:
        print("!")
        elem = elem.parent
    looked.parent 
    return elem




Inp = input()
N, C = Inp.strip().split(' ')
disjoint_set = Union_find(int(N))

for i in range(0, int(C)):
    tmp = input().strip().split(' ')
    if len(tmp) == 2:
        print(find_set(disjoint_set.people[int(tmp[1]) ]).size )
    else:
        person_one = disjoint_set.people[int(tmp[1])]
        person_two = disjoint_set.people[int(tmp[2])]
        root_one = find_set(person_one)
        root_two = find_set(person_two)
        if root_one != root_two:
            union(root_one,root_two)


