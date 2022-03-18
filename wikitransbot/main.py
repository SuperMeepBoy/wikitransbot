import json
import logging
import requests
import time

from pytwitter import Api


def get_since_id(file_path):
    try:
        with open(file_path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:  # 1st time bot in ran
        return 1


def build_search_article_url(*, tweet_text, keyword):
    splitted_tweet = tweet_text.split(keyword + ' ')

    # Trigger word not found
    if len(splitted_tweet) == 1:
        return ""

    base_url = "https://wikitrans.co/wp-admin/admin-ajax.php"
    parameters = "?action=jet_ajax_search&search_taxonomy%5D=&data%5Bvalue%5D="
    url = base_url + parameters
    return f"{url}{splitted_tweet[1]}"


def run(api, keyword, wikitransbot_id, since_id, config):
    try:
        new_since_id = since_id
        tweets = api.get_mentions(user_id=wikitransbot_id, since_id=since_id).data
        for tweet in tweets:
            new_since_id = max(int(tweet.id), new_since_id)

            request_url = build_search_article_url(tweet_text=tweet.text, keyword=keyword)
            if not request_url:
                continue

            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()['data']
                if data['post_count'] == 0:
                    api.create_tweet(
                        text=config['no_answer_template'],
                        reply_in_reply_to_tweet_id=tweet.id,
                        reply_exclude_reply_user_ids=[],
                    )
                else:
                    api.create_tweet(
                        text=config['answer_template'] % (data['posts'][0]['link']),
                        reply_in_reply_to_tweet_id=tweet.id,
                        reply_exclude_reply_user_ids=[],
                    )
        return new_since_id

    except Exception as e:
        logging.info(str(e))
        return since_id


def main():
    config = json.load(open('/etc/wikitransbot/config.json', 'r', encoding='utf-8'))
    twitter_config = config['twitter']
    last_id_file = config['last_id_file']

    api = Api(
        consumer_key=twitter_config['twitter_api_key'],
        consumer_secret=twitter_config['twitter_api_key_secret'],
        access_token=twitter_config['twitter_access_token'],
        access_secret=twitter_config['twitter_access_token_secret'],
    )

    wikitransbot_id = 1457666990554894337
    since_id = get_since_id(last_id_file)

    while True:
        since_id = run(api, config['trigger_keyword'], wikitransbot_id, since_id, config)
        with open(last_id_file, 'w') as f:
            f.write(str(since_id))  # So if the bot crashes we know where to start
        print("Sleeping")
        time.sleep(config['sleep_time'])


if __name__ == "__main__":
    main()
