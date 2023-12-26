import os
import face_recognition


def load_images_from_folder(folder):
    # 存储图像路径、文件名和人脸编码的列表
    image_encodings = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # 构建图像的完整路径
            image_path = os.path.join(folder, filename)
            # 加载图像文件并进行人脸编码
            image = face_recognition.load_image_file(image_path)
            try:
                face_encoding = face_recognition.face_encodings(image)[0]
                # 将图像路径、文件名和人脸编码添加到列表中
                image_encodings.append((image_path, os.path.splitext(filename)[0], face_encoding))
            except IndexError:
                # 捕获IndexError，表示未检测到人脸
                print(f"Skipping {filename}: No face found.")
    return image_encodings


# 指定包含已知人脸图像的文件夹路径
known_faces_folder = "pictures_of_people_i_know"

# 指定包含待识别人脸图像的文件夹路径
unknown_face_folder = "unknown_pictures"

# 从指定文件夹加载已知人脸图像
known_faces = load_images_from_folder(known_faces_folder)

# 从指定文件夹加载待识别人脸图像
unknown_faces = load_images_from_folder(unknown_face_folder)

# 遍历每张待识别人脸图像并与已知人脸比对
for unknown_image_path, unknown_image_name, unknown_face_encoding in unknown_faces:
    results = face_recognition.compare_faces([known_face[2] for known_face in known_faces], unknown_face_encoding)

    # 如果未检测到任何匹配的人脸
    if not True in results:
        print(f"{unknown_image_path},unknown_person")
    else:
        # 获取第一个匹配的已知人脸索引
        matched_index = results.index(True)
        # 获取匹配的已知人脸的文件名（去掉后缀）
        matched_person_name = os.path.splitext(os.path.basename(known_faces[matched_index][0]))[0]
        # 输出结果
        print(f"{unknown_image_path},{matched_person_name}")
