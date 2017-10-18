import time
from slackclient import SlackClient

config = {'token': "xoxb-258065498787-5rQHrVjvI1CYvH5fQ3RQYZmq", 'name': "cenebot", 'bot_id': '', 'at_bot': ''}


client = SlackClient(config['token'])

def get_bot_ID():
    members = client.api_call("users.list")['members']
    for member in members:
        if member['name'] == config['name']:
            config['bot_id'] = member['id']
            config['at_bot'] = "<@" + config['bot_id'] + ">"

def handle_command(command, channel, user_id):
    
    members = client.api_call("users.list")['members']
    username = ""
    response = ""

    for member in members:
        if member['id'] == user_id:
            username = member['name']
    
    if 'Regina' in command:
        response = "CAKE FOR ALL, PROVIDED BY " + username
    
    client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_socket_output(slack_rtm_output):
    """
    Zorgt ervoor dat enkel de output rechtstreeks gericht aan de bot
    zal verwerkt worden door de bot. Anders moet de bot alle output verwerken,
    ook als deze helemaal niet aan hem gericht is.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                if config['at_bot'] in output['text']:
                    return output['text'].split(config['at_bot'])[1].strip(), output['channel'], output['user']
                else:
                    return output['text'], output['channel'], output['user']
    return None,None, None

def get_channel_ID():
    channels = client.api_call("groups.list")['groups']
    for channel in channels:
        if channel['name'] == 'test':
            channel_id = channel['id']
    return channel_id

def main():
    READ_WEBSOCKET_DELAY = 1
    if client.rtm_connect():
        client.api_call("chat.postMessage", channel=get_channel_ID(), text="Up and running!", as_user=True)
        print "Cenebot up and running!"
        get_bot_ID()
        while True:
            command, channel, user_id = parse_socket_output(client.rtm_read())
            if command and channel and user_id:
                handle_command(command, channel, user_id)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Error: connection failed!"


if __name__ == '__main__':
    main()