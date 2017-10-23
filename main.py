import boto3
from datetime import datetime
from influxdb import InfluxDBClient


#top level handler function (needed for Lambda)
def lambda_handler(event, context):
  #assign ec2 var as a ec2 resource
  ec2 = boto3.resource('ec2')

  running_instances = count_instances(ec2)
  print('Number of running instances in the development environment ' + str(running_instances))
  update_influx(running_instances)

# count all instances that are running and are part of the dev environment
def count_instances(ec2):
  count = 0
  for i in ec2.instances.all():
      if i.state['Name'] == 'running':
        for t in i.tags:
           if t ['Key'] == 'env' and t ['Value'] == 'dev':
            count += 1
  return count

# update the Influx DB Docker container with number of running instances
def update_influx(instance_count):

    host = '54.219.171.245'
    port = 8086
    dbname = 'test'

    # client object with metrics populated
    client = InfluxDBClient(host, port, database=dbname)
    json_body = [
          {
              "measurement": "Running_Instances",
              "fields": {
                  "value": instance_count
              }
          }
      ]
    # write metric to DB
    client.write_points(json_body)

# for CLI testing but runs the top level handler function
if __name__ == '__main__':
    lambda_handler({}, {})
