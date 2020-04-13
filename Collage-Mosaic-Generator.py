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

			large_tile_img = img.resize((TILE_SIZE, TILE_SIZE), Image.ANTIALIAS)
			small_tile_img = img.resize((int(TILE_SIZE/TILE_BLOCK_SIZE), int(TILE_SIZE/TILE_BLOCK_SIZE)), Image.ANTIALIAS)

			return (large_tile_img.convert('RGB'), small_tile_img.convert('RGB'))
		except:
			return (None, None)

	def get_tiles(self):
		large_tiles = []
		small_tiles = []

		print('Reading tiles from {}...'.format(self.tiles_directory))

		# search the tiles directory recursively
		for root, subFolders, files in os.walk(self.tiles_directory):
			for tile_name in files:
				print('Reading {:40.40}'.format(tile_name), flush=True, end='\r')
				tile_path = os.path.join(root, tile_name)
				large_tile, small_tile = self.__process_tile(tile_path)
				if large_tile:
					large_tiles.append(large_tile)
					small_tiles.append(small_tile)


		print('Processed {} tiles.'.format(len(large_tiles)))

		return (large_tiles, small_tiles)