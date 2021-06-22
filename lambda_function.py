import boto3
import json

# Create an S3 client
s3 = boto3.client('s3')

ssm = boto3.client('ssm')

parameter = ssm.get_parameter(Name='/Custodian/PrincipalOrgPaths', WithDecryption=True)

def lambda_handler(event, context):

    # TODO implement
    orgpaths = [parameter['Parameter']['Value']]

    valor = list(map(lambda x: (x['Name'], json.loads(x['Policy'])), event['resources']))
    
    for bucket, policy in valor:
        check = list(filter(lambda y:
            True
            if check_statement_bucket(bucket, y)
            else
            policy['Statement'].remove(y),
            reversed(policy['Statement'])
            )
        )
        
        if policy['Statement']:
            #response = update_bucket_policy(policy, bucket)
            response = bucket_tag(bucket)
            print(response)
        else:
            #response = s3.delete_bucket_policy(Bucket=bucket)
            response = bucket_tag(bucket)
            print(response)


def check_statement_bucket(bucket_name, policy): 
    sid = policy
        
    if 'AWS' in sid['Principal']:
        
        if 'Condition' in sid:
            if 'ForAnyValue:StringLike' in sid['Condition']:
                
                if 'aws:PrincipalOrgPaths' in sid['Condition']['ForAnyValue:StringLike']:

                    if sid['Condition']['ForAnyValue:StringLike']['aws:PrincipalOrgPaths'] != orgpaths:
                        
                        return False
                        
                    else:
                        
                        return True
                        
                else:

                    return False
                    
            else:
                
                return False
                
                
        else:

            return False

    else:

        return True

    
def update_bucket_policy(policy, bucket_name):
    
    response = s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(policy)
    )
        
    return response

def bucket_tag(bucket):
    response = s3.put_bucket_tagging(
        Bucket=bucket,
        Tagging={
            'TagSet': [
                {
                    'Key': 'c7n-bucket-x-account',
                    'Value': 'True'
                },
            ]
        },
    )
    return response