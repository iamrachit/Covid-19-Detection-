# -*- coding: utf-8 -*-
"""Covid19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xnbgivC8oRwSUm7lp1PThoR2yB445i-P
"""

import os 
# the main purpose of the OS module is to interact with our operating system
# primary uses of OS module is creating folder , remove folder , change directory or move folder

import shutil
# the main purpose of the shutil module is to offer several functions to deal with operations on files and their collections
# it provide the ability to copy and remove the files

import random
# we can generate random numbers in python using random module

import torch 
# PyTorch is the premier open-source deep learning framework developed and maintained my facebook 
# PyTorch provide computation and automatic differentiation on graph_based models
# PyTorch is a python machine learnin package based on Torch 
# PyTorch automatic differentiation for building and tarining nerual networks

import torchvision 
# the torchvision package consists of popular datasets , model architectures and common images

import numpy as np 
# numpy is converted into short form as np
# numpy is an open source numerical python library 
# numpy contains a mulit dimensional array and matrix ddata structures
# it can perform mulitiple fucntion on array such as trignometric , stastical and algebraric routines 
# numpy is an extension of numeric and numarray 
# numpy can also generate random number generators 
# pandas objects rely heavily on numpy objects

pip install Pillow

pip uninstall PIL

pip uninstall Pillow

pip install Pillow

pip install --upgrade --force-reinstall pillow

from PIL import Image
# PIL - python image library 
# to diasplay the image the pillow library is sing an image class within it 
# its primiary function are load images , create images and etc
from matplotlib import pyplot as plt 
# each pyplot fuction makes some change to a figure lie creting plottin area , plot some lines in a plotting area

torch.manual_seed(0)
# torch.manual_seed(seed),is used so that is will set the seed of the random number generator to a fixed value

print('Using PyTorch version', torch.__version__)
# printing the version of PyTorch

"""Preparing the training and tesing set"""

class_names = ['normal','viral','covid']
root_dir = 'COVID -19 Radiograpy Database'
source_dirs = ['/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/normal','/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/viral','/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/covid']

if os.path.isdir(os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database',source_dirs[1])):


    for i,d in enumerate(source_dirs):
        os.rename(os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database',d),  os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database',class_names[i]))
  
    
    for c in class_names:
        images = [x for x in os.listdir(os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database',c)) if x.lower().endswith('png')]
        selected_images = random.sample(images,30)

        for image in selected_images:
            source_path = os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database',c,image)
            target_path = os.path.join('/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database','test',c,image)
            shutil.move(source_path,target_path)

"""Creating Custom Dataset"""

class ChestXRayDataset(torch.utils.data.Dataset):
    def __init__(self, image_dirs, transform):
        def get_images(class_name):
            images = [x for x in os.listdir(image_dirs[class_name]) if x[-3:].lower().endswith('png')]
            print(f'Found {len(images)} {class_name} examples')
            return images
        
        self.images = {}
        self.class_names = ['normal', 'viral', 'covid']
        
        for class_name in self.class_names:
            self.images[class_name] = get_images(class_name)
            
        self.image_dirs = image_dirs
        self.transform = transform
        
    
    def __len__(self):
        return sum([len(self.images[class_name]) for class_name in self.class_names])
    
    
    def __getitem__(self, index):
        class_name = random.choice(self.class_names)
        index = index % len(self.images[class_name])
        image_name = self.images[class_name][index]
        image_path = os.path.join(self.image_dirs[class_name], image_name)
        image = Image.open(image_path).convert('RGB')
        return self.transform(image), self.class_names.index(class_name)

"""Image Transformations"""

train_transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize(size=(224, 224)),
    torchvision.transforms.RandomHorizontalFlip(),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

test_transform = torchvision.transforms.Compose([
    torchvision.transforms.Resize(size=(224, 224)),
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

"""Prepare DataLoader"""

train_dirs = {
    'normal': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/normal',
    'viral': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/viral',
    'covid': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/covid'
}

train_dataset = ChestXRayDataset(train_dirs, train_transform)

test_dirs = {
    'normal': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/test/normal',
    'viral': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/test/viral',
    'covid': '/content/drive/My Drive/Covid 19 Data/COVID-19 Radiography Database/test/covid '
}

test_dataset = ChestXRayDataset(test_dirs, test_transform)

batch_size = 6

dl_train = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
dl_test = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

print('Number of training batches', len(dl_train))
print('Number of test batches', len(dl_test))

"""Data Visualization"""

class_names = train_dataset.class_names


def show_images(images, labels, preds):
    plt.figure(figsize=(8, 4))
    for i, image in enumerate(images):
        plt.subplot(1, 6, i + 1, xticks=[], yticks=[])
        image = image.numpy().transpose((1, 2, 0))
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = image * std + mean
        image = np.clip(image, 0., 1.)
        plt.imshow(image)
        col = 'green'
        if preds[i] != labels[i]:
            col = 'red'
            
        plt.xlabel(f'{class_names[int(labels[i].numpy())]}')
        plt.ylabel(f'{class_names[int(preds[i].numpy())]}', color=col)
    plt.tight_layout()
    plt.show()

images, labels = next(iter(dl_train))
show_images(images, labels, labels)

images, labels = next(iter(dl_test))
show_images(images, labels, labels)

"""Creating the Model"""

resnet18 = torchvision.models.resnet18(pretrained=True)

print(resnet18)

resnet18.fc = torch.nn.Linear(in_features=512, out_features=3)
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(resnet18.parameters(), lr=3e-5)

def show_preds():
    resnet18.eval()
    images, labels = next(iter(dl_test))
    outputs = resnet18(images)
    _, preds = torch.max(outputs, 1)
    show_images(images, labels, preds)

show_preds()

"""Training the Model"""

def train(epochs):
    print('Starting training..')
    for e in range(0, epochs):
        print('='*20)
        print(f'Starting epoch {e + 1}/{epochs}')
        print('='*20)

        train_loss = 0.
        val_loss = 0.

        resnet18.train() # set model to training phase

        for train_step, (images, labels) in enumerate(dl_train):
            optimizer.zero_grad()
            outputs = resnet18(images)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            if train_step % 20 == 0:
                print('Evaluating at step', train_step)

                accuracy = 0

                resnet18.eval() # set model to eval phase

                for val_step, (images, labels) in enumerate(dl_test):
                    outputs = resnet18(images)
                    loss = loss_fn(outputs, labels)
                    val_loss += loss.item()

                    _, preds = torch.max(outputs, 1)
                    accuracy += sum((preds == labels).numpy())

                val_loss /= (val_step + 1)
                accuracy = accuracy/len(test_dataset)
                print(f'Validation Loss: {val_loss:.4f}, Accuracy: {accuracy:.4f}')

                show_preds()

                resnet18.train()

                if accuracy >= 0.95:
                    print('Performance condition satisfied, stopping..')
                    return

        train_loss /= (train_step + 1)

        print(f'Training Loss: {train_loss:.4f}')
    print('Training complete..')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# train(epochs=1)

"""Final Results"""

show_preds()

