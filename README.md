# kindle-annotations
This repo contains a code that allows you to back up the annotations you made in your Kindle while reading a book, by move them to the same version of the book, but in a PDF format, so you can access them in the PDF comments sections. 

## Getting started
### Prerequisites:
To install the Python packages that allows this code to run:
```
pip install -r requirements.txt
```

You will also need a copy of your Kindle annotations. You can get it by connecting your kindle to your machine, and copying the txt file to the root folder of this project. Make sure it is called `My Clippings.txt`

Finally, you will need the PDF version of the book you want to move your annotations to, in the root folder of this project. Now, make sure the PDF file is named after the same way your Kindle names the books. That is, in the `My Clippings.txt` file, all annotations start with the name of the book. That is the name of the book this code uses for filtering everything!
## Usage

Simply run:
```
python main.py
```

## Working on...

I need to be able to connect the hightlights with the notes I took for every other annotation, and add it to the pdf. Aaaaand I need to be able to add the name of the book as a parameter for the function. Some carpentry for the file and it'll run smoothly. 

That's all folks!