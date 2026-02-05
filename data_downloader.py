from bs4 import BeautifulSoup
import requests, time, math, threading, json, os



def parse_card(card):
    cards = []

    front_img = card.select_one(".card-image-front img")
    back_img = card.select_one(".card-image-back img")

    front_image = front_img["src"] if front_img else None
    back_image = back_img["src"] if back_img else None

    titles = card.select(".card-text-card-name")
    types = card.select(".card-text-type-line")
    oracle_blocks = card.select(".card-text-oracle")
    flavor_blocks = card.select(".card-text-flavor")
    stats_blocks = card.select(".card-text-stats")

    mana = card.select(".card-text-mana-cost abbr")
    mana_cost = "".join(m.get_text() for m in mana) if mana else None

    front_card = {
        "title": titles[0].get_text(strip=True) if titles else None,
        "cost": mana_cost,
        "type": types[0].get_text(strip=True) if len(types) > 0 else None,
        "oracle_text": ("\n".join(p.get_text(" ", strip=True) for p in oracle_blocks[0].select("p")) if len(oracle_blocks) > 0 else None),
        "flavor_text": ("\n".join(p.get_text(" ", strip=True) for p in flavor_blocks[0].select("p")) if len(flavor_blocks) > 1 else None),
        "statistics": stats_blocks[0].get_text(strip=True) if len(stats_blocks) > 0 else None,
        "side": "front",
        "transform": None,
        "_image": front_image
    }
    cards.append(front_card)

    if len(titles) > 1:
        front_card["transform"] = titles[1].get_text(strip=True)

        back_card = {
            "title": titles[1].get_text(strip=True),
            "cost": None,
            "type": types[1].get_text(strip=True) if len(types) > 1 else None,
            "oracle_text": ("\n".join(p.get_text(" ", strip=True) for p in oracle_blocks[1].select("p")) if len(oracle_blocks) > 1 else None),
            "flavor_text": ("\n".join(p.get_text(" ", strip=True)for p in flavor_blocks[1 if len(flavor_blocks) > 1 else 0].select("p")) if len(flavor_blocks) > 0 else None),
            "statistics": stats_blocks[1].get_text(strip=True) if len(stats_blocks) > 1 else None,
            "side": "back",
            "transform": titles[0].get_text(strip=True),
            "_image": back_image
        }
        cards.append(back_card)

    return cards



def scrape(id, start, end):
    filename = f"{id}_temp.jsonl"
    cards_map = {}

    startTime = time.time()

    for i in range(start, end):
        url = f"https://scryfall.com/search?as=full&order=name&page={i+1}&q=%28game%3Apaper%29+include%3Aextras+unique%3Aprints+prefer%3Abest&unique=cards"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        for card in soup.find_all(class_="card-profile"):
            parsed_cards = parse_card(card)

            for c in parsed_cards:
                key = (c["title"], c["side"])
                img = c.pop("_image")

                if key not in cards_map:
                    c["images"] = []
                    cards_map[key] = c

                if img and img not in cards_map[key]["images"]:
                    cards_map[key]["images"].append(img)

    with open(filename, "w", encoding="utf-8") as file:
        for card in cards_map.values():
            file.write(json.dumps(card, ensure_ascii=False) + "\n")

    endTime = time.time()
    print(f"Thread {id + 1} took {endTime-startTime}s")



def merger(files_count):
    outfile = "MTG-Card-Data.jsonl"

    print(f"Merging {files_count} temporary files...")
    with open(outfile, "w", encoding="utf-8") as file:
        for i in range(files_count):
            filename = f"{i}_temp.jsonl"

            with open(filename, "r", encoding="utf-8") as temp:
                for line in temp:
                    file.write(line)
            os.remove(filename)

    print(f"Merging is complete!")



if __name__ == "__main__":
    THREADS = 24
    cards_number = 102639
    cards_per_page = 20

    print(f"Initializing code on {THREADS} threads...")
    startTime = time.time()

    pages = math.ceil(cards_number / cards_per_page)
    pages_per_threat = math.ceil(pages / THREADS)

    print(f"Scraping {cards_number} cards on {pages} pages...")

    threads = []
    for i in range(THREADS):
        start = pages_per_threat * i
        end = min(pages, pages_per_threat * (i + 1))

        if (start > end):
            continue

        print(f"Thread {i + 1} scraping pages from {start} to {end}")
        t = threading.Thread(target=scrape, args=(i, start, end))
        t.start()
        threads.append(t)

    print("\n")
    for t in threads:
        t.join()

    merger(THREADS)



    endTime = time.time()
    print(f"Code took {round(endTime - startTime, 2)}s")