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

def annotate_pdf(annotations, notes):
    doc = fitz.open(f"{book_name}.pdf")
    last_page = None
    found_anns = set()
    notes_pos = list(notes.keys())
    note_alert = None
    note = None
    # Extract positions:
    for key in annotations.keys():
        try:
            key_splited = key.split('-')
            for z in key_splited:
                if z in notes_pos:
                    note_alert = True
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

        # If the annotation was already found, it goes to the next one:
        if annotations[key] in found_anns:
            continue

        for i, page in enumerate(doc):
            if page == last_page:
                start = i
            else:
                start = 0
            # Search
            text_instances = page.search_for(annotations[key])
            # If the text is found in a page, then we mark the annotation:
            if len(text_instances) > 0:
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
                # When I include the annotations:
                if note:
                    highlight.set_info(content=note, title=author)
                    note = None
                highlight.update()

                # Page control over the loop:
                last_page = page
                found_anns.add(annotations[key])
                break
                

    ### Output
    doc.save(f"{book_name} Annotaded.pdf", garbage=4, deflate=True, clean=True)


def clippings_filter():
    # Text file name
    text_file = clippings

    # Book name you want to search for
    desired_book_name = book_name

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
            if desired_book_name in line:
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
    return extracted_text, extracted_notes

def clean():
    clean = args.clean

    if clean == "y":
        os.remove(f"{book_name}.pdf")
        print("All done!")
    else:
        print("All done!")
        

if __name__ == "__main__":


    book_name = args.book
    clippings = f'{args.clippings}.txt'
    author = args.author
    print("Annotating...")
    extracted_highs, extracted_notes = clippings_filter()
    annotate_pdf(extracted_highs, extracted_notes)
    clean()