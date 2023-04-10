from numpy import unicode

from FaceRecognizer import FaceRecognizer
from ImageLoader import ImageLoader


class User:
    def __init__(self, user_id, rgb=None):
        """
        初始化User类的新实例。
        :param user_id: 用户的唯一标识符。
        """
        self.user_id = user_id
        self.image_loader = ImageLoader()
        self.path = f'../user/{user_id}/images/'
        self.features = []
        self.RGB = rgb

    def load_user_images(self):
        """
        加载用户的图像。
        :return: 用户的图像列表。
        """
        images = self.image_loader.load_folder_images(self.path)
        return images

    def load_user_features(self, modelD_path, modelR_path, input_shape):
        """
        加载用户的人脸特征向量。
        :param modelD_path: 人脸检测模型文件的路径。
        :param modelR_path: 人脸识别模型文件的路径。
        :param input_shape: 图像文件的统一尺寸
        """
        images = self.image_loader.load_folder_images(self.path)
        recognizer = FaceRecognizer(modelD_path, modelR_path, input_shape)
        for image in images:
            feature = recognizer.recognize_face(image)
            self.features.append(feature)
