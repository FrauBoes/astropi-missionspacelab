from iss_speed import *
from take_photos import *
import os

# Estimate kmph based on historical images
# image_1 = 'resources/astropi-iss-speed-en-resources/photo_07464.jpg'
# image_2 = 'resources/astropi-iss-speed-en-resources/photo_07465.jpg'

project_dir = os.getcwd()
photo_dir = project_dir + "/data/photos/"

if not os.path.exists(photo_dir):
    os.makedirs(photo_dir)

take_photo_sequence(photo_dir)

image_1 = photo_dir + "image-1.jpg"
image_2 = photo_dir + "image-2.jpg"

time_difference = get_time_difference(image_1, image_2)
image_1_cv, image_2_cv = convert_to_cv(image_1, image_2)
keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000)
matches = calculate_matches(descriptors_1, descriptors_2)
coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
estimate_kmps = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference) 

# Format the estimate_kmps to have a precision
# of 5 significant figures
estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

# Create a string to write to the file
output_string = estimate_kmps_formatted

# Write to the file
file_path = "result.txt" 
with open(file_path, 'w') as file:
    file.write(output_string)

print("Data written to", file_path)