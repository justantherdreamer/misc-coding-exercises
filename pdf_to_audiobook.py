import pyttsx3
import PyPDF2
import sys

'''
following this tutorial: https://www.youtube.com/watch?v=kyZ_5cvrXJI&list=WL&index=19
I had to make small changes, since some functions from PyPDF2 are deprecated.

A small command line tool to read text via TTS.
Functionality to choose a pdf to read, change the voice of the TTS, and choose a page to read
'''

def setup(book_path):
	# we try opening the pdf
	try:
		book = open(book_path, "rb")
	except OSError: # TODO: Is this the right error?
		print("Couldnt open File")
		sys.exit()

	# we set up the pdf reader and get the page number
	pdfReader = PyPDF2.PdfReader(book)
	pages = len(pdfReader.pages)
	return pdfReader, pages


def choose_page_and_read(pages, pdfReader, narrator):
	# we set the current page we want to read
	while True:
		try:	
			desired_page = int(input("What page would you like to read?\n"))
		except ValueError:
			print("Page number must be a *number*.")
			continue
		else:
			break

	if 0 <= desired_page < pages:
		cur_page = pdfReader.pages[desired_page]
		text = cur_page.extract_text()

		# speak
		narrator.say(text)
		narrator.runAndWait()
	else:
		print("The desired page does not exist.")

def get_available_voices(narrator, voices):
	voice = narrator.getProperty('voices')
	for index, voice in enumerate(voices):
		print(f"Voice {index}:")
		print(f" - ID: {voice.id}")
		print(f" - Name: {voice.name}")
		print(f" - Languages: {voice.languages}")
		print(f" - Gender: {voice.gender}")
		print(f" - Age: {voice.age}")
		print()

def set_voice(narrator, voices, voice_id):
	narrator.setProperty("voice", voices[2].id)

def get_ready_to_read(narrator):
	book_path = input("Which book would you like to read?\nGive the filename. The file needs to be a pdf located in the folder the python file is in.\n")
	pdfReader, pages = setup(book_path)
	choose_page_and_read(pages, pdfReader, narrator)

def run_app():
	# setting up the narrator
	narrator = pyttsx3.init()
	voices = narrator.getProperty("voices")
	set_voice(narrator, voices, 2)

	choice = input("What would you like to do?\n1: Change voice	2: Read book\n3: Quit\n")

	if choice not in ["1","2","3"]:
		print("This is not a valid choice.\n")

	match choice:
		case "1":
			get_available_voices(narrator, voices)
			while True:
				try: 
					v = int(input("Which voice would you like?\n"))
				except ValueError:
					print("This is not a valid number.\n")
					continue
			
				if 0 <= v < len(voices):
					set_voice(narrator, voices, v)
					get_ready_to_read(narrator)
					break
				else:
					print("The voice is not available.\n")
					continue
		case "2":
			get_ready_to_read(narrator)
		case "3":
			sys.exit()

if __name__ == "__main__":
	run_app()
