# input = [file1, file2, ...]
# res = {filename: [world1, word2]}

import re
import math

from tqdm import tqdm


class BuildIndex:

    def __init__(self, files, verbose=False):
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.filenames = files
        self.verbose = verbose
        if self.verbose:
            print('Dang phan tich noi dung tin dang...')
        self.file_to_terms = self.process_files()
        self.regdex = self.regIndex()
        self.totalIndex = self.execute()
        self.vectors = self.vectorize()
        self.mags = self.magnitudes(self.filenames[:, 0])
        self.populateScores()

    def process_files(self):
        file_to_terms = {}
        ls = tqdm(range(len(self.filenames))) if self.verbose else range(
            len(self.filenames))
        for i in ls:  # tqdm(range(len(self.filenames))):
            file = self.filenames[i]
        # for file in self.filenames:
            # stopwords = open('stopwords.txt').read().close()
            pattern = re.compile('[\W_]+')
            file_to_terms[file[0]] = file[1].lower()
            file_to_terms[file[0]] = pattern.sub(' ', file_to_terms[file[0]])
            re.sub(r'[\W_]+', '', file_to_terms[file[0]])
            file_to_terms[file[0]] = file_to_terms[file[0]].split()
            # file_to_terms[file] = [w for w in file_to_terms[file] if w not in stopwords]
            # file_to_terms[file] = [stemmer.stem_word(w) for w in file_to_terms[file]]

        # print('\n')
        return file_to_terms

    # input = [word1, word2, ...]
    # output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
    def index_one_file(self, termlist):
        fileIndex = {}
        for index, word in enumerate(termlist):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
        return fileIndex

    # input = {filename: [word1, word2, ...], ...}
    # res = {filename: {word: [pos1, pos2, ...]}, ...}
    def make_indices(self, termlists):
        total = {}
        # print('Đang tạo chỉ mục tin đăng...\n')
        keys = list(termlists.keys())

        ls = tqdm(range(len(keys))) if self.verbose else range(len(keys))

        for i in ls:  # tqdm(range(len(keys))):
            filename = keys[i]
        # for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])

        # print('\n')
        return total

    # input = {filename: {word: [pos1, pos2, ...], ... }}
    # res = {word: {filename: [pos1, pos2]}, ...}, ...}
    def fullIndex(self):
        total_index = {}
        indie_indices = self.regdex
        keys = list(indie_indices.keys())

        if self.verbose:
            print('\nDang tao chi muc tin dang...')
        ls = tqdm(range(len(keys))) if self.verbose else range(len(keys))

        for i in ls:  # tqdm(range(len(keys))):
            filename = keys[i]
        # for filename in indie_indices.keys():
            self.tf[filename] = {}
            for word in indie_indices[filename].keys():
                self.tf[filename][word] = len(indie_indices[filename][word])
                if word in self.df.keys():
                    self.df[word] += 1
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(
                            indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {
                        filename: indie_indices[filename][word]}
        return total_index

    def vectorize(self):
        vectors = {}
        if self.verbose:
            print('\nDang vector hoa tin dang...')

        ls = tqdm(range(len(self.filenames))
                  ) if self.verbose else range(len(self.filenames))

        for i in ls:  # tqdm(range(len(self.filenames))):
            filename = self.filenames[i]
        # for filename in self.filenames:
            vectors[filename[0]] = [len(self.regdex[filename[0]][word])
                                    for word in self.regdex[filename[0]].keys()]
        return vectors

    def document_frequency(self, term):
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys())
        else:
            return 0

    def collection_size(self):
        return len(self.filenames)

    def magnitudes(self, documents):
        mags = {}
        if self.verbose:
            print('\nDang tinh toan do dai vector tin dang...')

        ls = tqdm(range(len(documents))
                  ) if self.verbose else range(len(documents))

        for i in ls:  # tqdm(range(len(documents))):
            document = documents[i]
        # for document in documents:
            mags[document] = pow(
                sum(map(lambda x: x**2, self.vectors[document])), .5)
        return mags

    def term_frequency(self, term, document):
        return self.tf[document][term] / self.mags[document] if term in self.tf[document].keys() else 0

    # pretty sure that this is wrong and makes little sense.
    def populateScores(self):
        if self.verbose:
            print('\nDang tinh toan diem tf*idf cho tin dang...')
        files = self.filenames[:, 0]

        ls = tqdm(range(len(files))) if self.verbose else range(len(files))

        for i in ls:  # tqdm(range(len(files))):
            filename = files[i]
        # for filename in self.filenames[:, 0]:
            for term in self.getUniques():
                self.tf[filename][term] = self.term_frequency(term, filename)
                if term in self.df.keys():
                    self.idf[term] = self.idf_func(
                        self.collection_size(), self.df[term])
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    def idf_func(self, N, N_t):
        if N_t != 0:
            return math.log(N / N_t)
        else:
            return 0

    def generateScore(self, term, document):
        return self.tf[document][term] * self.idf[term]

    def execute(self):
        return self.fullIndex()

    def regIndex(self):
        return self.make_indices(self.file_to_terms)

    def getUniques(self):
        return self.totalIndex.keys()
