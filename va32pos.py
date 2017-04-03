from sys import argv
import pickle
import re
from itertools import islice
from nltk.tag.stanford import StanfordPOSTagger

"""
This class takes three arguments:
	(1) .VA3 file from GIZA++ output for sentence allignments from l1 --> l2
	(2) .VA3 file from GIZA++ output for sentence allignements from l2 --> l1
	(3) An integer specifying how many sentences the user wishes to pos tag

It produces:
	- A pickled file containing a list, with the following format:
		[(L1 word, [list of l2 word allignments], L1 POS tag),
		(L2 word, [list of L2 word allignments], L2 POS tag)]

Assumptions:
	- the Stanford POS Tagger has been downloaded, its folder named to 'stanford-postagger'
	- The Stanford POS Tagger folder has been placed in the same directory as this script
	- The two .VA3 files are outputs from GIZA++ v.2
"""

class Va3ToPos:

	def __init__(self):

		# Specify paths to Stanford taggers
		english_modelfile = './stanford-postagger/models/english-bidirectional-distsim.tagger'
		spanish_modelfile = './stanford-postagger/models/spanish-distsim.tagger'
		jarfile = './stanford-postagger/stanford-postagger-3.7.0.jar'

		# Initialize taggers
		self.en_tagger = StanfordPOSTagger(model_filename=english_modelfile, path_to_jar=jarfile)
		self.es_tagger = StanfordPOSTagger(model_filename=spanish_modelfile, path_to_jar=jarfile)

		# Store the string literals from the VA3 files
		self.va3l1 = []
		self.va3l2 = []

		# Store tokenized plaintext sentences
		self.l1_tok_sent = []
		self.l2_tok_sent = []

		# Store the alignments as lists of lists of ints
		self.l1_alignments = []
		self.l2_alignments = []

		# Stor the POS tags as lists of strings
		self.l1_pos_tags = []
		self.l2_pos_tags = []

	def read_va3(self, l1filename, l2filename):

		# VA3 file is structured in lines of 3, the 3rd line being the allignment
		with open(l1filename) as f:
			while True:
				next_3 = list(islice(f, 3))
				if not next_3:
					break
				self.va3l1.append(next_3[2].strip())

		with open(l2filename) as f:
			while True:
				next_3 = list(islice(f, 3))
				if not next_3:
					break
				self.va3l2.append(next_3[2].strip())

	def read_alignments(self):

		# Extracts the list of allignments from plaintext. Stores them as list of ints.
		for sent in self.va3l1:
			align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', sent)
			self.l1_tok_sent.append([elem[0].strip() for elem in align_toks])
			self.l1_alignments.append(([elem[1].split() for elem in align_toks]))

		for sent in self.va3l2:
			align_toks = re.findall(r'(.*?) \(\{([\d ]+)\}\)', sent)
			self.l2_tok_sent.append([elem[0].strip() for elem in align_toks])
			self.l2_alignments.append(([elem[1].split() for elem in align_toks]))

	def pos_tag(self, num_iters):
		# Prints to let users know how fast we're tagging (probably pretty slowly!)
		print("====================================")
		print("Part of Speech Tagging " + str(num_iters) + " Sentences...")
		print("====================================")
		for i in range(int(num_iters)):

			print(str(i + 1) + " / " + str(num_iters))

			l1_sent = self.l1_tok_sent[i]
			self.l1_pos_tags.append([elem[1] for elem in self.en_tagger.tag(l1_sent)])

			l2_sent = self.l2_tok_sent[i]
			self.l2_pos_tags.append([elem[1] for elem in self.es_tagger.tag(l2_sent)])

	def combine_pos_alignments(self):
		result = []
		for i in range(len(self.l1_pos_tags)):
			en = ([(self.l1_tok_sent[i][j], self.l1_alignments[i][j], self.l1_pos_tags[i][j]) for j in range(len(self.l1_tok_sent[i]))])
			es = ([(self.l2_tok_sent[i][j], self.l2_alignments[i][j], self.l2_pos_tags[i][j]) for j in range(len(self.l2_tok_sent[i]))])
			result.append([en, es])

		# For the purposes of demonstration, print to console
		for n in range(len(result)):
			print(result[n][0])
			print(result[n][1])
			print("\n")

		pickle.dump(result, open( "alligend_pos_sents.p", "wb" ) )

pos_tagger = Va3ToPos()
pos_tagger.read_va3(argv[1], argv[2])
pos_tagger.read_alignments()
pos_tagger.pos_tag(argv[3])
pos_tagger.combine_pos_alignments()


















