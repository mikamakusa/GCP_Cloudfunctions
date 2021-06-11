from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import datetime, logging, base64, json
from string import Template


def python_resize_region_instance_group(event, context):
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    service = discovery.build('compute', 'v1', credentials=GoogleCredentials.get_application_default())
    try:
        current_time = datetime.datetime.utcnow()
        log_message = Template('Cloud Function was triggered on $time')
        logging.info(log_message.safe_substitute(time=current_time))
        resize_action = (service.regionInstanceGroupManagers().resize(project=message['project'],
                                                                     region=message['region'],
                                                                     instanceGroupManager=message['name'],
                                                                     size=message['size'])).execute()
        return resize_action
    except Exception as error:
        log_message = Template('$error').substitute(error=error)
        logging.error(log_message)
