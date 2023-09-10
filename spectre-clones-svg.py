import sys
import math

def placeTile(level, mystic, keyIdx, keyLoc, rotation):
	tiles = []
	if level == 0:
		x = 0
		y = 0
		points = []
		for a in (9, 6, 4, 7, 5, 2, 4, 1, 3, 0, 10, 10, 8, 11):
			points.append((x, y))
			x += 10.0*math.cos(a*math.pi/6)
			y += 10.0*math.sin(a*math.pi/6)
		keypoints = [points[0], points[2], points[4], points[10]]
	else:
		# construct at an arbitrary position in rotation 0
		keypoints = [None, None, None, None]
		_, points = placeTile(level - 1, False, 0, (0.0, 0.0), 6)
		tiles.append((points[0], 6))
		_, points = placeTile(level - 1, False, 3, points[1], 8)
		tiles.append((points[0], 8))
		keypoints[3] = points[1]
		_, points = placeTile(level - 1, True, 2, points[2], 4)
		tiles.append((points[0], 4))
		_, points = placeTile(level - 1, False, 3, points[3], 0)
		tiles.append((points[0], 0))
		keypoints[2] = points[0]
		_, points = placeTile(level - 1, False, 3, points[1], 2)
		tiles.append((points[0], 2))
		keypoints[1] = points[1]
		_, points = placeTile(level - 1, False, 0, points[2], 2)
		tiles.append((points[0], 2))
		_, points = placeTile(level - 1, False, 3, points[1], 4)
		tiles.append((points[0], 4))
		keypoints[0] = points[0]
		if not mystic:
			_, points = placeTile(level - 1, False, 3, points[1], 6)
			tiles.append((points[0], 6))
	# translate the desired key point to the origin and mirror
	transx = -keypoints[keyIdx][0]
	transy = -keypoints[keyIdx][1]
	keypoints = [(-(k[0] + transx), k[1] + transy) for k in keypoints]
	tiles = [((-(t[0][0] + transx), t[0][1] + transy), t[1]) for t in tiles]
	# rotate
	c = math.cos(rotation*math.pi/6)
	s = math.sin(rotation*math.pi/6)
	keypoints = [(k[0]*c + k[1]*-s, k[0]*s + k[1]*c) for k in keypoints]
	tiles = [((t[0][0]*c + t[0][1]*-s, t[0][0]*s + t[0][1]*c), t[1] + rotation) for t in tiles]
	# translate to the desired position
	transx = keyLoc[0]
	transy = keyLoc[1]
	keypoints = [(k[0] + transx, k[1] + transy) for k in keypoints]
	tiles = [((t[0][0] + transx, t[0][1] + transy), t[1]) for t in tiles]
	
	#debug output
	#for i, k in enumerate(keypoints):
	#	sys.stdout.write('\t<circle cx="{:.6f}" cy="{:.6f}" r="{:d}" style="fill:{}; stroke: none;"/>\n'.format(
	#		k[0], k[1],
	#		2 + level,
	#		('#FF0000', '#FFFF00', '#00FF00', '#0000FF')[i]
	#	))
	return tiles, keypoints

def outputTile(level, mystic):
	if level == 0:
		if mystic:
			sys.stdout.write("""<g id="lmystic0" inkscape:groupmode="layer" inkscape:label="Mystic 0">
	<g id="mystic0">
		<use xlink:href="#spectre0"/>
		<use xlink:href="#spectre0" transform="translate(""")
			x = 0
			y = 0
			for a in (9, 0, 2, 11, 1, 4):
				x += 10.0*math.cos(a*math.pi/6)
				y += 10.0*math.sin(a*math.pi/6)
			sys.stdout.write('{:.6f}, {:.6f}'.format(x, y))
			sys.stdout.write(""") rotate(30)"/>
	</g>
</g>
""")
		else:
			sys.stdout.write('<g id="lspectre0" inkscape:groupmode="layer" inkscape:label="Spectre 0">\n\t<g id="spectre0">\n\t\t<path d="m 0,0 ')
			for a in (3, 6, 8, 5, 7, 10, 8, 11, 9, 12, 2, 2, 4):
				sys.stdout.write('l {:.6f},{:.6f} '.format(10.0*math.cos(a*math.pi/6), -10.0*math.sin(a*math.pi/6)))
			sys.stdout.write('z" style="fill: none; stroke: #000000; stroke-width: 0.5; stroke-linecap: round; stroke-linejpin: round;"/>\n\t</g>\n</g>\n')
	else:
		tiles, keypoints = placeTile(level, mystic, 0, (0.0, 0.0), 0)
		sys.stdout.write('<g id="l{}{:d}" inkscape:groupmode="layer" inkscape:label="{} {:d}">\n\t<g id="{}{:d}">\n'.format('mystic' if mystic else 'spectre', level, 'Mystic' if mystic else 'Spectre', level, 'mystic' if mystic else 'spectre', level))
		for i, t in enumerate(tiles):
			sys.stdout.write('\t\t<use xlink:href="#{}{:d}" transform="translate({:.6f}, {:.6f}) rotate({:d}) scale(-1, 1)"/>\n'.format(
				'mystic' if i == 2 else 'spectre',
				level - 1,
				-t[0][0], t[0][1], # undo the mirroring that placeTile already did in expectation of being called from a higher level of itself
				t[1]*30
			))
		sys.stdout.write('\t</g>\n</g>\n')

def main():
	sys.stdout.write("""<?xml version="1.0" standalone="no"?>
<svg width="210mm" height="297mm" viewBox="0 0 210 297" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
""")
	outputTile(0, False)
	outputTile(0, True)
	outputTile(1, False)
	outputTile(1, True)
	outputTile(2, False)
	outputTile(2, True)
	outputTile(3, False)
	outputTile(3, True)
	outputTile(4, False)
	sys.stdout.write('</svg>\n')

if __name__ == "__main__":
	main()
