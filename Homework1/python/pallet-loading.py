import sys


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Dimension:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.area = x * y
        self.id = id


class Pallet:
    def __init__(self,  dimension, position):
        self.dimension = dimension
        self.position = position
        self.start_x = position.x
        self.end_x = position.x + dimension.x
        self.start_y = position.y
        self.end_y = position.y + dimension.y


def sort_area(dimension):
    return dimension.area


def read_input():
    store_parameters = input()
    sliced_parameters = store_parameters.split('\t')
    store_dimensions = Dimension(int(sliced_parameters[1]), int(sliced_parameters[0]), 0)
    pillar_count = int(input().split()[0])
    pallet_count = int(input().split()[0])
    pillar_array = []
    for _ in range(store_dimensions.x):
        row = []
        for _ in range(store_dimensions.y):
            row.append(0)
        pillar_array.append(row)
    for i in range(pillar_count):
        input_array = input().split('\t')
        pillar_array[int(input_array[0])][int(input_array[1])] = 1
    pallet_dimensions = []
    for i in range(pallet_count):
        input_array = input().split('\t')
        pallet_dimensions.append(Dimension(
            int(input_array[1]), int(input_array[0]), i+1))
    pallet_dimensions.sort(key=sort_area, reverse=True)
    output_array = []
    for _ in range(store_dimensions.x):
        row = []
        for _ in range(store_dimensions.y):
            row.append(0)
        output_array.append(row)
    return store_dimensions, pillar_array, pallet_dimensions, output_array


def check_borders(pallet, store_dimensions):
    if(pallet.position.x+pallet.dimension.x > store_dimensions.x) or (pallet.position.y+pallet.dimension.y > store_dimensions.y):
        return False
    return True


def check_pillars(pallet, pillar_positions):
    for x in range(pallet.start_x + 1, pallet.end_x):
        for y in range(pallet.start_y + 1, pallet.end_y):
            if(pillar_positions[x][y] != 0):
                return False
    return True


def check_pallets(pallet, output_array):
    for x in range(pallet.start_x, pallet.end_x):
        for y in range(pallet.start_y, pallet.end_y):
            if(output_array[x][y] != 0):
                return False
    return True

def check_everything(pallet, store_dimensions, pillar_positions, output_array):
    if(check_borders(pallet, store_dimensions) and check_pillars(pallet, pillar_positions) and check_pallets(pallet, output_array)):
        return True
    return False

def add_to_output_array(pallet, output_array):
    for x in range(pallet.start_x, pallet.end_x):
        for y in range(pallet.start_y, pallet.end_y):
            output_array[x][y] = pallet.dimension.id
    return output_array


def remove_from_output_array(pallet, output_array):
    for x in range(pallet.start_x, pallet.end_x):
        for y in range(pallet.start_y, pallet.end_y):
            output_array[x][y] = 0
    return output_array


def place(pallet_dimensions, pillar_positions, output_array, store_dimensions, recursion_depth):
    for x in range(store_dimensions.x):
        for y in range(store_dimensions.y):
            if(output_array[x][y] == 0):
                pallet_position = Position(x, y)
                pallet = Pallet(pallet_dimensions[recursion_depth], pallet_position)
                if(check_everything(pallet, store_dimensions, pillar_positions, output_array)):
                    output_array = add_to_output_array(pallet, output_array)
                    if(recursion_depth == len(pallet_dimensions) - 1):
                        output_array = add_to_output_array(pallet, output_array)
                        return True
                    if(place(pallet_dimensions, pillar_positions, output_array, store_dimensions, recursion_depth + 1)):
                        return True
                    output_array = remove_from_output_array(pallet, output_array)
                rotated_pallet = Pallet(
                    Dimension(pallet.dimension.y, pallet.dimension.x, pallet.dimension.id), pallet_position)
                if(check_everything(rotated_pallet, store_dimensions, pillar_positions, output_array)):
                    output_array = add_to_output_array(rotated_pallet, output_array)
                    if(recursion_depth == len(pallet_dimensions) - 1):
                        output_array = add_to_output_array(rotated_pallet, output_array)
                        return True
                    if(place(pallet_dimensions, pillar_positions, output_array, store_dimensions, recursion_depth + 1)):
                        return True
                    output_array = remove_from_output_array(rotated_pallet, output_array)
    return False


def print_output_array(output_array):
    for row in output_array:
        string = ""
        index = 0
        for z in row:
            string += str(z)
            if(len(row)-1 != index):
                string += "\t"
            index += 1
        print(string)


def main():
    if(len(sys.argv) > 1 and sys.argv[1] == 'FILE'):
        fd = open('input.txt', 'r')
        sys.stdin = fd

    store_dimensions, pillars_array, pallet_dimensions, output_array = read_input()

    if(len(pallet_dimensions) > 0):
        place(pallet_dimensions, pillars_array, output_array, store_dimensions, 0)

    print_output_array(output_array)


main()
