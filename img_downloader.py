import time, threading, json, requests, os, re



def download_img(start, end, step, data):
    startTime = time.time()
    session = requests.Session()

    for i in range(start, end, step):
        card = json.loads(data[i])
        title = re.sub(r'[<>:"/\\|?*]', '_', card["title"])

        if f"imgs/{title}_{j}.png" in os.listdir("imgs"):
            duplicat = True
        else:
            duplicat = False

        for j in range(len(card["images"])):
            if duplicat == False:
                filename = f"imgs/{title}_{j}.png"
            else:
                counter = 1
                while f"imgs/{title}_{j}.png" in os.listdir("imgs"):
                    filename = f"imgs/{title}{counter}_{j}.png"
                    counter = counter + 1

            url = card["images"][j]

            img_data = session.get(url, timeout=10)
            img_data.raise_for_status()

            with open(filename, "wb") as img:
                img.write(img_data.content)
                img.close()

    endTime = time.time()
    print(f"Thread {start + 1} took {endTime-startTime}s")



if __name__ == "__main__":
    THREADS = 24
    threads = []

    startTime = time.time()

    if os.path.exists("imgs/") == False:
        os.mkdir("imgs")

    print("Loading file...")
    with open("MTG-Card-Data.jsonl", "r", encoding="utf-8") as file:
        lines = file.readlines()
        cards_count = len(lines)

    print(f"Initializing code on {THREADS} threads...")
    for i in range(THREADS):
        print(f"Thread {i + 1} downloading images")
        t = threading.Thread(target=download_img, args=(i, cards_count, THREADS, lines))
        t.start()
        threads.append(t)

    print("\n")
    for t in threads:
        t.join()

    endTime = time.time()
    print(f"Downloading images took {round(endTime - startTime, 2)}s")