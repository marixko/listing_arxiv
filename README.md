# Personalized list of today's articles from ArXiv

Print and/or send to your gmail a personalized list of today's articles published in ArXiv based on your pre-defined multiple sets of keywords. The script returns: title, abstract and the ArXiv link for each article. Entries are grouped  by your pre-defined key. 

## Example




## Info

This is a very simple code that I wrote for my own personal usage. Some possible future implementations are:

- Add a feature to run the code everyday automatically at a certain fixed time
- Improve text formatting 
- Improve accessibility and user-friendliness
- Add other options for saving the article list
- Get the code ready to be published in PyPi

If you are willing to help, feel free to open a Pull Request and/or contact me.


## How to run?

First, make sure you have Python 3+ installed and the bs4 package. If you only want to print the list and do not want to send it to your email, ignore steps 3-4. 

1. Clone the repository in your computer
2. Open user_settings.py in your editor and set the ArXiv's /new URL, a dictionary of keywords (all words must be lowercase) and your gmail. Example:

```
URL = "https://arxiv.org/list/astro-ph/new"

list_key = {"PHOTO-Zs":["photometric redshift", "photo-z", "photometric redshifts", "photo-zs"],
                "QUASARS":["quasar", "qso", "quasars", "qsos"],
                "HIGH-REDSHIFT UNIVERSE": ["high redshift", "high-redshift", "high-z"],
                "ML": ["machine learning", "deep learning"],
                "AGBs": ["agbs", "agb", "assymptotic giant branch"]}
```
3. Install Google Client Library:

```
pip install --upgrade google-api-python-client
```

4. In order to send the list to your email, you need to create a Google API [here](https://console.cloud.google.com/apis/enableflow?apiid=gmail&project=imposing-kite-247601). Follow the instructions from [here](https://mailtrap.io/blog/send-emails-with-gmail-api/). Make sure you name the application as "Gmail API quickstart" and download the JSON file as "client_secret.json" in this directory location. 

5. Run list_arxiv.py in your terminal or IDE

6. Now check your email inbox!








