from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS 

import pandas as pd

import urllib.request
from PIL import Image
from PIL import ImageDraw

import easyocr


app = Flask(__name__)
cors = CORS(app)


app.config['DEBUG'] == True

# load the csv file
flipkart_df = pd.read_csv('final.csv')

# folder path to save image
DETECT_FOLDER = os.path.join(os.getcwd(), "static/detect")
NORMAL_FOLDER = os.path.join(os.getcwd(), "static/normal")


# draw detected bounding box on the image
def draw_boxes(image, bounds, color='red', width=5):
		print('------------boxxx',image)
		img = Image.open(image)
		draw = ImageDraw.Draw(img)
		for bound in bounds:
				p0, p1, p2, p3 = bound[0]
				draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)

		img.save(os.path.join(DETECT_FOLDER, image.split('\\')[-1]))

		# return image name
		return image.split('\\')[-1]


# extract text from image
def ocr(img):
	text_list = []
	try:
		# call ocr object and specify language
		reader = easyocr.Reader(['en'])

		# insert image for ocr
		output = reader.readtext(img)

		# call method to draw bounding box
		detect_img_name = draw_boxes(img, output)

		# get the text from the array
		for no, txt in enumerate(output):
			if len(output[no][-2]) > 1:
				detect_text = output[no][-2]
				text_list.append(detect_text)

		if not text_list:
			return 'no text', None
		else:
			return text_list, detect_img_name
	except:
		return 'Could not load image', img.split('\\')[-1]


@app.route('/')
def home():
	name = list(flipkart_df['product_name'].values)
	return render_template('index.html', name=name)


@app.route('/predict', methods = ['GET', 'POST'])
def predict():

	# get the selected product name
	product_name = request.form.get('productName')

	# get the selected product image
	image_url = flipkart_df['image'][flipkart_df['product_name'] == product_name].values[0]

	# pre process the url
	image_url = image_url.split(',')[0].split('[')[-1].split('"')[1]

	# image name
	image_name = str(image_url.split('/')[-1].strip().split('.')[0])

	image_name = image_name +'.jpg'


	# download the image and save it in image/normal directory
	try:
		all_ok = urllib.request.urlretrieve(image_url, os.path.join(NORMAL_FOLDER, image_name))

	except:
			print('Broken link. Please select another product')

		
	if  all_ok:
		detect_text, detect_fname = ocr(os.path.join(NORMAL_FOLDER, image_name))

		if detect_fname == None:
			return render_template('index.html', normal_fname= image_name, no_text='No text detected')
		else:
			return render_template('index.html', product_name=detect_text, detect_fname= detect_fname, normal_fname= image_name)
	else:
		# if url throw 404
		return render_template('index.html', product_name= 'Image not found')
		

if __name__ == '__main__':
	app.run()

