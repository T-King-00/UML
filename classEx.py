import helperFunctions


deps_attr = ["pobj", "dobj", "conj"]
deps_class = ["nsubj", "nsubjpass", "conj", "attr"]


def preprocess_text(text):
    if not text.endswith("."): text += "."
    doc = helperFunctions.nlp(text)
    for token in doc:
        # check for compound words
        if token.dep_ == "compound":
            text = text.replace(token.text + " " + token.head.text, token.text + "_" + token.head.text)
        # check for gerund followed by a noun
        if token.pos_ == "VERB" and token.tag_ == "VBG" and token.head.pos_ == "NOUN":
            text = text.replace(token.text + " " + token.head.text, token.text + "_" + token.head.text)
        # check if a noun is followed by a gerund
        if token.pos_ == "NOUN" and token.head.pos_ == "VERB" and token.head.tag_ == "VBG":
            text = text.replace(token.head.text + " " + token.text, token.head.text + "_" + token.text)
        # check for adjectives followed by a noun
        if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
            text = text.replace(token.text + " " + token.head.text, token.text + "_" + token.head.text)
    return text

def discard_attr_from_classes(classes_attr, attribute):
    for cls in classes_attr.keys():
        if attribute in classes_attr[cls]:
            classes_attr[cls].discard(attribute)
    return classes_attr
def add_to_classes(classes_attr, sent, token):
    if token not in classes_attr.keys():
        classes_attr[token] = set()
    else:
        classes_attr[token].add(token)
    classes_attr = discard_attr_from_classes(classes_attr, token)
    return classes_attr

def add_to_attributes(classes_attr, sent, token):
    if token not in classes_attr.keys():
        try:
            classes_attr[list(sent.root.children)[0].lemma_].add(token)
        except KeyError:
            pass
    return classes_attr
def get_classes_attributes(text):
    classes_attr = {}
    doc = helperFunctions.nlp(text)
    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "NOUN":
                # attribute
                if token.dep_ in deps_attr:
                    classes_attr = add_to_attributes(classes_attr, sent, token.lemma_)
                # class
                elif token.dep_ in deps_class:
                    classes_attr = add_to_classes(classes_attr, sent, token.lemma_)
    return classes_attr
