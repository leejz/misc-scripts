#!/usr/bin/env bash
# usage: ec2_flip.sh your_instance_name [on/off] profile
iname=$1
onoff=$2
profile="--profile $3"

if [ -z "$iname" ]; then
    echo "invalid: $iname"
    exit
fi

iid=$(aws ec2 describe-instances $profile | grep "InstanceId\|$iname" | grep -B1 "$iname"  | head -n 1 | sed 's/.* \(i\-.*\) .*/\1/')

if [ -z "$iid" ]; then
    echo "invalid: $iid"
    exit
fi
echo $iid
if [ -z "$onoff" ]; then
    echo "no command given"
    exit
elif [ $onoff == "on" ]; then
    cmd="aws ec2 start-instances --instance-ids $iid $profile"
elif [ $onoff == "off" ]; then
    cmd="aws ec2 stop-instances --instance-ids $iid $profile"
else
    echo "command not on or off"
    cmd=""
fi

echo $cmd
eval $cmd


