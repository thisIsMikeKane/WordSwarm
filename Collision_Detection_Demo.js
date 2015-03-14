// Window size
var width = 960,
    height = 500;

// Randomly generate 200 circles with radius between 4-16
//	range(200) generates an array 0..199 (or maybe 200)
//	map() populates the array I think
var nodes = d3.range(200).map(function() { return {radius: Math.random() * 12 + 4}; });

var root = nodes[0]; // Root node is the first
var color = d3.scale.category10(); // Construct a new ordinal scale with a range of ten categorical colors.

root.radius = 0;
root.fixed = true;

// Use the D3 Force Layout
var force = d3.layout.force()
    .gravity(0.05)
    .charge(function(d, i) { return i ? 0 : -2000; }) // Set the root node charge to 0, and all others to -2000 so they all repel from the root node.
    .nodes(nodes) // Populate the layout with the nodes
    .size([width, height]); // Set the layout size

// Start the D3 Force Layout
force.start();

// Append an SVG element, which same size as the Force Layout, to the body
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


svg.selectAll("circle")
    .data(nodes.slice(1)) // slice the starting from 1 to the end
  .enter().append("circle") // enter() iterates over the data and appends a circle
    .attr("r", function(d) { return d.radius; }) // set each circle radius
    .style("fill", function(d, i) { return color(i % 3); }); // set each circle color

force.on("tick", function(e) {
  var q = d3.geom.quadtree(nodes),
      i = 0,
      n = nodes.length;

  while (++i < n) q.visit(collide(nodes[i]));

  svg.selectAll("circle")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
});

svg.on("mousemove", function() {
  var p1 = d3.mouse(this);
  root.px = p1[0];
  root.py = p1[1];
  force.resume();
});

function collide(node) {
  var r = node.radius + 16,
      nx1 = node.x - r,
      nx2 = node.x + r,
      ny1 = node.y - r,
      ny2 = node.y + r;
  return function(quad, x1, y1, x2, y2) {
    if (quad.point && (quad.point !== node)) {
      var x = node.x - quad.point.x,
          y = node.y - quad.point.y,
          l = Math.sqrt(x * x + y * y),
          r = node.radius + quad.point.radius;
      if (l < r) {
        l = (l - r) / l * .5;
        node.x -= x *= l;
        node.y -= y *= l;
        quad.point.x += x;
        quad.point.y += y;
      }
    }
    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
  };
}