from picamzero import Camera

def take_image_sequence(photo_dir):
    """
    Takes a sequence of 42 images at a10 second interval.
    It accepts a path to the destination directory and returns nothing.
    """
    cam = Camera(resolution='4056x3040')
    cam.capture_sequence(photo_dir + "image.jpg", num_images=42, interval=10)
    cam.close()

def write_estimate(estimate_kmps, estimates):
    """
    Writes a formatted estiamte string to result.txt.
    It accepts a list of estimates and returns nothing.
    """
    estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

    file_path = "result.txt" 
    with open(file_path, 'a', buffering=1) as file:
        file.write(estimate_kmps_formatted + "\n")

    estimates.append(estimate_kmps)

def get_datetime_difference_in_minutes(start, end):
    """
    Returns the difference in minutes of the start and end datetimes passed.
    """
    difference = end - start
    return "{:.2f}".format(difference.total_seconds() / 60)
