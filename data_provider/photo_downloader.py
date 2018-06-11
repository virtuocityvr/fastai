import os
import sys
import libs.S3Client as S3Client
import logging
import json
import csv
import threading
import queue
import shutil

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
q = queue.Queue(10)

def setup_logger():
    global logger
    formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(screen_handler)


setup_logger()


class PhotoList:

    def __init__(self, input_json):
        self.json = input_json
        logger.debug("found " + str(len(input_json["stills"])) + " stills")
        logger.debug("found " + str(len(input_json["photoSpheres"])) + " photoSpheres")




def load_json_from_file(filename):
    with open(filename) as json_file:
        return json.load(json_file)


def load_photo_list_from_file(filename):
    with open(filename) as json_file:
        return PhotoList(json.load(json_file))


def download_photo():
    while True:
        item = q.get()
        if item is None:
            break
        item[0].download_photo(item[1])
        q.task_done()


def download_photos(source_photo_list, photo_field_name):
    still_directory = "/tmp/photos/"+photo_field_name+"/"
    if not os.path.exists(still_directory):
        os.makedirs(still_directory)
    s3_client = S3Client.S3Client(still_directory)

    threads = []
    for i in range(10):
        t = threading.Thread(target=download_photo)
        t.start()
        threads.append(t)

    for photo in source_photo_list.json[photo_field_name]:
        q.put([s3_client, photo])

    # block until all tasks are done
    q.join()

def export_csv(source_photo_list, photo_field_name, category_name, output_file, photo_folder):
    with open(output_file, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['id', category_name])

        for photo in source_photo_list.json[photo_field_name]:
            name = photo["media"]["path"]
            category = photo[category_name]
            if category is None:
                category = "None"
            photo_file = photo_folder + name
            if os.path.exists(photo_file):
                filewriter.writerow([name, category])

def move_files_in_csv(cvs_file, sourceFolder, target_folder):
    with open(cvs_file, 'r') as f:
        contents = f.readlines()
        for line in contents:
            file_name = line.split(",")[0]
            photo_file = sourceFolder+ file_name;
            if os.path.exists(photo_file):
                shutil.copy2(photo_file, target_folder)

if __name__ == "__main__":
    import sys

    # photo_list = load_photo_list_from_file("data/photos_data.json")

    move_files_in_csv("/Users/binlin/playground/fastai/experiments/still_photos/stills_by_filter.csv",
                      "/tmp/photos/stills_resized/",
                      "/tmp/photos/stills_resized_filtered/")
    # download_photos(photo_list, "stills")
    # export_csv(photo_list, "stills", "type", "/tmp/photos/stills_by_scene_type.csv", "/tmp/photos/stills_resized/")
    # export_csv(photo_list, "stills", "filter", "/tmp/photos/stills_by_filter.csv", "/tmp/photos/stills_resized/")
    # download_photos(photo_list, "photoSpheres")
