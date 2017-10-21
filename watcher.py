from PIL import ImageChops
from PIL import ImageGrab
from PIL import Image
import pyautogui
import time
import threading
import datetime
import sys

# Setup
# Probably need to redo images per machine, but you can test
# Check for screen coordinate translation
# Might need to adjust screenshot region
# Turn on continuous auto for everything
# Create a filter for friend units so no companion will ever be displayed (1* with level 8 black magic)
# Must start at earth shrine quest select

pyautogui.FAILSAFE = True

screenshotRegion = (0, 0, 1100, 2000)
# ss = pyautogui.screenshot(region=screenshotRegion)
# ss.save('screenshot.png')

def translateScreenLocation(location):
	return tuple([x/2 for x in location])

def cleanLocateTuple(location):
	x, y, *rest = location
	return (x, y)

def checkPhase(phaseImage):
	screen = pyautogui.screenshot(region=screenshotRegion)
	location = pyautogui.locate(phaseImage, screen, grayscale=True)
	return location

def clickButton(buttonImage):
	screen = pyautogui.screenshot(region=screenshotRegion)
	location = pyautogui.locate(buttonImage, screen, grayscale=True)
	success = False
	if location:
		location = cleanLocateTuple(location)
		location = translateScreenLocation(location)
		pyautogui.click(location, button='left')
		success = True
	return success

def processPhase(phaseImage, buttonImage):
	location = checkPhase(phaseImage)
	success = False
	if location:
		if buttonImage:
			success = clickButton(buttonImage)
		else:
			location = cleanLocateTuple(location)
			location = translateScreenLocation(location)
			pyautogui.click(location, button='left')
			success = True
	return success


def process():
	print("Starting bot...")
	curPhase = "esEntrance"
	while True:
		print(curPhase)
		if curPhase == "esEntrance":
			if processPhase("esEntrance.png", None):
				curPhase = "esMissions"
		elif curPhase == "esMissions":
			if processPhase("esMissionPage.png", "nextBtn.png"):
				curPhase = "companionSelect"
		elif curPhase == "companionSelect":
			if processPhase("companionSelect.png", "departWithoutCompanion.png"):
				curPhase = "depart"
		elif curPhase == "depart":
			if processPhase("esMissionPage.png", "departBtn.png"):
				curPhase = "results"
		elif curPhase == "results":
			if processPhase("results.png", "resultsNextBtn.png"):
				curPhase = "resultsUnitExp"
		elif curPhase == "resultsUnitExp":
			if processPhase("resultsUnitExp.png", None):
				curPhase = "resultsItemsObtained"
		elif curPhase == "resultsItemsObtained":
			if processPhase("resultsItemsObtained.png", "itemsObtainedNextBtn.png"):
				curPhase = "esEntrance"

thread = threading.Thread(target=process)
thread.daemon = True
thread.start()

try :
	input('Press enter to end\n')
except SyntaxError:
	sys.exit(0)
sys.exit(0)
