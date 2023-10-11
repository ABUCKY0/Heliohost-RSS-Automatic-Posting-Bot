import requests #dependencyrer
from HeliohostInstagramImageGenerator import makeimage
import os
import tweepy
import facebook
import json
import shutil
import rss
import time
from heliohostInstagram import heliohostInstagram
from replaceHTMLCodes import replaceHTMLCodes

def defineVariables():
    try:
        with open('credentials_dev.json') as f: 
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
def run(textin):
    defineVariables()
    try:
        #deletes all old images in the output directory before running
        shutil.rmtree(outputdir)
        os.mkdir(outputdir)
    except:
        #if it is already not there, make it without erroring. Won't catch or care about other errors, so I hope there is no issue
        os.mkdir(outputdir)
    #------------------------------- VARIABLES -------------------------------#

    
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    text = textin
    data = {
        "content" : "@everyone " + text
    }

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
        print("An Exception Occured while attempting to post to Discord, but was caught. Here is the error: ")
        print(disc)
    #------------------------------- END DISCORD WEBHOOK -------------------------------#
    #---------------------------------- INSTAGRAM BOT ----------------------------------#
    print()
    ig = heliohostInstagram(instagram_app_token)
    photos = []

    try:
        maxlength = 600 #max amount of characters on an image
        if (len(text) > maxlength):
            sections = int(len(text)/maxlength + 1) #number of images to create, aka the sections of text to use in each image
            if (sections > 10):
                sections = 10
            for i in range(sections):
                ig_text = text[maxlength * i:maxlength * (i + 1)] + "..."
                outfile = "outputdir/output-" + str(i) + ".png"
                with open(outfile, 'w') as fp:
                    pass
                photo = makeimage("dependencies/images/heliohost-bg.png",text=ig_text,font_size=85, font_down_offset=200, savetype="file", output_filename=outfile)
                print(photo[1] + " " + str(i))
                photos += [[photo][0]]
            ig.upload_carousel(photos, text, image_url)
        
        else:
            ig_text = text
            photo = makeimage("dependencies/images/heliohost-bg.png",text=ig_text,font_size=85, font_down_offset=200, savetype="both", output_filename=outputdir + "output-0.png")
            ig.upload_photo(photo, text, image_url)
    except Exception as i:
        print("An Exception Occured while attempting to post to Instagram, but was caught. Here is the error:")
        print(i)
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
        print("An Exception Occured while attempting to post to Facebook, but was caught. Here is the error:")
        print(f)
    #-------------------------------- END FACEBOOK BOT -------------------------------#
    #---------------------------------- TWITTER BOT ----------------------------------#
    print()
    # Authenticate to Twitter
    try:
        auth = tweepy.OAuthHandler(twitter_api, twitter_api_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        try:
            print("Authenticating to Twitter")
            api.verify_credentials()
            print("Authentication OK")
        except:
            print("Error during Twitter authentication")

        tweettext = text
        if (len(tweettext) > 280):
            api.update_status(text[:277] + "...")
        else:
            api.update_status(text)
    except Exception as t:
        print("An Exception Occured while attempting to post to Twitter, but was caught. Here is the error:")
        print(t)

    #------------------------------- END TWITTER BOT -------------------------------#


if __name__ == '__main__':
    while(True):
        datapt = rss.heliohostrss()
        if (datapt[0] == True):
            run(datapt[1])
        time.sleep(10)