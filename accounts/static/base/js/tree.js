var margin = {
    top: 20,
    right: 120,
    bottom: 20,
    left: 120
},



width = 960 - margin.right - margin.left,
height = 800 - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    rectW = 100,
    rectH = 60;

var tree = d3.layout.tree().nodeSize([150, 140]);
var diagonal = d3.svg.diagonal()
    .projection(function (d) {
    return [d.x + rectW / 2, d.y + rectH / 2];
});
var screenWidth  = window.innerWidth;
var ElBodyWidth = $('#body').width()
var svg = d3.select("#body").append("svg").attr("width","100%").attr("height", 1000)
    .call(zm = d3.behavior.zoom().scaleExtent([1,3]).on("zoom", redraw)).append("g")
    .attr("transform", "translate(" + ElBodyWidth/2 + "," + 100 + ")")



//necessary so that zoom knows where to zoom and unzoom from
zm.translate([ElBodyWidth/2, 100]);

root.x0 = 0;
root.y0 = height / 2;

function collapse(d) {
    if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
    }
}

root.children.forEach(collapse);
update(root);

d3.select("#body").style("height", "800px");

function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function (d) {
        d.y = d.depth * 180;
    });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function (d) {
        return d.id || (d.id = ++i);
    });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
        return "translate(" + source.x0 + "," + source.y0 + ")";
    })
        .on("click", click);

    nodeEnter.append("rect")
        .attr("width", rectW)
        .attr("height", rectH)
        .attr("stroke", "#3baaff")
        .attr("stroke-width", 2)

//        .style("fill", function (d) {
//        return d._children ? "lightsteelblue" : "#fff";
//    });




    nodeEnter.append("a")
    .attr("xlink:href", function (d)  { return "/tree/" + d.id; })
    .append("text")
    .attr("x", rectW / 2)
    .attr("y", rectH / 2)
    .attr("dy", ".35em")
    .attr("text-anchor", "middle")
    .attr("transform", "translate(" + rectW / 2 + "," + 0 + ")")

    .text(function (d) {
        return d.name;
    })
    .call(wrap, rectW - 10); // вызов функции обертывания текста

    function wrap(text, width) {
  text.each(function () {
    var text = d3.select(this),
        words = text.text().split(/\s+/).reverse(),
        word,
        line = [],
        lineNumber = 0,
        lineHeight = 1.1, // расстояние между строками
        y = text.attr("y"),
        dy = parseFloat(text.attr("dy")),
        tspan = text
            .text(null)
            .append("tspan")
            .attr("x", 0)
            .attr("y", y)
            .attr("dy", dy + "em");

    while ((word = words.pop())) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text
            .append("tspan")
            .attr("x", 0)
            .attr("y", y)
            .attr("dy", ++lineNumber * lineHeight + dy + "em")
            .text(word);
      }
    }
  });


}


    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

    nodeUpdate.select("rect")
        .attr("width", rectW)
        .attr("height", rectH)
//        .attr("stroke", "#3baaff")
//        .attr("stroke-width", 2)
//        .style("stroke", function (d) {
//        return d._children ? "lightsteelblue" : "#fff";
//    });





    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) {
        return "translate(" + source.x + "," + source.y + ")";
    })
        .remove();

    nodeExit.select("rect")
        .attr("width", rectW)
        .attr("height", rectH)
    //.attr("width", bbox.getBBox().width)""
    //.attr("height", bbox.getBBox().height)
//        .attr("stroke", "black")



    nodeExit.select("text");

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function (d) {
        return d.target.id;
    });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("x", rectW / 2)
        .attr("y", rectH / 2)
        .attr("d", function (d) {
        var o = {
            x: source.x0,
            y: source.y0
        };
        return diagonal({
            source: o,
            target: o
        });
    });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
        var o = {
            x: source.x,
            y: source.y
        };
        return diagonal({
            source: o,
            target: o
        });
    })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

// Toggle children on click.
function click(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
    checkLinks()
}

//Redraw for zoom
function redraw() {
  svg.attr("transform",
      "translate(" + d3.event.translate + ")"
      + " scale(" + d3.event.scale + ")");
}


checkLinks()







function checkLinks() {
  d3.selectAll('.node').each(function(d) {
    var link = d3.select(this).select('a').attr('xlink:href');
    if (link) {

      var id = parseInt(link.split('/').pop());
      if (INTERESTED.includes(id)) {
        d3.select(this).select('rect').style('fill', '#F5DE5C')
      } else if (LEARNING.includes(id)) {
        d3.select(this).select('rect').style('fill', '#01A3D2')
      }else if (LEARNED.includes(id)) {
        d3.select(this).select('rect').style('fill', '#00C692')
      }else if (VALIDATED.includes(id)) {
        d3.select(this).select('rect').style('fill', '#00964E')
      }else {
        d3.select(this).select('rect').style('fill', '#9298AA')
      }

      if (THEORY.includes(id)){
        d3.select(this).select('rect').attr("rx", 100).attr("ry", 100)
      }else if (PRACTICE.includes(id)) {
        d3.select(this).select('rect')
      }else {
        d3.select(this).select('rect').attr("rx", 20)
      }

      if (get_leaves_without_children.includes(id)){
        d3.select(this).select('rect').attr("stroke", "black").attr("stroke-width", 1.5)
      }


    }
  });
}