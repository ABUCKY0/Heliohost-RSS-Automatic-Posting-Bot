import requests #dependencyrer
from HeliohostInstagramImageGenerator import makeimage
import tweepy
import facebook
import json
import rss
import time
from heliohostInstagram import heliohostInstagram
from replaceHTMLCodes import replaceHTMLCodes
import traceback
from pathlib import Path

def defineVariables():
    try:
        with open('credentials_dev.json') as f: 
                credentials = json.load(f)
    except:
        try:
            with open('credentials_hhprod.json') as f: 
                credentials = json.load(f)
        except:
            with open('credentials_prod.json') as f: 
                credentials = json.load(f)
    
    global image_url, discord, twitter, insta, fb, discord_url, twitter_api, twitter_api_secret, twitter_access_token_secret, twitter_api_secret, twitter_bearer_token, twitter_access_token, fb_app_token, fb_page_id, ig_username, ig_password, outputdir, instagram_app_token, instagram_page_id

    discord = credentials["discord"] #discord section
    twitter = credentials["twitter"] #retreves twitter section for use below 
    insta = credentials["instagram"] #gets instagram section
    fb = credentials["facebook"] #gets facebook section

    discord_url = discord["webhook_url"] #webhook url from discord

    twitter_api = twitter["api_key"] #twitter api key public
    twitter_api_secret = twitter["api_key_secret"] #twitter api key secret
    twitter_bearer_token = twitter["bearer_token"] #not needed now, but just in case
    twitter_access_token = twitter["access_token"] #twitter access token
    twitter_access_token_secret = twitter["access_token_secret"] #twitter access token secret

    fb_app_token = fb["access_token"] #facebook app token
    fb_page_id = fb["page_id"] #facebook page id
    """
    ig_username = insta["username"]
    ig_password = insta["password"]
    """
    instagram_app_token = insta["access_token"]
    instagram_page_id = insta["page_id"]

    outputdir = credentials["general"]["img_dir"]
    image_url = credentials["general"]["img_url"]
def run(textin, title, link, pubdate):
    defineVariables()
    """
    try:
        #deletes all old images in the output directory before running
        #shutil.rmtree(outputdir)
        os.mkdir(outputdir)
    except:
        #if it is already not there, make it without erroring. Won't catch or care about other errors, so I hope there is no issue
        os.mkdir(outputdir)
    """
    Path(outputdir).mkdir(parents=True, exist_ok=True) # makes the output directory if it doesn't exist
    #------------------------------- VARIABLES -------------------------------#
    # Most of these are used for the discord webhook, but some are used for the other parts
    
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook

    # Makes sure text fits within a character limit
    text = textin

    # Truncates the link to remove the ?do=findComment&comment=###### part
    try:
        updated_link = link[:link.index("?")]
    except ValueError:
        updated_link = link
    # Adds the title to the beginning of the text
    text = "\n# " + title + "\n\n" + text
    if (len(text) > 2000):
        text = text[:1900] + "..."
    
    # Webhook Data
    data = {
        #"username" : title, # Username of the webhook
        "content" : "@everyone " + text + "\n\n" + updated_link # Message Contents and adds edited link to the end
    }

    # Replaces HTML Codes with their respective characters
    rpHTML = replaceHTMLCodes(text)
    text = rpHTML.replaceAmpersandCodes()
    #------------------------------- END VARIABLES -------------------------------#
    #------------------------------ DISCORD WEBHOOK ------------------------------#
    print()
    try:
        #Trying to post to discord
        result = requests.post(discord_url, json = data)
        #idk what this does, I got it from the internet, but it works so i'm happy.
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
    except Exception as disc:
        # if an error occured, catch it so the rest of the program still runs
        print("\033[31m" + "An Exception Occured while attempting to post to Discord, but was caught. Here is the error: ")
        traceback.print_tb(disc.__traceback__)
        print("\033[33m" + "The Program is still running, but the Discord post was not made." + "\033[0m")
    #------------------------------- END DISCORD WEBHOOK -------------------------------#
    #---------------------------------- INSTAGRAM BOT ----------------------------------#
    print()
    
    
    try:
        
        ig = heliohostInstagram(instagram_app_token)
        photos = []
        maxlength = 600 #max amount of characters on an image
        if (len(text) > maxlength):
            sections = int(len(text)/maxlength + 1) #number of images to create, aka the sections of text to use in each image
            if (sections > 10):
                sections = 10
            for i in range(sections):
                ig_text = text[maxlength * i:maxlength * (i + 1)] + "..."
                outfile = outputdir + "/output-" + time.strftime("%Y%m%d-%H%M%S") + "-" + str(i) + ".png"
                with open(outfile, 'w') as fp:
                    pass
                photo = makeimage("dependencies/images/heliohost-bg.png",text=ig_text,font_size=85, font_down_offset=200, savetype="file", output_filename=outfile)
                print(photo[1] + " " + str(i))
                photos += [[photo][0]]
            ig.upload_carousel(photos, text, image_url)
        
        else:
            ig_text = text
            outfile = outputdir + "/output-" + time.strftime("%Y%m%d-%H%M%S") + "-0.png"
            photo = makeimage("dependencies/images/heliohost-bg.png",text=ig_text,font_size=85, font_down_offset=200, savetype="both", output_filename=outfile)
            ig.upload_photo(photo, text, image_url)
    except Exception as i:
        print("\033[31m" + "An Exception Occured while attempting to post to Instagram, but was caught. Here is the error:")
        traceback.print_tb(i.__traceback__)
        print("\033[33m" + "The Program is still running, but the Instagram post was not made." + "\033[0m")
    #------------------------------- END INSTAGRAM BOT -------------------------------#
    #---------------------------------- FACEBOOK BOT ---------------------------------#
    try:
        fb = facebook.GraphAPI(access_token=fb_app_token, version="2.12")
        resp = fb.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == fb_page_id:
                page_access_token = page['access_token']
            fb = facebook.GraphAPI(page_access_token)
        
        fb.put_object(
            parent_object="me",
            connection_name="feed",
            message=text,
            link="https://heliohost.org")
    except Exception as f:
        print("\033[31m" + "An Exception Occured while attempting to post to Facebook, but was caught. Here is the error:")
        traceback.print_tb(f.__traceback__)
        print("\033[33m" + "The Program is still running, but the Facebook post was not made." + "\033[0m")
    #-------------------------------- END FACEBOOK BOT -------------------------------#
    #---------------------------------- TWITTER BOT ----------------------------------#
    print()
    # Authenticate to Twitter
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        print("Authenticating to Twitter")
        print(api.verify_credentials().screen_name)

        tweettext = text
        if (len(tweettext) > 280):
            api.update_status(text[:277] + "...")
        else:
            api.update_status(text)
    except Exception as t:
        print("\033[31m" + "An Exception Occured while attempting to post to Twitter, but was caught. Here is the error:")
        traceback.print_tb(t.__traceback__)
        print("\033[33m" + "The Program is still running, but the Twitter post was not made." + "\033[0m")

    #------------------------------- END TWITTER BOT -------------------------------#


# Main Loop
if __name__ == '__main__':
    # HAHA SUCKER YOU THOUGHT THAT WAS THE MAIN LOOP IT WAS JUST AN IF STATEMENT
    # THIS IS THE MAIN LOOP
    while(True):
        # datapt is short for data point, it is the data point that is returned from the rss feed
        datapt = rss.heliohostrss()
        if (datapt[0] == True):
            # text, title, link, publication date
            run(datapt[1], datapt[2], datapt[3], datapt[4])
        time.sleep(10)
