from argparse import ArgumentParser
from collections import namedtuple
from shutil import rmtree
import json
import nltk.tokenize as tok
import pathlib
import progressbar as pb

cite_span = namedtuple('cite_span', 'start end')

def convert_to_corpus(folder_in, folder_out):
    folder_in = pathlib.Path(folder_in)
    folder_out = pathlib.Path(folder_out)
    abstract_out = folder_out.joinpath('./abstract')
    body_out = folder_out.joinpath('./body')

    cleanup_structure(abstract_out)
    cleanup_structure(body_out)

    i = 1
    widgets = [ 'Converting File # ', pb.Counter(), ' ', pb.Timer(), ' ', pb.BouncingBar(marker = '.', left = '[', right = ']')]
    with pb.ProgressBar(widgets = widgets) as bar:
        for file_name in folder_in.iterdir():
            if file_name.is_file() and file_name.suffix.lower() == '.json':
                bar.update(i)
                i = i + 1

                file_in = file_name
                with file_in.open('r', encoding = 'utf-8') as file_in:
                    raw_data = json.load(file_in)
                
                abstract = extract_paragraphs(raw_data['abstract'])
                abstract = convert_to_sentences(abstract)
                body = extract_paragraphs(raw_data['body_text'])
                body = convert_to_sentences(body)

                if len(abstract) == 0 or len(body) == 0:
                    print(f'file {file_name.stem} is not a full text article')
                else:
                    write_corpus(abstract_out.joinpath(f'./{file_name.stem}.txt'), abstract)
                    write_corpus(body_out.joinpath(f'./{file_name.stem}.txt'), body)

def cleanup_structure(folder):
    if folder.exists():
        if folder.is_dir():
            rmtree(folder)
        else:
            folder.unlink()
    folder.mkdir(parents = True)

def extract_paragraphs(paragraphs):
    result = [clean_paragraph(paragraph) for paragraph in paragraphs]
    return result

def clean_paragraph(paragraph):
    text = paragraph['text']
    cite_spans = paragraph['cite_spans']
    cite_spans = [cite_span(x['start'], x['end']) for x in cite_spans]
    for x in sorted(cite_spans, key = lambda x: x.end, reverse = True):
        text = text[0: x.start:] + text[x.end + 1::]
    return text

def convert_to_sentences(paragraphs):
    result = [tok.sent_tokenize(paragraph) for paragraph in paragraphs]
    return result

def write_corpus(file_out, paragraphs):
    first = True
    with file_out.open('w', encoding = 'utf-8') as file_out:
        for paragraph in paragraphs:
            if first:
                first = False
            else:
                file_out.write('\n')
            for sentence in paragraph:
                file_out.write(sentence)
                file_out.write('\n')                

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-in', '--folder-in', help = 'Folder containing the raw JSON files', required = True)
    parser.add_argument('-out', '--folder-out', help = 'Folder containing the newly created text corpus', required = True)
    args = parser.parse_args()
    print(f'folder in: {args.folder_in}')
    print(f'folder out: {args.measure_out}')
    convert_to_corpus(args.folder_in, args.folder_out)
