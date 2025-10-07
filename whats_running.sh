#/usr/bin/env bash
# script listing nodes owner 
# usage: whats_running.sh owner
owner=$1
aws ec2 describe-instances --filter "Name=tag-key,Values=Owner" --query 'Reservations[*].Instances[*].{Instance:InstanceId,AZ:Placement.AvailabilityZone,Owner:Tags[?Key==`Owner`]|[0].Value,Name:Tags[?Key==`Name`]|[0].Value,State:State.Name}' | grep $owner


