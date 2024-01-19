from requests import get, post

class heliohostInstagram:
    """
    Class to publish to the instagram account
    """
    def __init__(self, access_token):
        """
        Initialize the class
        
        Parameters
        ----------
        self : heliohostInstagram
            The class itself
        access_token : str
            The access token to use to publish to the heliohost instagram account
            
        Returns
        -------
        None
        """
        
        
        self.access_token = access_token
        self.pages = "https://graph.facebook.com/v16.0/me/accounts?access_token={}".format(self.access_token)
        print(get(self.pages).text)
        self.page_id = get(self.pages).json()["data"][0]["id"]
        self.pages_account = "https://graph.facebook.com/v16.0/{}?fields=instagram_business_account&access_token={}".format(self.page_id, self.access_token)
        self.business_account_id = get("https://graph.facebook.com/v16.0/{}?fields=instagram_business_account&access_token={}".format(self.page_id, self.access_token)).json()["instagram_business_account"]["id"]

    def upload_carousel(self, photos, text, url):
        """
        Upload photos to the instagram graph api and return the response, uses carusels
        
        Parameters
        ----------
        self : heliohostInstagram
            The class itself
        photos : list
            A list of photos to upload
        text : str
            The text to use for the caption
        url : str
            The url that the instagram api will get the image from

        Returns
        -------
        post : requests.models.Response
            The response from the post request to the instagram api uploading the reel"""
        containers = ""
        for photo in photos:
            containers += post("https://graph.facebook.com/v16.0/{}/media?image_url={}&access_token={}&is_carousel_item=true".format(self.business_account_id, url + photo, self.access_token)).json()["id"] + "%2c"

            return post("https://graph.facebook.com/v16.0/{}/media?media_type=CAROUSEL&caption={}&children={}&access_token={}".format(self.business_account_id, text, containers, self.access_token)) 
    def upload_photos(self, photo, text, url):
        """
        Upload photos to the instagram graph api and return the response
        
        Parameters
        ----------
        self : heliohostInstagram
            The class itself
        photo : str
            The photo to upload
        text : str
            The text to use for the caption
        url : str
            The url that the instagram api will get the image from

        Returns
        -------
        post : requests.models.Response
            The response from the post request to the instagram api uploading the reel"""
        return post("https://graph.facebook.com/v16.0/{}/media?image_url={}&caption={}&access_token={}".format(self.business_account_id, url + photo, text, self.access_token))