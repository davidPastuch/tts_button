import pyttsx3  # deprecated but can be used for lower latency tts
import tweepy as tw
import random
import RPi.GPIO as GPIO
from gtts import gTTS
import pygame

# set up twitter keys
# YOU WILL NEED TO FILL THESE OUT TO DOWNLOAD ANY TWEETS
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_token_secret = 'access_token_secret'

# specify a twitter account to get tweets from
acct = 'dril'


def main():
    # button setup
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin 10, configured for input, set pulldown resistor

    # twitter login
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # tts engine setup
    # engine = pyttsx3.init()
    # engine.setProperty('rate', 140)
    pygame.mixer.init()
    pygame.init()

    while True:  # enter infinite loop
        if GPIO.input(10) == GPIO.HIGH:  # only trigger if button is pressed
            tweets = []
            for tweet in tw.Cursor(api.user_timeline, id=acct).items(15):  # find tweets
                tweets.append(tweet)
            random.shuffle(tweets)

            # read out the tweets
            for tweet in tweets:
                if tweet.user.screen_name == acct and tweet.in_reply_to_screen_name is None and tweet.text[:2] != 'RT' \
                        and 'https' not in tweet.text:
                    tts = gTTS(tweet.text, lang='en')  # convert tweet to speech
                    filename = '/tmp/temp.mp3'  # save as a temp file
                    tts.save(filename)
                    pygame.mixer.music.load(filename)  # use pygame to read out the temp file
                    pygame.mixer.music.play()
                    # engine.say(tweet.text)
                    break
            # engine.runAndWait()


if __name__ == "__main__":
    main()
