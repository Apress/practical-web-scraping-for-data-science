from keras.models import load_model
import pickle
import os.path
from glob import glob
from random import choice
from functions import *
from constants import *

with open(LABELS_FILE, "rb") as f:
    lb = pickle.load(f)

model = load_model(MODEL_FILE)

# We simply pick a random training image here to illustrate how predictions work.
# In a real setup, you'd obviously plug this into your web scraping pipeline
# and pass a "live" captcha image
image_files = list(glob(os.path.join(CAPTCHA_FOLDER, '*.png')))
image_file = choice(image_files)

print('Testing:', image_file)

image = cv2.imread(image_file)
image = process_image(image)
contours = get_contours(image)
letters = get_letters(image, contours)

for letter in letters:
    letter = cv2.resize(letter, MODEL_SHAPE)
    letter = np.expand_dims(letter, axis=2)
    letter = np.expand_dims(letter, axis=0)
    prediction = model.predict(letter)
    predicted = lb.inverse_transform(prediction)[0]
    print(predicted)