"""Launch one bounded, tagged EC2 measurement host using AWS CLI login.

No AWS credentials are copied to the instance. SSH is restricted to the
caller's public IPv4. The first user-data command schedules an OS shutdown;
EC2's shutdown behavior is STOP, preserving data until verified retrieval.
"""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import base64
import json
import subprocess
import urllib.request

AWS = r'C:\Program Files\Amazon\AWSCLIV2\aws.exe'
REGION, PROFILE = 'eu-north-1', 'codex-conway'


def aws(*args):
    result = subprocess.run([AWS, *args, '--profile', PROFILE, '--region', REGION,
                             '--output', 'json', '--no-cli-pager'], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout) if result.stdout.strip() else {}


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2)+'\n', encoding='utf-8')


def launch(folder):
    folder.mkdir(parents=True, exist_ok=False)
    name = 'codex-conway-v10-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    key = Path.home()/'.ssh'/name
    key.parent.mkdir(exist_ok=True)
    subprocess.run(['ssh-keygen', '-t', 'ed25519', '-f', str(key), '-N', '', '-C', name],
                   check=True, capture_output=True)
    # Keep key material outside the repository and archives.
    aws('ec2', 'import-key-pair', '--key-name', name,
        '--public-key-material', 'fileb://'+str(key.with_suffix('.pub')))
    caller_ip = urllib.request.urlopen('https://checkip.amazonaws.com', timeout=20).read().decode().strip()
    vpcs = aws('ec2', 'describe-vpcs', '--filters', 'Name=is-default,Values=true')['Vpcs']
    assert len(vpcs) == 1
    vpc = vpcs[0]['VpcId']
    group = aws('ec2', 'create-security-group', '--group-name', name,
                '--description', 'Bounded Conway solver pilot; SSH from one caller only',
                '--vpc-id', vpc)['GroupId']
    aws('ec2', 'authorize-security-group-ingress', '--group-id', group,
        '--protocol', 'tcp', '--port', '22', '--cidr', caller_ip+'/32')
    aws('ec2', 'create-tags', '--resources', group, '--tags', 'Key=Name,Value='+name,
        'Key=Experiment,Value=Conway-V10')
    subnets = aws('ec2', 'describe-subnets', '--filters', 'Name=vpc-id,Values='+vpc)['Subnets']
    image = aws('ssm', 'get-parameter', '--name',
        '/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id')['Parameter']['Value']
    image_info = aws('ec2', 'describe-images', '--image-ids', image)['Images'][0]
    assert image_info['OwnerId'] == '099720109477' and image_info['Architecture'] == 'x86_64'
    user_data = '''#!/bin/bash
set -eu
systemd-run --unit=conway-budget-stop --on-active=40m --timer-property=AccuracySec=1s /usr/sbin/shutdown -h now
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-venv
mkdir -p /opt/conway
python3 -m venv /opt/conway/venv
/opt/conway/venv/bin/pip install --no-cache-dir ortools==9.15.6755 numpy sympy
chown -R ubuntu:ubuntu /opt/conway
touch /opt/conway/READY
'''
    (folder/'bootstrap.sh').write_text(user_data, encoding='utf-8', newline='\n')
    request = dict(ImageId=image, InstanceType='c7a.32xlarge', MinCount=1, MaxCount=1,
                   KeyName=name, InstanceInitiatedShutdownBehavior='stop',
                   MetadataOptions=dict(HttpTokens='required', HttpEndpoint='enabled'),
                   NetworkInterfaces=[dict(DeviceIndex=0, SubnetId=sorted(subnets, key=lambda s:s['AvailabilityZone'])[0]['SubnetId'],
                                           Groups=[group], AssociatePublicIpAddress=True)],
                   BlockDeviceMappings=[dict(DeviceName=image_info['RootDeviceName'],
                       Ebs=dict(VolumeSize=30, VolumeType='gp3', Encrypted=True, DeleteOnTermination=True))],
                   UserData=base64.b64encode(user_data.encode()).decode(),
                   TagSpecifications=[dict(ResourceType=t, Tags=[dict(Key='Name',Value=name),
                         dict(Key='Experiment',Value='Conway-V10'), dict(Key='AutoStopMinutes',Value='40')])
                                      for t in ('instance','volume')],
                   ClientToken=name)
    save(folder/'launch-request.json', request)
    state = dict(created_utc=datetime.now(timezone.utc).isoformat(), name=name, ssh_key=str(key),
                 security_group=group, region=REGION, profile=PROFILE, image=image,
                 hourly_usd=7.03232, auto_stop_minutes=40, caller_cidr=caller_ip+'/32',
                 status='PREPARED', purpose='Bounded measurement pilot, not an unbounded search')
    save(folder/'state.json', state)
    result = aws('ec2', 'run-instances', '--cli-input-json', 'file://'+str((folder/'launch-request.json').resolve()))
    state.update(instance_id=result['Instances'][0]['InstanceId'], status='LAUNCHED')
    save(folder/'state.json', state)
    save(folder/'launch-response.json', result)
    print(json.dumps(state))


def status(folder):
    state = json.loads((folder/'state.json').read_text())
    result = aws('ec2', 'describe-instances', '--instance-ids', state['instance_id'])
    item = result['Reservations'][0]['Instances'][0]
    info = dict(instance_id=item['InstanceId'], state=item['State']['Name'],
                public_ip=item.get('PublicIpAddress'), launch_time=item['LaunchTime'],
                cpu_options=item['CpuOptions'])
    save(folder/'instance-status.json', info)
    print(json.dumps(info))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=('launch','status'))
    p.add_argument('folder', type=Path)
    a = p.parse_args()
    globals()[a.command](a.folder)
