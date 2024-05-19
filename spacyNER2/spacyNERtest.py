import spacy
import sys
from spacy.tokens import DocBin
import json
import os
import random
import warnings
warnings.filterwarnings('ignore')


def loadAnnot(path, fileBase):
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create
    trainX = None
    with open(path, 'r') as f:
        trainX = json.load(f)

    for txt, annot in trainX['annotations']:
        doc = nlp.make_doc (txt)
        ents = []
        for s, e, l in annot['entities']:
            span = doc.char_span(s, e, label=l, alignment_mode='contract')
            if (span is None):
                print("skipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

    db.to_disk(fileBase+".spacy")

def main():
    # all_labels = ['GEN', 'OCC', 'TOF', 'COL', 'FAB', 'PRI']
    loadAnnot('./annotations.json', "annotations")
    loadAnnot("./test_annotations.json", "test_annot")

def test():
    prompt = sys.argv[1]
    nlpner = spacy.load("./spacyNER2/model-best")
    doc = nlpner(prompt)
    # print(doc.ents)
    # for ent in doc.ents:
        # print(f'ent: {ent.text.strip()}, label: {ent.label_}')
    return doc.ents

def get_random_image_by_label(label, imageDir):
    if not os.path.exists(imageDir):
        # print(f"Directory '{imageDir}' does not exist.")
        return None

    label_dir = os.path.join(imageDir, label)
    if not os.path.exists(label_dir):
        # print(f"Directory '{label_dir}' does not exist.")
        return None

    # Get list of all image files in the label directory
    image_files = []
    for root, dirs, files in os.walk(label_dir):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                image_files.append(os.path.join(root, file))

    # If no images found for the label
    if not image_files:
        # print(f"No images found for label '{label}' in directory '{imageDir}'.")
        return None

    # Select a random image file
    random_image = random.choice(image_files)
    return random_image

# Example usage:
label = ""
# label = 

imageDir = r"DeepFashion/In-shop_Clothes_Retrieval_Benchmark/Img/img/"
# random_image = get_random_image_by_label(label, imageDir)

# if random_image:
#     print(f"Random image for label '{label}': {random_image}")

if __name__ == "__main__":
    # ch = int(input("Enter test(1) or main(2): "))
    # if (ch == 1):
    ents = test()
    if ('FEMALE' in ents[1].label_):
        label += 'WOMEN/'
    else:
        label += 'MEN/'
    typeofoutfits = ['Sweatshirts_Hoodies' ,'Sweaters', 'Shorts' ,'Suiting','Shirts_Polos', 'Pants','Jackets_Vests','Denim', 'Tees_Tanks']
    for i in typeofoutfits:
        if (i.lower() in str(ents[0])):
            label += i
            break
    image = get_random_image_by_label(label, imageDir)
    if (image != None):
        image = image.replace(imageDir, "http://127.0.0.1:4000/")
    print(image, end='')
    # else:
    #     main()
