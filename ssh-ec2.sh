#/usr/bin/env bash
# script to ssh to instances
# usage: ssh-ec2.sh profile user pem
profile="--profile $1"
user=$2
pem=$3
ip=$(aws ec2 describe-instances $profile | grep "PrivateIpAddress\|$user" | grep -B1 "$user" | head -n1 | sed 's/.* \(10\..*\) .*/\1/')

echo $ip
if [[ $ip == *.*.*.* ]]; then
    ssh -i "$3" ubuntu@$ip
fi
