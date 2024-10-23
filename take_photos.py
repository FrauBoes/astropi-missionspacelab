from picamzero import Camera

def take_photo_sequence(photo_dir):
    cam = Camera()
    cam.capture_sequence(photo_dir + "image.jpg", num_images=2, interval=10)
