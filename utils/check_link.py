import re

def checkLink(link):
    is_check = True
    item = re.search(r'chegg.com/homework-help/questions-and-answers/(.*?)', link)
    if not item:
        is_check = False

    return is_check