#!/usr/bin/env python3
"""Read supplied source SFF including PNG-compressed and linked sprites."""
import io
import numpy as np
from PIL import Image
from make_combo_preview import Sff2,lz5_decode

class ReferenceSff(Sff2):
    def image(self,group,number):
        value=self.sprites[group,number];axis=(value[4],value[5]);v=value
        while v[10]==0:
            v=list(self.sprites.values())[v[6]]
        if v[7]==4:
            block=self.tdata_offset if v[-1]&1 else self.ldata_offset;raw=self.data[block+v[9]:block+v[9]+v[10]]
            indices=np.frombuffer(lz5_decode(raw[4:]+b'\0',v[2]*v[3]),dtype=np.uint8).reshape(v[3],v[2]);palette=np.array(self.palette(v[11]),dtype=np.uint8);pixels=palette[indices];pixels[:,:,3]=np.where(indices==0,0,pixels[:,:,3]);return Image.fromarray(pixels),axis
        if v[7] not in [10,11,12]:
            if v is value:return super().image(group,number)
            key=(v[0],v[1]);return super().image(*key)[0],axis
        block=self.tdata_offset if v[-1]&1 else self.ldata_offset
        raw=self.data[block+v[9]:block+v[9]+v[10]]
        im=Image.open(io.BytesIO(raw[4:]));im.load()
        if im.mode=='P':
            indices=np.array(im);palette=np.array(self.palette(v[11]),dtype=np.uint8);pixels=palette[indices];pixels[:,:,3]=np.where(indices==0,0,pixels[:,:,3]);im=Image.fromarray(pixels)
        return im.convert('RGBA'),axis
