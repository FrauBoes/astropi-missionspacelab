from datetime import datetime
from exif import Image
import cv2
import math

# Resolution of HQ camera is 4056 x 3040
GSD_HQ_Camera = 12648
# Resolution of replay tool camera is 1412 × 1412
GSD_Replay_Tool_Camera = 46633

def get_time(image):
    """
    Returns the datetime of the given image.
    """
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get('datetime_original')
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    return time

def get_time_difference(image_1, image_2):
    """
    Returns the time difference in seconds of when the two images passed where
    taken.
    """
    time_1 = get_time(image_1)
    time_2 = get_time(image_2)
    time_difference = time_2 - time_1
    return time_difference.seconds

def convert_to_cv(image_1, image_2):
    """
    Returns the two passed images as OpenCV objects.
    """
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv

def calculate_features(image_1_cv, image_2_cv, feature_number):
    """
    Returns the keypoints and descriptors of the two passed images.
    """
    orb = cv2.ORB.create(nfeatures=feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):
    """
    Returns a list of matches of the two descriptors passed.
    """
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    """
    Returns two lists of coordinates that are describe the matches between 
    the two keypoints passed.
    """
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1, y1))
        coordinates_2.append((x2, y2))
    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    """
    Returns the mean distance of the two coordinates passed.
    """
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)

def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
    """
    Returns the speed in kmps based on the parameters passed.
    """
    distance = feature_distance * GSD / 100000
    speed = distance / time_difference
    return speed

def get_speed_estimate(image_1, image_2):
    """
    Returns a speed estimate based on the two images passed.
    """
    time_difference = get_time_difference(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
    matches = calculate_matches(descriptors_1, descriptors_2)
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    return calculate_speed_in_kmps(average_feature_distance, GSD_Replay_Tool_Camera, time_difference) 
