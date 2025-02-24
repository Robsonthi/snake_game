import numpy as np
from classes.snake import Snake
import random as rd

class SnakeHexagon(Snake):
    def __init__(self,field=None,type_search='bfs',sort='default'):
        self.field=field
        self.movements=np.linspace(-2*np.pi/3,2*np.pi/3,5,True)
        self.V=np.sqrt(3)*self.field.size_pixel #Step forward
        #Creating head
        self.head=np.eye(4) #Begin on center
        pos_initial=((3/4)*np.sqrt(3)*self.field.size_pixel,(3/4)*self.field.size_pixel,rd.choice(self.movements))
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
        y=(pos[1]*3*self.field.size_pixel/2 - self.field.height/2) + self.field.size_pixel
        x=(pos[0]*np.sqrt(3)*self.field.size_pixel - self.field.width/2) + (np.sqrt(3)*3*self.field.size_pixel/4)
        if pos[1]%2==0:
            x+=np.sqrt(3)*self.field.size_pixel/4
        else:
            x-=np.sqrt(3)*self.field.size_pixel/4
        return (x,y)

    def coord_to_id(self,pos):
        idy=int((pos[1] + self.field.height/2)//(3*self.field.size_pixel/2))
        width=np.sqrt(3)*self.field.size_pixel*self.field.map.shape[0]
        idx=int((pos[0] + width/2)//(np.sqrt(3)*self.field.size_pixel))
        return (idx,idy)

    def build_head(self,pos):
        shapes=[]
        #Building hexagon
        l=self.field.size_pixel-10
        theta=np.linspace(np.pi/6,(11/6)*np.pi,6,endpoint=True)
        vertices=[[(l)*np.cos(i),
                   (l)*np.sin(i),
                   0,
                   1] for i in theta]
        shapes.append(np.array(vertices))
        
        #Building triangle
        theta=np.linspace(-np.pi/2,np.pi/2,3,endpoint=True)
        vertices=[[(3*l/4)*np.cos(i),
                   (3*l/4)*np.sin(i),
                   0,
                   1] for i in theta]
        shapes.append(np.array(vertices))
        self.shape_head=shapes
        self.shape_head=self.move_head(pos)
        return self.shape_head

    def draw_snake(self,pen):
        #Draw goal
        self.draw_face(self.shape_goal,'blue',pen)
        #Draw Snake
        if len(self.body)>0:
            snake_body=self.shape_head[0][0:2]
            point_2=self.shape_head[0][2:3]
            point_3=self.shape_head[0][3:4]
            reverse_way=(self.shape_head[0][4:6])[::-1]
            dist_aux=20
            for part in self.shape_body:
                snake_body=np.append(snake_body,point_2,axis=0)
                reverse_way=np.append(reverse_way,point_3,axis=0)
                # Straight
                # 2 = 0 -> 0, 1
                if np.sqrt(np.sum((point_2-part[0:1])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[0:2],axis=0)
                    reverse_way=np.append(reverse_way,(part[4:6])[::-1],axis=0)
                # 2 = 4 -> 4, 5, 0, 1
                elif np.sqrt(np.sum((point_2-part[4:5])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[4:6],axis=0)
                    snake_body=np.append(snake_body,part[0:2],axis=0)
                # 2 = 5 -> 5, 0, 1
                elif np.sqrt(np.sum((point_2-part[5:6])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[5:6],axis=0)
                    snake_body=np.append(snake_body,part[0:2],axis=0)
                    reverse_way=np.append(reverse_way,part[4:5],axis=0)
                # 2 = 1 -> 1
                elif np.sqrt(np.sum((point_2-part[1:2])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[1:2],axis=0)
                    reverse_way=np.append(reverse_way,part[0:1],axis=0)
                    reverse_way=np.append(reverse_way,(part[4:6])[::-1],axis=0)
                # 2 = 2
                elif np.sqrt(np.sum((point_2-part[2:3])**2))<dist_aux:
                    reverse_way=np.append(reverse_way,(part[0:2])[::-1],axis=0)
                    reverse_way=np.append(reverse_way,(part[4:6])[::-1],axis=0)
                point_2=part[2:3]
                point_3=part[3:4]
            snake_body=np.append(snake_body,part[2:4],axis=0)
            snake_body=np.append(snake_body,reverse_way[::-1],axis=0)
        else:
            snake_body=self.shape_head[0]
        self.draw_face(snake_body,'green',pen)
        self.draw_face(self.shape_head[1],'blue',pen)