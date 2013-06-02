#!/usr/bin/python -O
#
# GeneticM
# 
# Grow beat reactive digital art with ProjectM
#
# Copyright (c) 2010 Lydia Sevelt <LydiaSevelt@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import os, sre, random

import re

import time, sys

import optparse

import GeneticMlib

# preset directory to use, this should be fixed as something a bit more dynamic and configurable later
global presets_directory
#presets_directory = '/home/krylen/GeneticMcode3/test/'
#presets_directory = '/etc/projectM/presets/:/etc/projectM/presets.orig/'

# if set to less than 2 it will default to 2
# possible number of parents for each child, how polyamorus of them
possible_parents = 2 

# how many children to produce on each run through
children = 25

# how many generations does a preset live for?
# dead presets will be omitted from the flock
lifespan = 10

# parent weighting
primary_parent_weight = 60

# tree parent weight
tree_parent_weight = 60

# block parent line swapping weight
block_parent_weight = 60

# maximum allowed shapecodes via mutation
max_shapecodes = 10

# maximum allowed wavecodes via mutation
max_wavecodes = 6

# maximum allowed swaps in a single equation swap mutation
max_swaps = 4

# group all mutation chances into a single dictionary
mutation_chances = { \
	# chance of mutation, chance is one out of #, zero means everytime
	'mutation_chance':50, \
	# chance of lesser mutations, chance is one out of #, zero means everytime
	'lesser_mutation_chance':30, \
	# chance of additions to equations (evaulation done on every element of an equation)
	'addition_chance':20, \
	# chance of dropping the line entirly
	'drop_chance':1000, \
	# number of branches (between 1 and constructor) to be built for a function fill in
	'constructor':6, \
	# object code (shapecode and wavecode for now) renumbering, chance is one out of #, zero means everytime
	'renumber':20, \
	# chance of swapping two equations
	'equation_mixer':20 \
	}

# special images mutation chances
images_mutation_chances = { \
	# chance of mutation, chance is one out of #, zero means everytime
	'mutation_chance':1, \
	# chance of lesser mutations, chance is one out of #, zero means everytime
	'lesser_mutation_chance':30, \
	# chance of additions to equations (evaulation done on every element of an equation)
	'addition_chance':20, \
	# chance of dropping the line entirly
	'drop_chance':1000, \
	# number of branches (between 1 and constructor) to be built for a function fill in
	'constructor':6, \
	# object code (shapecode and wavecode for now) renumbering, chance is one out of #, zero means everytime
	'renumber':20, \
	# chance of swapping two equations
	'equation_mixer':20 \
	}

# for breeding weights
# can total to any number
# using the Fibonacci sequence because that's what nature does
# starting at three instead of zero to make the lowest rating a little bit lower.
weighting_ranges = { \
	# will not breed
	1:None, \
	# matches 3
	2:3, \
	# matches between 3 and 5
	3:5, \
	# matches between 3 and 8
	4:8, \
	# matches between 3 and 13
	5:13, \
	# matches between 3 and 21
	6:21 \
	}

##################
#
# for debugging
#
##################

#from IPython.Shell import IPShellEmbed

#ipshell = IPShellEmbed()

#################
#
# end
#
#################

class ProjectMPlaylist:
	"""Project M Playlist Object"""
	
	def __init__(self, filename):
		"""Fill me in with descriptive words"""
		self.filename = filename
		self.file_lines = []
		self.flock = {}

	def readFile(self):
		"""Read in a playlist"""
		try:
			rawfile = open(self.filename, 'r')
		except:
			sys.exit('failed to open preset: ' + self.filename)
		rawfile = rawfile.readlines()
		count = 0
		breed_flag = False
		for line in rawfile:
			# skip this section if looking for breedability
			if not breed_flag:
				linefile = re.search('/.[^>,<]*\.prjm', line)
				if linefile == type([]):
					sys.exit('Playlist file in wrong format, more than one preset per line')
				if not linefile:
					self.file_lines.append( [ line, None, None ] )
					continue
				breed_flag = True
				continue
			# else...
			
			###
			#
			# start new breedability

			# skip this section
			if breed_flag:
				breedability = re.search('breedability>\d\\n', line)
				if not breedability:
					print `line`
					print `breedability`
					sys.exit('Playlist file in wrong format, no breedability on line that follows preset line')
			
			
			# end breedability
			# 
			###

			####
			#
			# old rating format
			#rating = re.search('rating>\d\\n', line)
			#if not rating:
			#	print `line`
			#	print `rating`
			#	sys.exit('Playlist file in wrong format, no rating on line that contains preset')
			#
			# end old rating format

			# else...
			linefile = linefile.group()
			#rating = rating.group()[7:8]
			breedability = breedability.group()[13:14]
			try:
				#rating = int(rating)
				breedability = int(breedability)
			except:
				print `line`
				print `breedability`
				sys.exit('Failure converting breedability to an intiger!')
			#self.file_lines.append( [ line, linefile , rating ] )
			#self.flock[count] = GeneticMlib.Evolver(linefile, rating, False)
			self.file_lines.append( [ line, linefile , breedability ] )
			self.flock[count] = GeneticMlib.Evolver(linefile, breedability, False)
			count += 1
			breed_flag = False
		self.total_presets = count

# end ProjectMPlaylist class

# basic function to check the directory for the format of generation-number and find the current generation, incrimenting for "this" generation
# that wasn't a confusing sentance at all.
def checkGeneration(flock):
	"""This checks to see what generation we are one and returns the next generation"""
	current = 0
	for count in flock:
		#print `flock[count].file`
		prjm_file = flock[count].file.split('/')
		if sre.match('GeneticM', prjm_file[-1]):
			parts = prjm_file[-1].split('-')
			try: 
				new = int(parts[1])
			except:
				continue
			if current <= new: 
				current = new
	current += 1
	return current

def selectBreeders(seeds, children, possible_parents, too_old, flock):
	"""This takes in the flock and randomly selects #children presets to breed
	This returns a dictionary of randomly selected presets pairs to breed"""
	# subtrack one from the seeds, random.randint will otherwise end up with out of range vaules by one
	seeds -= 1
	parents = {} 
	selections = 0
	flag = True
	while selections < children:
		num_parents = random.randint(2, possible_parents)
		count = 0
		while count < num_parents:
			breeder = random.randint(0, seeds)
			if parents.has_key(breeder):
				continue
			# do not accept presets that are too old to breed
			# ERROR - This creates an endless loop if there are not enough parents - FIXME
			prjm_file = flock[breeder].file.split('/')
			parts = prjm_file[-1].split('-')
			try: 
				preset_generation = int(parts[1])
			except:
				flag = False
				break
			if preset_generation < too_old:
				continue
			# end too_old code
			if count == 0:
				main_parent = breeder
				parents[main_parent] = [ breeder ]
				count += 1
				continue
			if not main_parent == breeder:
				parents[main_parent].append(breeder)
				count += 1
		if flag:
			selections += 1
			flag = True
	return parents

def selectBreeders2(seeds, children, possible_parents, too_old, flock):
	"""Rewriting this function
	
	This takes in the flock and randomly selects #children presets to breed
	This returns a dictionary of randomly selected presets pairs to breed"""
	# subtrack one from the seeds, random.randint will otherwise end up with out of range vaules by one
	seeds -= 1
	parents = {} 
	selections = 0
	# find the list of available parents
	available_parents = {}
	actual_available_count = 0
	for preset in flock:
		#print `flock[preset].file`
		prjm_file = flock[preset].file.split('/')
		parts = prjm_file[-1].split('-')
		try:
			preset_generation = int(parts[1])
		except:
			print "File not an available parent:", prjm_file
			continue
		# too old?
		if preset_generation < too_old:
			continue
		# rating 1 presets are not available for breeding
		if not weighting_ranges[flock[preset].rating]:
			print "Not available: ", preset
			continue
		available_parents[flock[preset].file] = True
	# end find available parents list
	# check to see we have enough parents to breed all requested children, if not fail
	if len(available_parents) < children:
		print "Not enough parents (" + `len(available_parents)` + ") to breed " + `children` + " children."
		sys.exit('add more available parents or breed less children...  extinction is a bitch.')

	# we have enough children so lets pick them
	parents = {} 
	selections = 0
	flag = True
	while selections < children:
		num_parents = random.randint(2, possible_parents)
		count = 0
		while count < num_parents:
			breeder = random.randint(0, seeds)
			if parents.has_key(breeder):
				continue
			# check to see if this is a valid parent
			if not available_parents.has_key(flock[breeder].file):
				continue
			# weighting - drop some presets based on their weighted downness
			# yeah, this is a terrible way to do it, I'll fix it later
			#if weighting_ranges[flock[breeder].rating] <= random.randint(0, weighting_ranges[6]):
			# weighting starts at three for Fibonacci sequence
			weight_test = random.randint(3, weighting_ranges[6])
			if weighting_ranges[flock[breeder].rating] <= weight_test:
				print "rejected for weight:", breeder, flock[breeder].rating, weighting_ranges[flock[breeder].rating], weight_test
				continue
			if count == 0:
				main_parent = breeder
				parents[main_parent] = [ breeder ]
				count += 1
				continue
			if not main_parent == breeder:
				print "success:", breeder, flock[breeder].rating, weighting_ranges[flock[breeder].rating], weight_test
				parents[main_parent].append(breeder)
				count += 1
		selections += 1
	return parents


def breedParents(breeders, flock, seeds, generation, mutation_chances, possible_parents, presets_directory, pretend, verbose):
	"""This takes the dictionary of pairs and breeds them together
	This includes mutation, and later will include equation editing"""
	# group is a terrible name for this variable
	# group is really the "main parent" as refered to in select breeders used as the key in the dictionary to retrive the list of all parents
	# this actually has no bearing on which parent is picked to be the primary parent
	# { parent1:[parent2, parent3, etc ] }
	for group in breeders:
		# count number of parents in list
		# -1 is because everything else starts counting from zero
		count = len(breeders[group]) - 1

		# what? why
#		count = -1
#		for parent in breeders[group]:
#			count += 1

		# lets find out which is "parent one" and set it's weight
		winner = random.randint(0, count)
		# set the weight of the primary parent
		weight = random.randint(0, primary_parent_weight)
		# read the full file into the flock object
		flock[breeders[group][winner]].readFile(False)
		#print `flock[breeders[group][winner]].blocks`
		parent_one = flock[breeders[group][winner]]
		# choose next parent
		seeds += 1
		child_file = presets_directory + 'GeneticM-' + `generation` + '-' + `count` + '.prjm'
		child = GeneticMlib.Evolver(child_file, False)
		# append parent name
		child.parents_names.append(parent_one.file)
		child_num = 0
		parent_count = 0
		start_flag = True
		# block referencing tracking
		blocks_reference = {}
		blocks_reference_count = []
		# primary parent file loaded
		# new child file loaded
		for parent in breeders[group]:
			if parent_count == winner:
				parent_count += 1
				continue
			# if child has contents, then it is new, set parent_one to the child
			# this allows the original "parent_one" to be the primary parent
			if start_flag:
				start_flag = False
			else:
				parent_one = child
				child = GeneticMlib.Evolver(child_file, False)
				#print "printing new child ", child.tree
#				child = { 'tree':{}, 'order':[] }
			#print parent_one
			#next_parent = readPresetFileExp(pool[parent], verbose)
			#print flock[parent].file
			# append parent name
			child.parents_names.append(flock[parent].file)
			time.sleep(.1)
			next_parent = flock[parent]
			print parent
			flock[parent].readFile(False)
			#print "two:", `flock[parent].blocks`
#			dupes_list = []
#			for l in next_parent.order:
#				if l in dupes_list:
#					print "explode! ", flock[parent]
#				else:
#					dupes_list.append(l)
#			if not next_parent.tree.has_key('blocks'):
#				print "uh oh"
#				print "tree"
#				print next_parent.tree
#				sys.exit('crap')
			# start mixing
#			dupes_list = []
#			print `parent_one.tree`
			# this is a terrible, no good, aweful, very bad hack
			warp_flag = False
			comp_flag = False
			for gene in parent_one.tree:
#				print "yo?", gene
#				if gene in dupes_list:
#					print "start"
#					for l in parent_one.order:
#						print l
#					print "ack! ", gene
#					sys.exit()
#				else:
#					dupes_list.append(gene)

#				# chance of dropping the gene
#				drop = random.randint(0, mutation_chances['drop_chance'])
#				if drop == 0:
#					continue
				if next_parent.tree.has_key(gene):
					which = random.randint(0, tree_parent_weight)
					if which >= weight:
						child.tree[gene] = parent_one.tree[gene]
						child.parents_order.append( ( parent_one.order[gene], gene ) )
					else:
						child.tree[gene] = next_parent.tree[gene]
						child.parents_order.append( ( next_parent.order[gene], gene ) )
					#child.order.append(gene)
					# mutate?
#					child.mutator(child.tree[gene], gene, mutation_chances, verbose)
					child.mutator(child.tree[gene], gene, mutation_chances, 'pre', verbose)
				else:
#					# parent_two does not have gene
#					include = random.randint(0, 1)
#					if include == 0:
#					child.tree[gene] = child.mutator(parent_one.tree[gene], gene, mutation_chances, verbose)
					child.tree[gene] = parent_one.tree[gene]
					child.mutator(parent_one.tree[gene], gene, mutation_chances, 'pre', verbose)
					child.parents_order.append( ( parent_one.order[gene], gene ) )
					#child.order.append(gene)
#				print child.order
#				print child.tree[gene]
			for gene in next_parent.tree:
				if parent_one.tree.has_key(gene):
					# parent_one already has the gene, this has been done already
					continue
				# chance of dropping gene
#				drop = random.randint(0, mutation_chances['drop_chance'])
#				if drop == 0:
#					continue
				else:
#					include = random.randint(0, 1)
#					if include == 0:
					child.tree[gene] = next_parent.tree[gene]
					child.mutator(next_parent.tree[gene], gene, mutation_chances, 'pre', verbose)
					child.parents_order.append( ( next_parent.order[gene], gene ) )
					#child.order.append(gene)
 #			   print child.tree[gene]
 			# block code time
			block_number = None
			for gene in parent_one.blocks:
				offset = 2
				type_offset = 4
				print "this is it", `gene`
				if gene[3] == "post-script":
					#                  per-frame          0
					gene_block_number = gene[2]
					offset = 1
					type_offset = 3
				elif gene[3] == "script":
					#               wave or shape          0             per_point
					gene_block_number = gene[4] + "_" + `gene[1]` + "_" + gene[5]
					offset = 1
					type_offset = 3
				elif gene[3] == "pixel shader":
					#                 warp or comp
					gene_block_number = gene[2]
					# this is a terrible, no good, aweful, very bad hack
					if gene_block_number == "warp":
						warp_flag = True
					elif gene_block_number == "comp":
						comp_flag = True
					offset = 1
					type_offset = 3
				elif gene[4] == "init":
					#                  wavecode            0              init
					gene_block_number = gene[3] + "_" + `gene[2]` + "_" + gene[4]
				else:
					print `gene`
					print "failure"
					sys.exit()
				# check to see if this gene block has been seen before
				print "blocks reference", `blocks_reference`, "gene block num", `gene_block_number`
				block_exists_flag = False
				if blocks_reference.has_key(gene_block_number):
				# use the block_number variable to check if this is a new block
				# this is stupid
				#if block_number != gene_block_number:
					block_exists_flag = True
					#print gene_block_number
					# set the block_number variable to the current block number we are on <- why?
					block_number = gene_block_number
					#print "block number:", block_number
					# more goes here, like when blocks change and shit
					#
					# All that code replaced with this?
					#
					#blocks_reference[block_number] = gene[0]
					#blocks_reference_count.append(gene[0])
					#
					########################################
					#
					# Has this all become obsolete? really?
					#
					print "1", `blocks_reference`, `block_number`
					block_count_flag = False
					# This block has been seen before, does it's number match?
					if not blocks_reference[block_number] == gene[0]:
						# it does not, set it to the choosen number for this block
						print "fixing block gene number due to it already existing"
						new_block_number = blocks_reference[block_number]
						block_count_flag = True
					# we have not seen this block before, is it's block number in use?
					elif gene[0] not in blocks_reference_count:
						# this should make sure we advance the number
						print "block reference count fix", `gene`, `blocks_reference`, `blocks_reference_count`
						blocks_reference_count.sort()
						new_block_number = blocks_reference_count[-1] + 1
						print "block num:", `block_number`, "last ref count num:", `blocks_reference_count[-1]`, "new:", `new_block_number`
						block_count_flag = True
						blocks_reference[block_number] = gene[0]
					if block_count_flag:
						# crazy tuple adjust function
						blocks_reference[block_number] = new_block_number
						print "should happen", `gene`
						gene_len = len(gene) - 1
						if gene_len == 5:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4], gene[5] )
							print "block num gene mod 0 - 5"
						elif gene_len == 4:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4] )
							print "block num gene mod 0 - 4"
						elif gene_len == 3:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3] )
							print "block num gene mod 0 - 3"
						else:
							print "fail:", gene_len
							sys.exit()
						print "happened anyway", `gene`
						#gene[0] = blocks_reference[block_number]
						block_count_flag = False
					#
					# Dead code running?
					#
					###########################################
					blocks_reference[block_number] = gene[0]
					blocks_reference_count.append(gene[0])
				#
				#########################
				#
				# End blocks_reference.has_key(gene_block_number)
				#
				#########################
#				else:
					# blocks_reference does not contain this gene_block_number
					# meaning a block like wave_0_script_per_point has not been defined in the reference dict yet

				# genero flag
#				flag = False
#				if gene[3] == 'init':
#					flag = True
#					gene_check = GeneticMlib.projectm_wave_genes
#				elif gene[2] == 'shapecode':
#					flag = True
#					gene_check = GeneticMlib.projectm_shape_genes
#				else:
#					# not init stuff
#					pass
				# got a shapecode or wavecode, this is init stuff
#				if flag:
				# seriously cheaping out here to get stuff working now
				if next_parent.blocks_content.has_key( gene[offset:] ):
					which = random.randint(0, block_parent_weight)
					# do not mix pixel shaders for now - parent one always wins
					if gene[3] == "pixel shader":
						child.blocks_content[ gene[offset:] ] = parent_one.blocks_content[ gene[offset:] ]
						print "p1 win 1 - pixel shader"
					else:
						if which >= weight:
							child.blocks_content[ gene[offset:] ] = parent_one.blocks_content[ gene[offset:] ]
							print "p1 win 1"
						else:
							child.blocks_content[ gene[offset:] ] = next_parent.blocks_content[ gene[offset:] ]
							print "p2 win 1"
					if options.images:
						# if images then change the mutation chances
						image_flag = False
						if gene[3] == 'shapecode':
							# broken into two statments as some genes will not have element 5
							if gene[5] == 'ImageURL':
								image_flag = True
								print "Images Mutation changes"
								print "gene:", `gene`, offset
								child.mutator(child.blocks_content[ gene[offset:] ], gene, images_mutation_chances, gene[type_offset], verbose, options.images)
								print "set to: ", child.blocks_content[ gene[offset:] ]
						if not image_flag:
							# not an image gene, normal mutation
							child.mutator(child.blocks_content[ gene[offset:] ], gene, mutation_chances, gene[type_offset], verbose)
					else:
						child.mutator(child.blocks_content[ gene[offset:] ], gene, mutation_chances, gene[type_offset], verbose)
				
					###########################################
					#
					# Start Check funtion
					#
					if not block_exists_flag and blocks_reference_count:
						#	if gene[0] not in blocks_reference_count:
						# this should make sure we advance the number
						print "block reference count fix 2", `gene`, `blocks_reference`, `blocks_reference_count`
						blocks_reference_count.sort()
						new_block_number = blocks_reference_count[-1] + 1
						print "block num: 2 ", `gene_block_number`, "last ref count num:", `blocks_reference_count[-1]`, "new:", `new_block_number`
						# crazy tuple adjust function
						blocks_reference[gene_block_number] = new_block_number
						print "should happen", `gene`
						gene_len = len(gene) - 1
						if gene_len == 5:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3], gene[4], gene[5] )
							print "block num gene mod 4 - 5"
						elif gene_len == 4:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3], gene[4] )
							print "block num gene mod 4 - 4"
						elif gene_len == 3:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3] )
							print "block num gene mod 4 - 3"
						else:
							print "fail:", gene_len
							sys.exit()
						print "happened anyway", `gene`
						#gene[0] = blocks_reference[block_number]
						#block_count_flag = False
					#
					# End Check funtion
					#
					###########################################
					if not gene in child.blocks:
						print "child add block 1", `gene`
						blocks_reference[gene_block_number] = gene[0]
						blocks_reference_count.append(gene[0])

						child.blocks.append(gene)
				else:
					# this secondary parent does not have this gene, add and/or mutate it
					child.blocks_content[ gene[offset:] ] = parent_one.blocks_content[ gene[offset:] ]
					if options.images:
						# if images then change the mutation chances
						image_flag = False
						if gene[3] == 'shapecode':
							# broken into two statments as some genes will not have element 5
							if gene[5] == 'ImageURL':
								image_flag = True
								print "Images Mutation changes"
								child.mutator(child.blocks_content[ gene[offset:] ], gene, images_mutation_chances, gene[type_offset], verbose, options.images)
								print "set to: ", child.blocks_content[ gene[offset:] ]
						if not image_flag:
							# not an image gene, normal mutation
							child.mutator(child.blocks_content[ gene[offset:] ], gene, mutation_chances, gene[type_offset], verbose)
					else:
						child.mutator(child.blocks_content[ gene[offset:] ], gene, mutation_chances, gene[type_offset], verbose)

					###########################################
					#
					# Start Check funtion
					#
					if not block_exists_flag and blocks_reference_count:
						#	if gene[0] not in blocks_reference_count:
						# this should make sure we advance the number
						print "block reference count fix 2", `gene`, `blocks_reference`, `blocks_reference_count`
						blocks_reference_count.sort()
						new_block_number = blocks_reference_count[-1] + 1
						print "block num: 2 ", `gene_block_number`, "last ref count num:", `blocks_reference_count[-1]`, "new:", `new_block_number`
						# crazy tuple adjust function
						blocks_reference[gene_block_number] = new_block_number
						print "shouldn't happen", `gene`
						gene_len = len(gene) - 1
						if gene_len == 5:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3], gene[4], gene[5] )
							print "block num gene mod 5 - 5"
						elif gene_len == 4:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3], gene[4] )
							print "block num gene mod 5 - 4"
						elif gene_len == 3:
							gene = ( blocks_reference[gene_block_number], gene[1], gene[2], gene[3] )
							print "block num gene mod 5 - 3"
						else:
							print "fail:", gene_len
							sys.exit()
						print "happened anyway", `gene`
						#gene[0] = blocks_reference[block_number]
						#block_count_flag = False
					#
					# End Check funtion
					#
					###########################################
					if not gene in child.blocks:
						print "child add block 0", `gene`
						blocks_reference[gene_block_number] = gene[0]
						blocks_reference_count.append(gene[0])

						child.blocks.append(gene)
				continue
#				if next_parent.has_key(gene):
#					which = random.randint(0, 100)
#					if which >= weight:
#						child.tree[gene] = parent_one.tree[gene]
#					else:
#						child.tree[gene] = next_parent.tree[gene]
#					child.mutator(child.tree[gene], gene, mutation_chances, verbose)
#				else:
#					child.tree[gene] = parent_one.tree[gene]
#					child.mutator(parent_one.tree[gene], gene, mutation_chances, verbose)
			print "next parent"
			for gene in next_parent.blocks:
				if parent_one.blocks_content.has_key( gene[offset:] ):
					# already done, skip it
					continue
				# offset checks
				offset = 2
				type_offset = 4
				print "fixme", `gene`
				if gene[3] == "post-script":
					#                  per-frame          0
					gene_block_number = gene[2]
					offset = 1
					type_offset = 3
				elif gene[3] == "script":
					#                wave or shape         0             per_point
					gene_block_number = gene[4] + "_" + `gene[1]` +  "_" + gene[5]
					offset = 1
					type_offset = 3
				elif gene[3] == "pixel shader":
					#                 warp or comp
					gene_block_number = gene[2]
					offset = 1
					type_offset = 3
				elif gene[4] == "init":
					#                  wavecode            0              init
					gene_block_number = gene[3] + "_" + `gene[2]` + "_" + gene[4]
				else:
					print `gene`
					print "failure"
					sys.exit()
				# end offset checks
				#block order fixes
				if block_number != gene_block_number:
					#print gene_block_number
					block_number = gene_block_number
					print "block number:", block_number
					# more goes here, like when blocks change and shit
					print `blocks_reference`, `block_number`
					if blocks_reference.has_key(block_number):
						# this *WILL* happen
						block_count_flag = True
					elif gene[0] in blocks_reference_count:
						# this should make sure we advance the number
						print "block reference count fix", `gene`, `blocks_reference`, `blocks_reference_count`
						blocks_reference_count.sort()
						new_block_number = blocks_reference_count[-1] + 1
						print "block num:", `block_number`, "last ref count num:", `blocks_reference_count[-1]`, "new:", `new_block_number`
						block_count_flag = True
						blocks_reference[block_number] = gene[0]
					if block_count_flag:
						# crazy tuple adjust function
						print "fix it", `gene`
						gene_len = len(gene) - 1
						if gene_len == 5:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4], gene[5] )
							print "block num gene mod - 5"
						elif gene_len == 4:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4] )
							print "block num gene mod - 4"
						elif gene_len == 3:
							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3] )
							print "block num gene mod - 3"
						else:
							print "fail:", gene_len
							sys.exit()
						print "better?", `gene`
						block_count_flag = False
						#gene[0] = blocks_reference[block_number]
	#					print "do it", `gene`
	#					if gene[0] in blocks_reference_count:
	#						# this should make sure we advance the number
	#						blocks_reference_count.sort()
	#						new_block_number = blocks_reference_count[-1] + 1
	#
	#						blocks_reference[block_number] = new_block_number
	#						# crazy tuple adjust function
	#						gene_len = len(gene) - 1
	#						if gene_len == 5:
	#							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4], gene[5] )
	#							print "bad gene mod 2 - 5"
	#						elif gene_len == 4:
	#							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3], gene[4] )
	#							print "bad gene mod 2 - 4"
	#						elif gene_len == 3:
	#							gene = ( blocks_reference[block_number], gene[1], gene[2], gene[3] )
	#							print "bad gene mod 2 - 3"
	#						else:
	#							print "fail:", gene_len
	#							sys.exit()
	#						print "why not", `gene`
	#						blocks_reference[block_number] = gene[0]
	#						blocks_reference_count.append(gene[0])
	#					else:
	#						blocks_reference[block_number] = gene[0]
	#						blocks_reference_count.append(gene[0])
					blocks_reference[block_number] = gene[0]
					blocks_reference_count.append(gene[0])
				
				# genero flag
				#print "test1- no! -", `offset`
				# if it's a pixel shader we do not want to add extra lines from the secondary parent
				# this is a terrible, no good, aweful, very bad hack
				if (gene[2] == "warp" and warp_flag == False) or (gene[2] == "comp" and comp_flag == False):
					child.blocks_content[ gene[offset:] ] = next_parent.blocks_content[ gene[offset:] ]
					child.mutator(child.blocks_content[ gene[offset:] ], gene, mutation_chances, gene[type_offset], verbose)
					if not gene in child.blocks:
						print "child add block 2", `gene`
						child.blocks.append(gene)
#			if not parent_one.tree.has_key('blocks'):
#				#rint "holy shit"
#				print gene
#				print "tree"
#				print child.tree
#				sys.exit('crap')
#			for gene in parent_one.tree['blocks']:
#				print gene
			parent_count += 1
		if pretend:
			print "parents " + `breeders[group]`
			print "child " + `generation` + "-" + `seeds`
			print
		else:
#			for gene in child.tree:
#				print gene
			if child.blocks == []:
				print "fuck"
				sys.exit()
			##########
			#
			# child post-processing block
			#
			
			# object numbering mutator
			if random.randint(0, 100) < mutation_chances["renumber"]:
				child.object_mutator(max_wavecodes, max_shapecodes)

			#ipshell()
			# equation swapper code
			if random.randint(0, 100) < mutation_chances["equation_mixer"]:
				child.equation_swapping_mutator(max_swaps)

			#
			# end child post-processing block
			#
			##########
			child.blocks.sort()
			#print `blocks_reference`
			for block_line in blocks_reference:
				print `block_line`, blocks_reference[block_line]
			print `child.blocks`
			child.writeFile(seeds, generation, presets_directory, pretend)
#			print "writeChildPreset_exp(" + child.file, seeds, generation, presets_directory, `pretend` + ")"
	return

def main():
	"""non-playlist based breeding no longer allowed
	Legacy code that will hopefully go away someday soon"""

	if not options.playlist_file:
		print "Playlist now required"
		sys.exit(1)

	if not options.output_path:
		print "Output path required"
		sys.exit(1)
	
	presets_directory = options.output_path

	if options.playlist_file:
		playlist = ProjectMPlaylist(options.playlist_file)
		playlist.readFile()
		
		# Return "This" Generation's number
		generation = checkGeneration(playlist.flock)

		# find the last surviving generation
		too_old = generation - lifespan

		# select the breeders from the pool and return them in a dictionary of lists:
		#  { primary_parent: [ child1,
		#			child2,
		#			child3...  ]
		breeders = selectBreeders2(playlist.total_presets, children, possible_parents, too_old, playlist.flock)

		#print breeders
		#for file in flock:

		breedParents(breeders, playlist.flock, playlist.total_presets, generation, mutation_chances, possible_parents, presets_directory, False, False)

		print "new ok"

	else:
		# old shit code
		flock = {}
		full_list = []
		split_dirs = presets_directory.split(':')
		main_dir = split_dirs[0]
		for dir in split_dirs:
			list = os.listdir(dir)
		#	list = list.split('\n')
		#	full_list.extend(list)
			# ewwww, gross, this is *way* slower than extend
			# fix this later, it sucks, especially when you have thousands and thousands of presets
			for file in list:
				if sre.match('GeneticM', file):
					full_list.append(dir + file)
		print "list generated"

		# find the current number of presets to give our secondary count starting number.
		count = 0
		for file in full_list:
			flock[count] = GeneticMlib.Evolver(file, False)
			count += 1

		# Return "This" Generation's number
		generation = checkGeneration(flock)

		# find the last surviving generation
		too_old = generation - lifespan

		# select the breeders from the pool and return them in a dictionary of lists:
		#  { primary_parent: [ child1,
		#			child2,
		#			child3...  ]
		breeders = selectBreeders(count, children, possible_parents, too_old, flock)

		#print breeders
		#for file in flock:

		breedParents(breeders, flock, count, generation, mutation_chances, possible_parents, main_dir, False, False)

		print "a-ok"
	return

if not sre.match(".*pydoc$", sys.argv[0]):
	# option parsing with optparse
	opts_parser = optparse.OptionParser("usage: %prog [options]")
	opts_parser.add_option("-l", "--playlist", dest="playlist_file", default=False, help="Specify the playlist file to use")
	opts_parser.add_option("-o", "--outputpath", dest="output_path", default=False, help="Specify the output path, where new presets will be written")
	opts_parser.add_option("-i", "--images", action="store_true", dest="images", default=False, help="Use images mode to mutate in images")
	options, args = opts_parser.parse_args()
	# run the main loop
	main()

