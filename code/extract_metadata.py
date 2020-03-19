from argparse import ArgumentParser
from collections import namedtuple
import csv
import json
import pathlib
import progressbar as pb

article = namedtuple('article', 'id references authors figures tables fullText title')

def extract_metadata(folder_in, file_out):
    folder_in = pathlib.Path(folder_in)
    file_out = pathlib.Path(file_out)
    ensure_path(file_out)
    i = 1
    widgets = [ 'Extracting File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        with file_out.open('w', encoding = 'utf-8', newline='') as file_out:
            writer = csv.writer(file_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            writer.writerow(['id', 'referenceCount', 'authorCount', 'figureCount', 'tableCount', 'isFullText', 'title'])
            for file_name in folder_in.iterdir():
                if file_name.is_file() and file_name.suffix.lower() == '.json':
                    bar.update(i)
                    i = i + 1
                    article = parse_json_to_article(file_name)
                    writer.writerow([article.id, article.references, article.authors, article.figures, article.tables, article.fullText, article.title])
                    
def ensure_path(file_out):
    file_out.parent.mkdir(parents = True, exist_ok = True)
    if file_out.exists():
         file_out.unlink()

def parse_json_to_article(file_name):
    file_in = file_name
    with file_in.open('r', encoding = 'utf-8') as file_in:
        raw_data = json.load(file_in)
    id = raw_data['paper_id']
    references = dict_count(raw_data['bib_entries'], 'BIBREF')
    authors = len(raw_data['metadata']['authors'])
    figures = dict_count(raw_data['ref_entries'], 'FIGREF')
    tables = dict_count(raw_data['ref_entries'], 'TABREF')
    fullText = len(raw_data['abstract']) > 0 and len(raw_data['body_text']) > 0
    title = raw_data['metadata']['title']    
    return article(id, references, authors, figures, tables, fullText, title)

def dict_count(dictionary, prefix):
    res = [x for x in dictionary.keys() if x.startswith(prefix)]
    return len(res)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--folder-in', help = 'Folder containing the raw JSON files', required = True)
    parser.add_argument('-out', '--file-out', help = 'File to contain the metadata', required = True)
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'file out: {args.file_out}')
    extract_metadata(args.folder_in, args.file_out)
