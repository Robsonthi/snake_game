import numpy as np
import time
import random as rd
from classes.frontier import Stack, Queue, QueueSort, HeapSort
from classes.node import Node

def rotAxis(vec,ref,theta,n_axis):
    a,b,c=ref[0][3],ref[1][3],ref[2][3]
    u,v,w=ref[0][n_axis],ref[1][n_axis],ref[2][n_axis]
    ct=np.cos(theta)
    st=np.sin(theta)
    R=np.array([[u**2+(v**2+w**2)*ct, u*v*(1-ct)-w*st, u*w*(1-ct)+v*st, (a*(v**2+w**2)-u*(b*v+c*w))*(1-ct)+(b*w-c*v)*st],
               [u*v*(1-ct)+w*st, v**2+(u**2+w**2)*ct, v*w*(1-ct)-u*st, (b*(u**2+w**2)-v*(a*u+c*w))*(1-ct)+(c*u-a*w)*st],
               [u*w*(1-ct)-v*st, v*w*(1-ct)+u*st, w**2+(u**2+v**2)*ct, (c*(u**2+v**2)-w*(a*u+b*v))*(1-ct)+(a*v-b*u)*st],
               [0,0,0,1]])
    return np.matmul(R,vec)

def trans(vec,coord=(0,0,0)):
    mat=np.array([[1,0,0,coord[0]],
                    [0,1,0,coord[1]],
                    [0,0,1,coord[2]],
                    [0,0,0,1]])
    return np.matmul(mat,vec)

class Snake:
    def __init__(self,field=None,type_search='bfs',sort='default'):
        self.field=field
        self.movements=np.array([-np.pi/2,0.,np.pi/2])
        self.V=self.field.size_pixel #Step forward
        #Creating head
        self.head=np.eye(4) #Begin on center
        pos_initial=(self.field.size_pixel//2,self.field.size_pixel//2,rd.choice(self.movements))
        self.shape_head=self.build_head(pos_initial)#List 2 shapes
        self.head=self.move(vec=self.head,pos=pos_initial) #Vector 4x4
        #Creating body
        self.body=[] #List of tuples 2 values
        self.shape_body=[] #List of arrays 2d
        #Update map
        idx,idy=self.coord_to_id((self.head[0,3],self.head[1,3]))
        self.field.map[idx][idy]=1.
        #Generating the goal
        self.pos_goal,self.shape_goal=self.goal_generation() #Tuple 2 values, Array 2d
        self.type_search=type_search #'bfs', 'dfs', 'greedy', 'a*'
        self.sort=sort #'default', 'heap' -> work just with 'greedy', 'a*'
    
    def id_to_coord(self,pos):
        x=(pos[0]*self.field.size_pixel - self.field.width/2) + (self.field.size_pixel//2)
        y=(pos[1]*self.field.size_pixel - self.field.height/2) + (self.field.size_pixel//2)
        return (x,y)

    def coord_to_id(self,pos):
        idx=int((pos[0] + self.field.width/2)//self.field.size_pixel)
        idy=int((pos[1] + self.field.height/2)//self.field.size_pixel)
        return (idx,idy)

    def move(self,vec,pos):
        return trans(rotAxis(vec,self.head,pos[2],2),(pos[0],pos[1],0))

    def move_head(self,pos):
        for i,shape in enumerate(self.shape_head):
            for j,point in enumerate(shape):
                self.shape_head[i][j]=self.move(point,pos)
        return self.shape_head

    def build_head(self,pos):
        shapes=[]
        #Building square
        l=self.field.size_pixel-10
        theta=np.linspace(0,2*np.pi,4,endpoint=False)
        vertices=[[(l/2)*(np.cos(i)-np.sin(i)),
                   (l/2)*(np.cos(i)+np.sin(i)),
                   0,
                   1] for i in theta]
        shapes.append(np.array(vertices))
        #Building triangle
        theta=np.linspace(-np.pi/2,np.pi/2,3,endpoint=True)
        vertices=[[(3*l/8)*np.cos(i),
                   (3*l/8)*np.sin(i),
                   0,
                   1] for i in theta]
        shapes.append(np.array(vertices))
        self.shape_head=shapes
        self.shape_head=self.move_head(pos)
        return self.shape_head

    def get_angle(self):
        nx=self.head[0][0]
        ny=self.head[1][0]
        angle=np.arctan2(ny,nx)
        if angle>np.pi:
            angle-=2*np.pi
        elif angle<-np.pi:
            angle+=2*np.pi
        return angle
    
    @staticmethod
    def draw_face(shape,color,pen):
        pen.setpos(shape[0][0],shape[0][1])
        pen.down()
        pen.color('black',color)
        #pen.fillcolor(color)
        pen.begin_fill()
        for point in shape[1:]:
            pen.goto(point[0],point[1])
        pen.goto(shape[0][0],shape[0][1])
        pen.end_fill()
        pen.up()
    
    def draw_snake(self,pen):
        #Draw goal
        self.draw_face(self.shape_goal,'blue',pen)
        #Draw Snake
        if len(self.body)>0:
            snake_body=self.shape_head[0][0:1]
            point_1=self.shape_head[0][1:2]
            #point_2=self.shape_head[0][2:3]
            reverse_way=self.shape_head[0][3:4]
            dist_aux=15
            for part in self.shape_body:
                # Straight
                # 1 = 3 -> 0
                if np.sqrt(np.sum((point_1-part[3:4])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[0:1],axis=0)
                    reverse_way=np.append(reverse_way,part[2:3],axis=0)
                # 1 = 1 -> 1
                elif np.sqrt(np.sum((point_1-part[1:2])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[1:2],axis=0)
                    reverse_way=np.append(reverse_way,part[3:4],axis=0)
                point_1=part[1:2]
            snake_body=np.append(snake_body,part[1:3],axis=0)
            snake_body=np.append(snake_body,reverse_way[::-1],axis=0)
        else:
            snake_body=self.shape_head[0]
        self.draw_face(snake_body,'green',pen)
        self.draw_face(self.shape_head[1],'blue',pen)
    
        
    def goal_generation(self):
        id_=rd.choice(np.argwhere(self.field.map==0.)) #Choice a empty place
        self.pos_goal=self.id_to_coord(id_) #Tuple 2 values
        self.shape_goal=self.build_goal() #Array 2d
        self.field.map[id_[0]][id_[1]]=-1.
        return self.pos_goal,self.shape_goal
    
    def build_goal(self):
        r=20
        #Building circle
        theta=np.linspace(0,2*np.pi,10,endpoint=False)
        vertices=[[r*np.cos(i),
                   r*np.sin(i),
                   0,
                   1] for i in theta]
        self.shape_goal=np.array(vertices)
        for i,point in enumerate(self.shape_goal):
            self.shape_goal[i]=trans(point,(self.pos_goal[0],self.pos_goal[1],0))
        return self.shape_goal
    
    def distance_to_goal(self):
        d_idx=self.pos_goal[0]-self.head[0,3]
        d_idy=self.pos_goal[1]-self.head[1,3]
        return np.sqrt(d_idx**2 + d_idy**2)

    def angle_to_goal(self):
        d_idx=self.pos_goal[0]-self.head[0,3]
        d_idy=self.pos_goal[1]-self.head[1,3]
        theta_ref=np.arctan2(d_idy,d_idx)
        if theta_ref>np.pi:
            theta_ref-=2*np.pi
        elif theta_ref<-np.pi:
            theta_ref+=2*np.pi
        return theta_ref
    
    def arrived_goal(self):
        return self.distance_to_goal()<15
    
    def update_pos(self,id_movement):
        angle_pos=self.get_angle()
        angle_pos+=self.movements[id_movement]
        dpos=(self.V*np.cos(angle_pos),self.V*np.sin(angle_pos),self.movements[id_movement])
        #Update head
        old_pos_head=(self.head[0,3],self.head[1,3])
        old_shape_head=self.shape_head[0].copy()
        self.shape_head=self.move_head(dpos)
        self.head=self.move(self.head,dpos)
        self.update_map(old_pos_head)
        #Update body
        self.update_body(old_pos_head,old_shape_head)
    
    def update_map(self,old_pos_head):
        idx,idy=self.coord_to_id((self.head[0,3],self.head[1,3]))
        self.field.map[idx][idy]=1.
        if not self.arrived_goal():
            if len(self.body)>0:
                idx,idy=self.coord_to_id(self.body[-1])
                self.field.map[idx][idy]=0.
            else:
                idx,idy=self.coord_to_id(old_pos_head)
                self.field.map[idx][idy]=0.
    
    def update_body(self,old_pos_head,old_shape_head):
        if not self.arrived_goal():
            if len(self.body)>0:
                for i in range(len(self.body)-1,0,-1):
                    self.body[i]=self.body[i-1]
                    self.shape_body[i]=self.shape_body[i-1].copy()
                self.body[0]=old_pos_head
                self.shape_body[0]=old_shape_head
        else:
            self.body.insert(0,old_pos_head)
            self.shape_body.insert(0,old_shape_head)
            self.pos_goal,self.shape_goal=self.goal_generation()

    def trying(self,movement):
        angle_pos=self.get_angle()
        angle_pos+=movement
        dpos=(self.V*np.cos(angle_pos),self.V*np.sin(angle_pos),movement)
        copy_head=self.head.copy()
        copy_head=self.move(copy_head,dpos)
        idx,idy=self.coord_to_id((copy_head[0,3],copy_head[1,3]))
        n=self.field.map.shape[0]
        m=self.field.map.shape[1]
        if (idx>=0 and idx<n) and (idy>=0 and idy<m) and self.field.map[idx][idy]!=1.:
            return True
        return False
        
    def calculating_motion(self):
        angle_pos=self.get_angle()
        B=self.angle_to_goal()
        A=B-angle_pos
        if A>np.pi:
            A-=2*np.pi
        elif A<-np.pi:
            A+=2*np.pi
        A=np.abs(self.movements-A)
        id_movement=np.argmin(A)
        return id_movement
    
    #Choose the shortest movement
    def calculating_motion_dodge(self):
        angle_pos=self.get_angle()
        B=self.angle_to_goal()
        A=B-angle_pos
        if A>np.pi:
            A-=2*np.pi
        elif A<-np.pi:
            A+=2*np.pi
        A=np.abs(self.movements-A)
        id_sort=np.argsort(A)
        for id_movement in id_sort:
            if self.trying(self.movements[id_movement]):
                return id_movement
        print('The end!')
        time.sleep(5)
        exit()
    
    #Choose the longest movement
    def calculating_motion_repel(self):
        angle_pos=self.get_angle()
        B=self.angle_to_goal()
        A=B-angle_pos
        if A>np.pi:
            A-=2*np.pi
        elif A<-np.pi:
            A+=2*np.pi
        A=np.abs(self.movements-A)
        id_sort=(np.argsort(A))[::-1]
        for id_movement in id_sort:
            if self.trying(self.movements[id_movement]):
                return id_movement
        print('The end!')
        time.sleep(5)
        exit()
            
    ## To searching algorithms (temp)
    def move_temp(self,vec,pos):
        return trans(rotAxis(vec,vec,pos[2],2),(pos[0],pos[1],0))
    
    def get_angle_temp(self,head):
        nx=head[0][0]
        ny=head[1][0]
        angle=np.arctan2(ny,nx)
        if angle>np.pi:
            angle-=2*np.pi
        elif angle<-np.pi:
            angle+=2*np.pi
        return angle
    
    def distance_to_goal_temp(self,head):
        d_idx=self.pos_goal[0]-head[0,3]
        d_idy=self.pos_goal[1]-head[1,3]
        return np.sqrt(d_idx**2 + d_idy**2)

    def trying_temp(self,movement,head,map):
        angle_pos=self.get_angle_temp(head)
        angle_pos+=movement
        dpos=(self.V*np.cos(angle_pos),self.V*np.sin(angle_pos),movement)
        copy_head=head.copy()
        copy_head=self.move_temp(copy_head,dpos)
        idx,idy=self.coord_to_id((copy_head[0,3],copy_head[1,3]))
        n=map.shape[0]
        m=map.shape[1]
        if (idx>=0 and idx<n) and (idy>=0 and idy<m) and map[idx][idy]!=1.:
            return True
        return False

    def update_map_temp(self,old_pos_head,head,map,body):
        idx,idy=self.coord_to_id((head[0,3],head[1,3]))
        map[idx][idy]=1.
        if len(body)>0:
            idx,idy=self.coord_to_id(self.body[-1])
            map[idx][idy]=0.
        else:
            idx,idy=self.coord_to_id(old_pos_head)
            map[idx][idy]=0.
        return map

    def update_body_temp(self,old_pos_head,body):
        if len(body)>0:
            for i in range(len(body)-1,0,-1):
                body[i]=body[i-1]
            body[0]=old_pos_head
        return body
        
    def update_pos_temp(self,id_movement,head,map,body):
        angle_pos=self.get_angle_temp(head)
        angle_pos+=self.movements[id_movement]
        dpos=(self.V*np.cos(angle_pos),self.V*np.sin(angle_pos),self.movements[id_movement])
        #Update head
        old_pos_head=(head[0,3],head[1,3])
        head=self.move_temp(head,dpos)
        map=self.update_map_temp(old_pos_head,head,map,body)
        body=self.update_body_temp(old_pos_head,body)
        return head,map,body

    def neighbors(self,head,map):
        children=[]
        for i,movement in enumerate(self.movements):
            if self.trying_temp(movement,head,map):
                children.append(i)
        return children

    def calculating_motion_search(self):
        num_explored = 0
        visited=[]
        start = Node(head=self.head.copy(),
                    map=self.field.map.copy(),
                    body=self.body.copy(),
                    parent=None,
                    action=None, 
                    value=self.distance_to_goal())
        
        if self.type_search=='dfs':
            frontier = Stack()
        elif self.type_search=='bfs':
            frontier = Queue()
        elif (self.type_search=='greedy' or self.type_search=='a*') and self.sort=='default':
            frontier = QueueSort()
        elif (self.type_search=='greedy' or self.type_search=='a*') and self.sort=='heap':
            frontier = HeapSort()

        frontier.add(start)
        while True:
            if frontier.empty():
                time.sleep(1)
                return []
                #raise Exception("No solution")

            node = frontier.remove()
            num_explored += 1

            if self.distance_to_goal_temp(node.head)<(self.V+5):
                solution=[]
                while node.parent is not None:
                    solution.append(node.action)
                    node = node.parent
                solution.reverse()
                if solution==[]:
                    return None
                return solution
            
            idx,idy=self.coord_to_id((node.head[0,3],node.head[1,3]))
            visited.append((idx,idy))
            for action in self.neighbors(node.head,node.map):
                child_head,child_map,child_body=self.update_pos_temp(action,node.head.copy(),node.map.copy(),node.body.copy())
                idx,idy=self.coord_to_id((child_head[0,3],child_head[1,3]))
                if not ((idx,idy) in visited):
                    visited.append((idx,idy))
                    value_child=self.distance_to_goal_temp(child_head)
                    if self.type_search=='a*':
                        value_child+=(node.level+1)*self.V
                    node_child = Node(head=child_head,
                                    map=child_map,
                                    body=child_body,
                                    parent=node,
                                    action=action, 
                                    value=value_child)
                    frontier.add(node_child)
