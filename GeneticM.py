#!/usr/bin/python -O

import os, sre, random

import time, sys

import GeneticMlib

# preset directory to use, this should be fixed as something a bit more dynamic and configurable later
presets_directory = '/home/adam/GeneticMcode3/test/'
#presets_directory = '/etc/projectM/presets/:/etc/projectM/presets.orig/'

# if set to less than 2 it will default to 2
# possible number of parents for each child, how polyamorus of them
possible_parents = 2 

# how many children to produce on each run through
children = 64

# parent weighting
primary_parent_weight = 100

# tree parent weight
tree_parent_weight = 100

# block parent line swapping weight
block_parent_weight = 100

# group all mutation chances into a single dictionary
mutation_chances = { 
	# chance of mutation, chance is one out of #, zero means everytime
	'mutation_chance':50, \
	# chance of lesser mutations, chance is one out of #, zero means everytime
	'lesser_mutation_chance':50, \
	# chance of additions to equations (evaulation done on every element of an equation)
	'addition_chance':50, \
	# chance of dropping the line entirly
	'drop_chance':1000, \
	# number of branches (between 1 and constructor) to be built for a function fill in
	'constructor':3 \
	}   

def checkGeneration(flock):
	"""This checks to see what generation we are one and returns the next generation"""
	current = 0
	for file in flock:
		prjm_file = flock[file].file.split('/')
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

def selectBreeders(seeds, children, possible_parents):
	"""This takes in the flock and randomly selects #children presets to breed
	This returns a dictionary of randomly selected presets pairs to breed"""
	# subtrack one from the seeds, random.randint will otherwise end up with out of range vaules by one
	seeds -= 1
	parents = {} 
	selections = 0
	while selections < children:
		num_parents = random.randint(2, possible_parents)
		count = 0
		while count < num_parents:
			breeder = random.randint(0, seeds)
			if parents.has_key(breeder):
				continue
			if count == 0:
				main_parent = breeder
				parents[main_parent] = [ breeder ]
				count += 1
				continue
			if not main_parent == breeder:
				parents[main_parent].append(breeder)
				count += 1
		selections += 1
	return parents

def breedParents(breeders, flock, seeds, generation, mutation_chances, possible_parents, presets_directory, pretend, verbose):
	"""This takes the dictionary of pairs and breeds them together
	This includes mutation, and later will include equation editing"""
	for group in breeders:
		# count number of parents in list
		# -1 is because everything else starts counting from zero
		count = -1
		for parent in breeders[group]:
			count += 1

		# lets find out which is "parent one" and set it's weight
		winner = random.randint(0, count)
		# Setting the weight manually
		weight = random.randint(0, primary_parent_weight)
#		weight = 95
#		parent_one = readPresetFileExp(pool[breeders[group][winner]], verbose)
		flock[breeders[group][winner]].readFile(False)
		#print `flock[breeders[group][winner]].blocks`
		parent_one = flock[breeders[group][winner]]
		# choose next parent
#		child = { 'tree':{}, 'order':[] }
		seeds += 1
		child_file = presets_directory + 'GeneticM-' + `generation` + '-' + `count` + '.prjm'
		child = GeneticMlib.Evolver(child_file, False)
		child_num = 0
		parent_count = 0
		start_flag = True
#		for gene in parent_one.tree:
#			if sre.match('^wavecode*', gene):
#				print gene
#				print "done"
#				sys.exit()
#	   print 'experimental'
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
			print flock[parent].file
			time.sleep(.1)
			next_parent = flock[parent]
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
				if gene[4] == "post-script":
					gene_block_number = gene[3]
				elif gene[4] == "script":
					gene_block_number = gene[5] + "_" + gene[2]
				elif gene[4] == "init":
					gene_block_number = gene[3] + "_" + gene[2]
				else:
					print `gene`
					print "failure"
					sys.exit()
				if block_number != gene_block_number:
					#print gene_block_number
					block_number == gene_block_number
					# more goes here, like when blocks change and shit
					# all kinds of sanity checks needed
					# but none for now
					# livin' on the edge baby
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
				if next_parent.blocks_content.has_key( gene[2:] ):
					which = random.randint(0, block_parent_weight)
					if which >= weight:
						child.blocks_content[ gene[2:] ] = parent_one.blocks_content[ gene[2:] ]
					else:
						child.blocks_content[ gene[2:] ] = next_parent.blocks_content[ gene[2:] ]
					child.mutator(child.blocks_content[ gene[2:] ], gene, mutation_chances, gene[4], verbose)
					if not gene in child.blocks:
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
			for gene in next_parent.blocks:
				if parent_one.blocks_content.has_key( gene[2:] ):
					# already done, skip it
					continue
				print "test1- no!"
				child.blocks_content[ gene[2:] ] = next_parent.blocks_content[ gene[2:] ]
				child.mutator(child.blocks_content[ gene[2:] ], gene, mutation_chances, gene[4], verbose)
				if not gene in child.blocks:
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
			child.blocks.sort()
			child.writeFile(seeds, generation, presets_directory, pretend)
#			print "writeChildPreset_exp(" + child.file, seeds, generation, presets_directory, `pretend` + ")"
	return

print "testing only for now"

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
		full_list.append(dir + file)
print "list generated"

count = 0
for file in full_list:
	flock[count] = GeneticMlib.Evolver(file, False)
#	flock[count].readFile(False)
	count += 1

generation = checkGeneration(flock)

breeders = selectBreeders(count, children, possible_parents)

#print breeders
#for file in flock:

breedParents(breeders, flock, count, generation, mutation_chances, possible_parents, main_dir, False, False)

print "a-ok"
