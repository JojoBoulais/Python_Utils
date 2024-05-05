from urllib_utils import UrlPage

url = "https://fr.wikipedia.org/wiki/Ollantaytambo#:~:text=Ollantaytambo%20est%20une%20forteresse%20inca,apr%C3%A8s%20la%20chute%20de%20Cuzco."
# url = "https://stackoverflow.com/questions/13532531/python-stats-how-do-i-write-it-to-a-human-readable-file"
# url = "file:///C:/Users/Jordan/Desktop/Web_1_Projet_Final-main/Web_1_Projet_Final-main/accueil.html"
# url = "https://www.ncbi.nlm.nih.gov/books/NBK559166/"

url_page = UrlPage(url)

for para in url_page.get_paragraphs():
    print(para)
