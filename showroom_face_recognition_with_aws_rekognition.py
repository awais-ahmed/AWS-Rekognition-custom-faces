import boto3
from botocore.exceptions import ClientError

bucket = "bucket
collectionId = "collection"
maxResults = 2

#Crea collezione
def create_collection():
    rekognition_client = boto3.client('rekognition')
    print('Creating collection:' + collectionId)
    response = rekognition_client.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

#Lista delle collezioni
def listing_collection():
    rekognition_client = boto3.client('rekognition')

    print('Displaying collections...')
    response = rekognition_client.list_collections(MaxResults=maxResults)

    while True:
        collections = response['CollectionIds']

        for collection in collections:
            print(collection)
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = rekognition_client.list_collections(NextToken=nextToken, MaxResults=maxResults)

        else:
            break

    print('done...')

#Elimina collezione
def deleting_collection():
    collectionId = 'deleting'
    print('Attempting to delete collection ' + collectionId)
    client = boto3.client('rekognition')
    statusCode = ''
    try:
        response = client.delete_collection(CollectionId=collectionId)
        statusCode = response['StatusCode']

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('The collection ' + collectionId + ' was not found ')
        else:
            print('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        statusCode = e.response['ResponseMetadata']['HTTPStatusCode']
    print('Operation returned Status Code: ' + str(statusCode))
    print('Done...')

#Lista facce memorizzate
def listing_faces():
    client = boto3.client('rekognition')
    response = client.list_faces(CollectionId=collectionId,
                                 MaxResults=maxResults)
    tokens = True
    print('Faces in ' + collectionId)

    while tokens:

        faces = response['Faces']

        for face in faces:
            print(face)
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_faces(CollectionId=collectionId,
                                         NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False

#Elimina facce
def delete_face():
    faces = []
    faces.append("456b9f10-e417-407f-abf4-58abf7d31c34")

    client = boto3.client('rekognition')

    response = client.delete_faces(CollectionId=collectionId,
                                   FaceIds=faces)

    print(str(len(response['DeletedFaces'])) + ' faces deleted:')
    for faceId in response['DeletedFaces']:
        print(faceId)

#Aggiungi facce alla collezione
def index_faces():
    rekognition_client = boto3.client('rekognition')
    image_file= "DELGIO.png"
    externalimageid = "DELGIO"
    with open(image_file, 'rb') as image:
        rekognition_response = rekognition_client.index_faces(
            Image={"Bytes": image.read()},
            CollectionId=collectionId,
            ExternalImageId=externalimageid
        )
    print(rekognition_response)

#Cerca facce (Predict)
def search_face_in_image():
    imagebytes = "immagine.jpg"
    threshold = 20
    maxFaces = 2
    rekognition_client = boto3.client('rekognition')
    with open(imagebytes, 'rb') as imagebytes:
        response = rekognition_client.search_faces_by_image(CollectionId=collectionId,
                                Image={"Bytes": imagebytes.read()},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)
        #print(response)
        faceMatches = response['FaceMatches']
    for match in faceMatches:
        print('ExternaImageId: '+ match['Face']['ExternalImageId'])
        print('FaceId:' + match['Face']['FaceId'])
        print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")

#main
if __name__ == '__main__':
    rekognition_client = boto3.client('rekognition')
    search_face_in_image()
    
###AWS CLI
#predict windows-->aws rekognition search-faces-by-image --image "S3Object={Bucket=bucket,Name=immagine.jpg}" --collection-id collection --region eu-west-1

#add image to coll--> aws rekognition index-faces --image "S3Object={Bucket=bucket,Name=immgine-jpg}" --collection-id collection --max-faces 1 --quality-filter AUTO  --detection-attributes ALL --external-image-id FIOGIA --region eu-west-1

#listing faces--> aws rekognition list-faces --collection-id qui_id

#delete faces--> aws rekognition delete-faces --collection-id qui_id --faces-ids qui_face_id

#search face in coll by id--> aws rekognition search-faces --face-id qui-face-id --collection-id id_coll

#create collection--> aws rekognition create-collection --collection-id qui_id_della_collezione

#list collection--> aws rekognition list-collections

#describing collection--> aws rekognition describe-collection --collection-id qui_id_della_collezione

#delete collection--> aws rekognition delete-collection --collection-id qui
