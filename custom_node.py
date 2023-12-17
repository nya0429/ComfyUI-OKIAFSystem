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

class GetServerParameter:

    def __init__(self):
        self.prev_prompt = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api": ("STRING", {"default": "https://w001-api.studiognu.org/api/prompt/mv/Music1"}),
                "music1_title": ("STRING", {"default": "Music1"}),
                "music1_output": ("STRING", {"default": folder_paths.get_output_directory()}),
                "music1_batch_size": ("INT",{"default": 16, "min": 1, "step": 1},),
                "music1_title": ("STRING", {"default": "Music1"}),
                "music2_title": ("STRING", {"default": "Music2"}),
                "music2_output": ("STRING", {"default": folder_paths.get_output_directory()}),
                "music2_batch_size": ("INT",{"default": 30, "min": 1, "step": 1},),
                "music3_title": ("STRING", {"default": "Music3"}),
                "music3_output": ("STRING", {"default": folder_paths.get_output_directory()}),
                "music3_batch_size": ("INT",{"default": 15, "min": 1, "step": 1},),
                "positive_prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
            }
        }
    RETURN_TYPES = ("STRING", "STRING","STRING","INT")
    RETURN_NAMES = ("positive_prompt", "negative_prompt","filename_prefix","video_frame")
    FUNCTION = "run"
    OUTPUT_NODE = True

    CATEGORY = "OKIAF"

    def run(self,api, positive_prompt,negative_prompt,
            music1_title,music2_title,music3_title,
            music1_output,music2_output,music3_output,
            music1_batch_size,music2_batch_size,music3_batch_size):
        
        res = get(api)
        if res.status_code != 200:
            _positive_prompt = positive_prompt
            _negative_prompt = negative_prompt
        
        data = res.json()

        #データが前回と同じだったら1秒待機して再取得する
        while self.prev_prompt == data["prompt"]:
            time.sleep(1)
            res = get(api)
            data = res.json()

        prompt = data["prompt"]
        _positive_prompt = prompt["positive"]
        _negative_prompt = prompt["negative"]
        title = data["music"]
        self.prev_prompt = prompt

        dt_now_ict = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        today = dt_now_ict.date()
        formatted_date = today.strftime("%m%d")

        filename_prefix = ""
        outputdir = ""
        video_frame = 1

        if title == music1_title:
            filename_prefix = music1_title
            outputdir = music1_output
            video_frame = music1_batch_size
        elif title == music2_title:
            filename_prefix = music2_title
            outputdir = music2_output
            video_frame = music2_batch_size
        elif title == music3_title:
            filename_prefix = music3_title
            outputdir = music3_output
            video_frame = music3_batch_size
        else:
            filename_prefix = music1_title
            outputdir = music1_output
            video_frame = music1_batch_size

        outputdir = outputdir + '\\' + formatted_date
        print(folder_paths.get_output_directory())
        print(outputdir)
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        folder_paths.set_output_directory(outputdir)

        return (_positive_prompt, _negative_prompt,filename_prefix,video_frame)

NODE_CLASS_MAPPINGS = {
    "GetServerParameter": GetServerParameter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetServerParameter": "Get Server Parameter",
}
