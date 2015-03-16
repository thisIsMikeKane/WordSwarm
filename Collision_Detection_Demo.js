// Window size
var window_w = 960,
    window_h = 500;

// Randomly generate 200 circles with radius between 4-16
//	range(200) generates an array 0..199 (or maybe 200)
//	map() populates the array I think
var objects = d3.range(100).map(function() { return {
	w: Math.random() * 20 + 10, h: Math.random() * 20 + 10}; });

var root = objects[0]; // Root object is the first in the list 
var color = d3.scale.category10(); // Construct a new ordinal scale with a range of ten categorical colors.

root.w = 0;
root.h = 0;
root.fixed = true;

// Use the D3 Force Layout
var force = d3.layout.force()
    .gravity(0.05)
    .charge(function(d, i) { return i ? 0 : -1000; }) // Set the root node charge to 0, and all others to -2000 so they all repel from the root node.
    .nodes(objects) // Populate the layout with the objects
    .size([window_w, window_h]); // Set the layout size

// Start the D3 Force Layout
force.start();

// Append an SVG element, which same size as the Force Layout, to the body
var svg = d3.select("body").append("svg")
    .attr("width", window_w)
    .attr("height", window_h);


svg.selectAll("rect")
    .data(objects.slice(1)) // slice the starting from 1 to the end
  .enter().append("rect") // enter() iterates over the data and appends a Rectangle
    .attr("width", function(d) { return d.w; }) // set each Rectangle width
	.attr("height", function(d) { return d.h; }) // set each Rectangle height
    .style("fill", function(d, i) { return color(i % 3); }); // set each Rectangle color

force.on("tick", function(e) {
  var q = d3.geom.quadtree(objects), // Define a quadtree with the coordinates of all the objects
      i = 0,
      n = objects.length;

  while (++i < n) q.visit(collide(objects[i])); // Detect collisions with any of the quads

  svg.selectAll("rect")
      .attr("x", function(d) { return d.x + d.w/2; }) // Set the x position of the center of the Rectangle on the layout
      .attr("y", function(d) { return d.y - d.h/2; }); // Set the y position of the center of the Rectangle on the layout
});

svg.on("mousemove", function() {
	
  var p1 = d3.mouse(this); // Get the mouse position
  
  // Set the x/y or the root node
  root.px = p1[0];
  root.py = p1[1];
  
  force.resume(); // Resume the Force Layout, that is increase the temperature
});

// Test object for collision
//	Assumes its a circle with position at center
function collide(obj) {
  var buffer = 0,
	  r = Math.sqrt(obj.w*obj.w + obj.h*obj.h) + buffer, // determine circumscribed radius of obj in quadtree
      nx1 = obj.x - obj.w/2, // left bound of object
      nx2 = obj.x + obj.w/2, // right bound of object
      ny1 = obj.y - obj.h/2, // lower bound of object
      ny2 = obj.y + obj.h/2; // upper bound of object
	  
  // Return the function to be executed as the quadtree visit callback
  //	The children of the current quad should be visited if returns true
  return function(quad, x1, y1, x2, y2) {
	  
	// If the current node in the quadtree has a point (i.e. it is a leaf node) and that point is not the current object then...
    if (quad.point && (quad.point !== obj)) {
		
      // Compute x, y, & geometric distance between quadtree point and point of current object
	  var x = obj.x - quad.point.x, 
          y = obj.y - quad.point.y,
          l = Math.sqrt(x * x + y * y); // Geometric distance between points
	  
	  // Min distance w/o collision
	  var r = Math.sqrt(obj.w*obj.w + obj.h*obj.h) + Math.sqrt(quad.point.w*quad.point.w + quad.point.h*quad.point.h); 
		  
      if (l < r) { // If collision
        l = (l - r) / l * .5; // Half the difference between the current distance and the non-clash distance
		
		// Move the elements apart by half the over-lap distance
        obj.x -= x *= l;
        obj.y -= y *= l;
        quad.point.x += x;
        quad.point.y += y;
		
		// This assumes that they are clashing at 45*. Must be an iterative process to converge?
      }
    }
    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
  };
}