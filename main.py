import requests
import time

import tweepy

import credentials


LAST_ID_FILE = 'since_id.txt'


def get_since_id():
    try:
        with open(LAST_ID_FILE, 'r') as f:
            return int(f.read())
    except FileNotFoundError:  # 1st time bot in ran
        return 1


def check_mentions(api, keywords, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        tweet_text = tweet.text.split(' ')

        if tweet_text[1] != "article":
            continue

        url = f"https://wikitrans.co/wp-admin/admin-ajax.php?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D={' '.join(tweet_text[2:])}"
        response = requests.get(url)
        if response.status_code == 200:
            api.update_status(f"@{tweet.author.screen_name} Check : {response.json()['data']['posts'][0]['link']}", tweet.id)
    return new_since_id


def main():
    # Twitter things
    auth = tweepy.OAuthHandler(credentials.TWITTER_API_KEY, credentials.TWITTER_API_KEY_SECRET)
    auth.set_access_token(credentials.TWITTER_ACCESS_TOKEN, credentials.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    since_id = get_since_id()

    while True:
        since_id = check_mentions(api, ["article"], since_id)
        with open(LAST_ID_FILE, 'w') as f:
            f.write(str(since_id))  # So if the bot crashes we know where to start
        print("Sleeping")
        time.sleep(60)


if __name__ == "__main__":
    main()
