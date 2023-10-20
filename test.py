from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import cv2
import os

def initialize_models():
    mtcnn0 = MTCNN(image_size=240, margin=0, keep_all=False, min_face_size=40)
    mtcnn = MTCNN(image_size=240, margin=0, keep_all=True, min_face_size=40)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    return mtcnn0, mtcnn, resnet

def read_data_from_folder(folder_path):
    dataset = datasets.ImageFolder(folder_path)
    idx_to_class = {i: c for c, i in dataset.class_to_idx.items()}
    return dataset, idx_to_class

def process_data(dataset, mtcnn0, resnet):
    loader = DataLoader(dataset, collate_fn=lambda x: x[0])
    name_list, embedding_list = [], []
    
    for img, idx in loader:
        face, prob = mtcnn0(img, return_prob=True)
        if face is not None and prob > 0.92:
            emb = resnet(face.unsqueeze(0))
            embedding_list.append(emb.detach())
            name_list.append(idx_to_class[idx])
    
    return embedding_list, name_list

def save_data(embedding_list, name_list, filename='data.pt'):
    data = [embedding_list, name_list]
    torch.save(data, filename)

def load_saved_data(filename='data.pt'):
    load_data = torch.load(filename)
    embedding_list, name_list = load_data[0], load_data[1]
    return embedding_list, name_list

def recognize_faces(mtcnn, resnet, embedding_list, name_list):
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame, try again")
            break

        img = Image.fromarray(frame)
        img_cropped_list, prob_list = mtcnn(img, return_prob=True)

        if img_cropped_list is not None:

            for i, prob in enumerate(prob_list):
                if prob > 0.90:
                    emb = resnet(img_cropped_list[i].unsqueeze(0)).detach()

                    dist_list = []

                    for _, emb_db in enumerate(embedding_list):
                        dist = torch.dist(emb, emb_db).item()
                        dist_list.append(dist)

                    min_dist = min(dist_list)
                    min_dist_idx = dist_list.index(min_dist)
                    name = name_list[min_dist_idx]

                    print(name)
        else:
            os.system("shutdown -s -t 10")

# Main execution
mtcnn0, mtcnn, resnet = initialize_models()
dataset, idx_to_class = read_data_from_folder('accepted')
embedding_list, name_list = process_data(dataset, mtcnn0, resnet)
save_data(embedding_list, name_list)
embedding_list, name_list = load_saved_data()
recognize_faces(mtcnn, resnet, embedding_list, name_list)
