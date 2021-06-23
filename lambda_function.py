import time
from urllib.request import urlopen


def lambda_handler(event, context):
    url = 'https://4hsinyili-ufc.xyz/test_ip'
    urlopen(url)
    time.sleep(0.5)
