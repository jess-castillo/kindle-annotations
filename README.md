# kindle-annotations
This repo contains a code that allows you to back up the annotations you made in your Kindle while reading a book, by move them to the same version of the book, but in a PDF format, so you can access them in the PDF comments sections. It also copies the notes you've made to their corresponding highlights, if any.

## Getting started
### Prerequisites:
1. To install the Python packages that allows this code to run:
```
pip install -r requirements.txt
```

2. You will also need a copy of your Kindle annotations. You can get it by connecting your kindle to your machine, and copying the `txt` file to the root folder of this project. By default, it is called `My Clippings.txt`, but if the file has a different name, make sure to parse it as an argument.

3. Finally, you will need the PDF version of the book you want to move your annotations to, in the root folder of this project. Now, make sure the PDF file is named the same way your Kindle names the books. That is, in the `My Clippings.txt` file, all annotations start with the name of the book. That is the name of the book this code uses for filtering everything!
## Usage

Simply run:
```
python main.py --book name-of-the-book
```

### Arguments

Here are the available command-line arguments for the script:

- `--book`: (Required) The name of the book, without the pdf extension. Make sure the PDF file is named the same way your Kindle names the books.
- `--author`: (Optional, Default: *Casti*) The name of the author that will appear in every single annotation. 
- `--clippings`: (Optional, Default: *My Clippings*) Name of Kindle's clipping file.
- `--clean`: (Optional: y/n, Defaut: *y*) If you want to remove the oiginal PDF after annotation. 


That's all folks!