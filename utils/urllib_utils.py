import os
import re
import urllib
import urllib.request

from locations import DESKTOP

HTTPS = "https:"


# ------------------- CLASSES -------------------

class UrlReq(object):
    DEFAULT_HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux i686)"}

    def __init__(self, url, header=None):
        self._header = header if header else self.DEFAULT_HEADER
        self._url = url
        self._data = ""
        self._res = None
        self.get_request()
        self.get_res()
        self.get_data()

    def get_request(self):
        self._req = urllib.request.Request(self._url, headers=self._header)

    def get_res(self):
        try:
            self._res = urllib.request.urlopen(self._req)
        except urllib.error.URLError as e:
            print(e.reason)

    def get_data(self):

        if not self._data and self._res:
            self._data = self._res.read()
        return self._data

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value


class UrlParser(UrlReq):

    def __init__(self, url, header=None):

        super().__init__(url, header)

    def get_images(self):

        url_images = []

        parsed_imgs = re.findall(r"<img(.*)?>", self.get_data().decode())

        for img in parsed_imgs:
            src = ""
            width = 0
            height = 0

            src_search = re.search(r"src=\"([^\"]*)\"", img)
            if src_search:
                src = src_search.group(1)

            width_search = re.search(r"width.(\d+)px", img)
            if width_search:
                width = width_search.group(1)

            height_search = re.search(r"height.(\d+)px", img)
            if height_search:
                height = height_search.group(1)

            url_images.append(UrlImg(src, width, height))

        return url_images

    def get_hrefs(self, urlreq_filter=True):
        hrefs = []
        found_hrefs = re.findall(r"href=\"([^\"]*)\"", self.get_data().decode())

        if urlreq_filter:
            for href in found_hrefs:
                try:
                    UrlReq(href)
                    hrefs.append(href)
                except ValueError:
                    continue
        else:
            for href in found_hrefs:
                if re.search(HTTPS, href) or re.search("www.", href):
                    hrefs.append(href)

        return hrefs

    def get_paragraphs(self):

        paragraphs = re.findall(r"<p>((?!(</p>)).{1,})", self.get_data().decode())
        cleaned_up = []
        for para in paragraphs:
            para = str(para).replace("\\", "")

            # Start Clean
            start_para = re.split("<", para)[0]

            # Middle Clean
            middle_para = re.findall(r">[^<]*<", para)
            middle_cleanup = []
            for m_p in middle_para:
                mp = m_p[1:-1]
                middle_cleanup.append(mp)

            # End Clean
            end_para = re.split(">", para)[-1]
            if end_para != start_para:
                end_para = end_para[0:-6]
            else:
                start_para = start_para[0:-6]
                end_para = ""

            # Joining
            all_para = [start_para[2:]]
            all_para.extend(middle_cleanup)
            all_para.append(end_para)

            # Joined Clean
            joined_para = "".join(all_para).strip()
            joined_para = "".join(re.split("\[\d+]", joined_para))
            joined_para = re.sub(r"&#\d+;", "", joined_para)
            cleaned_up.append(joined_para)

        return cleaned_up

    def get_titles(self):
        pass


class UrlPage(UrlParser):

    def __init__(self, url, header=None):
        super().__init__(url, header)
        self._images = []
        self._hrefs = []
        self._paragraphs = []
        self._titles = []

    @property
    def images(self):
        if not self._images:
            self._images = self.get_images()
        return self._images

    @property
    def hrefs(self):
        if not self._hrefs:
            self._hrefs = self.get_hrefs()
        return self._hrefs

    @property
    def paragraphs(self):
        if not self._paragraphs:
            self._paragraphs = self.get_paragraphs()
        return self._paragraphs

    @property
    def titles(self):
        if not self._titles:
            self._titles = self.get_titles()
        return self._titles


# ---

class UrlImg(object):

    def __init__(self, src, width=0, height=0):
        self._src = src
        self._width = width
        self._height = height

    @property
    def src(self):
        return self._src

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._src


# ------------------- FUNCTIONS -------------------

def copy_images_from_url(url, destination):
    """
    Copy all images from given url into destination

    :param str url: given url
    :param str destination:
    :return:
    """

    output_images = []

    url_page = UrlPage(url)

    for url_image in url_page.images:
        try:
            path = url_image.src
            if HTTPS not in path:
                path = HTTPS + path
            resource = urllib.request.urlopen(path)
            output = open(os.path.join(destination, os.path.basename(path)), "wb")
            output_images.append(output)
            output.write(resource.read())
            output.close()

        except Exception as e:
            print(e)

    return output_images
