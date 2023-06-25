import helperFunctions



if __name__ == '__main__':

    sentence="Details about user are name , email , password and age,gender .Details about user should be stored in database."


    #helperFunctions.displayRender(sentence)
    sent=helperFunctions.nlp(sentence)
    for word in sent:
        print(word.text,"  : "  , word.pos_,word.dep_, word.is_stop,"  :  " ,word.tag_,word.ent_type_)

