import math
import tkinter
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
from queue import PriorityQueue
import time
import random


start_point = None
end_point = None

start_point_bool = False
end_point_bool = False

graph = {}

draw_shortest_path = []
draw_graph_array = []
draw_graph_bool = False

btn_draw_graph = None
draw_map = []

n = 0
m = 0

def random_map():
    global draw_map
    for i in range(len(draw_map)):
        canvas.delete(draw_map[i])
    global coordinates
    
    global start_point_bool
    global end_point_bool
    global leftclicked_id
    global rightclicked_id

    global start_point
    global end_point

    global draw_graph_array
    global draw_graph_bool

    
    
    if (start_point_bool==True):
        canvas.delete(leftclicked_id)
    if (end_point_bool==True):
        canvas.delete(rightclicked_id)
    start_point_bool = False
    end_point_bool = False
    start_point = None
    end_point = None

    for i in range(len(draw_shortest_path)):
        canvas.delete(draw_shortest_path[i])

    btn_draw_graph['text'] = "Hiện đường đi"
    for i in range(len(draw_graph_array)):
        canvas.delete(draw_graph_array[i])
    draw_graph_array = []
    draw_graph_bool = False

    coordinates = []
    draw_map = []
    global line

    random_map_id = random.randint(1,1)

    with open(f"maps/map{random_map_id}.txt") as file:
        line = file.read().splitlines()

    for i in range(len(line)-1):
        a = line[i].split(" ")
        b = line[i+1].split(" ")
        coordinates.append((int(a[0]), int(a[1])))
        tmp = canvas.create_line(int(a[0]), int(a[1]), int(b[0]), int(b[1]), fill="black", width=2)
        draw_map.append(tmp)
    coordinates.append((int(line[0].split(" ")[0]), int(line[0].split(" ")[1])))

def create_graph():
    global coordinates
    global graph
    global n
    global m
    n = 0
    m = 0
    graph = {}
    main_polygon = Polygon(coordinates)

    for i in range(len(coordinates)):
        graph[i]=[]
        n = n+1

    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            if (i!=j):
                m = m+1
                
                path = LineString([coordinates[i], coordinates[j]])
                point = path.interpolate(0.5)

                if not path.crosses(main_polygon):
                    if (main_polygon.contains(point) or abs(i-j)==1):
                        tmp1 = [j, math.sqrt((coordinates[i][0]-coordinates[j][0])**2 + (coordinates[i][1]-coordinates[j][1])**2)]
                        graph[i].append(tmp1)

def draw_lines():
    global coordinates
    global draw_graph_array
    global start_point
    global end_point


    main_polygon = Polygon(coordinates)
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            if (i!=j):
                
                path = LineString([coordinates[i], coordinates[j]])
                point = path.interpolate(0.5)

                if not path.crosses(main_polygon):
                    if (main_polygon.contains(point)):
                        tmp = canvas.create_line(coordinates[i][0], coordinates[i][1], coordinates[j][0], coordinates[j][1], fill="gray", width=1)
                        draw_graph_array.append(tmp)
    for i in range(len(coordinates)):
        path = LineString([coordinates[i], start_point])
        point = path.interpolate(0.5)
        if not path.crosses(main_polygon):
            if (main_polygon.contains(point)):
                tmp = canvas.create_line(coordinates[i][0], coordinates[i][1], start_point.x, start_point.y, fill="gray", width=1)
                draw_graph_array.append(tmp)
    for i in range(len(coordinates)):
        path = LineString([coordinates[i], end_point])
        point = path.interpolate(0.5)
        if not path.crosses(main_polygon):
            if (main_polygon.contains(point)):
                tmp = canvas.create_line(coordinates[i][0], coordinates[i][1], end_point.x, end_point.y, fill="gray", width=1)
                draw_graph_array.append(tmp)
    
    path = LineString([start_point, end_point])
    point = path.interpolate(0.5)
    if not path.crosses(main_polygon):
        if (main_polygon.contains(point)):
            tmp = canvas.create_line(start_point.x, start_point.y, end_point.x, end_point.y, fill="gray", width=1)
            draw_graph_array.append(tmp)

def draw_graph():
    global btn_draw_graph
    global draw_graph_bool
    global draw_graph_array

    
    if not draw_graph_bool:
        btn_draw_graph['text'] = "Ẩn đường đi"
        draw_graph_bool = True
        draw_lines()
    else:
        btn_draw_graph['text'] = "Hiện đường đi"
        for i in range(len(draw_graph_array)):
            canvas.delete(draw_graph_array[i])
        draw_graph_array = []
        draw_graph_bool = False

def draw_start_point(event):
    global start_point_bool
    global leftclicked_id
    global draw_graph_bool
    global draw_graph_array

    global start_point
    global end_point

    global draw_shortest_path

    for i in range(len(draw_shortest_path)):
        canvas.delete(draw_shortest_path[i])
    draw_shortest_path = []

    x1 = event.x-3
    y1 = event.y-3
    x2 = event.x+3
    y2 = event.y+3
    x = event.x
    y = event.y
    tmppoint = Point(x, y)
    
    polygon = Polygon(coordinates)
    
    if polygon.contains(tmppoint):
        start_point = tmppoint
        if not start_point_bool:
            leftclicked_id = canvas.create_oval(x1,y1,x2,y2,fill="red", outline="")
            start_point_bool = True
        else:
            canvas.delete(leftclicked_id)
            leftclicked_id = canvas.create_oval(x1,y1,x2,y2,fill="red", outline="")

    if draw_graph_bool:
        draw_lines()


def draw_end_point(event):
    global end_point_bool
    global rightclicked_id
    global draw_graph_bool
    global draw_graph_array

    global start_point
    global end_point
    global n
    global m

    global draw_shortest_path

    for i in range(len(draw_shortest_path)):
        canvas.delete(draw_shortest_path[i])
    draw_shortest_path = []

    x1 = event.x-3
    y1 = event.y-3
    x2 = event.x+3
    y2 = event.y+3
    x = event.x
    y = event.y
    tmppoint = Point(x, y)
    
    polygon = Polygon(coordinates)
    if polygon.contains(tmppoint):
        end_point = tmppoint
        if not end_point_bool:
            rightclicked_id = canvas.create_oval(x1,y1,x2,y2,fill="green", outline="")
            end_point_bool = True          
        else:
            canvas.delete(rightclicked_id)
            rightclicked_id = canvas.create_oval(x1,y1,x2,y2,fill="green", outline="") 

    if draw_graph_bool:
        draw_lines()

def dijkstra():
    global n
    global m
    global draw_shortest_path

    start_time = time.time()
    if (start_point_bool == True and end_point_bool == True):
        print(end_point)
        print(start_point)
        print("Dijkstra")
        create_graph()
        
        graph[n] = []
        n=n+1
        graph[n] = []
        n=n+1
        
        polygon = Polygon(coordinates)
        for i in range(len(coordinates)-1):
            path = LineString([coordinates[i], end_point])
            if not path.crosses(polygon):
                tmp1 = [i, math.sqrt((coordinates[i][0]-end_point.x)**2 + (coordinates[i][1]-end_point.y)**2)]
                graph[n-2].append(tmp1)

                tmp2 = [n-2, math.sqrt((coordinates[i][0]-end_point.x)**2 + (coordinates[i][1]-end_point.y)**2)]
                graph[i].append(tmp2)

        for i in range(len(coordinates)-1):
            path = LineString([coordinates[i], start_point])
            if not path.crosses(polygon):
                tmp1 = [i, math.sqrt((coordinates[i][0]-start_point.x)**2 + (coordinates[i][1]-start_point.y)**2)]
                graph[n-1].append(tmp1)

                tmp2 = [n-1, math.sqrt((coordinates[i][0]-start_point.x)**2 + (coordinates[i][1]-start_point.y)**2)]
                graph[i].append(tmp2)

        path = LineString([end_point, start_point])
        if not path.crosses(polygon):
            tmp1 = [n-1, math.sqrt((end_point.x-start_point.x)**2 + (end_point.y-start_point.y)**2)]
            graph[n-2].append(tmp1)

            tmp2 = [n-2, math.sqrt((end_point.x-start_point.x)**2 + (end_point.y-start_point.y)**2)]
            graph[n-1].append(tmp2)
        
        start = n-2
        end = n-1
        visited = []
        distance = []
        par = []
        for i in range(n):
            visited.append(False)
            distance.append(float('inf'))
            par.append(None)
        distance[start] = 0
        pq = PriorityQueue()
        pq.put((0, start))
        while not pq.empty():
            (d, v) = pq.get()
            visited[v] = True
            for i in range(len(graph[v])):
                if not visited[graph[v][i][0]] and distance[v] + graph[v][i][1] < distance[graph[v][i][0]]:
                    distance[graph[v][i][0]] = distance[v] + graph[v][i][1]
                    par[graph[v][i][0]] = v
                    pq.put((distance[graph[v][i][0]], graph[v][i][0]))
        print(distance[end])
        distancetoend = distance[end]
        coordinates.append((end_point.x, end_point.y))
        coordinates.append((start_point.x, start_point.y))
        while par[end] != None:
            
            tmp = canvas.create_line(coordinates[par[end]][0], coordinates[par[end]][1], coordinates[end][0], coordinates[end][1], fill="blue", width=2)
            print(end, " ", par[end], " ", coordinates[end], " ", coordinates[par[end]])
            draw_shortest_path.append(tmp)
            end = par[end]
        coordinates.pop()
        coordinates.pop()
    elapsed_time = time.time() - start_time
    timetext['text'] = "Thời gian chạy: " + "{:.2f}".format(elapsed_time) + " giây"
    print(distance[end])
    distancetext['text'] = "Khoảng cách: " + "{:.2f}".format(distancetoend) + " px"

if __name__ == '__main__':
    
    window = tkinter.Tk()
    window.title("Đường đi ngắn nhất trên đa giác")
    window.geometry("1300x760")
    window['bg'] = 'white'
    btn_dijkstra = tkinter.Button(window, text="Tìm đường đi ngắn nhất", command=dijkstra, fg = 'black', bg = 'gray')
    btn_dijkstra.place(relx=0.1, rely=0.05, anchor="center")
    
    btn_draw_graph = tkinter.Button(window, text="Hiện đường đi", command=draw_graph, fg = 'black', bg = 'gray')
    btn_draw_graph.place(relx=0.2, rely=0.05, anchor="center")

    random_map = tkinter.Button(window, text="Tạo đa giác", command=random_map, fg = 'black', bg = 'gray')
    random_map.place(relx=0.3, rely=0.05, anchor="center")

    canvas = tkinter.Canvas(window, width=1500, height=700, bg="white")
    canvas.pack(side="top", fill="both", expand="true")
    for x in range(1,1500,50):
        for y in range(1,700,50):
            canvas.create_rectangle(x, y, x+50, y+50, outline='gray', width=0.1)
    canvas.place(relx=0.5, rely=0.6, anchor="center")
    
    timetext = tkinter.Label(window, text="Thời gian chạy: ")
    timetext.place(relx=0.1, rely=0.1, anchor="center")

    distancetext = tkinter.Label(window, text="Khoảng cách: ")
    distancetext.place(relx = 0.2, rely=0.1, anchor="center")

    tkinter.Label(window, text="Hướng dẫn: \n1. Nhấn nút 'Tạo đa giác' để tạo đa giác ngẫu nhiên \n2. Nhấn nút 'Tìm đường đi ngắn nhất' để tìm đường đi ngắn nhất \n3. Nhấn nút 'Hiện đường đi' để hiện tất cả các cạnh có thể đi").place(relx=0.5, rely=0.07, anchor="center")

    coordinates = []
    

    create_graph()

    canvas.bind('<Button-1>', draw_start_point)
    canvas.bind('<Button-3>', draw_end_point)

    
    window.mainloop() 