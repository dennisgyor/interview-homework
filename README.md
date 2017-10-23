# Interview Homework


## Problem 1

### Scenario
Due to data requirements, developers need to spin up application and database instances in a special AWS account to be able to test their code.  In order to contain costs, the SRE team needs to keep track of how many instances are running at any given time to make sure that we do not cross certain cost thresholds.

### Requirement
Create a Lambda function that can be run on a regular schedule (Cloudwatch Events) that get the number of EC2 Instances running in an account that have a specific tag and put the results in an InfluxDB.

### Instructions
Fork this repo to your personal GitHub account.  After you have completed your function, email a link to your repository for review (an address will be provided to you).  For convenience. , an InfluxDB Docker compose file is included to spin up the InfluxDB

## What You Will Need
1.  A GitHub account
2.  AWS Account
3.  Docker

## Scenario:
Requirements dictate that all EC2 instances created with the 'dev' tag must be tracked in a database.

## Approach:

Clone the repo into your local filesystem.

There is a main.py which is the Python Lambda function which contains logic that counts the dev instances and writes it to the Influx Database.
You set a new rule up in Cloudwatch with the following event pattern and link it to the Lambda function as the target:

{
"source": [
  "aws.ec2"
],
"detail-type": [
  "EC2 Instance State-change Notification"
],
"detail": {
  "state": [
    "running"
  ]
}
}

This should set to rule to fire when there is a change in state for any EC2 instances (running, terminated, etc.).
Also set the target as the Lambda function. This executes the function on a pattern match.
Then in the Lambda function tab, set a trigger to the Lambda function to execute on Cloudwatch Event Rule.

Setting up the InfluxDB container:

1. Spin up a new t2.micro instance and ssh into it (make sure proper ports are accessible via security groups)
2. Run a '<sudo yum update -y>' to update the system.
3. Install docker and docker-compose with: '<sudo yum install docker>' and '<yum install docker-compose>'.
4. Copy the docker-compose.yml or SCP it over to your InfluxDB EC2 instance.
5. To make things easier: you can set your user to be in the docker group so you dont have to run everything as sudo
by running this command exit '<sudo usermod -aG docker $(whoami)>'.
6. Run '<docker-compose up>' to bring up the InfluxDB. You can test that its listening on port 8086 by running '<lsof -i :8086>'
to verify the service is up and is listening on the correct port. You can also test with 'docker inspect'.

## Creating your ZIP file for upload to Lambda:

Navigate to the 'interview-homework/deployment' folder and zip the files up using the following command:
    '<zip -r deploy.zip .>'

This should create a deploy.zip file. Save this for the upload to Lambda later.

## Setting up the function:

1. Copy and paste the main.py text into the editor
2. Change handler to main.lambda_handler
3. Save it
4. Then upload a zip by clicking the "Code Entry type" dropdown and selecting "Upload a .zip file" and upload the deploy.zip (you need this uploaded to AWS to run python modules that the Lambda function needs).

## Create DB via CLI:
curl -X POST -G 54.219.171.245:8086/query --data-urlencode "q=CREATE DATABASE test"

## Query the DB via CLI:

curl -G 54.219.171.245:8086/query --data-urlencode "q=Select * from Running_Instances" --data-urlencode "db=test"

## Test case:
Create a new EC2 host either in the console or via API with the Name:env=Value:dev tags.
This should fire off the Cloudwatch event and then trigger the Lambda function.

You can verify by looking at the cloudwatch log stream in the console and you can
also query the database directly via curl:

curl -G 54.219.171.245:8086/query --data-urlencode "q=Select * from Running_Instances" --data-urlencode "db=test"

Provided that your InfluxDB EC2 instance is avaiable via the internet, you should return back something like this:

{"results":[{"statement_id":0,"series":[{"name":"Running_Instances","columns":["time","value"],"values":[["2017-10-23T00:56:07.082175331Z",1],["2017-10-23T01:05:22.15776887Z",2],["2017-10-23T01:52:30.792649792Z",1]]}]}]}
