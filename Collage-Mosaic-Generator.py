import sys
import os
from PIL import Image
from multiprocessing import Process, Queue, cpu_count

# Change these 3 config parameters to suit your needs...
TILE_SIZE      = 50		# height/width of mosaic tiles in pixels
TILE_MATCH_RES = 5		# tile matching resolution (higher values give better fit but require more processing)
ENLARGEMENT    = 8		# the mosaic image will be this many times wider and taller than the original

TILE_BLOCK_SIZE = TILE_SIZE / max(min(TILE_MATCH_RES, TILE_SIZE), 1)
WORKER_COUNT = max(cpu_count() - 1, 1)
OUT_FILE = 'mosaic.jpeg'
EOQ_VALUE = None

class TileProcessor:
	def __init__(self, tiles_directory):
		self.tiles_directory = tiles_directory

	def __process_tile(self, tile_path):
		try:
			img = Image.open(tile_path)
			# tiles must be square, so get the largest square that fits inside the image
			w = img.size[0]
			h = img.size[1]
			min_dimension = min(w, h)
			w_crop = (w - min_dimension) / 2
			h_crop = (h - min_dimension) / 2
			img = img.crop((w_crop, h_crop, w - w_crop, h - h_crop))