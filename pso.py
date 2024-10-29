# import section
import random
from PIL import Image , ImageDraw
import datetime
import time
import math

flock_size = 20
flight_size = 10
awareness_prob = 0.09
maximum_iteration = 5

# class section
class Segment:
    def __init__(self,start,end,y) -> None:
        self.start = start # Start Point
        self.end = end     # End point
        self.y = y
       
class Rectangle:
    def __init__(self, w, h, id) -> None:
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.id = id
        self.bin_id = -1
        self.wasPacked = False

class Crow:
    def __init__(self, position) -> None:
        self.position = position
        self.awareness = awareness_prob
        self.best_position = position
        self.best_items = []
        self.best_value = 0

# method section

def read_items():
    items = []
    i = 2
    for line in base_lines[2:]:
        item = Rectangle(int(line.split(' ')[0]), int(line.split(' ')[1]),i-2)
        items.append(item)
        i+=1
    return items
 
def findSegments(sky, segments, rect):

    for segment in sky:
        if rect.w + segment.start <= bin_width and rect.h + segment.y <= bin_height:
            # then item less than segment width or is equal to width of segment
            if rect.w + segment.start <= segment.end:
                segments.append(segment)
            else:
                # check number of collisions thats occure when this rect placed on sky segment
                collision = 0
                for line in sky[sky.index(segment):]:
                    if rect.w + segment.start > line.start and segment.y < line.y:
                        collision += 1
                if collision == 0:
                    segments.append(segment)

def packing(rectangles): 
    packed = 0
    bin_id = 0
    while packed < len(rectangles):
        sky = [Segment(0,bin_width,0)] # this list of all segemtns
        for rect in rectangles:
            if rect.wasPacked == False: 
                valid_segments = []
                findSegments(sky=sky, segments=valid_segments, rect=rect)
                if len(valid_segments) > 0:
                    rand = random.randint(0,len(valid_segments) - 1)
                    # segment = valid_segments[rand]          
                    segment = valid_segments[0]
                    if segment.end - segment.start < rect.w: # merge section
                        index = sky.index(segment)
                        segment_1 = Segment(segment.start, segment.start + rect.w, rect.h + segment.y)
                        sky.insert(index, segment_1)
                        rect.x = segment_1.start
                        rect.y = segment.y
                        rect.wasPacked = True
                        rect.bin_id = bin_id
                        packed += 1
                        
                        for line in sky[index+1:]:
                            if line.end <= segment_1.end and line.y < segment_1.y:
                                sky.remove(line)
                            elif line.start < segment_1.end and line.end > segment_1.end:
                                index_line = sky.index(line)
                                segment_2 = Segment(segment_1.end, line.end, line.y)
                                sky.insert(index_line, segment_2)
                                sky.remove(line)
                                
                    else: # insert section
                        segment_1 = Segment(segment.start, segment.start+rect.w, segment.y+rect.h)
                        segment_2 = Segment(segment.start+rect.w, segment.end, segment.y)
                        index = sky.index(segment)
                        sky.remove(segment)
                        sky.insert(index,segment_1)
                        sky.insert(index+1,segment_2)
                        rect.x = segment_1.start
                        rect.y = segment.y
                        rect.wasPacked = True
                        rect.bin_id = bin_id
                        packed += 1
        bin_id += 1
    rectangles.sort(key=lambda x: x.id)
    binary_matrix = []
    for rect in rectangles:
        result_list = [0] * bin_id
        result_list[rect.bin_id] = 1
        binary_matrix.append(result_list)
    
    return [binary_matrix, bin_id]
 
def gen_random(i):
    while True:
        rand = random.randint(0,flock_size-1)
        if rand != i:
            return rand

def subtrackt_nested_list(list1, list2):
    result = []
    for sublist1, sublist2 in zip(list1, list2):
        result_sublist = [a - b for a, b in zip(sublist1, sublist2)]
        result.append(result_sublist)
    return result

def multiply_nested_list(nested_list, k):
    result = []
    for sublist in nested_list:
        result_sublist = [element * k for element in sublist]
        result.append(result_sublist)
    return result

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_nested_list(nested_list):
    result = []
    for sublist in nested_list:
        result_sublist = [sigmoid(element) for element in sublist]
        result.append(result_sublist)
    return result

def discretize_sigmoid(nested_list):
    num_columns = len(nested_list[0])
    for row in nested_list:
        selected_index = row.index(max(row))
        row[:] = [1 if i == selected_index else 0 for i in range(num_columns)]

def packing_column_items(bin_id, rectangles):
    unpacked = []
    sky = [Segment(0,bin_width,0)] # this list of all segemtns
    for rect in rectangles:
        valid_segments = []
        findSegments(sky=sky, segments=valid_segments, rect=rect)
        if len(valid_segments) > 0:
            rand = random.randint(0,len(valid_segments) - 1)
            segment = valid_segments[rand]
            if segment.end - segment.start < rect.w: # merge section
                index = sky.index(segment)
                segment_1 = Segment(segment.start, segment.start + rect.w, rect.h + segment.y)
                sky.insert(index, segment_1)
                rect.x = segment_1.start
                rect.y = segment.y
                rect.wasPacked = True
                rect.bin_id = bin_id
                
                for line in sky[index+1:]:
                    if line.end <= segment_1.end and line.y < segment_1.y:
                        sky.remove(line)
                    elif line.start < segment_1.end and line.end > segment_1.end:
                        index_line = sky.index(line)
                        segment_2 = Segment(segment_1.end, line.end, line.y)
                        sky.insert(index_line, segment_2)
                        sky.remove(line)
                        
            else: # insert section
                segment_1 = Segment(segment.start, segment.start+rect.w, segment.y+rect.h)
                segment_2 = Segment(segment.start+rect.w, segment.end, segment.y)
                index = sky.index(segment)
                sky.remove(segment)
                sky.insert(index,segment_1)
                sky.insert(index+1,segment_2)
                rect.x = segment_1.start
                rect.y = segment.y
                rect.wasPacked = True
                rect.bin_id = bin_id

        if rect.wasPacked == False:
            unpacked.append(rect)
    return unpacked

def repair(sigmoid, items):
    length = len(sigmoid[0]) # number of bins
    unpacked_in_sigmoid = 0
    for i,row in enumerate(sigmoid):
        if 1 in row:
            items[i].bin_id = row.index(1)
        else:
            unpacked_in_sigmoid += 1
    unpacked = []
    if unpacked_in_sigmoid == len(items):
        sigmoid,bins = packing(items)
    else:
        # if all items have a bin_id thats mean to item at least exist in one bin, else item is not on to a bin
        for column in range(length):
            rects  = unpacked
            for rect in items:
                if rect.bin_id == column or rect.bin_id == -1:
                    rects.append(rect)
            rects.sort(key=lambda x: x.w, reverse=True)
            unpacked = packing_column_items(column, rectangles=rects)
            

        for i, rect in enumerate(items):
            if rect.wasPacked:
                selected_index = rect.bin_id
                sigmoid[i][:]= [1 if i == selected_index else 0 for i in range(length)]
        
        
        
        for rect in unpacked:
            sigmoid[rect.id][:] = [0 for i in range(length)]
    
    return [unpacked, sigmoid]

def visualize(item_copy, bins):
    # Draw image 
    margin = 6
    gap = 0
    row = 0
    t = 0
    offset_x  = margin
    offset_y = margin
    col = 1000 // bin_width
    img = Image.new(mode="RGB", size=((col+2) * bin_width, ((bins//col)+1) * bin_height), color="white")
    img1 = ImageDraw.Draw(img)
    for bin in range(bins):
        offset_x = t * (bin_width + margin) + margin
        offset_y = row * (bin_height + margin) + margin
        t += 1
        if t > col:
            row += 1 
            t = 0 
        empty = True
        for item in item_copy:
            if item.wasPacked and item.bin_id == bin:
                empty = False
                x1 = offset_x+item.x+gap
                x2 = offset_x+item.x+item.w
                y1 = offset_y+item.y+gap
                y2 = offset_y+item.y+item.h
                if x1 > x2:
                    x2 = x1 + 2
                if y1 > y2:
                    y2 = y1 + 2
                shape = [(x1,y1),(x2,y2)]
                color = random.randrange(0, 2**24)
                hex_color = hex(color)
                while len(hex_color) < 8:
                    hex_color += '0'
                
                std_color = "#" + hex_color[2:]
                img1.rectangle(shape, outline="black", fill=std_color)
                img1.text(text=str(item.id), xy=(x1+5,y1+5), outline="black", fill='white')
        if empty == False:
            shape = [(offset_x,offset_y),(offset_x+bin_width+gap,offset_y+bin_height+gap)]
            img1.rectangle(shape, outline="black")
            
    img.show()

def fitness(items,bins):
    avg_area = 0
    bin = 0
    for i in range(bins):
        fill_u = 0
        for rect in items:
            if rect.bin_id == i:
                fill_u += rect.h * rect.w
        
        if fill_u != 0: bin += 1
        avg_area += (fill_u/(bin_width*bin_height))**4
    return [avg_area / bin,bin]

def print_time(a, msg):
    b = datetime.datetime.now()
    print(msg,b-a)
    
def scaling(matrix, max_col):
    length = len(matrix[0])
    if length < max_col:
        for row in matrix:
            row.extend([0] * (max_col - length))
    else:
        return False
    return True

# algorithm
def pso_csa():
    max_length = 0
    bins = 0
    best_global_items = []
    best_global_binary = []
    best_global_value = 0
    best_global_bins = 0
    crow_list = []
    a = datetime.datetime.now()
    for i in range(flock_size):
        item_copy = read_items()
        random.shuffle(item_copy)
        binary_matrix,length = packing(item_copy)
        if length > max_length:
            max_length = length
        crow = Crow(binary_matrix)
        crow_list.append(crow)
        fitness_value,bins = fitness(item_copy,length)
        # init best global
        if fitness_value > best_global_value:
            best_global_binary = binary_matrix
            best_global_value = fitness_value
            best_global_items = item_copy
            best_global_bins = bins
    
    # It often increases in size after fixing infeasible matrices. It is appropriate to add this amount to keep these answers.
    max_length+=50
    # Scaling matrix ; set equal size to solutions
    for crow in crow_list:
        scaling(crow.position, max_length)
    
    scaling(best_global_binary, max_length)

    print(f'Global_value:{best_global_value}, Global_Bins: {best_global_bins}')
    print_time(a, 'construct time')

    improvement = 0
    sum = 0
    valid  = 0
    ittr = 0

    a = datetime.datetime.now()
    st = time.time()

    while time.time() - st < 60:
    # for iteration in range(maximum_iteration):
        # print_time(a,f'iteration {ittr}')
        for i, crow in enumerate(crow_list):
            crow_j = crow_list[gen_random(i)]
            valid_solution = False
            item_copy = read_items()
            if random.uniform(0,1) >= crow_j.awareness:
                # print("Crow")
                sum += 1
                # Follow crow j by crow i , exploitation , Repair need
                subtrackt = subtrackt_nested_list(crow_j.best_position, crow.position)
                g = multiply_nested_list(subtrackt,flight_size*random.uniform(0,1))
                sigmoid = sigmoid_nested_list(g)
                discretize_sigmoid(sigmoid)
                unpacked, binary_matrix = repair(sigmoid, item_copy)
                if len(unpacked) > 0:
                    valid_solution = False
                else:
                    valid+=1
                    length = len(binary_matrix[0])
                    if length < max_length:
                        valid_solution = True
                        for row in crow.position:
                            row.extend([0] * (max_length - length))
                    elif length == max_length: valid_solution = True

            else:
                # print("Random")
                # Random feasible solution , exploration
                random.shuffle(item_copy)
                binary_matrix,bin_id = packing(item_copy)
                length = bin_id
                if length < max_length:
                    valid_solution = True
                    for row in crow.position:
                        row.extend([0] * (max_length - length))
                elif length == max_length: valid_solution = True

            if valid_solution:
                fitness_value,bins = fitness(item_copy,max_length)
                if fitness_value > crow.best_value:
                    crow.best_position = binary_matrix
                    crow.best_items = item_copy
                    crow.best_value = fitness_value
                    crow.position = binary_matrix
                
                crow.position = binary_matrix

                if fitness_value > best_global_value:
                    improvement += 1 
                    best_global_value = fitness_value
                    best_global_items = item_copy
                    best_global_binary = binary_matrix
                    best_global_bins = bins
                    print(f'Fitness_value crow {i} : {fitness_value}')
                    print(f'Best_global_value: {best_global_value} , Bin: {bins}')
        ittr += 1
    
    print(f'Rate : {valid/sum}')
    b = datetime.datetime.now()
    print(f'Time: {b-a} , Improvement: {improvement}')
    print(f'Global_value:{best_global_value}, Global_Bins: {best_global_bins}')
    visualize(best_global_items,best_global_bins)
    

# initialize section
base_lines = []
# filename = 'random_generated.txt'
# filename = '5- random_generated_02.txt'
# filename = '4- random_generated_01.txt'
filename = '3- cl_10_100_01.ins2D'
# filename = 'cl_10_100_04.ins2D'
# filename = 'cl_01_040_04.ins2D'
# filename = 'cl_01_060_05.ins2D'

with open(filename) as file:
    base_lines = [line.rstrip() for line in file]

n = int(base_lines[0])

bin_width = int(base_lines[1].split(' ')[0])
bin_height = int(base_lines[1].split(' ')[1])

if __name__ == '__main__':
    pso_csa()
