# Credits:
# Piotr Gralczyk: https://github.com/PGralczyk
# Maciej Włodarczyk: https://github.com/maciejwlodarczyk15

import numpy as np
import time
import math
import xlsxwriter # Saving many results to file
import os # Reading files from folder
# import sys # Running program from CMD

# Default launch options
algo = "bfs"
order = "LURD"
read_file = "puzzle.txt"
save_file = "solution.txt"
info_file = "info.txt"

# Launch options (CMD)
# algo = sys.argv[1]
# order = sys.argv[2]
# read_file = sys.argv[3]
# save_file = sys.argv[4]
# info_file = sys.argv[5]
# /Launch options (CMD)

# Maximum depth of recursion
depth = 20
reached_depth = 0

# Boards
final_board = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
problem_board = np.loadtxt(read_file, skiprows=1, dtype=int)

# Searched array
searched = []
visited = 0

# Find where are the blank space coordinates
where0 = np.where(problem_board == 0)
currentX = where0[0]
currentY = where0[1]

# Length of path
path_length = 0

# Final path
final_path = ""

# Time of algorithm working
time_spent = 0

# BFS utilities
queue = []
pathQueue = []
safeValve = 0
truePath = 'X'

# Hamming utilities
aqueue = np.array([9999, problem_board, "X"], dtype=object)
apath = ""

# Global search stopper
proceed = True

# Path string
path = "X"


def unique(array):
    global searched
    for i in range(len(searched)):
        if np.array_equal(array, searched[i]):
            return False
    return True


def string_hash(arrayone):
    stringr = ""
    for i in range(4):
        for j in range(4):
            stringr += chr(100 + arrayone[i, j])
    return stringr


final_string = string_hash(final_board)


def hammdist(arrayone, arraytwo):
    sum_r = 0
    for i in range(4):
        for j in range(4):
            if arrayone[i, j] != arraytwo[i, j]:
             sum_r += 1
    return sum_r


def mandist(arrayone):
    sum_r = 0
    for i in range(4):
        for j in range(4):
            if arrayone[i, j] != 0:
                sum_r = sum_r + abs(i - math.floor(arrayone[i, j] / 4)) + abs(j - ((arrayone[i, j]-1) % 4))
    return sum_r


# Function to swap blank space with another in table
def swapper(x1, y1, x2, y2):  # Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
    temporary = problem_board[x1, y1]
    problem_board[x1, y1] = problem_board[x2, y2]
    problem_board[x2, y2] = temporary
    global currentX
    global currentY
    currentX = x2
    currentY = y2


# Deep first search
def dfs(array, origin, brake):
    whereise0 = np.where(array == 0)
    currentex = whereise0[0]
    currentey = whereise0[1]
    global proceed
    global path
    global order
    global searched
    global visited
    global reached_depth

    if len(path) > reached_depth:
        reached_depth = len(path)
    # Check if current board is not a solution yet
    if string_hash(array) == final_string:
        visited += 1
        proceed = False
        return
    # If it's not the solution
    elif proceed:
        # When we go beyond depth
        if brake >= depth:
            return
        # Go through board with correct order
        visited += 1
        for i in range(4):
            if order[i] == "R":
                if proceed and origin != 'L' and currentey + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper(currentX, currentY, currentX, currentY + 1)
                    path = path + "R"
                    dfs(array, 'R', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX, currentY - 1)
            elif order[i] == "L":
                if proceed and origin != 'R' and currentey - 1 >= 0:
                    swapper(currentX, currentY, currentX, currentY - 1)
                    path = path + "L"
                    dfs(array, 'L', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX, currentY + 1)
            elif order[i] == "D":
                if proceed and origin != 'U' and currentex + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper(currentX, currentY, currentX + 1, currentY)
                    path = path + "D"
                    dfs(array, 'D', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX - 1, currentY)
            elif order[i] == "U":
                if proceed and origin != 'D' and currentex - 1 >= 0:
                    swapper(currentX, currentY, currentX - 1, currentY)
                    path = path + "U"
                    dfs(array, 'U', brake + 1)
                    if proceed:
                        path = path[:-1]
                    swapper(currentX, currentY, currentX + 1, currentY)


# Function to swap blank space with another in table
def swapper2_0(x, y, array):  # Y IS FOR HORIZONTAL, X IS FOR DIAGONAL
    whereis0 = np.where(array == 0)
    currentx = whereis0[0]
    currenty = whereis0[1]
    temporary = array[currentx, currenty]
    array[currentx, currenty] = array[currentx + x, currenty + y]
    array[currentx + x, currenty + y] = temporary


# Breadth first search
def bfs(array, origin):
    whereise0 = np.where(array == 0)
    currentex = whereise0[0]
    currentey = whereise0[1]
    global proceed
    global queue
    global truePath
    global visited
    global searched
    if unique(array):
        searched.append(np.array(array))
    else:
        visited += 1
    if np.array_equal(array, final_board):
        queue.pop(0)
        truePath = pathQueue.pop(0)
        proceed = False
        return
    elif proceed:
        queue.pop(0)
        pathQueue.pop(0)
        for i in range(4):
            if order[i] == "R":
                if origin[-1] != 'L' and currentey + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper2_0(0, 1, array)
                    queue.append(np.array(array))
                    originr = origin + "R"
                    pathQueue.append(originr)
                    swapper2_0(0, -1, array)
            elif order[i] == "L":
                if proceed and origin[-1] != 'R' and currentey - 1 >= 0:
                    swapper2_0(0, -1, array)
                    queue.append(np.array(array))
                    originl = origin + "L"
                    pathQueue.append(originl)
                    swapper2_0(0, 1, array)
            elif order[i] == "D":
                if proceed and origin[-1] != 'U' and currentex + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                    swapper2_0(1, 0, array)
                    queue.append(np.array(array))
                    origind = origin + "D"
                    pathQueue.append(origind)
                    swapper2_0(-1, 0, array)
            elif order[i] == "U":
                if proceed and origin[-1] != 'D' and currentex - 1 >= 0:
                    swapper2_0(-1, 0, array)
                    queue.append(np.array(array))
                    originu = origin + "U"
                    pathQueue.append(originu)
                    swapper2_0(1, 0, array)
        bfs(queue[0], pathQueue[0])


def hamming(array, origin):
    whereise0 = np.where(array == 0)
    currentex = whereise0[0]
    currentey = whereise0[1]
    global proceed
    global aqueue
    global final_board
    global safeValve
    global apath
    global searched
    global visited
    global reached_depth

    if unique(array):
        searched.append(np.array(array))
        if np.array_equal(array, final_board):
            apath = aqueue[0, 2]
            aqueue = np.delete(aqueue, 0, axis=0)
            proceed = False
            return
        elif proceed:
            if origin[-1] != 'L' and currentey + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                swapper2_0(0, 1, array)
                originr = origin + "R"
                aqueue = np.vstack([aqueue, np.array([hammdist(array, final_board) + len(originr), np.array(array), originr], dtype=object)])
                swapper2_0(0, -1, array)

            if proceed and origin[-1] != 'R' and currentey - 1 >= 0:
                swapper2_0(0, -1, array)
                originl = origin + "L"
                aqueue = np.vstack([aqueue, np.array([hammdist(array, final_board) + len(originl), np.array(array), originl], dtype=object)])
                swapper2_0(0, 1, array)

            if proceed and origin[-1] != 'U' and currentex + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                swapper2_0(1, 0, array)
                origind = origin + "D"
                aqueue = np.vstack([aqueue, np.array([hammdist(array, final_board) + len(origind), np.array(array), origind], dtype=object)])
                swapper2_0(-1, 0, array)

            if proceed and origin[-1] != 'D' and currentex - 1 >= 0:
                swapper2_0(-1, 0, array)
                originu = origin + "U"
                aqueue = np.vstack([aqueue, np.array([hammdist(array, final_board) + len(originu), np.array(array), originu], dtype=object)])
                swapper2_0(1, 0, array)
    else:
        visited += 1
    aqueue = np.delete(aqueue, 0, axis=0)
    aqueue = aqueue[aqueue[:, 0].argsort()]
    if len(aqueue[0, 2]) > reached_depth:
        reached_depth = len(aqueue[0, 2])
    hamming(aqueue[0, 1], aqueue[0, 2])


def manhattan(array, origin):
    whereise0 = np.where(array == 0)
    currentex = whereise0[0]
    currentey = whereise0[1]
    global proceed
    global aqueue
    global final_board
    global safeValve
    global apath
    global searched
    global visited
    global reached_depth

    if unique(array):
        searched.append(np.array(array))
        if np.array_equal(array, final_board):
            apath = aqueue[0, 2]
            aqueue = np.delete(aqueue, 0, axis=0)
            proceed = False
            return
        elif proceed:
            if origin[-1] != 'L' and currentey + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                swapper2_0(0, 1, array)
                originr = origin + "R"
                aqueue = np.vstack([aqueue, np.array([mandist(array) + len(originr), np.array(array), originr], dtype=object)])
                swapper2_0(0, -1, array)

            if proceed and origin[-1] != 'R' and currentey - 1 >= 0:
                swapper2_0(0, -1, array)
                originl = origin + "L"
                aqueue = np.vstack([aqueue, np.array([mandist(array) + len(originl), np.array(array), originl], dtype=object)])
                swapper2_0(0, 1, array)

            if proceed and origin[-1] != 'U' and currentex + 1 <= 3:  # ADD SPECIFIC VALUE READ FROM FILE!!!
                swapper2_0(1, 0, array)
                origind = origin + "D"
                aqueue = np.vstack([aqueue, np.array([mandist(array) + len(origind), np.array(array), origind], dtype=object)])
                swapper2_0(-1, 0, array)

            if proceed and origin[-1] != 'D' and currentex - 1 >= 0:
                swapper2_0(-1, 0, array)
                originu = origin + "U"
                aqueue = np.vstack([aqueue, np.array([mandist(array) + len(originu), np.array(array), originu], dtype=object)])
                swapper2_0(1, 0, array)
    else:
        visited += 1

    aqueue = np.delete(aqueue, 0, axis=0)
    aqueue = aqueue[aqueue[:, 0].argsort()]
    if len(aqueue[0, 2]) > reached_depth:
        reached_depth = len(aqueue[0, 2])
    manhattan(aqueue[0, 1], aqueue[0, 2])


# Main function
if __name__ == '__main__':
    print("Final board:")
    print(final_board)

    print("\nCurrent board:")
    print(problem_board)

    print("\nCurrent position of blank space(X/Y):")
    print(currentX)
    print(currentY)

    # Options (PyCharm)
    algo = input("Choose algorithm: ")
    # /Options (PyCharm)

    # queue.append(problem_board)
    # pathQueue.append("X")
    # print("\nAlgorithm start:")
    #
    # # After the algorithm has been chosen
    # if algo == "bfs":
    #     start_time = time.time()
    #     bfs(problem_board, truePath)
    #     time_spent = round(((time.time() - start_time) * 1000), 3)
    #     final_path = truePath[1:]
    #     reached_depth = len(final_path)
    #     queue.clear()
    #     pathQueue.clear()
    # elif algo == "dfs":
    #     start_time = time.time()
    #     dfs(problem_board, 'N', 0)
    #     time_spent = round(((time.time() - start_time) * 1000), 3)
    #     final_path = path[1:]
    # elif algo == "hamm" or order == "hamm":
    #     start_time = time.time()
    #     hamming(problem_board, "X")
    #     time_spent = round(((time.time() - start_time) * 1000), 3)
    #     final_path = apath[1:]
    #     reached_depth -= 1
    # elif algo == "manh" or order == "manh":
    #     start_time = time.time()
    #     manhattan(problem_board, "X")
    #     time_spent = round(((time.time() - start_time) * 1000), 3)
    #     final_path = apath[1:]
    #     reached_depth -= 1
    # else:
    #     print("!!!Error: Non-existing algorithm was chosen!!!")
    #
    # # Calculate path length
    # path_length = len(final_path)
    #
    # # Information about operation
    # print("\n\nAlgorithm: ", algo)
    # print("Order: ", order)
    # print("Board file: ", read_file)
    #
    # print("\nLength of solution: ", path_length)
    # print("Solution: ", final_path)
    # print("Maximum depth: ", reached_depth)
    # if algo == "dfs":
    #     print("Amount processed: ", visited)
    # else:
    #     print("Amount processed: ", len(searched))
    #
    # print("Amount visited: ", len(searched) + visited)
    #
    # print("\nAlgorithm took: %s milliseconds" % time_spent)
    #
    # # FILES
    # # Save solution to file
    # o_file = open(save_file, "w")
    # o_file.write(str(path_length) + "\n")
    # o_file.write(final_path)
    #
    # # Close the file
    # o_file.close()
    #
    # # Save additional info to file
    # o_file = open(info_file, "w")
    # o_file.write(str(path_length) + "\n")
    # o_file.write(str(len(searched) + visited) + "\n")
    # if algo == "dfs":
    #     o_file.write(str(visited) + "\n")
    # else:
    #     o_file.write(str(len(searched)) + "\n")
    # o_file.write(str(reached_depth) + "\n")
    # o_file.write(str(time_spent))
    # o_file.close()

    # Excel

    # Initializing Excel
    workbook = xlsxwriter.Workbook("Results.xlsx")
    worksheet = workbook.add_worksheet('Results')

    worksheet.write('A1', 'Name')
    worksheet.write('B1', 'Type')
    worksheet.write('C1', 'Length')
    worksheet.write('D1', 'Visited')
    worksheet.write('E1', 'Searched')
    worksheet.write('F1', 'Depth')
    worksheet.write('G1', 'Time')

    index = 2
    yourpath = '7'
    # iterator = 0
    for root, dirs, files in os.walk(yourpath, topdown=False):
        for name in files:
            # print(os.path.join(name))
            # Function
            problem_board = np.loadtxt("7/"+os.path.join(name), skiprows=1, dtype=int)
            # print(problem_board)

            where0 = np.where(problem_board == 0)
            currentX = where0[0]
            currentY = where0[1]
            path = "X"

            truePath = "X"
            proceed = True
            queue.append(problem_board)
            pathQueue.append("X")
            searched = []
            visited = 0
            reached_depth = 0
            apath = ""
            aqueue = np.array([9999, problem_board, "X"], dtype=object)
            if algo == "bfs":
                start_time = time.time()
                bfs(problem_board, truePath)
                time_spent = round(((time.time() - start_time) * 1000), 3)
                final_path = truePath[1:]
                reached_depth = len(final_path)
                queue.clear()
                pathQueue.clear()
            elif algo == "dfs":
                start_time = time.time()
                dfs(problem_board, 'N', 0)
                time_spent = round(((time.time() - start_time) * 1000), 3)
                final_path = path[1:]
                #reached_depth = visited
            elif algo == "hamm":
                start_time = time.time()
                hamming(problem_board, "X")
                time_spent = round(((time.time() - start_time) * 1000), 3)
                final_path = apath[1:]
                reached_depth -= 1
            elif algo == "manh":
                start_time = time.time()
                manhattan(problem_board, "X")
                time_spent = round(((time.time() - start_time) * 1000), 3)
                final_path = apath[1:]
                reached_depth -= 1
            else:
                print("!!!Error: Non-existing algorithm was chosen!!!")

            # Calculate path length
            path_length = len(final_path)

            # Information about operation
            print("\n\nAlgorithm: ", algo)
            print("Order: ", order)
            print("Board file: ", os.path.join(name))

            print("\nLength of solution: ", path_length)
            print("Solution: ", final_path)
            print("Maximum depth: ", reached_depth)
            if algo == "dfs":
                print("Amount processed: ", visited)
            else:
                print("Amount processed: ", len(searched))

            print("Amount visited: ", len(searched) + visited)

            print("\nAlgorithm took: %s milliseconds" % time_spent)

            worksheet.write('A' + str(index), os.path.join(name))
            worksheet.write('B' + str(index), order)
            worksheet.write('C' + str(index), path_length)
            worksheet.write('D' + str(index), len(searched) + visited)
            if algo == "dfs":
                worksheet.write('E' + str(index), visited)
            else:
                worksheet.write('E' + str(index), len(searched))
            worksheet.write('F' + str(index), reached_depth)
            worksheet.write('G' + str(index), time_spent)

            index = index + 1

            # End of function

    workbook.close()

    # /Excel
