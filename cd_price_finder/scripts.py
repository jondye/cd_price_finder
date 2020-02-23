import cd_price_finder
import argparse

def cdpf_test():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', action='store', required=True)
    parser.add_argument('-p', '--password', action='store', required=True)
    args = parser.parse_args()

    websites = [
#        cd_price_finder.MusicMagpie(),
#        cd_price_finder.Ziffit(),
        cd_price_finder.WeBuyBooks(),
    ]

    for website in websites:
        website.login(args.username, args.password)

    barcodes = cd_price_finder.load_barcodes_from_csv('barcodes.csv')

    best = []

    for b in barcodes[:3]:
        best_price = 0.0
        best_website = -1
        for idx, website in enumerate(websites):
            website.add_barcode(b)
            r = website.results()
            for barcode, name, price in reversed(r):
                if barcode == b:
                    if price > best_price:
                        websites[best_website].remove_barcode(b)
                        best_price = price
                        best_website = idx
                    else:
                        website.remove_barcode(b)
        best.append((b, websites[best_website], best_price))

    print(best)

    for website in websites:
        website.save_order()
