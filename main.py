import fitz

book_name = 'Good Omens (Neil Gaiman;Terry Pratchett)' 
clippings = 'My Clippings.txt'


def annotate_pdf(annotations):
    doc = fitz.open(f"{book_name}.pdf")

    last_page = None
    found_anns = set()
    for ann in annotations:
        # If the annotation was already found, it goes to the next one:
        if ann in found_anns:
            continue

        for i, page in enumerate(doc):
            if page == last_page:
                start = i
            else:
                start = 0
            # Search
            text_instances = page.search_for(ann)
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
                # Custom color:
                highlight.set_colors(stroke=[0.302, 0.82, 0.949])
                # When I include the annotations:
                # highlight.set_info(content='Example gratia')
                highlight.update()

                # Page control over the loop:
                last_page = page
                found_anns.add(ann)
                break
                

    ### Output
    doc.save(f"{book_name} Annotaded.pdf", garbage=4, deflate=True, clean=True)

def clippings_filter():
    # Text file name
    text_file = clippings

    # Book name you want to search for
    desired_book_name = book_name

    # Variable to store the extracted text
    extracted_text = []

    # Flag to indicate whether we are currently processing the desired book
    processing_desired_book = False

    # Open the text file in read mode with specified encoding
    with open(text_file, "r", encoding="utf-8") as file:
        for line in file:
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

                # Add the line to the extracted text
                extracted_text.append(line)

    # For now, I'll ignore the notes.
    filtered_list = [item for item in extracted_text if item and not item.startswith("-")]
    return filtered_list



filtered_list = clippings_filter()
annotate_pdf(filtered_list)