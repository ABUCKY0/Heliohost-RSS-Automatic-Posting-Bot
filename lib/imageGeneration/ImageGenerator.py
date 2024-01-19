from PIL import ImageFont, Image, ImageDraw
import textwrap
from string import ascii_letters


def makeimage(bg_filename="dependencies/images/heliohost_bg.png", font_filename = 'dependencies/fonts/Montserrat_Semibold.ttf',font_size=65, font_down_offset= 0, text = "",color = '#ffffff',savetype="both", output_filename="output.png"):
    ## -----------------------------------------------------------Manage User Set Variables Below------------------------------------------------------------------ ##
    # bg_filename == set to the filename of the background picture. Include the filepath if not at the root of the project folder

    #font_filename == set to the filename of the font. Include the filepath if not at the root of the project folder

    #text -- The Text to display on the image. Replace all presses of the enter key with \n or <br> to keep the same styling, may cause text to go off the image

    #font_size -- The Size of the font that is placed in the image

    #color == The Color of the onscreen text -- Default to a sample taken from the heliohost logo. Either use hex (#123456) or a normal color name (I had it as #fcb414, the heliohost theme color, but @sarp kept complaining)

    ## --------------------------------------------------Loading Images and creating image and text objects--------------------------------------------------------- ##

    # Open image
    try:
        img = Image.open(fp=bg_filename, mode="r" )
        img = img.convert("RGB")
        print("Heliohost Instagram Background Image Loaded with filename: " + bg_filename)
    except Exception as heliohost_err:
        print("Error Loading Background Picture, using Blank Back Background, and loading text color as #ffffff (White) to properly contrast. \n\n Error is as follows: " + str(heliohost_err))
        img = Image.new(mode = "RGB", size = (3000, 3000),color = (0,0,0))
        color="#ffffff"
        print("\n\nLoaded Default Blank image")
    # Load custom font
    try:
        font = ImageFont.truetype(font=font_filename, size=font_size)
        print("Loaded Font to use in the image as filename: " + font_filename)
    except Exception as font_err:
        print("Error Loading Font, using Default System Font \n\n Error is as follows: " + str(font_err))
        font = ImageFont.load_default()


    try:
        # Create DrawText object
        draw = ImageDraw.Draw(im=img)
        # Calculate the average length of a single character of our font.
        # Note: this takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)

        # Translate this average length into a character count
        max_char_count = int(img.size[0] / avg_char_width)
        
        #replaces all <br> tags with \n
        new_body = ""
        lines = text.replace('<br>', '\n').replace("\n\n", "\n").replace("""
        """, "\n").split("\n")

        for liner in lines:
            if len(liner) > max_char_count:
                w = textwrap.TextWrapper(width=max_char_count, break_long_words=False)
                liner = '\n'.join(w.wrap(liner))

            new_body += liner + "\n"
        draw.text(xy=(img.size[0]/2 , img.size[1]/2 + font_down_offset), text=new_body, font=font, fill=color, stroke_width=5,
        stroke_fill="black", anchor='mm', float="center", align="left")
        # view the result
        if (savetype == "return"):
            print("Program Successfully Completed, Returned Image")
            return img
        elif (savetype == "file"):
            print("Program Successfully Completed, Saved image to " + str(output_filename))
            img.save(output_filename)
        elif (savetype == "both"):
            print("Program Successfully Completed, Saved image to " + str(output_filename) + "and Returned the Image")
            img.save(output_filename)
            return img
        else:
            raise Exception("savetype parameter must be of type \"return\",\"file\", or\"both\". Return being the image is returned to your code, file being the image is saved to output.png, and both being both")

        
    except Exception as general_err:
        print("Error Loading Background Picture, using Blank Back Background, and loading text color as white to properly contrast. \n\n Error is as follows: " + str(general_err))

    return [output_filename, img]

if __name__ == "__main__":
    exit("Don't Run This File as a Standalone File! Import it into another file to use it")