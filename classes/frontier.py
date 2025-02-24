class Stack():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
    
    def remove(self):
        if self.empty():
            raise Exception('Frontier empty!')
        else:
            return self.frontier.pop()

    def empty(self):
        return len(self.frontier) == 0


class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception('Frontier empty!')
        else:
            return self.frontier.pop(0)


class QueueSort(Queue):
    def add(self, node):
        if self.empty() or self.frontier[-1].value<=node.value:
            self.frontier.append(node)
        else:
            #Looking fort the sort position
            for i, _node in enumerate(self.frontier): #O(N)
                if _node.value>node.value: #Min (>), Max (<)
                    self.frontier.insert(i,node)
                    break

##Heap sort
class HeapSort(Stack):
    def add(self, node):
        self.frontier.append(node) #insertion of end 
        j=len(self.frontier)-1 #child
        i=(j-1)//2 #dad
        # While dad bigger than child, swap
        while j>0 and self.frontier[i].value>self.frontier[j].value: #Min (>), Max (<)
            temp=self.frontier[i]
            self.frontier[i]=self.frontier[j]
            self.frontier[j]=temp
            j=i
            i=(j-1)//2
    
    def remove(self):
        if self.empty():
            raise Exception('Frontier empty!')
        else:
            node=self.frontier.pop(0)
            if self.empty() or len(self.frontier) == 1:
                return node
            
            temp=self.frontier.pop() #Remove the last element
            self.frontier.insert(0,temp) #insertion of begin
            i=0 #dad
            j=2*i+1 #child

            while j<len(self.frontier):
                if j<len(self.frontier)-1:
                    if self.frontier[j].value>self.frontier[j+1].value: #Min (>), Max (<)
                        j+=1
                if self.frontier[j].value>=self.frontier[i].value: #Min (>), Max (<)
                    return node
                temp=self.frontier[i]
                self.frontier[i]=self.frontier[j]
                self.frontier[j]=temp
                i=j
                j=2*i+1
            return node


if __name__=='__main__':
    class Node:
        def __init__(self,value):
            self.value=value
    
    inputs=[5,3,6,1,7,2,8,4,5,9]

    print('Stack')
    frontier=Stack()
    for i in inputs:
        frontier.add(Node(i))
        print([x.value for x in frontier.frontier])
    
    print('Queue')
    frontier=Queue()
    for i in inputs:
        frontier.add(Node(i))
        print([x.value for x in frontier.frontier])
    
    print('QueueSort')
    frontier=QueueSort()
    for i in inputs:
        frontier.add(Node(i))
        print([x.value for x in frontier.frontier])
    for i in range(len(frontier.frontier)):
        item=frontier.remove()
        print(item.value)
    print(frontier.frontier)

    print('HeapSort')
    frontier=HeapSort()
    for i in inputs:
        frontier.add(Node(i))
        print([x.value for x in frontier.frontier])
    for i in range(len(frontier.frontier)):
        item=frontier.remove()
        print(item.value)
    print(frontier.frontier)