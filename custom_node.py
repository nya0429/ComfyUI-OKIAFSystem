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

class MusicIndex:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_index": ("INT",{"default": 1, "min": 1,"step": 1},),
            }
        }
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("output_index",)
    FUNCTION = "run"
    CATEGORY = "OKIAF"
    OUTPUT_NODE = True
    def run(self,input_index):
        return (input_index)
    
    # @classmethod
    # def IS_CHANGED(s, latent):
    #     image_path = folder_paths.get_annotated_filepath(latent)
    #     m = hashlib.sha256()
    #     with open(image_path, 'rb') as f:
    #         m.update(f.read())
    #     return m.digest().hex()

    # @classmethod
    # def VALIDATE_INPUTS(s, latent):
    #     if not folder_paths.exists_annotated_filepath(latent):
    #         return "Invalid latent file: {}".format(latent)
    #     return True

class GetServerParameter:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "domain": ("STRING", {"default": "https://w001-api.studiognu.org/api/prompt/mv"}),
                "output": ("STRING", {"default": folder_paths.get_output_directory()}),
                "music1_batch_size": ("INT",{"default": 16, "min": 1, "step": 1},),
                "music2_batch_size": ("INT",{"default": 30, "min": 1, "step": 1},),
                "music3_batch_size": ("INT",{"default": 15, "min": 1, "step": 1},),
                "input_index": ("INT",{"default": 1, "min": 1, "step": 1},),
                "positive_prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
            }
        }
    RETURN_TYPES = ("STRING", "STRING","STRING","INT")
    RETURN_NAMES = ("positive_prompt", "negative_prompt","filename_prefix","video_frame")
    FUNCTION = "run"
    OUTPUT_NODE = True
    CATEGORY = "OKIAF"

    # @classmethod
    # def IS_CHANGED(s, latent):
    #     image_path = folder_paths.get_annotated_filepath(latent)
    #     m = hashlib.sha256()
    #     with open(image_path, 'rb') as f:
    #         m.update(f.read())
    #     return m.digest().hex()

    def run(self,domain,output,positive_prompt,negative_prompt,
            music1_batch_size,music2_batch_size,music3_batch_size):
        

        index = 1
        title = 'Music' + str(index)
        api = domain + '/' + title
        print('api : ',api)

        res = get(api)
        if res.status_code != 200:
            _positive_prompt = positive_prompt
            _negative_prompt = negative_prompt
        
        data = res.json()
        prompt = data["prompt"]
        _positive_prompt = prompt["positive"]
        _negative_prompt = prompt["negative"]

        video_frame = 1
        if index == 1:
            video_frame = music1_batch_size
        elif index == 2:
            video_frame = music2_batch_size
        elif index == 3:
            video_frame = music3_batch_size
        else:
            video_frame = music1_batch_size

        filename_prefix = title

        formatted_date = get_date_strings()
        outputdir = output + '\\' + title + '\\' + formatted_date
        absolute_path = os.path.abspath(outputdir)
        print('output path : ',absolute_path)
        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)
        folder_paths.set_output_directory(absolute_path)

        return (_positive_prompt, _negative_prompt,filename_prefix,video_frame)

NODE_CLASS_MAPPINGS = {
    "GetServerParameter": GetServerParameter,
    "MusicIndex":MusicIndex,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetServerParameter": "Get Server Parameter",
    "MusicIndex":"Music Index",
}
