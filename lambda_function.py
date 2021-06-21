import boto3
import json

# Create an S3 client
s3 = boto3.client('s3')
orgpaths = ["o-1122334455/r-abcd/ou-1/*", "o-1122334455/r-abcd/ou-2/*"]

def lambda_handler(event, context):
    # TODO implement
    print("SNS Event: " + json.dumps(event))
    
    orgpaths = ["o-1122334455/r-abcd/ou-1/*","o-1122334455/r-abcd/ou-2/*"]
    resources = []

    for i in event['resources']:
        resources.append(i)
    

    for x in resources:
        
        policy = json.loads(x['Policy'])
        
        bucket_name = x['Name']
        remediate = remediate_bucket(bucket_name, policy)
        print(remediate)
     
    
    
    #for sid in policy['Statement']:
            
    #    check = check_statement_bucket(bucket_name, sid)
            
    #    print('Check = ', check)
            
    #    remediate = remediate_bucket(check, bucket_name, sid, policy)
            
    #    print('Remediate = ', remediate)
            
    #    policy = remediate
            
    #print('Final = ', policy)

            
def remediate_bucket(bucket_name, policy):
    for sid in policy['Statement']:
            
        check = check_statement_bucket(bucket_name, sid)
            
        print('Check = ', check)
        
        if check is False:
            policy['Statement'].remove(sid)
            #update = update_bucket_policy(policy, bucket_name)
            
        print('Policy = ', policy['Statement'])
    #    remediate = remediate_bucket(check, bucket_name, sid, policy)
            
    #    print('Remediate = ', remediate)
            
    #    policy = remediat    
    

def check_statement_bucket(bucket_name, policy): 
    sid = policy
        
    if 'AWS' in sid['Principal']:
        
        if 'Condition' in sid:
            if 'ForAnyValue:StringLike' in sid['Condition']:
                
                if 'aws:PrincipalOrgPaths' in sid['Condition']['ForAnyValue:StringLike']:
                    print("Bucket Antes - ", bucket_name)
                    if sid['Condition']['ForAnyValue:StringLike']['aws:PrincipalOrgPaths'] != orgpaths:
                            #policy['Statement'].remove(sid)
                    #    r = update_bucket_policy(policy, bucket_name)
                        return False
                    else:
                        return True
                        
                else:
                  #  policy['Statement'].remove(sid)
                   # r = update_bucket_policy(policy, bucket_name)
                    return False
                    
            else:
                
                    #policy['Statement'].remove(sid)
                #r = update_bucket_policy(policy, bucket_name)
                return False
                
                
        else:
            #bucket_policy = policy['Statement'].remove(sid)
            return False
            #r = update_bucket_policy(policy, bucket_name)
    else:
        return True

    
def update_bucket_policy(policy, bucket_name):
    
    if policy['Statement']:
        
        response = s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(policy)
        )
        
        return response

    else:
        response = s3.delete_bucket_policy(Bucket=bucket_name)

        return response