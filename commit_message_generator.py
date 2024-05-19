#!/usr/bin/env python3.11

import boto3
import subprocess
import json

SERVICE = 'bedrock-runtime'
REGION = 'us-east-1'
MODEL_NAME = 'anthropic.claude-3-sonnet-20240229-v1:0'
PROMPT_TEMPLATE = """

Human:
You are a git commit message generator. Follow the instructions provided in the <instructions></instructions> XML tags to generate the commit message for the diff provided in the <diff></diff> XML tags. Only respond with the commit message without any preamble or ending.

<instructions>
Please generate a commit message with the format:
  <format>
    Subject line of the commit message

    - change one to files in the provided diff
    - another change to files in the provided diff
    - ....

    Plain english explanation of what the commit achieves. Do not make it too long.
  </format>
</instructions>

<diff>
{files_diff}
</diff>
"""

git_diff_command = [
  'git',
  'diff',
  '--staged'
]

files_diff = subprocess.check_output(
  git_diff_command, 
  stderr = subprocess.STDOUT,
  shell = False,
  universal_newlines = True
)

bedrock_client = boto3.client(service_name=SERVICE, region_name=REGION)

request_body = {
  "anthropic_version": "bedrock-2023-05-31",
  "max_tokens": 1000,
  "temperature": 0,
  "system": PROMPT_TEMPLATE,
  "messages": [
      {
          "role": "user",
          "content": [
              {
                  "type": "text",
                  "text": files_diff,
              },
          ],
      }
  ],
}

response = bedrock_client.invoke_model(
  modelId = MODEL_NAME,
  body = json.dumps(request_body),
)

print(json.loads(response.get("body").read()).get("content")[0].get("text"))