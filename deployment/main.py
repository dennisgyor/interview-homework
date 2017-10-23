import boto3
from datetime import datetime
from influxdb import InfluxDBClient


#top level handler function
def lambda_handler(event, context):
  #assign ec2 var as a ec2 resource
  ec2 = boto3.resource('ec2')
  #create cloudwatch client
  #cloudwatch = boto3.client('cloudwatch')

  running_instances = count_instances(ec2)
  print('Number of running instances in the development environment ' + str(running_instances))
  update_influx(running_instances)
  #timestamp = datetime.utcnow()
  #cw_metrics(cloudwatch, timestamp, running_instances)
  num_instances = count_instances(ec2)


def count_instances(ec2):
  count = 0
  for i in ec2.instances.all():
      if i.state['Name'] == 'running':
        for t in i.tags:
           if t ['Key'] == 'env' and t ['Value'] == 'dev':
            count += 1
  return count

# def cw_metrics(cloudwatch, timestamp, running_instances):
#     MetricData = []
#     cloudwatch.put_metric_data(
#         Namespace='EC2',
#         MetricData=[
#             {
#                 'MetricName': 'NumberRunningInstances',
#                 'Timestamp': timestamp,
#                 'Value': running_instances,
#                 'Unit': 'Count',
#             },
#             ]
#         )
#

def update_influx(instance_count):

    host = '54.219.171.245'
    port = 8086
    dbname = 'test'

    client = InfluxDBClient(host, port, database=dbname)
    json_body = [
          {
              "measurement": "Running_Instances",
              "fields": {
                  "value": instance_count
              }
          }
      ]

    client.write_points(json_body)

if __name__ == '__main__':
    lambda_handler({}, {})
