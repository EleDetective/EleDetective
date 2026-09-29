import torch
import os
from dreamsim import dreamsim
from PIL import Image
import torchvision.transforms as transforms
import torch

def dreamsim_load_model():
    # 选择设备（如果有 GPU 则使用 GPU）
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(device)
    model, preprocess = dreamsim(pretrained=True, cache_dir=os.environ.get("ELEDETECTIVE_DREAMSIM_CACHE", "/YOUR/DREAMSIM/CACHE/FOLDER"), device=device)
    
    return {"model": model, "preprocess": preprocess, "device": device}


def dreamsim_model_get_similarity(dreamsim_model, image_path1, boxes1, image_path2, boxes2):
    model, preprocess, device = dreamsim_model["model"], dreamsim_model["preprocess"], dreamsim_model["device"]

    image1 = Image.open(image_path1).convert("RGB")
    cropped_images1 = [image1.crop(box) for box in boxes1]
    preprocessed_images1 = [preprocess(img).to(device) for img in cropped_images1]
    
    image2 = Image.open(image_path2).convert("RGB")
    cropped_images2 = [image1.crop(box) for box in boxes2]
    preprocessed_images2 = [preprocess(img).to(device) for img in cropped_images2]

    distance = np.zeros((len(preprocessed_images1), len(preprocessed_images2)))
    for i in range(len(preprocessed_images1)):
        for j in range(len(preprocessed_images2)):
            distance = model(preprocessed_images1[i], preprocessed_images2[j]).cpu().item()

    return distance


def dreamsim_model_get_feature(dreamsim_model, image_path, boxes, convert="RGB"):
    model, preprocess, device = dreamsim_model["model"], dreamsim_model["preprocess"], dreamsim_model["device"]

    image = Image.open(image_path).convert(convert)
    cropped_images = [image.crop(box) for box in boxes]
    preprocessed_images = [preprocess(img) for img in cropped_images]

    image_tensor = torch.cat(preprocessed_images).to(device)
    print("shape", image_tensor.shape)

    with torch.no_grad():
        image_features = model.embed(image_tensor)
    image_features /= image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu().numpy()