
class replaceHTMLCodes:
    def __init__(self, text):
        """
        Initialize the class
        
        Parameters
        ----------
        self : replaceHTMLCodes
            The class itself
        text : str
            The text to replace the HTML codes in
        
        Returns
        -------
        None
        """
        self.text = text
    def replaceAmpersandCodes(self):
        """
        Replace HTML codes with their respective characters

        Parameters
        ----------
        self : replaceHTMLCodes
            The class itself
        
        Returns
        -------
        self.text : str
            The text with the HTML codes replaced
        """
        text = self.text
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&quot;", '"')
        text = text.replace("&copy;", "©")
        text = text.replace("&amp;", "&")

        return text
    def getText(self):
        """
        Return the text
        """
        return self.text
    