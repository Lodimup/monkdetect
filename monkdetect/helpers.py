import os
from monkdetect.source import Source

def gen_source_objs(source_dir: str) -> list[Source]:
    l_src_objs = []
    for file in os.listdir(source_dir):
        if file.endswith('.jpg') or file.endswith('.png'):
            l_src_objs.append(Source(os.path.join(source_dir, file)))
    return l_src_objs
