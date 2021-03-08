# # generate test image matrices
# from pylibdmtx.pylibdmtx import encode
# from PIL import Image
# import random
# import string

# letters = string.ascii_lowercase

# for x in range(20):
#     random_data = ''.join(random.choice(letters) for i in range(10))
#     encoded = encode(random_data)
#     img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
#     img.save('matrices/test' + str(x) + '.png')

import moviepy.editor as mp
import os, json

# get settings from json file
with open('settings.json') as file:
    settings = json.load(file)

# directory that stores the encoded matrix image files
matrix_directory = 'matrices'

# clip to overlay matrix
base_clip = mp.VideoFileClip('input_video/capture.mp4')

# list of clips to render out for the final video, intialized with base clip
composite_list = [base_clip]

# duration of each matrix in the video, in seconds
image_duration = settings['duration_desc']['active-time-ms'] / 1000

# running timestamp in seconds to keep track of image time offset
current_offset = settings['duration_desc']['offset-start-ms'] / 1000

# time between each matrix is displayed
dead_time = settings['duration_desc']['dead-time-ms'] / 1000

# duration that each matrix is display
active_time = settings['duration_desc']['active-time-ms'] / 1000

# percent of pixels from the right of the video to offset the matrices by
offset_x_percent = settings['image_desc']['placement']['offset-x'] / 100
offset_y_percent = settings['image_desc']['placement']['offset-y'] / 100

# convert the offset x percent to pixels based on the base video
offset_x_pixels = round(base_clip.w * offset_x_percent)
offset_y_pixels = round(base_clip.h * offset_y_percent)

# iterate through each of the images in the matrix directory
for filename in os.listdir(matrix_directory):

    # generate the matrix image clip
    matrix = (mp.ImageClip(os.path.join(matrix_directory, filename))
        .set_duration(image_duration)
        .set_start(current_offset)
        .set_pos(('right', 'bottom'))
        .margin(right=offset_x_pixels, bottom=offset_y_pixels, opacity=0.0))
    
    # add the image clip to our final list of clips
    composite_list.append(matrix)

    # increment the current offset
    current_offset += (image_duration + dead_time)

# build the composite vide clip
final = mp.CompositeVideoClip(composite_list)

# write to the final video file
final.write_videofile('test.mp4')