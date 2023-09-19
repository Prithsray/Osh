import os
import subprocess
from slack_sdk import WebClient
from nbformat import read, write
import json
import requests
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from flask import Flask
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

# Set your Slack Bot Token
@app.route('/slack/run')
def run():

        SLACK_TOKEN = 'xoxb-5853843101958-5873139582801-1IoV2maChVpuGeXHypLMf0VE'

        # Set the path to your Jupyter Notebook

        GITHUB_RAW_NOTEBOOK_URL = 'https://raw.githubusercontent.com/Prithsray/Osh_work/main/dummy.ipynb'

        # Set your GitHub Personal Access Token (PAT)
        GITHUB_PAT = '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'

        # Initialize Slack WebClient
        slack_client = WebClient(token=SLACK_TOKEN)

        headers = {
        'Authorization': f'Bearer {GITHUB_PAT}',
        'Accept': 'application/vnd.github.v3.raw'  # Request raw content
        }

        # Fetch the raw content of the notebook file
        response = requests.get(GITHUB_RAW_NOTEBOOK_URL, headers=headers)

        if response.status_code == 200:
                 notebook_content = response.text
        # Execute the Jupyter Notebook
        subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', GITHUB_RAW_NOTEBOOK_URL],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Open the executed notebook
        notebook = nbformat.reads(notebook_content,as_version=4)

        # Post the notebook content as a message in Slack
        execute_preprocessor = ExecutePreprocessor(timeout=600)  # Adjust the timeout as needed

        # Execute code cells in the notebook
        executed_notebook, _ = execute_preprocessor.preprocess(notebook, {})

        #print(executed_notebook)
        
        return slack_client.chat_postMessage(channel='test', text=" notebook executed successfully")



