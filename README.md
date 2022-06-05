![Twitter Follow](https://img.shields.io/twitter/follow/wikitransbot?style=social) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/SuperMeepBoy/wikitransbot?style=flat-square&color=pink) ![GitHub last commit](https://img.shields.io/github/last-commit/SuperMeepBoy/wikitransbot?color=blue&style=flat-square) ![GitHub](https://img.shields.io/github/license/SuperMeepBoy/wikitransbot?style=flat-square&color=purple)

![wikitransbot banner](./assets/wikitransbot_banner_dark.png "Welcome on the official Wikitransbot Github repo")

## 🪧 Description

This project is a Twitter Bot for the [Wikitrans website](www.wikitransbot.co) which allows any user to perform a request from Twitter.

## 📜 Commands

The available commands are the following :

- **article** [KEYWORDS]\
	*Looks for an article on the Wikitrans website with the provided keywords. Keywords must be separated by a space*
- **intro, bases**\
	*Gets the introduction to transidentity page from the Wikitrans website*
- **trombinoscope, trombi, galerie**\
	*Gets the photos page from the Wikitransbot website*
- **map, carte, associations, association, assos, asso**\
	*Gets the map of associations page from the Wikitransbot website*
- **help, aide**\
	*Gets this section of the project page, describing the available commands*

## 🔍 Examples

Below is an example of a request to look for an article with the keywords "numéro de sécurité sociale" on the Wikitrans website.

![screenshot from Twitter illustration an example of request to the Wikitransbot](./assets/screenshot_wikitransbot_example.png)

## 🔧 Configuration

A configuration template is provided in the repo. You can find it at the root of the project with the name `config_template.json`.

You can find different sections:

### 🐦 A Twitter section

- `twitter`
    - `twitter_api_key`: your Twitter API key
    - `twitter_api_key_secret`: your Twitter API key scret
    - `twitter_access_token`: your Twitter access token
    - `twitter_access_token_secret`: your Twitter access token secret
    - `twitter_bearer_token`: your Twitter bearer token
    - `user_id`: the user ID of your account
- `last_id_file`: the path to the file where the last checked tweet id (called since_id) is stored

### 🌎 A global section (at the root of the json)

 - `sleep_time`: the time between two runs, in seconds (60 is strongly adviced)
 - `trigger_keyword`: the keyword to use to ask the bot an article
 - `logfile_path`: the path to the logfile
 - `stop_words`: a list of words to ignore when performing a search

### 🧱 A command handlers section

They are configured in the `command_handlers` section.

 **You define a command handler section with the name of the class of the handler.**

Every command handlers must at least define :

- `module`: the path to the module of the handler
- `aliases`: the list of keywords to trigger the handler

More configuration can be put in a handler section as needed, (i.e. : templates for the answers)

## 🤝 Contributing

- To submit new issues, please do it in Github using the correct template if there is one. Before doing so, be sure your issue hasn't already been reported. For personnal support please send a mail to roelandt.jef@proton.me
- To contribute, fork the project and make a PR. Commits are expected to be atomics, functionnal and well-named. All features must be tested and must pass the CI.


## 🧑‍🤝‍🧑 Authors

- Jef *"SuperMeepBoy"* Roelandt - roelandt.jef@proton.me

## 🏷️ License

[MIT](LICENSE)
