call C:\code\AutoScaling-1.0.61.0\bin\as-describe-auto-scaling-groups.cmd
pause
call c:\code\AutoScaling-1.0.61.0\bin\as-describe-launch-configs.cmd
pause
call c:\code\AutoScaling-1.0.61.0\bin\as-delete-auto-scaling-group.cmd %2 --force-delete
pause
call c:\code\AutoScaling-1.0.61.0\bin\as-delete-launch-config.cmd %1
