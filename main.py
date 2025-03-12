import turtle
import os
import time
import numpy as np

from classes.snake import Snake
from classes.snake_hexagon import SnakeHexagon
from classes.snake_triangle import SnakeTriangle
from classes.field import Field, FieldHexagon, FieldTriangle

if __name__=='__main__':
    type_snake='hexagon' #'square', 'hexagon', 'triangle'
    #type_search and sort - Beta Version

    if type_snake=='square':
        map_file='assets/snake12x12.png'
        field=Field(map_file,size_pixel=50)
        snake=Snake(field,type_search='a*',sort='heap') #'dfs', 'bfs', 'greedy' or 'a*'
    elif type_snake=='hexagon':
        map_file='assets/snake_hexagon12x12.png'
        field=FieldHexagon(map_file,size_pixel=50)
        snake=SnakeHexagon(field,type_search='a*',sort='heap') #'dfs', 'bfs', 'greedy' or 'a*'
    else:
        map_file='assets/snake_triangle12x13.png'
        field=FieldTriangle(map_file,size_pixel=100)
        snake=SnakeTriangle(field,type_search='a*',sort='heap') #'dfs', 'bfs', 'greedy' or 'a*'

    #Draw space
    win=turtle.Screen()
    screen_offset=50
    win.setup(field.width+screen_offset,field.height+screen_offset)
    win.bgpic(map_file)
    win.title('Snake')
    win.tracer(0)
    my_pen=turtle.Turtle()
    my_pen.hideturtle()
    my_pen.up()

    time.sleep(15)

    ### Working
    if 1: # With dodge
        while(1):
            os.system('cls')
            print(snake.field.map.T[:][::-1])
            px,py=np.where(snake.field.map == -1)
            print('Goal:',(px[0],py[0]))
            my_pen.clear()
            snake.draw_snake(my_pen)
            win.update()
            #if snake.hit():
                #break
            time.sleep(0.1)
            id_movement=snake.calculating_motion_dodge()
            #id_movement=snake.calculating_motion_repel()
            snake.update_pos(id_movement)
        turtle.done()

    ### DRAFT
    else: #With searching algorithm (beta version)
        os.system('cls')
        print(snake.field.map.T[:][::-1])
        my_pen.clear()
        snake.draw_snake(my_pen)
        win.update()
        time.sleep(0.1)
        while(1):
            list_id_movement=snake.calculating_motion_search()
            if list_id_movement is None:
                id_movement=snake.calculating_motion_dodge()
                snake.update_pos(id_movement)
                os.system('cls')
                print(snake.field.map.T[:][::-1])
                my_pen.clear()
                snake.draw_snake(my_pen)
                win.update()
                time.sleep(0.1)
            elif len(list_id_movement)==0:
                id_movement=snake.calculating_motion_repel()
                snake.update_pos(id_movement)
                os.system('cls')
                print(snake.field.map.T[:][::-1])
                my_pen.clear()
                snake.draw_snake(my_pen)
                win.update()
                time.sleep(0.1)
            else:
                for id_movement in list_id_movement:
                    snake.update_pos(id_movement)
                    os.system('cls')
                    print(snake.field.map.T[:][::-1])
                    my_pen.clear()
                    snake.draw_snake(my_pen)
                    win.update()
                    time.sleep(0.1)
        turtle.done()