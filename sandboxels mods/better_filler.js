elements.better_filler {
	color: "#cb4cd9",
	behavior: [
		"CL|XX|CL",
		"XX|XX|XX",
		"CL|XX|CL",
	],
	tick: function(pixel) {
		for (var i = 0; i < adjacentCoords.length; i++) {
			var coords = adjacentCoords[i];
			var x = pixel.x + coords[0];
			var y = pixel.y + coords[1];
			if (!isEmpty(x,y,true) && pixelMap[x][y].element === "lattice") {
				deletePixel(x,y)
			}
		}
        for (var i = 0; i < diagonalCoords.length; i++) {
			var coords = diagonalCoords[i];
			var x = pixel.x + coords[0];
			var y = pixel.y + coords[1];
            pixelMap[x][y].color = pixel.color;
        }
	},
	onPlace: function(pixel) {
		if (pixel.del) return;
		if (Math.random() < 0.2) return;
		for (var i = 0; i < adjacentCoords.length; i++) {
			var coords = adjacentCoords[i];
			var x = pixel.x + coords[0];
			var y = pixel.y + coords[1];
			if (!isEmpty(x,y,true) && pixelMap[x][y].element === "lattice") {
				deletePixel(x,y);
			}
		}
	},
	reactions: {
		"cold_fire": { elem1:"ice_nine", chance:0.1 },
		"proton": { elem1:"filler", elem2:null, chance:0.1 },
		"electric": { elem1:null, elem2:"filler", chance:0.1 },
	},
	category:"special",
	excludeRandom: true,
	movable: false,
	density: 917
}
