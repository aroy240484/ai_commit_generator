#!/usr/bin/env python3.11

import boto3
import subprocess
from langchain.chains.llm import LLMChain
from langchain.llms import Bedrock
from langchain.prompts import PromptTemplate

SERVICE = 'bedrock'
REGION = 'us-east-1'
MODEL_NAME = 'anthropic.claude-v2:1'
PROMPT_TEMPLATE = """

Human:
You are a git commit message generator. Follow the instructions provided in the <instructions></instructions> XML tags to generate
the commit message for the diff provided in the <diff></diff> XML tags.

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
bedrock_runtime = boto3.client('bedrock-runtime')

configs = { "max_tokens_to_sample": 400, "temperature": 0 }
llm = Bedrock(
  client = bedrock_runtime,
  model_id = MODEL_NAME,
  model_kwargs = configs,
)

prompt_template = PromptTemplate(
  template = PROMPT_TEMPLATE,
  input_variables = [ 'files_diff' ]
)

generate_commit_message_chain = LLMChain(
  llm = llm,
  verbose = False,
  prompt = prompt_template,
)

message = generate_commit_message_chain.run(files_diff = files_diff)
print(message)