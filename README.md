# Pipeline for book translation/blending

## Introduction
This document details the automated pipeline created by (computational linguist fellows) Ethan Wilcox and Liam Geron during the winter and spring 2017. The pipeline is stored in a folder titled polli_blender on an EC2 instance which can be accessed via the address ubuntu@34.200.222.118. The following documentation assumes installation and operation on a linux server. For information about mac os installation, contact Ethan at wilcoxeg@gmail.com.

## Contents of /polli_blender/
- es.polli
- en.polli
- README.md
- setup.sh
- /giza-pp/
    * Makefile
    * /GIZA++-v2/
        * Makefile
        * Other files and folders...
    * Other files and folders...
- /mosesdecoder/
- /stanford-postagger/
- /python/
    * chunk_blender.py
    * va32pos.py
- /Blender_output/ (files should appear after running)
    * Aligned_pos_sents.p
    * Chunk_blender.p
    * source_tgt.A3
    * tgt_source.A3
    
## Overview
The pipeline takes in two side-by-side parallel corpuses in a source language (L1) and a target language (L2). For each sentence pair in the parallel corpus, it returns five blended sentences that combine the linguistic and grammatical features of L1 and L2 creating, in this instance, an imitation of the “spanglish” vernacular.

Running the setup.sh shell script with the following command triggers the pipeline:
- `sh setup.sh [L1 input file] [L2 input file] [number of sentences to be translated]`
- NB: Using “0” as the number of sentences to be translated forces the pipeline to create blends for the entire corpus.

For the rest of this document, I will describe each important file in the directory by the order in which it is used.

## en.polli / es.polli
These two files contain sentences separated by newlines, “en.polli” in English, “es.polli” in Spanish. Sentence (and line) n of en.polli corresponds to sentence n of es.polli -- thus, together, they conform to the side-by-side parallel corpus format that serves as the input to the polli pipeline. These two files are human-readable. For example:

![alt tag](/assets/en_es.png)

## setup.sh
A bash script that calls c++ executables, python scripts, and other files. The script (and thus the pipeline) is broken into four conceptual pieces, delineated by comments in the file itself:
- Tokenizing and preprocessing
- Alignment
- Part-of-Speech Tagging
- Blending

### Tokenization and Preprocessing
#### mosesdecoder
Can be downloaded from [this](https://github.com/moses-smt/mosesdecoder) github page. It is part of the moses statistical machine translation package. For the purposes of this pipeline, we don’t need to build any executables. Setup.sh merely calls a perl script that tokenizes the input files and stripts them of any uncessary punctuation. The used scripts can be found at /mosesdecoder/scripts/tokenizer/tokenizer.perl.

### Alignment
#### Giza-pp
Can be downloaded from [this](https://github.com/moses-smt/giza-pp) github page. This package requires a one modification before the makefile can be ran. You must navigate to: giza-pp/GIZA++-v2/Makefile. And change the line:
```
CFLAGS_OPT = $(CFLAGS) -O3 -funroll-loops -DNDEBUG
-DWORDINDEX_WITH_4_BYTE -DBINARY_SEARCH_FOR_TTABLE
-DWORDINDEX_WITH_4_BYTE
```
to...
```
CFLAGS_OPT = $(CFLAGS) -O3 -funroll-loops -DNDEBUG
-DWORDINDEX_WITH_4_BYTE
```
“Dbinary_search_for_ttable” is the problem here, although I don’t know why the “dwordindex_with_4_byte” is repeated -- it certainly doesn’t need to be. Once this is completed, you can navigate to the ./giza-pp directory and make the executables with the “make” command.

#### Giza-pp output
We run Giza++ twice, once from English → Spanish to create the English alignments and once from Spanish → English to create the Spanish alignments. The many files that this process produces are saved in the “output_source” directory and the “output_tgt” directory. The two relevant output files that contain alignment information (ending in .A3) are removed from these directories and placed in the “blender_output” directory. “Ouptut_source” and “output_tgt” are then deleted.

The .A3 output files contain alignments between the English and Spanish texts. For each entry line 1 specifies some metadata (including the probability of the alignment), line 2 specifies the target sentence and line 3 the source sentence with alignments. In the following Spanish sentence, Giza++ has determined that the Spanish word “día” corresponds to the second word in the English sentence, “day.”

![alt tag](/assets/parallel_sents.png)

### Part of Speech Tagging
#### va32pos.py
This file takes the two .A3 files provided by the Giza++ package. It combines the alignment information contained in these files and tags each word with a part-of-speech tag, using the stanford-postagger module. Results (aligned_pos_setns.p) are saved using the python pickle package to the /blender_output/ directory and conform to this standard:

![alt tag](/assets/full_aligned.png)

Where, for each tuple entry tuple[0] is the utf8 encoding of the word, tuple[1] is a list of all the aligned words, and tuple[2] is its part of speech tag. Note that the Spanish and English sentences have different part of speech tags. English conforms to the [Penn Treebank Standard](http://www.comp.leeds.ac.uk/amalgam/tagsets/upenn.html), whereas Spanish conforms to the [Simplified Eagles Standard](https://nlp.stanford.edu/software/spanish-faq.shtml#tagset).

### Blending
#### chunk_blender.py:
This python script takes the aligned, pos-tagged sentences and creates five blended sentences per L1/L2 sentence pair. It does this by “chunking” the sentences. If we think about the above sentence as a graph, with each word as a node and each alignment as a unidirectional edge, the chunking algorithm finds all of the closed subgraphs.

![alt tag](/assets/alligned.png)

In the above aligned sentence, the (non-Null) subgraphs include: (“greeted”, “le”, and “saludó”), (“Mei”, “Mei”). In order to create a blend between L1 and L2, we simply replace any contiguous component of a subgraph in L1 with its counterpart in L2. So “Mei greeted” becomes “Me le saludó” in this simple example.

Here’s another example, this one more complicated:

![alt tag](/assets/alligned2.png)

The final chunks include: (“Tiene que”, “Theres got to”), (“Haber una forma de ayudarlas saltar”, “be some way to help you bounce”), (“al”, “to the”), (“mismo”, “same”), (“ritmo”, “beat”), (“,”, “,”), (“Ceasar”, “Ceasar”), (“dijo”, “said”). The example highlights the need for contiguous wrapping, which forces the (“de”, “to”) chunk into the larger surrounding one.

If there are more than five closed loops, more than five blend combinations are possible, so some pruning is in order. The result looks something like this

![alt tag](/assets/blends.png)

The results are pickled into the “chunk_blender.p” file, where chunk_blender[n] is a list of sentences at blend level n (up to 5).

### Miscellaneous
#### Dependencies
The following packages must be installed for the pipeline to be operational:
- Python 3 (download and information [here](https://www.python.org/downloads/))
- NLTK (Natural Language Toolkit for python, installation information [here](http://www.nltk.org/install.html))
- NumPy (installation information [here](https://scipy.org/install.html))
- Java SDK with a gcc compiler (for running the Stanford POS tagger, found [here](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html))
- Pickle (usage information [here](https://wiki.python.org/moin/UsingPickle))
- Giza++ (covered above, found [here](https://github.com/moses-smt/giza-pp))
- Stanford POS Tagger (covered above, found [here](https://nlp.stanford.edu/software/tagger.shtml).) NB: Be sure to download the “full tagger version”, which includes models for Spanish and other languages. The package will download as “stanford-postagger-full-[release date], which must be renamed to simply “stanford-postagger” when integrated into the pipeline.
- Mosesdecoder (found [here](https://github.com/moses-smt/mosesdecoder))
