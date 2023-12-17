import face_recognition as fr
import cv2 as cv
import os


def face_recognizer(photo_url):
    photo = fr.load_image_file(photo_url)
    face = fr.face_encodings(photo)
    if len(face) > 0:
        return True, face

    return False, None


def prepare_faces():
    known_faces = []
    faces_names = []

    for image in os.listdir('./img'):
        if image.endswith('.jpg'):
            known_faces.append(face_recognizer('./img/' + image)[1][0])
            faces_names.append(image.split('.')[0])

    return known_faces, faces_names


def get_face_from_webcam():
    cam = cv.VideoCapture(0)
    s, img = cam.read()
    if s:
        cv.namedWindow("Tirar foto")
        cv.imshow("Tirar foto", img)
        cv.waitKey(0)
        cv.destroyWindow("Tirar foto")
        cv.imwrite("./temp/temp_image.jpg", img)
        print("Foto tirada com sucesso!")
    unknown = face_recognizer('./temp/temp_image.jpg')
    if unknown[0]:
        unknown_face = unknown[1][0]
        known_faces = prepare_faces()[0]
        known_names = prepare_faces()[1]
        results = fr.compare_faces(known_faces, unknown_face)
        counter = 0
        while not results[counter]:
            counter += 1
        os.remove('./temp/temp_image.jpg')
        return known_names[counter]
    os.remove('./temp/temp_image.jpg')
    return 'Rosto não identificado'


def register_new_user():
    name = input('Digite o nome da pessoa: ').strip().replace(' ', '-')
    cam = cv.VideoCapture(0)
    s, img = cam.read()
    if s:
        cv.namedWindow("Tirar foto")
        cv.imshow("Tirar foto", img)
        cv.waitKey(30)
        cv.destroyWindow("Tirar foto")
        cv.imwrite("./img/" + name + ".jpg", img)
        print("Foto tirada com sucesso!")
