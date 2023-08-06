import cv2
import cv2.aruco as aruco

def findAruco(img, marker_size=6, total_markers=250):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    key = getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()

    bbox, ids, _ = aruco.detectMarkers(gray, arucoDict, parameters=arucoParam)

    aruco.drawDetectedMarkers(img, bbox)

    return bbox, ids


def getDrawCoords(array):
    curr_coord = array[0]
    curr_max = array[0][0] + array[0][1]

    for i in range(len(array)):
        curr_sum = array[i][0] + array[i][1]
        if curr_sum < curr_max:
            curr_max = curr_sum
            curr_coord = array[i]

    curr_coord_tup = (int(curr_coord[0]), int(curr_coord[1])-10)

    return curr_coord_tup

file_name = input("Enter file name (The file should be in the same directory as the code): ")
marker_size = int(input("Enter marker size (4, 5, 6, 7): "))
total_markers = int(input("Enter total number of markers (50, 100, 250, 1000): "))

while True:

    image = cv2.imread(file_name)
    height = image.shape[0]

    image = cv2.resize(image, (0,0), fx=(500/height), fy=(500/height))

    bbox, ids = findAruco(image, marker_size, total_markers)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1

    for i in range(len(bbox)):

        coord = getDrawCoords((bbox[i][0]).tolist())

        image = cv2.putText(image, f"ID = {(ids[i][0])}", coord, font, fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("aruco", image)

    if cv2.waitKey(1) == 113:
        break
