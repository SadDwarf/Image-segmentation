from scipy import misc
 
IMAGE = 'plane.jpg'
 
T = [90, 97, 103]     #[79, 123, 196] - plane   [0, 255, 0] - ball
S = [85, 129, 204]    #[101, 106, 112] - plane  [255, 0, 0] - ball
 
def dist(x, y):
    return sum((x - y) ** 2)
 
def get_neighbours(i, j, max_i, max_j):
    result = []
    if i > 0:
        result.append((i - 1, j))
    if j > 0:
        result.append((i, j - 1))
    if (i + 1) < max_i:
        result.append((i + 1, j))
    if (j + 1) < max_j:
        result.append((i, j  + 1))
 
    return result
 
def flip(i, j, A, B):
    if (i, j) in A:
        A.remove((i, j))
        B.add((i, j))
    else:
        B.remove((i, j))
        A.add((i, j))

def check(image, i, j, A, B):
    sumA = 0
    dim_x, dim_y, colors = image.shape
    sumB = 0
    for elem in get_neighbours(i, j, dim_x, dim_y):
        flipped = False
        if elem in A:
            sumA += dist(image[i, j][:3], image[elem[0], elem[1]][:3])
        if elem in B:
            sumB += dist(image[i, j][:3], image[elem[0], elem[1]][:3])
        sumA += dist(image[i, j][:3], S)
        sumB += dist(image[i, j][:3], T)
        
        if (((i, j) in A) and (sumA < sumB)) or \
           (((i, j) in B) and (sumA > sumB)):
            flip(i, j, A, B)
            flipped = True
    if (flipped and i > 0):
        check(image, i - 1, j, A, B)
    elif (flipped and j > 0):
        check(image, i, j - 1, A, B)

def cut(image):
    dim_x, dim_y, colors = image.shape
    A = set()
    B = {(i, j) for i in range(dim_x) for j in range(dim_y)}
    for i in range(dim_x):
        for j in range(dim_y):
            check(image, i, j, A, B)
    return A, B
 
 
def main():
    image = misc.imread(IMAGE)
    dim_x, dim_y, colors = image.shape
    print("Loaded image of shape {x}, {y}".format(x=dim_x, y=dim_y))
 
    A, B = cut(image)
 
    for i in range(dim_x):
        for j in range(dim_y):
            if (i, j) in A:
                image[i, j, 0] = min(255, image[i, j, 0] + 100)
                image[i, j, 1] = image[i, j, 1] / 3
                image[i, j, 2] = image[i, j, 2] / 3
            elif (i,j) in B:
                image[i, j, 0] = image[i, j, 0] / 3
                image[i, j, 1] = min(255, image[i, j, 1] + 100)
                image[i, j, 2] = image[i, j, 2] / 3
 
    misc.imsave('out.png', image)
    print("Done")
 
if __name__ == '__main__':
    main()
