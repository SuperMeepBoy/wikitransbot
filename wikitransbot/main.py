import json
import requests
import time

import tweepy


def get_since_id(file_path):
    try:
        with open(file_path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:  # 1st time bot in ran
        return 1


def check_mentions(client, keywords, wikitransbot_id, since_id, config):
    new_since_id = since_id
    tweets = client.get_users_mentions(wikitransbot_id, since_id=since_id)
    if tweets.data:
        for tweet in tweets.data:
            new_since_id = max(tweet.id, new_since_id)
            tweet_text = tweet.text.split(' ')

            if tweet_text[1] != config['trigger_keyword']:
                continue

            base_url = "https://wikitrans.co/wp-admin/admin-ajax.php"
            parameters = "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D="
            url = base_url + parameters
            request_url = f"{url}{' '.join(tweet_text[2:])}"

            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()['data']
                if data['post_count'] == 0:
                    client.create_tweet(
                        text=config['no_answer_template'],
                        in_reply_to_tweet_id=tweet.id,
                    )
                else:
                    client.create_tweet(
                        text=config['answer_template'] % (data['posts'][0]['link']),
                        in_reply_to_tweet_id=tweet.id,
                    )
    return new_since_id


def main():
    config = json.load(open('/etc/wikitransbot/config.json', 'r', encoding='utf-8'))
    twitter_config = config['twitter']
    last_id_file = config['last_id_file']

    client = tweepy.Client(
        consumer_key=twitter_config['twitter_api_key'],
        consumer_secret=twitter_config['twitter_api_key_secret'],
        access_token=twitter_config['twitter_access_token'],
        access_token_secret=twitter_config['twitter_access_token_secret'],
        bearer_token=twitter_config['twitter_bearer_token'],
    )

    wikitransbot_id = 1457666990554894337
    since_id = get_since_id(last_id_file)

    while True:
        since_id = check_mentions(client, ["article"], wikitransbot_id, since_id, config)
        with open(last_id_file, 'w') as f:
            f.write(str(since_id))  # So if the bot crashes we know where to start
        print("Sleeping")
        time.sleep(config['sleep_time'])


if __name__ == "__main__":
    main()
