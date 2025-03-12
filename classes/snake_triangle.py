import numpy as np
from classes.snake import Snake

class SnakeTriangle(Snake):
    def __init__(self,field=None,type_search='bfs',sort='default'):
        self.field=field
        self.movements=np.array([-np.pi/3,np.pi/3])
        self.V=(np.sqrt(3)/3)*self.field.size_pixel #Step forward
        #Creating head
        self.head=np.eye(4) #Begin on center
        pos_initial=((np.sqrt(3)/6)*self.field.size_pixel,(1/2)*self.field.size_pixel,0)
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
        y=(pos[1]*self.field.size_pixel/2 - self.field.height/2) + self.field.size_pixel/2
        x=(pos[0]*np.sqrt(3)*self.field.size_pixel/2 - self.field.width/2) + np.sqrt(3)*self.field.size_pixel/4
        if pos[0]%2==pos[1]%2:
            x+=np.sqrt(3)*self.field.size_pixel/12
        else:
            x-=np.sqrt(3)*self.field.size_pixel/12
        return (x,y)

    def coord_to_id(self,pos):
        height=self.field.size_pixel*self.field.map.shape[1]/2
        idy=int((pos[1] + height/2)//(self.field.size_pixel/2))
        idx=int((pos[0] + self.field.width/2)//(np.sqrt(3)*self.field.size_pixel/2))
        return (idx,idy)

    def build_head(self,pos):
        shapes=[]
        #Building triangle
        l=self.field.size_pixel-30
        theta=np.linspace(-2*np.pi/3,2*np.pi/3,3,endpoint=True)
        vertices=[[(np.sqrt(3)*l/3)*np.cos(i),
                   (np.sqrt(3)*l/3)*np.sin(i),
                   0,
                   1] for i in theta]
        shapes.append(np.array(vertices))
        #Building triangle
        theta=np.linspace(-np.pi/2,np.pi/2,3,endpoint=True)
        vertices=[[(np.sqrt(3)*l/6)*np.cos(i),
                   (np.sqrt(3)*l/6)*np.sin(i),
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
            snake_body=self.shape_head[0][1:2]
            point_0=self.shape_head[0][0:1]
            point_2=self.shape_head[0][2:3]
            reverse_way=np.empty([0,4])
            dist_aux=30
            for part in self.shape_body:
                snake_body=np.append(snake_body,point_2,axis=0)
                reverse_way=np.append(reverse_way,point_0,axis=0)
                # Straight
                # 2 = 1 -> 1
                if np.sqrt(np.sum((point_2-part[1:2])**2))<dist_aux:
                    snake_body=np.append(snake_body,part[1:2],axis=0)
                # 2 = 2-> x
                elif np.sqrt(np.sum((point_2-part[2:3])**2))<dist_aux:
                    reverse_way=np.append(reverse_way,part[1:2],axis=0)
                point_0=part[0:1]
                point_2=part[2:3]
            snake_body=np.append(snake_body,part[2:3],axis=0)
            snake_body=np.append(snake_body,part[0:1],axis=0)
            snake_body=np.append(snake_body,reverse_way[::-1],axis=0)
        else:
            snake_body=self.shape_head[0]
        self.draw_face(snake_body,'green',pen)
        self.draw_face(self.shape_head[1],'blue',pen)