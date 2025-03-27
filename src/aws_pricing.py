import boto3

client = boto3.client('pricing', region_name='us-east-1')

response = client.get_products(
    ServiceCode='AmazonEC2',
    Filters=[
        {
            'Type': 'TERM_MATCH',
            'Field': 'location',
            'Value': 'US East (N. Virginia)',
        },
        {
            'Type': 'TERM_MATCH',
            'Field': 'instanceType',
            'Value': 't2.micro'
        },
        {
            'Type': 'TERM_MATCH',
            'Field': 'operatingSystem',
            'Value': 'Linux'
        }
    ],
    MaxResults=100
)

for priceItem in response['PriceList']:
    print(priceItem)
