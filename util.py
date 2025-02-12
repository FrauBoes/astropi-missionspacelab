from picamzero import Camera
import numpy as np

def take_image_sequence(photo_dir):
    """
    Takes a sequence of 42 images at 5 second intervals.
    Accepts a path to the destination directory and returns nothing.
    """
    cam = Camera()
    # Set resolution for HQ camera module, 
    # as per https://www.raspberrypi.com/documentation/accessories/camera.html#hardware-specification
    # cam.still_size = (4056, 3040)
    cam.capture_sequence(photo_dir + "image.jpg", num_images=42, interval=5)

def write_estimate(estimates):
    """
    Writes a formatted estimate string to result.txt.
    Accepts a list of estimates and returns nothing.
    """
    estimate_mean = sum(estimates) / len(estimates)
    estimate_kmps_formatted = "{:.4f}".format(estimate_mean)

    file_path = "result.txt" 
    with open(file_path, 'a', buffering=1) as file:
        file.write(estimate_kmps_formatted)
    print(f"Estimate: {estimate_kmps_formatted}")

def get_datetime_difference_in_minutes(start, end):
    """
    Returns the difference in minutes of the start and end datetimes passed.
    """
    difference = end - start
    return "{:.2f}".format(difference.total_seconds() / 60)

def write_estimate2(estimates):
    """
    Writes a formatted estimate string to result.txt.
    Accepts a list of estimates and returns nothing.
    """
    q1 = np.percentile(estimates, 25)
    q3 = np.percentile(estimates, 75)

    filtered_estimates = [x for x in estimates if q1 <= x <= q3]
    filtered_mean = np.mean(filtered_estimates)
    filtered_mean_formatted = "{:.4f}".format(filtered_mean)

    file_path = "result.txt" 
    with open(file_path, 'a', buffering=1) as file:
        file.write(filtered_mean_formatted)
