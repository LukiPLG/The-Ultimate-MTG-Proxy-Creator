import json, os, time



def deckList(addBack, addTransforms, deckname, cards_per_page, cards):
    if addTransforms == True:
        with open("MTG-Card-Data.jsonl", "r", encoding="utf-8") as data:
            for line in data:
                content = json.loads(line)
                for i in range(len(cards)):
                    if content["title"] == cards[i][1]:
                        cards[i].append(content["transform"])

    deckname = "decks/" + deckname + ".txt"
    with open(deckname, "w", encoding="utf-8") as deck:
        if addBack == False and addTransforms == False:
            for card in cards:
                for i in range(card[0]):
                    output = f"1 {card[1]}\n"
                    deck.write(output)


        elif addBack == True and addTransforms == False:
            counter = 0
            for count, title, index in cards:
                while counter + count > cards_per_page:
                    cards_on_current_page = cards_per_page - counter

                    for i in range(cards_on_current_page):
                        output = f"1 {title} {index}\n"
                        deck.write(output)

                    for i in range(cards_per_page):
                        output = f"1 Back 0\n"
                        deck.write(output)

                    count = count - cards_on_current_page
                    counter = 0

                for i in range(count):
                    output = f"1 {title} {index}\n"
                    deck.write(output)
                counter = counter + count

            for i in range(9 - counter):
                output = f"1 Blank 0\n"
                deck.write(output)

            for i in range(counter):
                output = f"1 Back 0\n"
                deck.write(output)


        elif addBack == False and addTransforms == True:
            for card in cards:
                for i in range(card[0]):
                    output = f"1 {card[1]} {card[2]}\n"
                    deck.write(output)
                if card[3] != None:
                    for i in range(card[0]):
                        output = f"1 {card[1]} {card[2]}\n"
                        deck.write(output)


        elif addBack == True and addTransforms == True:
            backList = ["Back"] * cards_per_page

            counter = 0
            for card in cards:
                while counter + card[0] > cards_per_page:
                    cards_on_current_page = cards_per_page - counter

                    for i in range(cards_on_current_page):
                        output = f"1 {card[1]} {card[2]}\n"
                        deck.write(output)

                    if card[3] != None:
                        for i in range(counter, counter + cards_on_current_page):
                            backList[i] = card[3]

                    for back in backList:
                        output = f"1 {back} 0\n"
                        deck.write(output)
                    backList = ["Back"] * cards_per_page

                    card[0] = card[0] - cards_on_current_page
                    counter = 0

                for i in range(card[0]):
                    output = f"1 {card[1]} {card[2]}\n"
                    deck.write(output)

                if card[3] != None:
                    for i in range(counter, counter + card[0]):
                        backList[i] = card[3]

                counter = counter + card[0]

            for i in range(9 - counter):
                output = f"1 Blank 0\n"
                deck.write(output)

            for i in range(counter):
                output = f"1 {backList[i]} {card[2]}\n"
                deck.write(output)




def dataPreparation(addBack, addTransforms, deckname, cards_per_page):
    if os.path.exists("toMerge/") == False:
        os.mkdir("toMerge")
        print("No files found in 'toMerge' folder...")
        quit()

    if os.path.exists("decks/") == False:
        os.mkdir("decks")

    inputList = []
    for file in os.listdir("toMerge"):
        with open("toMerge/" + file, "r", encoding="utf-8") as batch:
            for line in batch:
                splited = line.strip().split(" ")
                count = int(splited[0])
                try:
                    index = int(splited[-1])
                    str_len = len(splited) - 1
                except:
                    index = 0
                    str_len = len(splited)

                title = ""
                for i in range(1, str_len - 1):
                    title = title + splited[i] + " "
                title = title + splited[str_len - 1]

                inputList.append([count, title, index])

    deckList(addBack, addTransforms, deckname, cards_per_page, inputList)



if __name__ == "__main__":
    startTime = time.time()
    dataPreparation(True, True, "CustomDeckDoPrintu", 9)
    endTime = time.time()

    print("Time taken: ", round(endTime - startTime, 2))


