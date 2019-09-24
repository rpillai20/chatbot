import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postEphemeral",
  channel="CEMSF3CJ1",
  text="Hello!",
  user="rpillai"
