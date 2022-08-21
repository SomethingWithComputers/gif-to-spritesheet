import json
import math
import os
from PIL import Image

gifs_directory = 'gifs'
spritesheets_directory = 'assets/spritesheets'
tile_size = (64, 64)
spritesheet_max_size = (8, 3)

all_images = []


def parse(image_path):
    image = Image.open(image_path)

    # file name with extension
    file_name = os.path.basename(image_path)

    # file name without extension
    name = os.path.splitext(file_name)[0];

    path = ''
    number_of_frames = 1
    if image.format == 'PNG':
        path = parse_png(image, name)
    elif image.format == 'GIF':
        path, number_of_frames = parse_gif(image, name)

    # Only correctly sized images for now
    if image.size[0] % 64 == 0:
        all_images.append({'key': name, 'path': path, 'numberOfFrames': number_of_frames})


def parse_gif(image, name):
    # Only continue if it's animated to begin with
    if image.is_animated:
        number_of_frames = image.n_frames
        number_of_rows = math.ceil(number_of_frames / spritesheet_max_size[0])
        spritesheet_image = Image.new('RGBA', (
            min(number_of_frames * tile_size[0], spritesheet_max_size[0] * tile_size[0]),
            number_of_rows * tile_size[1]))

        # Loop over every frame
        for index in range(0, image.n_frames):
            image.seek(index)
            spritesheet_image.paste(image, (
                (index % spritesheet_max_size[0]) * tile_size[0],
                math.floor(index / spritesheet_max_size[0]) * tile_size[1]))

        spritesheet_filename = name + '_' + str(image.n_frames) + '.png'

        # Store all the frames in a single PNG
        full_path = os.path.join(spritesheets_directory, spritesheet_filename);
        spritesheet_image.save(full_path, 'PNG')

        return spritesheet_filename, image.n_frames

    # If it's not animated, pretend like it's a PNG/single image
    return parse_png(image, name), 1


def parse_png(image, name):
    # Just rename the image and copy it on over for now
    spritesheet_filename = name + '_1.png'
    spritesheet_image = Image.new('RGBA', image.size)
    spritesheet_image.paste(image)

    full_path = os.path.join(spritesheets_directory, spritesheet_filename);
    spritesheet_image.save(full_path, 'PNG')

    return spritesheet_filename


if __name__ == '__main__':
    for filename in os.listdir(gifs_directory):
        file = os.path.join(gifs_directory, filename)

        # Make sure we're only parsing files
        if os.path.isfile(file):
            parse(file)

    data = {
        'meta': {'assetPath': 'assets/spritesheets'},
        'images': all_images
    }
    with open('images.json', 'w') as file:
        json.dump(data, file)
