#data (vision) format
import base64
import json
import os
import oci
#request, io 

#getting the name of the screenshots that are already done
with open('image_text.csv', 'r') as f:
    data = f.read().split('\n')
filenames = [name.split(',')[0] for name in data if name.split(',')[0].endswith('.jpg')]
#print(len(filenames))

#Oracle Vision configurations
config = oci.config.from_file('~/.oci/config')
ai_service_vision_client = oci.ai_vision.AIServiceVisionClient(config=config)
analyze_image_details = oci.ai_vision.models.AnalyzeImageDetails()
inline_image_details = oci.ai_vision.models.InlineImageDetails()
image_object_detection_feature = oci.ai_vision.models.ImageObjectDetectionFeature()
image_text_detection_feature = oci.ai_vision.models.ImageTextDetectionFeature()

#creating a csv file to write the result text inside
f = open('image_text.csv', 'a')

#list the screenshots
image_files = os.listdir('../02-Screenshot/Screenshots-V2/')
#img_file = '../02-Screenshot/Screenshots/vd#3EeEQLZgEVQ.mp4_frame_at_00_00_04.jpg'

for img_file in image_files:
    if img_file not in filenames:
        #check if they end with jpg
        if img_file.endswith('.jpg'):
            #reading each image
            with open(f'../02-Screenshot/Screenshots-V2/{img_file}', "rb") as image_file:
                #converting the image data to the base64 format that works with oracle
                encoded_string = base64.b64encode(image_file.read())
                features = [image_object_detection_feature, image_text_detection_feature]
                inline_image_details.data = encoded_string.decode('utf-8')
                analyze_image_details.image = inline_image_details
                analyze_image_details.features = features

                res = ai_service_vision_client.analyze_image(analyze_image_details=analyze_image_details)
                #the json result
                res_json = json.loads(repr(res.data))
                #print(len(res_json))

                #getting the text from the json, putting it in a list and then to csv
                text_lst = []
                for result in res_json.get('image_text').get('words'):
                    #print(result.get('text'))
                    text_lst.append(result.get('text'))
                #print(' '.join(text_lst))
                f.write(f"{img_file},{' '.join(text_lst)}\n")
f.close()
