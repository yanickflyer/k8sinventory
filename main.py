from get_image import get_aks_image
from export_csv import export_csv
import json

image_list = get_aks_image()

export_csv(image_list, "output.csv")

print(json.dumps(image_list))