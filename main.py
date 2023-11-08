import fitz
import os
import re
import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--book", type=str, help="What's the name of the book you want to annotate? (Keep in mind the name must appear in the clippings file).", required=True)
parser.add_argument('--author', type=str, help='The author of the annotations', default='Casti')
parser.add_argument('--clippings', type=str, help='The name of the Kindle clippings file (without extension)', default='My Clippings')
parser.add_argument('--clean', type=str, help='Clean original pdf file after procedure? (y/n).', default='y')
args = parser.parse_args()

# Functions
def search_fullname_in_filenames(directory, search_string):
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]

    found_files = [pdf_file for pdf_file in pdf_files if search_string.lower() in pdf_file.lower()]

    return found_files

def clippings_filter():
    # Text file name
    text_file = clippings

    # Book name you want to search for
    desired_book_name = args.book

    # Variable to store the extracted text
    extracted_text = {}
    extracted_notes = {}
    key2 = None


    # Flag to indicate whether we are currently processing the desired book
    processing_desired_book = False

    # Open the text file in read mode with specified encoding
    with open(text_file, "r", encoding="utf-8") as file:
        for line in file:
            # If line is empty, go to the next one
            if not line.strip():
                continue
            # Remove leading and trailing whitespace from the line
            line = line.strip()
            # Check if the line starts with the desired book name
            if desired_book_name.lower() in line.lower():
                processing_desired_book = True
                continue

            if processing_desired_book:
                # If "==========" is encountered, stop processing the book
                if line == "==========":
                    processing_desired_book = False
                    continue

                # Extracts the location of the highlight to use it as key for saving the text:
                match = re.search(r'\| Location (\d+-\d+) \|', line)
                if match:
                    key = match.group(1)
                elif "- Your Note" in line:
                    match2 = re.search(r'\| Location (\d+) \|', line)
                    if match2:
                        key2 = match2.group(1)
                    
                # Filters only what I want to hightlight
                if not line.startswith("-"):
                    extracted_text[key] = line
                    key = None

                    if key2:
                        extracted_notes[key2] = line
                        key2 = None

    # The ones that got None as key are notes. I don't need them here:
    filtered_dict = {k: v for k, v in extracted_text.items() if v is not None}
    extracted_text.clear()
    extracted_text.update(filtered_dict)
    print(f"There were {len(extracted_text)} highlights and {len(extracted_notes)} notes found in the clippings file.")
    return extracted_text, extracted_notes

def annotate_pdf(annotations, notes):
    doc = fitz.open(f"{book_name}.pdf")
    # last_page = None
    found_anns = set()
    notes_pos = list(notes.keys())
    counter_highs = 0
    counter_notes = 0
    note = None
    not_found = []
    # Extract positions:
    for key in annotations.keys():
        found = False
        try:
            key_splited = key.split('-')
            for z in key_splited:
                if z in notes_pos:
                    # Extracts the note if the index work, if not, ignores the error 'cause I don't need it:
                    try:
                        note = extracted_notes[z]
                    except:
                        1
        except:
            1
            # print('Mmmm, weird:')
            # print(annotations[key])
            # print(key)

        # If the annotation was already found, it goes to the next one. 
        if annotations[key] in found_anns:
            continue
            

        for i, page in enumerate(doc):
            # Search
            text_instances = page.search_for(annotations[key])
            # If the text is found in a page, then we mark the annotation:
            if len(text_instances) > 0:
                found = True
                # We mark the borders:
                start = text_instances[0].tl
                stop = text_instances[-1].br
                clip = fitz.Rect()
                # We concatenat the multilines
                for t in text_instances:
                    clip |= t

                # Finally, we add the annotation:
                highlight = page.add_highlight_annot(start=start, stop=stop, clip=clip)
                highlight.set_info(title=author)
                # Custom color:
                highlight.set_colors(stroke=[0.302, 0.82, 0.949])
                counter_highs += 1
                # When I include the annotations:
                if note:
                    highlight.set_info(content=note, title=author)
                    counter_notes += 1
                    note = None

                highlight.update()

                # Page control over the loop:
                # last_page = page
                found_anns.add(annotations[key])
                break
                
        if not found:
            not_found.append(annotations[key])
                
    print(f"There were {counter_highs} highlights and {counter_notes} notes made!")
    if len(not_found) > 0:
        print("\nThe following annotations were not found:")
        for i in not_found:
            print(i+"\n")
             
    ### Output
    doc.save(f"{book_name} Annotaded.pdf", garbage=4, deflate=True, clean=True)

def clean():
    os.remove(f"{book_name}.pdf")
    print("\nAll done!")


# Main method
if __name__ == "__main__":
    # La idea también es intentar que funcione simplificando los nombres y las mayúsculas en ellos:
    book_name = search_fullname_in_filenames(os.getcwd(), args.book)[0][:-4]
    
    clippings = f'{args.clippings}.txt'
    author = args.author
    print(f"Annotating {book_name}\n\n")
    extracted_highs, extracted_notes = clippings_filter()
    annotate_pdf(extracted_highs, extracted_notes)
    
    if args.clean == "y":
        clean()
    else:
        print("\nAll done!")