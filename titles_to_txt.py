import json



def titlesToTxt():
    with open("MTG-Card-Data.jsonl", "r", encoding="utf-8") as source:
        lines = source.readlines()


    titles = []
    with open("card_titles.txt", "w", encoding="utf-8") as file:
        for line in lines:
            content = json.loads(line)

            title = content["title"]
            titles.append(title)
            file.write(title + "\n")

    return titles


if __name__ == "__main__":
    titles = titlesToTxt()
    for title in titles:
        print(title)