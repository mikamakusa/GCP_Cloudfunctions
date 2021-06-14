from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import datetime, logging, base64, json
from string import Template


def python_resize_gke_node_pool(event, context):
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    service = discovery.build('container', 'v1', credentials=GoogleCredentials.get_application_default())
    try:
        current_time = datetime.datetime.utcnow()
        log_message = Template('Cloud Function was triggered on $time')
        logging.info(log_message.safe_substitute(time=current_time))
        location = 'projects/%s/locations/%s' % (message['project'], message['location'])
        body = dict()
        body["nodeCount"] = message["size"]
        cluster = (service.projects().locations().clusters().list(parent=location)).execute()
        if len(cluster["clusters"]) == 1:
            cluster_path = 'projects/%s/locations/%s/clusters/%s' % (message['project'],
                                                                     message['location'],
                                                                     cluster["clusters"][0]["name"])
            node_pool_id = cluster_path + '/nodePools/%s' % (cluster["clusters"][0]["nodePools"][0]["name"])
            request = (service.projects().locations().clusters().nodePools().setSize(name=node_pool_id,
                                                                                     body=body)).execute()
            return request
        else:
            for _cluster in cluster["clusters"]:
                cluster_path = 'projects/%s/locations/%s/clusters/%s' % (message['project'],
                                                                         message['location'],
                                                                         _cluster["name"])
                node_pool_id = cluster_path + '/nodePools/%s' % (_cluster["nodePools"][0]["name"])
                request = (service.projects().locations().clusters().nodePools().setSize(name=node_pool_id,
                                                                                         body=body)).execute()
                return request
    except Exception as error:
        log_message = Template('$error').substitute(error=error)
        logging.error(log_message)
