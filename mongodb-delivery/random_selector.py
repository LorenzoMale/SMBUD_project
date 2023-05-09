import random
from settings import settings
import uuid

class RandomDocBodyGenerator:
    def __init__(self, path=settings["main_txt_file"], sep=".",\
        languages_file=settings["languages_file"],\
        universities_file=settings["universities_file"],\
        min_chap= settings["min_chapters"], max_chap=settings["max_chapters"],\
        min_sections=settings["min_sections"], max_sections=settings["max_sections"],\
        min_paragraphs=settings["min_paragraphs"], max_paragraphs=settings["max_paragraphs"],\
        min_sentences=settings["min_sentences"], max_sentences=settings["max_sentences"],\
        min_citations=settings["min_citations"], max_citations=settings["max_citations"],\
        min_figures=settings["min_figures"], max_figures=settings["max_figures"],\
        min_keywords=settings["min_keywords"], max_keywords=settings["max_keywords"],\
        text_prob=settings["text_to_other_prob"],\
        lang_prob = settings["has_language_prob"]) -> None:

        with open(path, "r") as f, open(languages_file, "r") as f1, open(universities_file, "r") as f2:
            self.sentences = tuple(line for line in f.read().split(sep))
            self.langs = tuple(line for line in f1.read().split("\n"))
            self.universities = tuple(line for line in f2.read().split("\n"))

        self.min_chap = min_chap
        self.max_chap = max_chap

        self.min_paragraphs = min_paragraphs
        self.max_paragraphs = max_paragraphs

        self.min_sections = min_sections
        self.max_sections = max_sections

        self.min_sentences = min_sentences
        self.max_sentences = max_sentences

        self.min_citations = min_citations
        self.max_citations = max_citations

        self.min_figures = min_figures
        self.max_figures = max_figures

        self.min_keywords = min_keywords
        self.max_keywords = max_keywords

        self.text_prob = text_prob
        self.lang_prob = lang_prob

    def generate_random_document_body(self):
        chapters_num = random.randint(self.min_chap, self.max_chap)
        chapters = []
        for _ in range(chapters_num):
            chapters.append(self.create_chapter())
        return chapters

    def create_chapter(self):
        sections_num = random.randint(self.min_sections, self.max_sections)
        sections = []
        for _ in range(sections_num):
            sections.append(self.create_section())
        return {"chapter" : {"title" : self.get_random_sentence(), "sections" : sections}}

    def create_section(self):
        paragraphs_num = random.randint(self.min_paragraphs, self.max_paragraphs)
        paragraphs =  []
        for _ in range(paragraphs_num):
            paragraphs.append(self.create_paragraph())    
        figures_num = random.randint(self.min_figures, self.max_figures)
        figures = []
        for _ in range(figures_num):
            figures.append(self.create_figure())
        return {"section" : {"title" : self.get_random_sentence(), "paragraphs": paragraphs, "figures": figures}}

    def create_paragraph(self):
        return self.create_text()

    def create_text(self):
        text = "".join(random.sample(self.sentences, random.randint(self.min_sentences, self.max_sentences)))
        return {"text":text}

    def get_random_sentence(self):
        return random.choice(self.sentences)

    def generate_random_text(self):
        return "".join(random.sample(self.sentences, random.randint(self.min_sentences, self.max_sentences)))

    def get_random_paper_citations(self, data):
        citations = [] # list of titles of cited papers
        n_citations = random.randint(self.min_citations, self.max_citations)
        n_papers = len(data) - 1
        for _ in range(n_citations):
            cited = random.randint(0, n_papers)
            citations.append(data[cited]["title"])
        return citations

    def create_figure(self):
        figure = {}
        random_url = f"https://{uuid.uuid4().hex}.com/{uuid.uuid4().hex}.jpg"
        caption = self.get_random_sentence()
        figure["url"] = random_url
        figure["caption"] = caption
        return figure

    def generate_random_keywords(self):
        keywords = self.get_random_sentence()[1:].split(" ")
        return keywords   

    def get_keywords(self, keywords):
        k = []
        n_keywords = random.randint(self.min_keywords, self.max_keywords)
        for _ in range(n_keywords):
            random_i = random.randint(0, len(keywords) - 1)
            k.append(keywords[random_i])
        return k

    def get_affiliation(self):
        return random.choice(self.universities)

    def get_lang(self):
        have_lang = random.uniform(0,1) <= self.lang_prob
        if not have_lang:
            raise Exception
        else:
            return random.choice(self.langs)