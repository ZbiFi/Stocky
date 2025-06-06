import datetime

from requests_oauthlib import OAuth1Session
import json
import TwitterAuth


consumer_key = TwitterAuth.consumer_key
consumer_secret = TwitterAuth.consumer_secret
bearer_token = TwitterAuth.bearer
access_token        = TwitterAuth.access_token
access_token_secret = TwitterAuth.access_token_secret

def makeSimpleTweet(text):
    payload = {"text": text}
    main(payload)

def main(payload):

    # # Get request token
    # request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    # oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    #
    # try:
    #     fetch_response = oauth.fetch_request_token(request_token_url)
    # except ValueError:
    #     print(
    #         "There may have been an issue with the consumer_key or consumer_secret you entered."
    #     )
    #
    # resource_owner_key = fetch_response.get("oauth_token")
    # resource_owner_secret = fetch_response.get("oauth_token_secret")
    # print("Got OAuth token: %s" % resource_owner_key)

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    # authorization_url = oauth.authorization_url(base_authorization_url)
    # print("Please go here and authorize: %s" % authorization_url)
    # verifier = access_token

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code == 403:
        print("You are not allowed to create a Tweet with duplicate content.")
        return
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))

def tweet(text):

    if len(text) + text.count('\n') < 280:
        makeSimpleTweet(text)
        print(text)
    else:
        print('Text is too long. Split into smaller tweets MAX 280 CHARACTERS!')

        tweets = text.split('|')

        for tweet in tweets:
            makeSimpleTweet(tweet)
            print(tweets)


def reduceMessage(text, textMode):

    message = ''
    message += formatDate(str(text[0][0])) + ' ' + textMode + '\n'
    counter = 1

    for record in text:
        newMessage = str(record[1]) + ':' + str(round(float(record[3]), 2)) + ':' + translateDescriptions(record[len(record)-1]) + '\n'
        if len(message) + message.count('\n') + len(newMessage) + newMessage.count('\n') + 9 >= (255 + message.count('|')) * counter:
            if counter == 1:
                message = '[' + str(counter) + '/' + '**' + ']' + '\n' + message

            counter += 1
            message += '|' + '[' + str(counter) + '/' + '**' + ']' + '\n' + formatDate(str(text[0][0])) + ' ' + textMode + '\n' + newMessage

        else:
            message += newMessage
    message = message.replace('**', str(counter))

    tweet(message)


def formatDate (date):

    newDate = f'{date[0]}{date[1]}{date[2]}{date[3]}-{date[4]}{date[5]}-{date[6]}{date[7]}'

    return newDate

def translateDescriptions(text):

    if text == 'BUY':
        return ''
    if text == 'BUY1':
        return ''
    if text == 'BUY2':
        return 'B'
    if text == 'BUY3':
        return 'B'
    if text == 'SELL':
        return 'S'
    if text == 'SELL1':
        return ''
    if text == 'SELL2':
        return ''
    if text == 'SELL3':
        return ''