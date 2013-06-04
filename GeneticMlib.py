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

import sre, sys, random

# valid projectm operators
projectm_operators = [ '=','-', '+', '*', '/', '|', '&', '%' ]

# projectm variables and if they are writable or not
# True or False for writable or not

# dictionary of projectM variables that take specific value ranges
# valid values are:
# >0 = greater than zero
# 0-1 = between zero and one
# bool = zero or one
# -1-1 = negative one to positive one
# 0-8 = integer zero through eight
# 0-.5 = zero through .5
# 0-5 = zero through 5
# 0-64 = zero through 64
# 0-48 = zero through 48
# 0-3 = zero through three
# any = any
greater_than_zero = { 'min':0, 'max':None, 'type':'int' }

greater_than_point_zero = { 'min':0, 'max':None, 'type':'float' }

zero_to_one = { 'min':0, 'max':1, 'type':'float' }

bool_val = { 'min':0, 'max':1, 'type':'int' }

negative_one_to_one = { 'min':-1, 'max':1, 'type':'float' }

negative_onehundred_to_onehundred = { 'min':-100, 'max':100, 'type':'int' }

zero_to_seven = { 'min':0, 'max':7, 'type':'int' }

zero_to_eight = { 'min':0, 'max':8, 'type':'int' }

zero_to_three = { 'min':0, 'max':3, 'type':'int' }

zero_to_point_two = { 'min':0, 'max':2, 'type':'float' }

zero_to_five = { 'min':0, 'max':5, 'type':'int' }

zero_to_sixyfour = { 'min':0, 'max':64, 'type':'float' }

zero_to_fortyeight = { 'min':0, 'max':48, 'type':'float' }

zero_to_point_five = { 'min':0, 'max':.5, 'type':'float' }

three_to_onehundred = { 'min':3, 'max':100, 'type':'int' }

zero_to_point_onehundred = { 'min':0, 'max':100, 'type':'float' }

one_to_fiveonetwo = { 'min':1, 'max':512, 'type':'int' }

one_to_twozerofoureight = { 'min':1, 'max':2048, 'type':'int' }

any_val = { 'min':None, 'max':None, 'type':'int' }

any_point_val = { 'min':None, 'max':None, 'type':'float' }

# ignore type for excluding lines from being changed
ignore = { 'min':None, 'max':None, 'type':'ignore' }

# images special, for lots of numbered images
images = { 'min':1, 'max':5, 'type':'images' }

projectm_genes = { \
	\
	'fWarpScale':greater_than_point_zero, \
	\
	'zoom':greater_than_zero, 'fZoomExponent':greater_than_zero, 'warp':greater_than_point_zero, \
	'sx':greater_than_point_zero, 'sy':greater_than_point_zero, 'fGammaAdj':greater_than_point_zero, \
	'fVideoEchoZoom':greater_than_point_zero, 'fVideoEchoAlpha':greater_than_zero, \
	'tex_zoom':greater_than_zero, 'rot':greater_than_zero, \
	\
	'cx':zero_to_one, 'cy':zero_to_one, 'wave_x':zero_to_one, 'wave_y':zero_to_one, \
	'wave_r':zero_to_one, 'wave_g':zero_to_one, 'wave_b':zero_to_one, 'fWaveAlpha':zero_to_point_onehundred, \
	'ob_r':zero_to_one, 'ob_g':zero_to_one, 'ob_b':zero_to_one, 'ob_a':zero_to_one, \
	'ib_r':zero_to_one, 'ib_g':zero_to_one, 'ib_b':zero_to_one, 'ib_a':zero_to_one, \
	'mv_r':zero_to_one, 'mv_g':zero_to_one, 'mv_b':zero_to_one, 'mv_a':zero_to_one, \
	'fDecay':zero_to_one, \
	\
	'bWaveDots':bool_val, 'bWaveThick':bool_val, 'bAdditiveWaves':bool_val, 'enabled':bool_val, \
	'bMaximizeWaveColor':bool_val, 'bDarkenCenter':bool_val, 'bTexWrap':bool_val, \
	'bInvert':bool_val, 'bBrighten':bool_val, 'bDarken':bool_val, 'bSolarize':bool_val, \
	'bModWaveAlphaByVolume':bool_val, 'bRedBlueStereo':bool_val, 'bMotionVectorsOn':bool_val, \
	\
	'fWaveParam':negative_one_to_one, 'mv_dx':negative_one_to_one, 'mv_dy':negative_one_to_one, \
	'fWaveSmoothing':negative_one_to_one, 'fModWaveAlphaStart':zero_to_point_two, 'fModWaveAlphaEnd':zero_to_point_two, 
	'fWarpAnimSpeed':zero_to_point_onehundred, 'fShader':negative_one_to_one, \
	\
	'ob_size':zero_to_point_five, 'ib_size':zero_to_point_five, \
	\
	'mv_l':zero_to_five,'fRating':zero_to_five, \
	\
	'nWaveMode':zero_to_eight, \
	\
	'nMotionVectorsX':zero_to_sixyfour, \
	\
	'nMotionVectorsY':zero_to_fortyeight, \
	\
	'nVideoEchoOrientation':zero_to_three, \
	\
	'dx':any_point_val, 'dy':any_point_val, 'fWaveScale':any_point_val \

}

projectm_wave_genes = { \
			'r':zero_to_one, 'g':zero_to_one, 'b':zero_to_one,'a':zero_to_one, \
			'x':zero_to_one, 'y':zero_to_one, \
			'sample':zero_to_one, 'smoothing':zero_to_one, \
			\
			'value1':negative_one_to_one, 'value2':negative_one_to_one, \
			\
			'bSpectrum':bool_val, 'bDrawThick':bool_val, 'bAdditive':bool_val, 'bUseDots':bool_val, \
			'enabled':bool_val, \
			\
			'scaling':greater_than_zero, 'scaling':greater_than_zero, \
			\
			'samples':one_to_fiveonetwo, \
			\
			'sep':negative_onehundred_to_onehundred \
}

projectm_shape_genes = { \
			'border_r':zero_to_one, 'border_g':zero_to_one, 'border_b':zero_to_one, 'border_a':zero_to_one, \
			'r2':zero_to_one, 'g2':zero_to_one, 'b2':zero_to_one, 'a2':zero_to_one, \
			'r':zero_to_one, 'g':zero_to_one, 'b':zero_to_one, 'a':zero_to_one, \
			'y':zero_to_one, 'x':zero_to_one, 
			\
			'textured':bool_val, 'enabled':bool_val, 'additive':bool_val, 'thickOutline':bool_val, \
			\
			'rad':greater_than_zero, 'ang':any_val, 'tex_ang':any_val, \
			\
			'sides':three_to_onehundred, \
			\
			'tex_zoom':zero_to_point_two, \
			\
			'ImageURL':ignore, \
			\
			'num_inst':greater_than_zero \
}
			#'ImageURL':ignore, \
			#'ImageURL':images, \
# num_inst for pixel shaders

# pixel shader fun, these vars have something to do with the pixel shaders, I'm not sure what
projectm_pixel_shader_genes = { \
				'ed':zero_to_one, 'n':zero_to_one, 'x':zero_to_one \
}

# this isn't really complete, but should do for now
projectm_variables = {  'zoom':True, \
			'zoomexp':True, \
			'rot':True, \
			'warp':True, \
			'cx':True, \
			'cy':True, \
			'dx':True, \
			'dy':True, \
			'sx':True, \
			'sy':True, \
			'wave_mode':True, \
			'wave_x':True, \
			'wave_y':True, \
			'wave_r':True, \
			'wave_g':True, \
			'wave_b':True, \
			'wave_a':True, \
			'wave_mystery':True, \
			'wave_usedots':True, \
			'wave_thick':True, \
			'wave_additive':True, \
			'wave_brighten':True, \
			'ob_size':True, \
			'ob_r':True, \
			'ob_g':True, \
			'ob_b':True, \
			'ob_a':True, \
			'ib_size':True, \
			'ib_r':True, \
			'ib_g':True, \
			'ib_b':True, \
			'ib_a':True, \
			'mv_r':True, \
			'mv_g':True, \
			'mv_b':True, \
			'mv_a':True, \
			'mv_x':True, \
			'mv_y':True, \
			'mv_l':True, \
			'mv_dx':True, \
			'mv_dy':True, \
			'decay':True, \
			'gamma':True, \
			'echo_zoom':True, \
			'echo_alpha':True, \
			'echo_orient':True, \
			'darken_center':True, \
			'wrap':True, \
			'invert':True, \
			'brighten':True, \
			'darken':True, \
			'solarize':True, \
			'monitor':True, \
			'time':False, \
			'fps':False, \
			'frame':False, \
			'progress':False, \
			'bass':False, \
			'mid':False, \
			'treb':False, \
			'bass_att':False, \
			'mid_att':False, \
			'treb_att':False, \
			'meshx':False, \
			'meshy':False, \
			# these from here out are per-pixel only..
			'x':False, \
			'y':False, \
			'rad':False, \
			'ang':False }

# projectm functions and their special circumstances
# the number is the number of values that must be contained within it,
# seperated by commas
projectm_functions = {  'int(':1, \
			'abs(':1, \
			'sin(':1, \
			'cos(':1, \
			'tan(':1, \
			'asin(':1, \
			'acos(':1, \
			'atan(':1, \
			'sqr(':1, \
			'sqrt(':1, \
			'exp(':1, \
			'log(':1, \
			'log10(':1, \
			'sign(':1, \
			'rand(':1, \
			'bnot(':1, \
			'fact(':1, \
			'atan2(':2, \
			'atan6(':2, \
			'pow(':2, \
			'min(':2, \
			'max(':2, \
			'sigmoid(':2, \
			'nchoosek(':2, \
			'bor(':2, \
			'equal(':2, \
			'above(':2, \
			'below(':2, \
			'band(':2, \
			'if(':3 }
# missing: exp nchoosek fact - These have been added, hopefully they are ok to be included

# scripting line check

# check for "init" sytle options for wavecode and shapecodes
init_check = sre.compile('^wavecode*|^shapecode*')
wavecode_check = sre.compile('^wavecode*')
shapecode_check = sre.compile('^shapecode*')

# check for "block" genes that are "script" style
block_script_check = sre.compile('^wave_\d*|^shape_\d*')
block_wave_script_check = sre.compile('^wave_\d*')
block_shape_script_check = sre.compile('^shape_\d*')

# check for script types
# these work for blocks and non since block genes get split and matched
# types are init, per_point, and per_frame
sub_init_check = sre.compile('^init*')
sub_point_init_check = sre.compile('^per_point_init*')
point_check = sre.compile('^per_point*')
frame_check = sre.compile('^per_frame*')
pixel_check = sre.compile('^per_pixel*')
frame_init_check = sre.compile('^per_frame_init*')

## check for wavecodes and it's sub-functions
#wavecode_check = sre.compile('^wavecode')
#wave_point_check = sre.compile('^wave_\d*_per_point')
#wave_frame_check = sre.compile('^wave_\d*_per_frame')

## check for shapecodes and it's sub-functions
#shapecode_check = sre.compile('^shapecode')
#shape_point_check = sre.compile('^shape_\d*_per_point')
#shape_frame_check = sre.compile('^shape_\d*_per_frame')

# check for boolean gene and treat it accordingly
boolean_gene_check = sre.compile('^b[A-Z]|_b[A-Z]|_enabled$|wave_additive')

# check to see if value is only a number, float or int
number_only = sre.compile('^\s*\-?[\d,.]+\s*(/{2,2}.*)*;*$')

# check for comments or end of line
comments_check = sre.compile('(^\s*/{2,2}.*)|(^\s*$)')

# regex's for parsing lines
#end_line_check = sre.compile('(^\s*[;*\s*|\s]/{2,2}.*$)|(^\s*$)|(^\s*;*\s*$)|(^/{2,2}.*$)')
end_line_check = sre.compile('(^\s*$)|(^/{2,2}.*$)')
number_check = sre.compile('^[\d\.]+\d*')
operator_check = sre.compile('[\=\+\-\*\&\%\|\/]')

# open and close paren and bracket checks
parens_check = sre.compile('[\(\[\)\]]')
open_parens_check = sre.compile('[\(\[]')

# check for functions, or words that end with (
function_check = sre.compile('^\w+\(')

# check for variables, or words that do not end with (
# fix me
# this only works cause the function check is right before it
variable_check = sre.compile('^\w+\d*(\W|$)')
variable_get = sre.compile('^\w+\d*')

class Evolver:
	"""GeneticM Evolver
	Breed presets and make them evolve
	
	format:
	
	self.order = []
		[ gene,
		  gene,
		  ]
	self.tree = {}
		{ (gene, type, section ) :[]
			[ """
	

	def __init__(self, file, rating=False, verbose=False):
		"""Fill me in with descriptive words"""
		self.tree = {}
		self.blocks_content = {}
		self.blocks = []
		self.blocks_order = {}
		self.blocks_order_count = 0
		self.blocks_chunk_count = 0
		self.order = {}
		self.order_count = 0
		self.parents_order = []
		self.file = file
		self.parents_names = []
		self.rating = rating
	
	def readFile(self, verbose):
		"""This replaces readPresetFile, reading the file and returning it's 'DNA' string
		Now files are read in order, meaning the order of lines is no longer completely
		randomized every time, instead that is part of the new DNA mutation code"""
		file = self.file
		print file
		try:
			file = open(file, 'r')
		except:
			try:
				file = open(file, 'r')
			except:
				sys.exit('failed to open preset: ' + file)
		file = file.readlines()
		# adding these here because blocks_order_count *sometimes* does not get set to zero
		# this should not be nessesary, but I'd rather bandaid it right now
		self.blocks_order_count = 0
		self.blocks_chunk_count = 0
		self.order_count = 0
		current_block_gene = ""
#		self.tree['blocks'] = []
#		self.tree = {}
#		self.blocks = []
#		self.order = []

	#   blah = { 'tree':[ [ depth, var ],.. ], 'reference':{ var:count, } }

	#   depth = 0
	#   count = 0
		for line in file:
			# reset flag
			flag = False
#			print line
			line = line[:-1]
			if line[-1] == '\r':
				line = line[:-1]
			if line == '':
				continue
			if sre.match('^//.*', line):
				continue
			if sre.match('\[preset.*', line):
				continue
			# more ignores for pixel shaders - this ignore section should be made pretty one day
			if sre.match('MILKDROP_PRESET_VERSION.*', line):
				continue
			if sre.match('PSVERSION.*',line):
				continue
			# end pixel shader ignores
			gene, line = sre.split('=', line, 1)
#			gene = line[0]
#			line = line[1]
#			self.tree[gene] = []
			# we like blank lines now?
#			# in case of null line set to zero
#			try:
#				tline = line[1]
#				line = tline
#			except:
#				line = '0'
#			if line == '':
#				line = '0'

			if self.order.has_key(gene):
				#print "duplicate! skipping", `gene`
				continue

			self.order_count += 1
			self.order[gene] = self.order_count
			#print `self.order`
			# check gene
#			for gene in self.tree:
#				if sre.match('^wavecode', gene):
#					print gene
#					print self.tree[gene]
#					print "connot be done 1"
#					sys.exit()
#			print "step 1"
			if projectm_genes.has_key(gene):
#				if sre.match('^wavecode', gene):
#					print "how'd i get in here?"
#					print gene
#				print "whoops?", gene
				# got a predefined gene
				# these are to be initialized only
				# if they aren't the right kind of value, fix them
				if projectm_genes[gene]['type'] == 'int':
					# check the value to see if it's valid
					fail_flag = False
					try:
						t_val = int(line)
						if projectm_genes[gene]['max'] and t_val > projectm_genes[gene]['max']:
							#print "over max"
							raise
						if projectm_genes[gene]['min'] and t_val < projectm_genes[gene]['min']:
							#print "over under min"
							raise
						#if t_val > projectm_genes[gene]['max'] or t_val < projectm_genes[gene]['min']:
						#	# not a valid value! raise an exception to fix it
						#	raise
					except:
						# not an int when it's supposed to be!
						fail_flag = True

					# try to change it
					if fail_flag:
						try:
							t_val = int(float(line))
							if projectm_genes[gene]['max'] and t_val > projectm_genes[gene]['max']:
								#print "over max"
								raise
							if projectm_genes[gene]['min'] and t_val < projectm_genes[gene]['min']:
								#print "over under min"
								raise
							#if t_val > projectm_genes[gene]['max'] or t_val < projectm_genes[gene]['min']:
							#	# not a valid value! raise an exception to fix it
							#	raise
							fail_flag = False
							#line = t_val
							#print "gene fixed: ", gene, line
						except:
							fail_flag = True
					# fill in 0 for now
					if fail_flag:
						#print "gene zeroed: ", gene
						#print "offender: ", `line`
						line = '0'
						#print "to1: ", line
					# set the values in the DNA and continue
#					print gene
					self.tree[gene] = line
					continue
				elif projectm_genes[gene]['type'] == 'float':
					# check the value to see if it's valid
					fail_flag = False
					try:
						t_val = float(line)
						if projectm_genes[gene]['max'] and t_val > projectm_genes[gene]['max']:
							#print "over max"
							raise
						if projectm_genes[gene]['min'] and t_val < projectm_genes[gene]['min']:
							#print "over under min"
							raise
						#if t_val > projectm_genes[gene]['max'] or t_val < projectm_genes[gene]['min']:
						#	# not a valid value! raise an exception to fix it
						#	raise
					except:
						# not a float when it's supposed to be!
						fail_flag = True
					# try to change it
					if fail_flag:
						try:
							t_val = float(int(line))
							if projectm_genes[gene]['max'] and t_val > projectm_genes[gene]['max']:
								#print "over max"
								raise
							if projectm_genes[gene]['min'] and t_val < projectm_genes[gene]['min']:
								#print "over under min"
								raise
							#if t_val > projectm_genes[gene]['max'] or t_val < projectm_genes[gene]['min']:
							#	# not a valid value! raise an exception to fix it
							#	raise
							fail_flag = False
							#line = t_val
							#print "gene fixed: ", gene, line
						except:
							fail_flag = True
					
					# fill it with the default 0.0 now
					if fail_flag:
						#print "gene zeroed: ", gene
						#print "offender: ", `line`
						line = '0.0'
						#print "to2: ", line
					# set the values in the DNA and continue
#					print gene
					self.tree[gene] = line
					continue
				else:
					print "this shouldn't happen 1"
					print gene
					print projectm_genes[gene]['type']
					sys.exit()
#			print "step 2 blocks"
			# must be block code, check for initialization types
			# matches wavecode and shapecode
#			if sre.match(init_check, gene):
#			print "stage 2", gene
			if gene[:8] == 'wavecode':
#				print "stage 2 wave", gene
				type_flag = 'wave'
				# set check dictionary
				gene_check = projectm_wave_genes
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 0
				flag = True
			elif gene[:9] == 'shapecode':
#				print "stage 2 shape", gene
				type_flag = 'shape'
				# set check dictionary
				gene_check = projectm_shape_genes
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 5
				flag = True
			# pixel shader "block"
			elif sre.match('^b[0-9].*', gene):
				type_flag = 'pixel shader'
				gene_check = projectm_pixel_shader_genes
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				flag = True
			else:
				flag = False
#				if sre.match(wavecode_check, gene):
#					# set check dictionary
#					gene_check = projectm_wave_genes
#					# set main order number 0 for wavecode
#					main_order = 0
#				elif sre.match(shapecode_check, gene):
#					# set check dictionary
#					gene_check = projectm_shape_genes
#					# set main order number 4 for shapecode
#					main_order = 4
#				else:
#					print "what? no.", gene
#					sys.exit()
			# wavecode and shapecode section
			# this is for init style genes
			if flag:
				#print `gene`
				if type_flag == 'pixel shader':
					# cheating for now, this just chops off the first two characters, i.e. b#
					# this will fail if we ever have 10 or more pixel shaders
					gene_parts = [ gene[:1], gene[1:2], gene[2:] ]
				else:
					gene_parts = gene.split('_', 2)
				#print `gene_parts`
				if gene_check.has_key(gene_parts[2]):
#					print "guh?", gene_parts
					# a predefined sub-gene
					# these are to be initialized only
					# if they aren't the right kind of value, fix them
					if gene_check[gene_parts[2]]['type'] == 'int':
						# check the value to see if it's valid
						fail_flag = False
						try:
							t_val = int(line)
							if gene_check[gene_parts[2]]['max'] and t_val > gene_check[gene_parts[2]]['max']:
								#print "over max"
								raise
							if gene_check[gene_parts[2]]['min'] and t_val < gene_check[gene_parts[2]]['min']:
								#print "over under min"
								raise
							#if t_val > gene_check[gene_parts[2]]['max'] or t_val < gene_check[gene_parts[2]]['min']:
							#	# not a valid value! raise an exception to fix it
							#	raise
						except:
							#print "what's this?", `gene_check[gene_parts[2]]`, `gene_parts[2]`, `line`
							fail_flag = True
						# try to change it
						if fail_flag:
							try:
								t_val = int(float(line))
								if gene_check[gene_parts[2]]['max'] and t_val > gene_check[gene_parts[2]]['max']:
									#print "over max"
									raise
								if gene_check[gene_parts[2]]['min'] and t_val < gene_check[gene_parts[2]]['min']:
									#print "over under min"
									raise
								#if t_val > projectm_genes[gene_parts[2]]['max'] or t_val < projectm_genes[gene_parts[2]]['min']:
								#	# not a valid value! raise an exception to fix it
								#	raise
								fail_flag = False
								#line = t_val
								#print "gene fixed: ", gene, line
							except:
								# not an int when it's supposed to be!
								fail_flag = True
						if fail_flag:
							# fill in 0 for now
							#print "gene zeroed: ", gene
							#print "offender: ", `line`
							line = '0'
							#print "to3: ", line
						# set this as a block gene
						# type = init or script
						# value is a tuple: number, order number, wave or shape, type, sub-gene, value (or parser list)
						#print "add1", `order_number`, `gene_parts`, "init"
						if not current_block_gene == (gene_parts[1],  gene_parts[0]):
							current_block_gene = (gene_parts[1],  gene_parts[0])
							self.blocks_chunk_count += 1
						self.blocks.append( ( self.blocks_chunk_count, order_number, int(gene_parts[1]),  gene_parts[0], 'init', gene_parts[2]) )
						self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2])] = line
						continue
					elif gene_check[gene_parts[2]]['type'] == 'float':
						# check the value to see if it's valid
						fail_flag = False
						try:
							t_val = float(line)
							if gene_check[gene_parts[2]]['max'] and t_val > gene_check[gene_parts[2]]['max']:
								#print "over max"
								raise
							if gene_check[gene_parts[2]]['min'] and t_val < gene_check[gene_parts[2]]['min']:
								#print "over under min"
								raise
							#if t_val > gene_check[gene_parts[2]]['max'] or t_val < gene_check[gene_parts[2]]['min']:
							#	# not a valid value! raise an exception to fix it
							#	raise
						except:
							# not a float when it's supposed to be!
							fail_flag = True

						# try to change it
						if fail_flag:
							try:
								t_val = float(int(line))
								if gene_check[gene_parts[2]]['max'] and t_val > gene_check[gene_parts[2]]['max']:
									#print "over max"
									raise
								if gene_check[gene_parts[2]]['min'] and t_val < gene_check[gene_parts[2]]['min']:
									#print "over under min"
									raise
								#if t_val > projectm_genes[gene_parts[2]]['max'] or t_val < projectm_genes[gene_parts[2]]['min']:
								#	# not a valid value! raise an exception to fix it
								#	raise
								fail_flag = False
								#line = t_val
								#print "gene fixed: ", gene, line
							except:
								# not an int when it's supposed to be!
								fail_flag = True
						if fail_flag:
							# fill it with the default 0.0 now
							#print "gene zeroed: ", gene
							#print "offender: ", `line`
							line = '0.0'
							#print "to4: ", line
						# set this as a block gene
						# type = init or script
						# value is a tuple: number, order number, wave or shape, type, sub-gene, value (or parser list)
						#print "add2", `order_number`, `gene_parts`, "init"
						if not current_block_gene == (gene_parts[1],  gene_parts[0]):
							current_block_gene = (gene_parts[1],  gene_parts[0])
							self.blocks_chunk_count += 1
						self.blocks.append( ( self.blocks_chunk_count, order_number, int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2]) )
						self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2])] = line
						continue
					# ignore types, do not change in any way
					elif gene_check[gene_parts[2]]['type'] == 'ignore':
						# adding the gene without checking or modifying in any way
						if not current_block_gene == (gene_parts[1],  gene_parts[0]):
							current_block_gene = (gene_parts[1],  gene_parts[0])
							self.blocks_chunk_count += 1
						self.blocks.append( ( self.blocks_chunk_count, order_number, int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2]) )
						self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2])] = line
						continue
					# special for many images mutation
					elif gene_check[gene_parts[2]]['type'] == 'images':
						# adding the gene without checking or modifying in any way
						if not current_block_gene == (gene_parts[1],  gene_parts[0]):
							current_block_gene = (gene_parts[1],  gene_parts[0])
							self.blocks_chunk_count += 1
						self.blocks.append( ( self.blocks_chunk_count, order_number, int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2]) )
						self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'init', gene_parts[2])] = line
						continue
					else:
						print "this shouldn't happen 2 - images"
						print gene
						print gene_parts[2]
						print gene_check[gene_parts[2]]['type']
						sys.exit()
				else:
					print "this shouldn't happen 2.5"
					print gene
					print gene_parts
					print gene_check[gene_parts[2]]['type']
					sys.exit()
				#continue
			# from here out every line should be a "scriptable" line
			# first let's see if it belongs to a block
#			if sre.match(block_script_check, gene):
			if gene[:5] == 'wave_':
#				print "stage 3 wave", gene
				flag = True
				type_flag = 'wave'
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 0
			elif gene[:6] == 'shape_':
#				print "stage 3 shape", gene
				flag = True
				type_flag = 'shape'
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 5
			else:
				# must be per_pixel, per_frame, or per_frame_init
				flag = False
			pixel_shader_flag = False
			if flag:
				# these are part of "blocks" still
				# ok, all these lines are "script types"
#				# check and set type flag
#				if sre.match(block_wave_script_check, gene):
#					type_flag = wave
#				elif sre.match(block_shape_script_check, gene):
#				else:
#					print "what? no. 2.7"
#					print gene
#					sys.exit()
				# three sub types are init, per_frame, and per_pixel
				gene_parts = gene.split('_', 2)
#				if sre.match(sub_init_check, gene_parts[2]):
				if gene_parts[2][:4] == 'init':
					# it's an init sub number
					sub_number = gene_parts[2][4:]
					#order_number += 1
					gene_parts[2] = gene_parts[2][:4]
				# does not exist
#				elif sre.match(sub_point_init_check, gene_parts[2]):
#					# it's a per_point sub init sub number
#					sub_number = gene_parts[2][14:]
				# frame_init check first!
				elif gene_parts[2][:14] == 'per_frame_init':
					# frame init line
					sub_number = gene_parts[2][14:]
					#order_number += 2
					gene_parts[2] = gene_parts[2][:14]
#				elif sre.match(frame_check, gene_parts[2]):
				elif gene_parts[2][:9] == 'per_frame':
					# it's a per_frame sub number
					sub_number = gene_parts[2][9:]
					#order_number += 3
					gene_parts[2] = gene_parts[2][:9]
#				elif sre.match(point_check, gene_parts[2]):
				elif gene_parts[2][:9] == 'per_point':
					# it's a per_point sub number
					sub_number = gene_parts[2][9:]
					#order_number += 4
					gene_parts[2] = gene_parts[2][:9]
				else:
					print "this shouldn't happen 3"
					print gene
					print gene_parts
					print gene_parts[2]
					sys.exit()
				# value is a tuple: wave or shape, number, type, sub-gene, value (or parser list)
#				gene_line = ( gene[0], gene[1], 'script', gene_parts[2], sub_number, line )
#				self.tree['blocks'].append( ( gene[0], gene[1], 'script', gene_parts[2], sub_number, line ) )
				#continue
			# it's not a block, so it's a per_frame, per_point, or per_frame_init
			# do frame_init check first!
#			elif sre.match(frame_init_check, gene):
			elif gene[:14] == 'per_frame_init':
				number = gene[15:]
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 'a'
				gene_parts = [ gene[:14], number ]
			# do frame check now, it should be this no matter what now
#			elif sre.match(frame_check, gene):
			elif gene[:9] == 'per_frame':
				number = gene[10:]
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 'b'
				gene_parts = [ gene[:9], number ]
#			elif sre.match(pixel_check, gene):
			elif gene[:9] == 'per_pixel':
				# these are script lines, nothing special, just numbered in order
				# these are considered their own block
				number = gene[10:]
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				#order_number = 'c'
				gene_parts = [ gene[:9], number ]
			# pixel shader blocks here
			# for now this does nothing except pass them along unmodified as an entire block
			elif gene[:4] == 'comp':
				number = gene[5:]
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				gene_parts = [ gene[:4], number ]
				pixel_shader_flag = True
			elif gene[:4] == 'warp':
				number = gene[5:]
				self.blocks_order_count += 1
				order_number = self.blocks_order_count
				gene_parts = [ gene[:4], number ]
				pixel_shader_flag = True
			# end pixel shader stuff
			else:
				print "this shouldn't happen 4"
				print gene
				print gene_parts
				print sys.exit()

			# don't touch the pixel shader stuff, it's all crazy
			if pixel_shader_flag:
				eq_dna = line
			else:
				# not a pixel shader, parse that equation
				eq_dna = self.parser(line, verbose)
#			print gene_parts
#			print gene_parts.index(gene_parts[-1])
			if gene_parts.index(gene_parts[-1]) == 1:
				#print "add3", `order_number`, `gene_parts`, "post-script"
				if not current_block_gene == gene_parts[0]:
					current_block_gene = gene_parts[0]
					self.blocks_chunk_count += 1
				if pixel_shader_flag:
					self.blocks.append( ( self.blocks_chunk_count, int(gene_parts[1]), gene_parts[0], 'pixel shader') )
					self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'pixel shader')] = eq_dna
				else:
					self.blocks.append( ( self.blocks_chunk_count, int(gene_parts[1]), gene_parts[0], 'post-script') )
					self.blocks_content[( int(gene_parts[1]), gene_parts[0], 'post-script')] = eq_dna
			else:
				#print "add4", `order_number`, `gene_parts`, "script"
				if not current_block_gene == (int(gene_parts[1]), gene_parts[0]):
					current_block_gene = (int(gene_parts[1]), gene_parts[0])
					self.blocks_chunk_count += 1
				self.blocks.append( ( self.blocks_chunk_count, int(gene_parts[1]), int(sub_number), 'script', gene_parts[0], gene_parts[2]) )
				self.blocks_content[( int(gene_parts[1]), int(sub_number), 'script', gene_parts[0], gene_parts[2])] = eq_dna
		#############
		#
		# Post Processing
		#
		#block_post_order = 0
		#current_gene = ""
		#for line in self.blocks:
		#	if not current_gene == line:
		#		current_gene = line
		#		block_post_order += 1
		#	
		#
		# End Post Processing
		#
		#############
		#print `self.order`
		self.blocks.sort()
		#print `self.blocks`
#		for gene in self.tree:
#			if sre.match('^wavecode', gene):
#				print self.blocks
#				for gene in self.tree:
#					print gene
#					print self.tree[gene]
#				print "connot be done"
#				sys.exit()
#		for gene in self.tree['blocks']:
#			print gene
	#	   count += 1
	
	def writeFile(self, count, generation, presets_directory, milkdrop, pretend):
		"""This writes out the new Child preset, numbering it"""
		if not pretend:
			if milkdrop:
				file = open(presets_directory + 'GeneticM-' + `generation` + '-' + `count` + '.milk', 'w')
			else:
				file = open(presets_directory + 'GeneticM-' + `generation` + '-' + `count` + '.prjm', 'w')
			file.write('[preset00]\n')
	#   print child
		#print "nothin"
		self.parents_order = sorted(self.parents_order)
		#print self.parents_order
		# changing to preserve ordering
		a = type('a')
		for gene in self.parents_order:
			line = gene[1]
#		for line in self.tree:
			# completely changed, much simplier
#			try:
#				temp = self.tree[line][1]
#				full_line = ''
#				for branch in self.tree[line]:
#					full_line += branch[1]
#	#		   print 'equation: ' + full_line
			if not pretend:
#				print line, self.tree[line]
				if not a == type(self.tree[line]):
					file.write(line + '=' + `self.tree[line]` + '\n')
				else:
					file.write(line + '=' + self.tree[line] + '\n')
#			except:
#				# not an equation, just print it and move on
#				if not self.tree[line]:
#					print line
#					print self.tree[line]
#					self.tree[line].append('0')
	#		   print 'number: ' + `child['tree'][line]`
	#		   print child['tree'][line]
#				if not pretend:
#					file.write(line + '=' + self.tree[line][0] + '\n')
		# not the correct solution
		# set variable 'a' to type object string for use in comparisons
		a = type('a')
		#print `self.blocks`
		for line in self.blocks:
			if line[3] == 'script':
				gene = line[4] + '_' + `line[1]` + '_' + line[5] + `line[2]`
				full_line = ''
				try:
					t_val = self.blocks_content[ line[1:] ][0][1]
					# if that works, then it's a list
					for part in self.blocks_content[ line[1:] ]:
						if not a == type(part[1]):
							part[1] = `part[1]`
						full_line += part[1]
				except:
					# not a list
					full_line = self.blocks_content[ line[1:] ]
					if not a == type(full_line):
						full_line = `full_line`
#				print gene, full_line
				# change an empty list to a blank string
				if full_line == [] or full_line == "[]":
					full_line = ''
				file.write(gene + '=' + full_line + '\n')
			elif line[3] == 'post-script':
				gene = line[2] + '_' + `line[1]`
				full_line = ''
				try:
					t_val = self.blocks_content[ line[1:] ][0][1]
					# if that works, then it's a list
					for part in self.blocks_content[ line[1:] ]:
						if not a == type(part[1]):
							part[1] = `part[1]`
						full_line += part[1]
				except:
					# not a list
					full_line = self.blocks_content[ line[1:] ]
					if not a == type(full_line):
						full_line = `full_line`
#				print gene, full_line
				# change an empty list to a blank string
				if full_line == [] or full_line == "[]":
					full_line = ''
				file.write(gene + '=' + full_line + '\n')
			elif line[3] == 'pixel shader':
				#print "here", `line`
				gene = line[2] + '_' + `line[1]`
				full_line = self.blocks_content[ line[1:] ]
				if not a == type(full_line):
					full_line = `full_line`
				file.write(gene + '=' + full_line + '\n')
			elif line[4] == 'init':
				#print `line`, line[3], line[2], line[5]
				# shitty bandaid fix to pixel shaders - I'll regret this later
				if line[3] == "b":
					gene = line[3] + `line[2]` + line[5]
				else:
					gene = line[3] + '_' + `line[2]` + '_' + line[5]
				full_line = ''
#				print gene, full_line
#				for part in self.blocks_content[line]:
#					if not a == type(part[1]):
#						part[1] = `part[1]`
#					full_line += part[1]
				full_line = self.blocks_content[ line[2:] ]
				if not a == type(full_line):
					full_line = `full_line`
#				print gene, full_line
				if full_line == []:
					full_line = ''
				file.write(gene + '=' + full_line + '\n')
			else:
				print "god damnit, why do i make these mistakes?"
				print line
				sys.exit()
		if not pretend:
			for parent in self.parents_names:
				file.write('//' + parent + '\n')
			file.close()
		return
	
	def parser(self, line, verbose):
		"""This parser is a copy of the original equation_mutator
		instead it will create the equation list tree for the new format"""
		parsed_list = []
		parens = []
		specials = []
		operators = []
		operator_flag = False
		old_line = ''
		new_line = ''
		depth = 0
		# serious equation mutation
		while True:
			if verbose:
				print line
				print parsed_list
			if old_line == line:
				#sys.exit('this help?')
				pass
			old_line = line
			# check one character at a time until we find a word like section
			if sre.match(comments_check, line):
				break
			if sre.match(end_line_check, line):
				break
			count = 0
			for char in line:
				if char == ' ':
					# skip spaces
					count += 1
					continue
				if char == ';':
					# add semi-colon, remove, and break
	#			   new_line += char
					depth += 1
					parsed_list.append( [ depth, char, 'end' ] )
					count += 1
					break
				if char == ',':
	#			   new_line += char
	#			   depth -= 1
					parsed_list.append( [ depth, char, 'seperator' ] )
					count += 1
					continue
				if sre.match(operator_check, char):
					# need special circumstances for = !
	#			   if char != '=':
	#				   mutate = random.randint(0, lesser_mutation_chance)
	#				   if mutate == 0:
	#					   while char == '=' and char == '':
	#						   char = operator_mutation(char)
	#			   new_line += char
					operator_flag = char
	#			   depth += 1
					parsed_list.append( [ depth, char, 'operator' ] )
					count += 1
					continue
				if sre.match(parens_check, char):
					# for now lets not bother mutating any sort or parens
					if sre.match(open_parens_check, char):
	#				   new_line += char
						depth += 1
	#				   operator_flag = False
						parsed_list.append( [ depth, char, 'open' ] )
	#				   parens.append(char)
					else:
	#				   new_line += char
						parsed_list.append( [ depth, char, 'close' ] )
						depth -= 1
	#				   parens.pop(-1)
					count += 1
					continue
				break
			if count != 0:
				remove = sre.compile('^.{' + `count` + ',' + `count` + '}')
				line = sre.sub(remove, '', line, 1)
			# now check for variables or known functions
			if sre.match(function_check, line):
				parens.append('(')
				function = sre.findall(function_check, line)
				function = function[0]
	#		   if projectm_functions.has_key(function):
					# if we don't recognize the function then skip mutation and continue
	#			   specials.append(projectm_functions[function])
	#			   mutate = random.randint(0, lesser_mutation_chance)
	#			   if mutate == 0:
	#				   function = function_mutation(function)
				line = sre.sub(function_check, '', line, 1)
	#		   new_line += function
				depth += 1
				parsed_list.append( [ depth, function, 'function' ] )
				continue
			if sre.match(number_check, line):
				number = sre.findall(number_check, line)
				number = number[0]
	#		   mutate = random.randint(0, lesser_mutation_chance)
	#		   if mutate == 0:
	#			   try:
	#				   tnumber = float(number)
	#				   number = tnumber
	#				   number = float_mutation(number)
	#			   except:
	#				   number = number_mutation(number)
				line = sre.sub(number_check, '', line, 1)
				if number == '.':
					number = '.0'
				parsed_list.append( [ depth, number, 'number' ] )
	#		   new_line += number
				continue
			if sre.match(variable_check, line):
				variable = sre.findall(variable_get, line)
				variable = variable[0]
	#		   mutate = random.randint(0, lesser_mutation_chance)
	#		   if mutate == 0:
	#			   variable = variable_mutation(variable)
				line = sre.sub(variable_get, '', line, 1)
				parsed_list.append( [ depth, variable, 'variable' ] )
				### Print out user variables here, for fixing cross contamination
				if not projectm_variables.has_key(variable):
					# must be user set or a variable we arn't dealing with, ignore it
					#print "user var:", `variable`
					pass
				### End User var notification

	#		   depth += 1
	#		   new_line += variable
		# check for forgotten parens and close them
		# hopefully this code won't actually ever run
	#   if parens:
	#	   print parens
	#	   parens = parens.reverse()
	#	   for paren in parens:
	#		   if paren == '(':
	#			   new_line += ')'
	#		   else:
	#			   new_line += ']'
		return parsed_list
	
	def equation_swapping_mutator(self, max_swaps):
		"""swap equations for scripts"""
		swaps = random.randint(0, max_swaps)
		count = 0
		# build list of swappable lines
		swapables = {}
		for line in self.blocks:
			if line[3] == 'script' or line[3] == 'post-script':
				swapables[line] = self.blocks_content[ line[1:] ]
		# make all swaps happen
		while count < swaps:
			# pick two different lines from the swappable lines
			line_one = random.choice(swapables.keys())
			line_two = line_one
			while line_one == line_two:
				line_two = random.choice(swapables.keys())
			# what kind of swap, pre equal sign, or post?
			# True is post equal sign
			if random.randint(0, 1):
				# This makes more better change
				try:
					#print 'equal swap 1'
					# store the equaled variables
					line_one_var = swapables[line_one][0]
					line_two_var = swapables[line_two][0]
					#print 'equal swap 2'
					# swap the two lines
					self.blocks_content[ line_one[1:] ] = swapables[line_two]
					self.blocks_content[ line_two[1:] ] = swapables[line_one]
					#print 'equal swap 3'
					# set back the equaled variables
					self.blocks_content[ line_one[1:] ][0] = line_one_var
					self.blocks_content[ line_two[1:] ][0] = line_two_var
					#print 'equal swap'
					# success, finish up loop
					count += 1
					continue
				except:
					# failure sends you to pre equal swapping
					# This will happen if one or both lines are blank
					#from IPython.Shell import IPShellEmbed
					#ipshell = IPShellEmbed()
					#ipshell()
					pass
			# False is pre equal sign - will also arrive here if post equal fails
			# just swap contents straight up.
			#print 'line_one', `line_one`, `swapables[line_one]`
			#print 'line_two', `line_two`, `swapables[line_two]`
			self.blocks_content[ line_one[1:] ] = swapables[line_two]
			self.blocks_content[ line_two[1:] ] = swapables[line_one]
			count += 1
		return

	def object_mutator(self, max_shapes, max_waves):
		"""swap shapecode and wavecode numbers around with other shapecodes or wavecodes"""
		# shapecode or wavecode?
		if random.randint(0, 1) == 0:
			# zero is shapecode
			mutate_type = "shapecode"
			mutate_type_script = "shape"
			mutate_max = max_shapes
		else:
			# one is wavecode
			mutate_type = "wavecode"
			mutate_type_script = "wave"
			mutate_max = max_waves
		# pick two numbers
		object_one = random.randint(0, mutate_max)
		while True:
			object_two = random.randint(0, mutate_max)
			if not object_one == object_two:
				break
		#print "object number swap:", object_one, object_two
		# swap numbers
		count = 0
		for line in self.blocks:
			if line[3] == mutate_type:
				if line[2] == object_one:
 					new_line = (line[0], line[1], object_two, line[3], line[4], line[5])
					self.blocks[count] = new_line
					self.blocks_content[ new_line[2:] ] = self.blocks_content[ line[2:] ]
				elif line[2] == object_two:
					new_line = (line[0], line[1], object_one, line[3], line[4], line[5])
					self.blocks[count] = new_line
					self.blocks_content[ new_line[2:] ] = self.blocks_content[ line[2:] ]
			elif line[3] == "script" and line[4] == mutate_type_script:
				if line[1] == object_one:
 					new_line = (line[0], object_two, line[1], line[3], line[4], line[5])
					self.blocks[count] = new_line
					self.blocks_content[ new_line[1:] ] = self.blocks_content[ line[1:] ]
				elif line[1] == object_two:
					new_line = (line[0], object_one, line[2], line[3], line[4], line[5])
					self.blocks[count] = new_line
					self.blocks_content[ new_line[1:] ] = self.blocks_content[ line[1:] ]
			count += 1
		return

	def mutator(self, line, entry_gene, mutation_chances, type, verbose, images_flag=False):
		"""decide what kind of line it is and mutate accordingly"""
		mutate = random.randint(0, mutation_chances['mutation_chance'])
		#print "is it me?"
		#print entry_gene
		#if True:
		#	# not going to mutate, return the line
		#	return
		if mutate != 0:
			# not going to mutate, return the line
			return
		# check for different types, meaning different gene structures
		gene_check = {}
		type_flag = 'block'
		if type == 'init':
			gene = entry_gene[5]
			# block init offset is 2
			full_gene = entry_gene[2:]
			type_flag = 'block init'
			if entry_gene[3] == 'wavecode':
				gene_check = projectm_wave_genes
			elif entry_gene[3] == 'shapecode':
				gene_check = projectm_shape_genes
				if images_flag:
					# if images then change from "ignore" to "images" for ImageURL gene
					gene_check['ImageURL'] = images
			elif entry_gene[3] == 'b':
				gene_check = projectm_pixel_shader_genes
			else:
				print "crap, i dones it again"
				print entry_gene
				sys.exit()
		elif type == 'script':
			gene = entry_gene[2:]
		elif type == 'post-script':
			gene = entry_gene[2:]
		elif type == 'pre':
			type_flag = 'not_block'
			gene = entry_gene
			gene_check = projectm_genes
		elif type == 'pixel shader':
			# do not mutate
			return
		else:
			print "what the fuck did i do now?"
			print type
			print gene
			sys.exit()
		#print "gene check for gene_check:", `gene`
		if gene_check.has_key(gene):
			if gene_check[gene]['type'] == 'int':
				if gene_check[gene]['max'] and gene_check[gene]['max'] != 0:
					# mutate this int within it's valid values
					if type == 'pre':
						self.tree[gene] = `random.randint(gene_check[gene]['min'], gene_check[gene]['max'])`
						#print "11--", `gene`
					elif type == 'block':
						#print "11-", `gene`
						self.blocks_content[gene] = `random.randint(gene_check[gene]['min'], gene_check[gene]['max'])`
					else:
						# type == 'block init'
						#print "11-", `gene`
						self.blocks_content[full_gene] = `random.randint(gene_check[gene]['min'], gene_check[gene]['max'])`
				elif gene_check[gene]['min'] and gene_check[gene]['min'] != 0:
					# this can be any number greater than 0
					# give the abs of good old integer mutation
					if type == 'pre':
						self.tree[gene] = `abs(int(self.integer_mutation(line)))`
						#print "12--", `gene`
					elif type == 'block':
						#print "12-", `gene`
						self.blocks_content[gene] = `abs(int(self.integer_mutation(line)))`
					else:
						# type == 'block init'
						#print "12-", `gene`
						self.blocks_content[full_gene] = `abs(int(self.integer_mutation(line)))`
				else:
					# any value goes here
					# use traditional integer mutation
					if type == 'pre':
						self.tree[gene] = self.integer_mutation(line)
						#print "13--", `gene`
					elif type == 'block':
						#print "13-", `gene`
						self.blocks_content[gene] = self.integer_mutation(line)
					else:
						# type == 'block init'
						#print "13-", `gene`
						self.blocks_content[full_gene] = self.integer_mutation(line)
				return
			elif gene_check[gene]['type'] == 'float':
				# this should probably get fixed at some point
#				print "float mutation"
#				print line, gene
				new_number = self.float_mutation(line)
				# loop around and do crap until we get a value in the valid range
				# yeah this sucks, i'll fix it later
#				print "starting crappy float fix loop"
				while True:
					if gene_check[gene]['min'] and gene_check[gene]['min'] != 0 and new_number < gene_check[gene]['min']:
						new_number = random.random() + float(new_number)
					elif gene_check[gene]['max'] and gene_check[gene]['max'] !=0 and new_number > gene_check[gene]['max']:
						new_number = float(new_number) - random.random()
					else:
						# within the valid range
						#new_number = `new_number`
						break
					#print new_number, gene_check[gene]['min'], gene_check[gene]['max']
				if type == 'pre':
					self.tree[gene] = new_number
					#print "14--", `gene`
				elif type == 'block':
					#print "14-", `gene`
					self.blocks_content[gene] = new_number
				else:
					# type == 'block init'
					#print "14-", `gene`
					self.blocks_content[full_gene] = new_number
#				print "done with crappy float fix loop"
			elif gene_check[gene]['type'] == 'ignore':
				# do nothing
				pass
			# special many images mutation
			elif gene_check[gene]['type'] == 'images':
				# select new image number
				print "successful image mutate"
				print "gene:", `gene`
				# we know images are block init type, no need to check
				self.blocks_content[full_gene] = `random.randint(gene_check[gene]['min'], gene_check[gene]['max'])` + '.tga'
				print "image mutate new     :", `self.blocks_content[full_gene]`
				for i in self.blocks_content:
					print i
			else:
				print "what?"
				print gene
				print gene_check[gene]
				sys.exit()
#			print "did i mess up?"
#			print gene
			return
# all lines from here out are now scripts, treat them as such
		#print "15-", `gene`
		self.blocks_content[gene] = self.equation_mutator(line, mutation_chances, verbose)

		# redundent check now *shrug*
#		if line == [] or line == None:
#			line = '0'
		# start old mutator code, this will probably become the code for scripting lines only
		# at some point there should be some checks here to verify
		# we are returning correct values for specific variables
		# for now let's cut some corrners and just get the
		# equation mutation working
	#   new_line = line[0] + '='
#		new_line = []
	#   line = line[1]
#		if verbose:
#			print "----------------------------------------------------------"
#			print line
		# yeah, stupid, but i'll fix it later
#		tflag = False
#		try:
#			tline = line[1]
#			tflag = True
#			# if it has more than one element then it's an equation
#			new_line = self.equation_mutator(line, mutation_chances, verbose)
#			if verbose:
#				print new_line
#			self.tree[gene] = new_line
#			return
#		except:
#			pass
#		if tflag:
#			new_line = self.equation_mutator(line, mutation_chances, verbose)
#			self.tree[gene] = new_line
#			return
#		try:
#			tline = int(line[0])
#			# we've got a number only, let's do a dice toss to see
#			# if we mutate it with an equation
#			new_line.append(self.integer_mutation(line[0]))
#			if verbose:
#				print new_line
#			self.tree[gene] = new_line
#			return
#		except:
#			pass
#		if sre.match(number_only, line[0]):
#			# we've got a number only, let's do a dice toss to see
#			# if we mutate it with an equation
#			try:
#				tline = float(line[0])
#	#		   line = tline
#				new_line.append(self.float_mutation(line[0]))
#			except:
#				new_line.append(self.number_mutation(line[0]))
#			if verbose:
#				print new_line
#			self.tree[gene] = new_line
#			return
#		# this should never happen! freak out!
#		print "nnnnnoooooooooo!"
#		print "i was trying to match this: ", line[0]
#		print "full line: ", line
#		sys.exit('ender')
		return

	def equation_mutator(self, equation, mutation_chances, verbose):
		"""new equation mutator for the new format"""
		# really really really basic, just impliment the old functionality with the new code
		if verbose:
			print "equation_mutator", equation
		type_flag = False
		branch_skip = 0
		new_equation = []
		#print "equation:", `equation`
		for branch in equation:
			if branch_skip < 0:
				#print "branch_skip", branch_skip
				branch_skip += 1
				continue
			if type_flag:
				new_equation = self.addition_post(type_flag, branch, new_equation)
				type_flag = False
			mutate = random.randint(0, mutation_chances['lesser_mutation_chance'])
			if mutate != 0:
				# do not mutate this
				new_equation.append(branch)
				continue
			if branch[2] == 'number':
				try:
					temp = int(branch[1])
					branch[1] = self.integer_mutation(branch[1])
					#print "int mute"
				except:
					# not an int
					pass
				try:
#					print "float test"
					temp = float(branch[1])
#					print "hey-ok", temp
					branch[1] = self.float_mutation(branch[1])
					#print "float mute"
#					print "what now?", branch
				except:
					# not a float
					# this should never happen
					# it's either an int or a float
					print "no number_mutats: ", branch
					#branch[1] = self.number_mutation(branch[1])
			elif branch[2] == 'operator':
				branch[1] = self.operator_mutation(branch[1])
			elif branch[2] == 'variable':
				branch[1] = self.variable_mutation(branch[1])
			elif branch[2] == 'function':
#				print "skipping function mutation till other stuff actually works"
#				continue
				branch[1], function_changes = self.function_mutation(branch[1])
				####
				# possible post function cleanup being built
				#print "no ", function_changes
				while function_changes != 0:
					#print "function changes=", function_changes
					if function_changes > 0:
						# the constructor is how many "equation parts" will be randomly generated and added to make a branch
						constructor = random.randint(1, mutation_chances['constructor'])
						insert_branch = [ branch[0], ',', 'seperator' ]
						while constructor > 0:
							new_equation, type_flag = self.addition_mutator(insert_branch, new_equation, verbose)
							new_equation = self.addition_post(type_flag, new_equation[-1], new_equation)
							insert_branch = new_equation[-1]
							type_flag = False
							constructor -= 1
						new_equation.append(insert_branch)
						function_changes -= 1
					elif function_changes < 0:
						branch_skip = function_changes
						#print "new branch_skip", branch_skip
						break
				# end
				###
			new_equation.append(branch)
			mutate = random.randint(0, mutation_chances['addition_chance'])
			if mutate == 0:
				# still really sucks, really just testing code
				results = self.addition_mutator(branch, new_equation, verbose)
				new_equation = results[0]
				type_flag = results[1]
#		print new_equation
		return new_equation

	def addition_post(self, type_flag, branch, new_equation):
		"""This is the post function for the addition mutator
		this does the cleanup to make sure additions are followed by sane syntax"""
		# addition just happened, verify stuff
		if type_flag == 'number' or type_flag == 'variable':
			if branch[2] == 'number' or branch[2] == 'variable' or branch[2] == 'open' or branch[2] == 'function':
				# we need an operator between these
				new_operator = self.operator_mutation(' ')
				new_equation.append( [ branch[0], new_operator, 'operator' ] )
		elif type_flag == 'function':
			# no code for here yet
			pass
		return new_equation

	def integer_mutation(self, number):
		"""This takes a float and mutates it, returning another float"""
		# kinda gross, but takes care of divide by zero and any other unexpected error
		# fix the float<->int issue
		bad_flag = False
		try:
			number = int(number)
		except:
			bad_flag = True
		if bad_flag:
			try:
				bad_flag = True
				number = int(float(number))
			except:
				bad_flag = False
			# did we fix it?
			if not bad_flag:
				print "I'm all wrong!", `number`
				sys.exit()
		while True:
			try:
				mutation = random.randint(0,9)
				type = random.randint(0,11)
				if type <= 4:
					new_int = number + mutation
				elif type <= 9:
					new_int = number - mutation
				elif type == 10:
					new_int = number * mutation
				elif type == 11:
					new_int = number / mutation
				break
			except:
				pass
		new_int = `new_int`
		return new_int

	def float_mutation(self, number):
		"""This takes a float and mutates it, returning another float"""
		# kinda gross, but takes care of divide by zero and any other unexpected error
#		print "i'm a float"
#		print "float loop"
		bad_flag = False
		try:
			number = float(number)
		except:
			bad_flag = True
		if bad_flag:
			try:
				bad_flag = True
				number = float(int(number))
			except:
				bad_flag = False
			# did we fix it?
			if not bad_flag:
				print "I'm all wrong!", `number`
				sys.exit()
		while True:
			try:
#				print "generateing"
#				print number
				#number = float(number)
#				print "num", number
				mutation = random.random()
#				print "m", mutation
				type = random.randint(0,11)
#				print "t", type
#				print "all", number, mutation, type
#				print "type number", type
				if type <= 4:
					new_float = number + mutation
				elif type <= 9:
					new_float = number - mutation
				elif type == 10:
					new_float = number * mutation
				elif type == 11:
					new_float = number / mutation
				new_float = `new_float`
				new_float = new_float[:5]
				break
			except:
				break
#		print "i'm free!"
		return new_float

	def number_mutation(self, number): 
		"""This takes a number and mutates it, some better code will be here soon
		This has become the fallback mutation for numbers that don't appear to fall
		into any of the correct categories"""
		# not an intiger, let's be crazy
		number_parts = number
		new_number = []
		print "I shouldn't be here"
		for char in number_parts:
			while True:
				try:
					# is it an intiger?
					char_int = int(char)
					# basic intiger mutation
					mutation = random.randint(0, 9)
					mtype = random.randint(0, 11)
					if mtype <= 4:
						char = char_int + mutation
					elif mtype <= 9:
						char = char_int - mutation
					elif mtype == 10: 
						char = char_int * mutation
					elif mtype == 11:
						char = char_int / mutation
					char = `char`
					break
				except:
					print "this didn't work"
					break
			new_number.append(char)
		# rebuild and assign our new line
		full_number = ""
		for char in new_number:
			full_number += char
		# try to fix the number now
		if sre.match('^\'.*', full_number) and sre.match('.*\'$', full_number):
			full_number = full_number[1:-1]
		try:
			full_number = int(full_number)
		except:
			print "number_mutation: fail inting", full_number, full_number[1:]
		try:
			full_number = float(full_number)
		except:
			print "number_mutation: fail floating", type(full_number)
		return full_number

	def operator_mutation(self, operator):
		"""operator mutation"""
		# wow, this should really get more complex, or just be merged into the parser code
		# but for now it seems best to break it out, still lots of special situations
		# that arn't being considered
		#
		# ^I had no idea how the = thing worked before
		# I *think* my line swapping code delt with this.
		if operator == '=':
			return operator
		# what is below here in this fuction is stupid and wrong, I don't know why I'm leaving it here
		#print "operator:", operator
		new_operator = '='
		while new_operator == '=':
			new_operator = random.choice(projectm_operators)
		#print "new operator:", new_operator
		return new_operator

	def variable_mutation(self, variable):
		"""variable mutation
		for now, if it's a user defined variable, do nothing
		if it's a projectm variable then give it a go at mutation"""
		if not projectm_variables.has_key(variable):
			# must be user set or a variable we arn't dealing with, ignore it
			#print "user var!", `variable`
			return variable
		# yeah, that same gross way of getting a random variable
		# oh well, it has to be gutted later anyway
		count = random.randint(1, 200)
		while count != 0:
			for new_variable in projectm_variables:
				if count == 0:
					break
				count -= 1
		return new_variable

	def function_mutation(self, function):
		"""function mutation"""
		# this is going to be a bitch, for now let's just do something basic and fix it later
		function = function.lower()
	#   if function == 'if(':
			# not dealing with mutating differing number of expressions for functions yet
			# since if is the only function with three expressions we'll just pass it back
	#	   return function
		try:
			expressions = projectm_functions[function]
		except: 
			print "not a valid projectm function! run like hell!"
			print `function`
			return function
		# since a dictionary is in random order this sorta works
		# yeah, it sucks, but this should become obseanly more complex later anyway
	#   while True:
			# loop around the dictionary a bunch of times to get random place
		count = random.randint(1, 200)
		while count != 0:
			for new_function in projectm_functions:
				if count == 0:
					break
				count -= 1
			# try this? probably won't work
		#   if projectm_functions[new_function] < expressions:
		#	   changes = expressions - projectm_functions[new_function]
		#   else:   
			changes = projectm_functions[new_function] - expressions
	#	   if projectm_functions[new_function] == expressions:
	#		   break
		####		
		# possible post function cleanup being built
	#   while changes != 0: 
	#	   print "function chances=" + `function_changes`
	#	   if function_changes > 0:
	#		   constructor = random.randint(1, mutation_chances['constructor'])
	#		   insert_branch = [ branch[0], ',', 'seperator' ]
	#		   new_equation.append(insert_branch)
	#		   while constructor > 0:
	#			   results = addition_mutator(insert_branch, new_equation, verbose)
	#			   new_equation = results[0]
	#			   type_flag = results[1]
	#			   new_equation = addition_post(type_flag, new_equation[-1], new_equation)
	#			   insert_branch = new_equation[-1]
	#			   type_flag = False
		# end
		###
		return (new_function, changes)

	def addition_mutator(self, branch, new_equation, verbose):
		"""This creates a new branch of equation to be added to an equation being mutated"""
		# this is still really really really basic code
		#verbose = True
		if verbose:
			print "orig_equation:", `new_equation`
		type = random.randint(0,2)
		if type == 0:
			type_flag = 'number'
			# number
			if branch[2] == 'number' or branch[2] == 'variable' or branch[2] == 'close':
				# add an operator before the new number
				new_operator = self.operator_mutation(' ')
				if verbose:
					print 'YO! --------- ' + `branch[0]` + ' ' + new_operator + ' operator'
				new_equation.append( [ branch[0], new_operator, 'operator' ] )
	#	   elif branch[2] == 'operator' or branch[2] == 'function' or branch[2] == 'open':
	#		   # operators and functions don't need operators before them
	#		   new_operator = None
			# float or int?
			if random.randint(0,1) == 0:
				new_number = self.integer_mutation('0')
			else:
				new_number = self.float_mutation('0')
			if verbose:
				print 'YO! --------- ' + `branch[0]` + ' ' + new_number + ' number'
			new_equation.append( [ branch[0], new_number, 'number' ] )
		elif type == 1:
			type_flag = 'variable'
			# variable
			if branch[2] == 'number' or branch[2] == 'variable' or branch[2] == 'close':
				# add and operator before the new variable
				new_operator = self.operator_mutation(' ')
				if verbose:
					print 'YO! --------- ' + `branch[0]` + ' ' + new_operator + ' operator'
				new_equation.append( [ branch[0], new_operator, 'operator' ] )
	#	   elif branch[2] == 'operator' or branch[2] == 'function' or branch[2] == 'open':
	#		   # operators and functions don't need operators before them
	#		   new_operator = None
			# pass it a valid projectm variable so that it will successfully mutate it
			new_variable = self.variable_mutation('zoom')
			if verbose:
				print 'YO! --------- ' + `branch[0]` + ' ' + new_variable + ' variable'
			new_equation.append( [ branch[0], new_variable, 'variable' ] )
		elif type == 2:
			if verbose:
				print 'YO! --------- functions not yet implimented'
			# due to complexity i'm skipping this for the moment
	#	   type_flag = 'function'
			# function
	#	   if branch[2] == 'number' or branch[2] == 'variable' or branch[2] == 'close':
	#		   # add and operator before the new function
	#		   new_operator = operator_mutation(' ')
	#		   new_equation.append(branch[0], new_operator, 'operator')
	#	   new_function = variable_mutation('zoom')
			type_flag = False
		if verbose:
			print "new_equation:", `new_equation`
		return (new_equation, type_flag)


