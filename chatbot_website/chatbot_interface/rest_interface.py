from chatbot import chatbot

import argparse
import json
import os
import logging
from tendo import colorer
from klein import Klein


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def decode_parameters(request):
    """Make sure all the parameters have the same encoding.
    Ensures  py2 / py3 compatibility."""
    return {
        key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict')
        for key, value in request.args.items()}


class DeepQAInterface(object):
    app = Klein()

    def __init__(self, model_tag, chatbot_path):
        self.bot = chatbot.Chatbot()
        self.bot.main(['--modelTag', model_tag,
                       '--test', 'daemon',
                       '--rootDir', chatbot_path,
                       '--keepAll'])

    def set_headers(self, request):
        request.setHeader('Content-Type', 'application/json')

    @app.route('/')
    def items(self, request):
        self.set_headers(request)
        return json.dumps("Hey there! I am the REST simple interface for DeepQA")

    @app.route('/parse', methods=['POST', 'GET'])
    def parse(self, request):

        if request.method.decode('utf-8', 'strict') == 'GET':
            request_params = decode_parameters(request)
        else:
            request_params = json.loads(
                request.content.read().decode('utf-8', 'strict'))

        try:
            q = request_params.get('q') or request_params.get('sentence', "")
            logger.info("Received: '{}'".format(q))
            return self.bot.daemonPredict(q)
        except Exception as e:
            return "Error {}".format(e)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_tag", default='cornell-tf1.3', help="Model to load")
    parser.add_argument("-p", "--port", type=int, default=5000, help="Server port")
    return parser.parse_args()


if __name__ == '__main__':

    args = get_args()

    chitchat = DeepQAInterface(args.model_tag,
                               os.getcwd())

    chitchat.app.run('localhost', args.port)
