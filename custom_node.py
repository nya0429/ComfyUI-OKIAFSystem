import comfy.utils
import numpy as np
import torchvision.transforms.functional as tf
import os
from pathlib import Path
from requests import get
import time

import folder_paths
import datetime


def get_request(api):
    res = get(api)
    return res

def get_date_strings():
    dt_now_ict = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    today = dt_now_ict.date()
    formatted_date = today.strftime("%m%d")
    return formatted_date

def read_index(file_path):
    if not os.path.exists(file_path):
        return 1
    else:
        with open(file_path, 'r') as file:
            index = int(file.read())
        return index
    
def increment_index(index,file_path):
    index = index + 1
    if index == 4:
        index = 1
    with open(file_path, 'w') as file:
        file.write(str(index))
    return index

class GetServerParameter:

    def __init__(self):
        self.index = 1

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "domain": ("STRING", {"default": "https://w001-api.studiognu.org/api/prompt/mv"}),
                "output": ("STRING", {"default": folder_paths.get_output_directory()}),
                "music1_batch_size": ("INT",{"default": 16, "min": 1, "step": 1},),
                "music2_batch_size": ("INT",{"default": 30, "min": 1, "step": 1},),
                "music3_batch_size": ("INT",{"default": 15, "min": 1, "step": 1},),
                "positive_prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
            }
        }
    RETURN_TYPES = ("STRING", "STRING","STRING","INT",)
    RETURN_NAMES = ("positive_prompt", "negative_prompt","filename_prefix","video_frame",)
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "OKIAF"

    def run(self,domain,output,positive_prompt,negative_prompt,
            music1_batch_size,music2_batch_size,music3_batch_size):
        
        title = 'Music' + str(self.index)
        api = domain + '/' + title

        res = get(api)
        if res.status_code != 200:
            _positive_prompt = positive_prompt
            _negative_prompt = negative_prompt
        
        data = res.json()
        prompt = data["prompt"]
        _positive_prompt = prompt["positive"]
        _negative_prompt = prompt["negative"]

        video_frame = 1
        if self.index == 1:
            video_frame = music1_batch_size
        elif self.index == 2:
            video_frame = music2_batch_size
        elif self.index == 3:
            video_frame = music3_batch_size
        else:
            video_frame = music1_batch_size

        filename_prefix = title

        if os.path.exists(output):
            formatted_date = get_date_strings()
            outputdir = output + '\\' + title + '\\' + formatted_date
            absolute_path = os.path.abspath(outputdir)
            print('output path : ',absolute_path)
            if not os.path.exists(absolute_path):
                os.makedirs(absolute_path)
            folder_paths.set_output_directory(absolute_path)

        self.index += 1
        if self.index == 4:
            self.index = 1

        return (_positive_prompt, _negative_prompt,filename_prefix,video_frame,)
    @classmethod
    def IS_CHANGED(s):
        return

NODE_CLASS_MAPPINGS = {
    "GetServerParameter": GetServerParameter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetServerParameter": "Get Server Parameter",
}
