from Backend.extract_video.posewrapper import PosePredictor

pred = PosePredictor()
result = pred.predict_image("images/picture.jpg")
print(result)