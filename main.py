from get_image import get_aks_image
import json

image_list=get_aks_image()

print(json.dumps(image_list))