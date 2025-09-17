import os
import io
from PIL import Image
import eyed3

imgformat = ""

def crop_and_replace_album_art(input_file):
    # load MP3 file
    audiofile = eyed3.load(input_file)

    if audiofile is None:
        return
    
    # Get album art
    if audiofile.tag and audiofile.tag.images:
        # take the first image (assuming there is only one)
        image_data = audiofile.tag.images[0].image_data

        # open image using pillow
        image = Image.open(io.BytesIO(image_data))

        # cropping
        width, height = image.size
        min_dimension = min(width, height)
        left = (width - min_dimension) / 2
        top = (height - min_dimension) / 2
        right = (width + min_dimension) / 2
        bottom = (height + min_dimension) / 2

        cropped_image = image.crop((left, top, right, bottom))

        # turn to binary
        buffered = io.BytesIO()
        cropped_image.save(buffered, format=imgformat.upper()) # TODO - have user be able to choose image encoding
        new_image_data = buffered.getvalue()


        for index,t_image in enumerate(audiofile.tag.images):
            t_image.image_data = new_image_data
        
        # early iterations of saving album art (did not work)
        # audiofile.tag.images[0].image_data = new_image_data
        # audiofile.tag.images.set(3, new_image_data, 'image/PNG')
        

        # save (idkw but for sum reason using this version works)
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)



        print("Album art successfully replaced. - " + input_file)
    else:
        print("!!! No album art found in the provided MP3 file. - " + input_file)

# loop through every subdirectory and driectory
def subdirectories(start_path):
    for root, dirs, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            crop_and_replace_album_art(file_path)
  
# loop through single directory
def directory(start_path):
    for filename in os.listdir(start_path):
        file_path = os.path.join(start_path, filename)
        if os.path.isfile(file_path):
            crop_and_replace_album_art(file_path)
         
print("Welcome to the super album art cropper (only tested on windows)")
while (True):
    usrinput = input("Would you like to encode with PNG or JPEG (j - jpeg, p - png)? ")
    if usrinput == "j":
        imgformat = "jpeg"
        break
    elif usrinput == "p":
        imgformat = "png"
        break
    else:
        print("Invalid parameter")

while (True):
    usrinput = input("Would you like to crop all mp3's in a directory, directory and subdirectory, or just a singular file? (d = directory, f = file, s = subdirectories) ")
    if usrinput == "s":
        subdirectories(input("Enter base directory path (no quotes): "))
        break
    elif usrinput == "f":
        crop_and_replace_album_art(input("Enter file path (no quotes): "))
        break
    elif usrinput == "d":
        directory(input("Enter directory path (no quotes): "))
        break
    else:
        print("Invalid parameter")