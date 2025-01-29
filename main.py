from calculate_speed import *
from util import *
from datetime import datetime, timedelta
from logzero import logger, logfile
from pathlib import Path
from time import sleep
import itertools
import os

logfile("events.log")

max_runtime = timedelta(minutes=8)
start_time = datetime.now()

estimates = list()

project_dir = os.getcwd()
image_dir = project_dir + "/data/images/"

print(image_dir)

if not os.path.exists(image_dir):
    os.makedirs(image_dir)
logger.info(f"image_dir set to: {image_dir}.")
    
take_image_sequence(image_dir)
logger.info(f"take_photo_sequence completed.")

image_files = [f for f in os.listdir(image_dir)]

now_time = datetime.now()

for img_1, img_2 in itertools.combinations(image_files, 2):
    if now_time >= start_time + max_runtime:
        logger.warning(f"Maximum runtime reached with {get_datetime_difference_in_minutes(start_time, now_time)} minutes. Program cancelled.")
        break

    image_1_path = os.path.join(image_dir, img_1)
    image_2_path = os.path.join(image_dir, img_2)

    if image_1_path is None or image_2_path is None:
        logger.error(f"Error loading images: {img_1}, {img_2}.")
        continue

    estimate = get_speed_estimate(image_1_path, image_2_path)
    logger.info(f"get_speed_estimate for {image_1_path}, {image_2_path} completed. Estimate: {estimate}.")
    write_estimate(estimates, estimate)

if len(estimates) > 0:
    print(f"Estimate: {sum(estimates) / len(estimates)}")

logger.info(f"Runtime: {get_datetime_difference_in_minutes(start_time, now_time)} minutes. Program finished.")
