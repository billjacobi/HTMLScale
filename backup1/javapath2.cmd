set JAVA_HOME=C:\Program Files (x86)\Java\jre6
set EC2_HOME=C:\code\ec2-api-tools-1.6.1.4
set AWS_AUTO_SCALING_HOME=C:\code\AutoScaling-1.0.61.0
set PATH=%PATH%;%JAVA_HOME%\bin
set PATH=%PATH%;%EC2_HOME%\bin
set PATH=%PATH%;%AWS_AUTO_SCALING_HOME%\bin

set AWS_CREDENTIAL_FILE=c:\awscerts\awscredentials.keys
set EC2_CERT=C:\awscerts\cert-CAXKZ4XPS2W2TQNIDQDRORKQD6PKDTKM.pem
set EC2_PRIVATE_KEY=c:\awscerts\bill-us-west2a.pem

set AWS_AUTO_SCALING_URL=https://autoscaling.us-west-2.amazonaws.com
set EC2_URL=https://ec2.us-west-2.amazonaws.com



REM Use clean.bat %1 %2 to delete the launch config and autoscaling group
