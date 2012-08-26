ver="Winscale 2.0"
lcname='lc8'
asgname='asg8'
amiid='ami-6e07885e' #Winscale 2.0
# Winscale 1.08: ami-6e07885e
loadbalancer='WinBal'
scaleup_threshold = '50'
scaledown_threshold = '30'
period='60'
print ver+' launch config: '+lcname+' autoscale group '+asgname +' ami id: '+amiid+' loadbalancer: '+loadbalancer+' Scaleup: '+ scaleup_threshold+'% Scaledown: '+scaledown_threshold +'%'+' period: '+period + ' sec'

import os
import sys
import time
import string
import pdb

import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.autoscale
import boto.ec2.cloudwatch

from boto.ec2.connection import EC2Connection
from boto.ec2.autoscale import AutoScaleConnection
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import ScalingPolicy

from boto.ec2.cloudwatch import MetricAlarm


akid='AKIAJRRUC3AJVTIAFL4A'    # aws access key id
sak='5OJBVRNx3IBwtSz/VO+T8JxSD+8IzPfjgGjia519'   # aws secret access key
conn=EC2Connection(akid,sak)
regions = boto.ec2.regions()
regions
us=regions[4]
conn=us.connect()
print 'Currently using EC2 connection'

# conn.run_instances(amiid) # can check if good connection to EC2

# Debugging code to make sure I could connect to AMI
# images = conn.get_all_images()
# images
# temp=repr(images)
# print 'The AMI is at position '+str(temp.find(amiid))

conn=boto.ec2.autoscale.AutoScaleConnection(aws_access_key_id=akid, aws_secret_access_key=sak)

regions=boto.ec2.autoscale.regions()
us=regions[4]
conn=us.connect()
print 'Switching to: '+repr(conn)
# temp=conn.get_all_groups()
# print  'Autoscale groups: '+repr(temp)
# 
lc = LaunchConfiguration(name=lcname, 
							 image_id=amiid, 
                             key_name='bill-us-west2-vm-key-pairs',  
                             security_groups=['secgroup-us-west-2a'],
							 instance_type='t1.micro',
							 instance_monitoring=1 
)
returncode=conn.create_launch_configuration(lc)
print 'launch config: '+repr(lc) 
# can add availabilty zone 'us-west-2b' at a later date
# pdb.set_trace()
ag = AutoScalingGroup(group_name=asgname, load_balancers=[loadbalancer],
                          availability_zones=['us-west-2a'],
                          launch_config=lcname, min_size=2, max_size=4)
returncode=conn.create_auto_scaling_group(ag)
print 'auto-scaling group: '+repr(ag)
returncode=conn.get_all_activities(asgname)
print 'time.sleep(60) to allow VMs to start'
time.sleep(60) # wait 60 seconds for VMs to start
returncode=conn.get_all_activities(asgname)
# pdb.set_trace()
scale_up_policy = ScalingPolicy(name='scale_up', 
								adjustment_type='ChangeInCapacity',
								as_name=asgname, 
								scaling_adjustment=1, 
								cooldown=180)

scale_down_policy = boto.ec2.autoscale.policy.ScalingPolicy(name='scale_down', 
								  adjustment_type='ChangeInCapacity',
								  as_name=asgname, 
								  scaling_adjustment=-1, 
								  cooldown=180)

returncode=conn.create_scaling_policy(scale_up_policy)
returncode=conn.create_scaling_policy(scale_down_policy)

# We need to get the ARN (Amazon Resource Name) of each policy
scale_up_policy = conn.get_all_policies(as_group=asgname, policy_names=['scale_up'])[0]
scale_down_policy = conn.get_all_policies(as_group=asgname, policy_names=['scale_down'])[0]

# pdb.set_trace()	
# connect to cloudwatch
cwconn=boto.ec2.cloudwatch.connect_to_region(region_name='us-west-2')
print "Switching to "+repr(cwconn)

alarm_actions = []
alarm_actions.append(scale_up_policy.policy_arn)

dimensions = {"AutoScalingGroupName": asgname}


scale_up_alarm = MetricAlarm(name='scale_up_on_cpu', 
			namespace='AWS/EC2',
            metric='CPUUtilization', 
			statistic='Average',
            comparison='>', 
			threshold=scaleup_threshold,    #50 by default
            period=period, 
			evaluation_periods=1,
            alarm_actions=[scale_up_policy.policy_arn],
            dimensions=dimensions)
			
alarm_actions = []
alarm_actions.append(scale_down_policy.policy_arn)

scale_down_alarm = MetricAlarm(name='scale_down_on_cpu', 
			namespace='AWS/EC2',
            metric='CPUUtilization', 
			statistic='Average',
            comparison='<', 
			threshold=scaledown_threshold,  #30 by default
            period=period, 
			evaluation_periods=1,
            alarm_actions=[scale_down_policy.policy_arn],
            dimensions=dimensions)
		
returncode=cwconn.create_alarm(scale_up_alarm)
print 'scale-up alarm '+repr(returncode) + ' with scale-threshold '+ scaleup_threshold +' duration: '+period + ' seconds'
cwconn.create_alarm(scale_down_alarm)
print 'scale-down alarm '+repr(returncode) + ' with scale-threshold '+ scaledown_threshold + ' period 60 seconds'
print 'Autoscale is enabled' 
sys.exit() 

########## batch file in windows to set this up ############
#set JAVA_HOME=C:\Program Files (x86)\Java\jre7
#set EC2_HOME=C:\aws\ec2-api-tools-1.5.6.0
#set PATH=%PATH%;%EC2_HOME%\bin
#set PATH=%PATH%;%JAVA_HOME%\bin
#set AWS_CREDENTIAL_FILE=c:\awscredentials.keys
#set EC2_CERT=C:\.as\cert-CAXKZ4XPS2W2TQNIDQDRORKQD6PKDTKM.pem
#set EC2_PRIVATE_KEY=c:\bill-us-west2a.pem
#REM set EC2_PRIVATE_KEY=c:\bill-us-west2-vm-key-pairs.pem
#REM set EC2_PRIVATE_KEY=C:\.as\pk-CAXKZ4XPS2W2TQNIDQDRORKQD6PKDTKM.pem
#set AWS_AUTO_SCALING_URL=https://autoscaling.us-west-2.amazonaws.com
#set EC2_URL=https://ec2.us-west-2.amazonaws.com
#set AWS_AUTO_SCALING_HOME=C:\autoscale\AutoScaling-2011-01-01\AutoScaling-1.0.61.0
#set PATH=%PATH%;%AWS_AUTO_SCALING_HOME%\bin
# Use clean.bat %1 %2 to delete the launch config and autoscaling group

