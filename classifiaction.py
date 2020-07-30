import matplotlib.pyplot as plt
import torch
from torchvision import datasets, transforms
from torch import nn, optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from PIL import Image
import numpy as np


def making_model():
    model  = models.densenet121(pretrained=True)
    # Use GPU if it's available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.densenet121(pretrained=True)    
    model.classifier = nn.Sequential(nn.Linear(1024, 256),
                                    nn.ReLU(),
                                    nn.Dropout(0.2),
                                    nn.Linear(256, 2),
                                    nn.LogSoftmax(dim=1))
    return model

def image_loader(image_name):


    loader =  transforms.Compose([transforms.Resize(255),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])

    """load image, returns cuda tensor"""
    image = Image.open(image_name).convert('RGB')
    image = loader(image).float()
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    return image  #assumes that you're using GPU

model = making_model()

state_dict = torch.load('checkpoint.pth')
model.load_state_dict(state_dict)

path = str(input())
image = image_loader(path)    
logps = model(image)
category  =  {0:'filler',1: 'nonfiller'}
ps = torch.exp(logps)
print('audio file is a', category[np.argmax(ps.detach().numpy())])                                                       