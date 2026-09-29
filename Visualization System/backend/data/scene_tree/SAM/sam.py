import torch
from segment_anything import sam_model_registry, SamPredictor
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import cv2
import random
from shapely.geometry import Polygon, MultiPolygon
from skimage import measure, morphology, filters, io
import shapely
import os

SAM_MODEL_PATH = os.environ.get("ELEDETECTIVE_SAM_CHECKPOINT", "YOU/SAM/MODEL/PATH")

def has_intersection(bounds1, bounds2):
    x1, y1, x2, y2 = bounds1[0], bounds1[1], bounds1[2], bounds1[3]
    x3, y3, x4, y4 = bounds2[0], bounds2[1], bounds2[2], bounds2[3]
    if x2 >= x3 and x4 >= x1 and y2 >= y3 and y4 >= y1:
        return True
    else:
        return False

class Mask:
    def __init__(self, data, width, height, need_bounds=True):
        self.shape = (width, height)
        self.bounds = [width, height, 0, 0]
        self.data = None
        self.area = 0
        if data is not None:
            self.data = data.astype(np.uint8)
            self.area = data.sum()
            if self.area > 0:
                if need_bounds:
                    # self.bounds = [0, 0, width-1, height-1]
                    rows, cols = np.where(self.data == 1)
                    self.bounds[0], self.bounds[1] = rows.min(), cols.min()
                    self.bounds[2], self.bounds[3] = rows.max(), cols.max()
                else:
                    self.bounds = [0, 0, width-1, height-1]

    def intersection(self, mask2, need_bounds=True):
        if not isinstance(mask2, Mask):
            bounds = mask2.bounds
            mask2 = getMaskFromBox(self.shape[0], self.shape[1], bounds[0], bounds[1], bounds[2], bounds[3], need_bounds=need_bounds)
        if self.data is None:
            return self
        if mask2.data is None:
            return mask2
        if has_intersection(self.bounds, mask2.bounds):
        # if True:
            new_data = np.bitwise_and(self.data, mask2.data)
        else:
            new_data = None

        new_mask = Mask(new_data, self.shape[0], self.shape[1], need_bounds=need_bounds)
        return new_mask

    def union(self, mask2, need_bounds=True):
        if not isinstance(mask2, Mask):
            bounds = mask2.bounds
            mask2 = getMaskFromBox(self.shape[0], self.shape[1], bounds[0], bounds[1], bounds[2], bounds[3], need_bounds=need_bounds)
        if self.data is None:
            return mask2
        if mask2.data is None:
            return self
        new_data = np.bitwise_or(self.data, mask2.data)
        new_mask = Mask(new_data, self.shape[0], self.shape[1], need_bounds=need_bounds)
        return new_mask


def getMaskFromBox(width, height, x1, y1, x2, y2, need_bounds=True):
    x1 = max(0, int(x1))
    y1 = max(0, int(y1))
    x2 = min(width, int(x2))
    y2 = min(height, int(y2))
    data = np.zeros((width, height), dtype=np.uint8)
    data[x1:x2, y1:y2] = 1
    return Mask(data, width, height, need_bounds=need_bounds)


def get_mask_predictor():
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(torch.cuda.is_available())
    MODEL_TYPE = "vit_h"
    sam = sam_model_registry[MODEL_TYPE](checkpoint=SAM_MODEL_PATH)
    sam.to(device=DEVICE)
    mask_predictor = SamPredictor(sam)
    return mask_predictor


def mask_to_object(data):
    return Mask(data.T, data.T.shape[0], data.T.shape[1])


def mask_to_polygons(mask, simplify=True):
    # 确保输入掩码为二值化
    mask = mask.astype(np.uint8)

    size = min(mask.shape)/100
    # print('size', size)
    
    # dilated_mask = morphology.dilation(mask, morphology.disk(size))
    # eroded_mask = morphology.erosion(dilated_mask, morphology.disk(size))
    # contours = measure.find_contours(eroded_mask, level=0.5)

    # contours = measure.find_contours(mask, level=0.5)

    padded_image = np.pad(mask, pad_width=1, mode='constant', constant_values=0)
    contours = measure.find_contours(padded_image, level=0.5)
    contours = [contour - 1 for contour in contours]
    
    # 将轮廓转换为 Shapely 多边形
    polygons = []
    for contour in contours:
        # 轮廓是以 (row, col) 的形式返回的，转换为 (x, y)
        contour = np.flip(contour, axis=1)
        
        # 创建 Polygon 对象，并检查其有效性
        if len(contour)<=2:
            continue

        polygon = Polygon(contour)
        if polygon.is_valid and len(polygon.exterior.coords) > 3:  # 确保多边形有效并且至少有3个点
            polygons.append(polygon)
    
    # 如果有多个多边形，返回 MultiPolygon
    if len(polygons) > 1:
        shape = MultiPolygon(polygons).buffer(0)
        if simplify:
            shape = shapely.simplify(shape, size/4).buffer(0)
        return shape
    elif len(polygons) == 1:
        shape = polygons[0].buffer(0)
        if simplify:
            shape = shapely.simplify(shape, size/4).buffer(0)
        return shape
    else:
        return None


def draw_polygon(draw, polygon, outline_color="blue", fill_color=None, line=1):
    if isinstance(polygon, Polygon):
        # 获取外部轮廓的坐标并绘制
        exterior_coords = list(polygon.exterior.coords)
        if len(exterior_coords) >= 2:
            draw.polygon(exterior_coords, outline=outline_color, fill=fill_color, width=line)
        
        # 如果有内部孔洞，也绘制出来
        for interior in polygon.interiors:
            interior_coords = list(interior.coords)
            draw.polygon(interior_coords, outline=outline_color, width=line)
    elif isinstance(polygon, MultiPolygon):
        # 如果是 MultiPolygon，迭代每个 Polygon 并绘制
        for poly in polygon.geoms:
            draw_polygon(draw, poly, outline_color, fill_color, line=line)


def sam_pred_image(mask_predictor, path):
    image_bgr = cv2.imread(path)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mask_predictor.set_image(image_rgb)


def sam_get_mask_shape(mask_predictor, box, image_path=None):
    masks, scores, logits = mask_predictor.predict(
        box=box,
        multimask_output=True
    )
    # print(scores)
    # print('start turn to shape')
    if len(masks) == 0:
        return None, None

    best_index = np.argmax(scores)
    mask = masks[best_index]

    poly = mask_to_polygons(mask)
    # poly = shapely.geometry.box(box[0], box[1], box[2], box[3])
    mask_obj = mask_to_object(mask)

    old_poly = poly

    if poly is None:
        return None, None
    poly = poly.intersection(shapely.geometry.box(box[0], box[1], box[2], box[3]))
    mask_obj = mask_obj.intersection(shapely.geometry.box(box[0], box[1], box[2], box[3]))
    # print('end turn to shape')

    def get_random_color():
        return tuple([random.randint(0, 255) for _ in range(3)] + [100])  # RGB + alpha
    
    if image_path is not None:
        
        image = Image.open(image_path)
        image = image.convert("RGBA")
        # print(np.array(image).shape)

        # mask_overlay = Image.new("RGBA", image.size)
        # mask_image = Image.fromarray(mask.astype(np.uint8) * 255)
        # color = get_random_color()
        # color_layer = Image.new("RGBA", image.size, color)
        # mask_image = mask_image.convert("L")
        # mask_colored = Image.composite(color_layer, Image.new("RGBA", image.size), mask_image)
        # mask_overlay = Image.alpha_composite(mask_overlay, mask_colored)
        # final_image = Image.alpha_composite(image, mask_overlay)

        final_image = image.copy()
        draw = ImageDraw.Draw(final_image)
        draw_polygon(draw, old_poly)

        # 保存结果
        output_path = "final_image_with_masks.png"
        final_image.save(output_path)

    # return poly, mask_obj
    return poly, None


if __name__ == "__main__":

    image_path = "water_tap.jpg"

    mask_predictor = get_mask_predictor()
    sam_pred_image(mask_predictor, image_path)

    # box = np.array([553, 1, 1399, 523])
    # box = np.array([9.63959229e+02, 5.50247314e+02, 1.39999988e+03, 1.25458313e+03]).astype('int')
    # box = np.array([7.91222046e+02, 5.35284851e+02, 1.05105029e+03, 7.95860962e+02]).astype('int')
    box = np.array([0, 0, 1399, 1746])
    print(sam_get_mask_shape(mask_predictor, box, image_path=image_path))