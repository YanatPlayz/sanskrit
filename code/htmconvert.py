import re
from bs4 import BeautifulSoup

with open("../data/epics/MBH1-18U.HTM", encoding="utf-8") as f: #mahabharata initial htm file
    soup = BeautifulSoup(f, "html.parser")

text = soup.get_text(separator="\n") #parse text from htm file

text = re.sub(r'[\r\n]+', '\n', text) #cut multiple nL to single nL
text = text.strip() #remove leading/trailing whitespace

with open("../data/epics/MBH1-18U.txt", "w", encoding="utf-8") as out: #mahabharata final txt file
    out.write(text)