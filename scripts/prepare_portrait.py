"""Create reusable ASCII portrait data from a red- or blue-background headshot."""
import argparse
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

parser=argparse.ArgumentParser()
parser.add_argument('photo',help='Local headshot; the original is never copied into the repository')
parser.add_argument('--crop',type=float,nargs=4,default=[.1442,.0657,.8365,.9662],metavar=('LEFT','TOP','RIGHT','BOTTOM'),help='Crop as fractions of source width and height')
parser.add_argument('--background',choices=['red','blue','none'],default='red',help='Background color to remove before ASCII conversion')
args=parser.parse_args()
photo=ImageOps.exif_transpose(Image.open(args.photo)).convert('RGB')
w,h=photo.size
left,top,right,bottom=args.crop
if not (0<=left<right<=1 and 0<=top<bottom<=1):
    parser.error('Crop fractions must be ordered and inside 0..1')
photo=photo.crop((round(left*w),round(top*h),round(right*w),round(bottom*h)))
a=np.asarray(photo).astype(float)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
if args.background=='blue':
    a[(b>r*1.25+20)&(b>g*1.12)&(g>r*1.2)]=255
elif args.background=='red':
    a[(r>g*2.2+20)&(r>b*2.2+20)]=255
im=ImageEnhance.Contrast(ImageOps.autocontrast(Image.fromarray(a.astype('uint8')).convert('L'))).enhance(1.15)
grid=np.asarray(im.resize((96,68),Image.Resampling.LANCZOS))
ramp=' .:-=+*#%@'
rows=[''.join(ramp[min(9,int((255-int(v))/256*10))] for v in row) for row in grid]
root=Path(__file__).resolve().parents[1]
(root/'data/portrait.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
