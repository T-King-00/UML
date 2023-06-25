import helperFunctions



if __name__ == '__main__':

    sentence="A user is identified with name , email and password,age,gender ."

    #helperFunctions.displayRender(sentence)
    sent=helperFunctions.nlp(sentence)
    for word in sent:
        print(word.text,"  : "  , word.pos_,word.dep_, word.is_stop,"  :  " ,word.tag_,word.ent_type_)

