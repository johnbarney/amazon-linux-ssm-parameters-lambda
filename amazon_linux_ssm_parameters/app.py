import boto3

# Boto3 Clients
SSM_CLIENT = boto3.client('ssm')
EC2_CLIENT = boto3.client('ec2')

IMAGE_MAP = {
    'amzn2-ami-hvm-*-x86_64-gp2':      '/images/amazon/amazon-linux-2',
    'amzn-ami-hvm-*-x86_64-gp2':       '/images/amazon/amazon-linux',
    'amzn-ami-*-amazon-ecs-optimized': '/images/amazon/amazon-linux-ecs',
    'amzn2-ami-ecs-hvm-*-x86_64-ebs':  '/images/amazon/amazon-linux-2-ecs'
}


def lambda_handler(event, context):
    for k, v in IMAGE_MAP.items():
        if __find_and_store_image(k, v) is not True:
            return False
    return True


def __find_and_store_image(name, ssm_param):
    # Find latest AMI-ID
    images = EC2_CLIENT.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': [
                    name
                ]
            },
            {
                'Name': 'state',
                'Values': [
                    'available'
                ]
            }
        ],
        Owners=[
            'amazon'
        ]
    ).get('Images')

    latest = sorted(images, key=lambda k: k['CreationDate'], reverse=True)[0]

    # Write AMI ID to SSM parameter
    response = SSM_CLIENT.put_parameter(
        Name=ssm_param,
        Description=latest.get('Description'),
        Value=latest.get('ImageId'),
        Type='String',
        Overwrite=True
    )

    if type(response['Version']) is int:
        return True
    else:
        return False
