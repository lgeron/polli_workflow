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
