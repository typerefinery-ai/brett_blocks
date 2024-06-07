import { select, json, zoom, drag, event } from 'd3';
import { createContextMenu } from './contextMenu.js';

//----------------------------------------
// key id functions
var getLinkId = function (d) {
  return d.source + '-' + d.target;
};
var getNodeId = function (d, i) {
  return d.id;
};

//------------------------------------------
// Adjaceny List Class
//-------------------------------------------
class Graph {
  constructor() {
    this.t = new Map();
  }
  addEdge(node1, node2) {
    const s = this.t.get(node1);
    if (s == null) this.t.set(node1, new Set([node2]));
    else s.add(node2);
  }
  getAdjacencies(node) {
    var z = this.t.get(node);
    if (z == null) {
      z = new Set();
    }
    return z;
  }
  *dir(node, path = Array(), visited = new Set()) {
    yield [...path, node];
    path.push(node);
    visited.add(node);
    for (const adj of this.getAdjacencies(node)) {
      if (!visited.has(adj)) {
        yield* this.dir(adj, path, visited);
      }
    }
    path.pop();
  }
  *dirs(nodes) {
    for (const node of nodes) {
      yield* this.dir(node);
    }
  }
}

//------------------------------------------
// Reference Component Namesapce
//-----------------------------------------
//namespace for all of the object functions and variables
//will be passed to the declared function
// window.workP = {};
// (function (ns) {
//   console.group('testObject');

//   //declare a variable for this namespace
//   ns.testValue = 'value';

//   ns.testFunction = function () {
//     return 'function value';
//   };
//   console.log(['testObject namespace contents', ns]);

//   console.groupEnd();
// })(window.testObject); //execte declaration and pass namespace

// console.log([
//   'testObject',
//   testObject.testValue,
//   testObject.testFunction(),
// ]);

//------------------------------------------
// visualisation component
//-----------------------------------------
window.workP = {};
(function (ns) {
  // A. Initialise the object
  ns.initSVG = function (graph, options) {
    console.group('initSVG');
    console.log(['config', graph, options]);
    if (options.theme === 'light') {
      ns.theme = options.light_theme;
    } else {
      ns.theme = options.dark_theme;
    }
    //
    // Step 1: Setup the 3 svg's and the tooltip
    var promotable_svg = select('#working_svg')
      .append('svg')
      .attr('width', options.working_width)
      .attr('height', options.height / 2)
      .attr('class', 'promotable_svg');
    var scratch_svg = select('#working_svg')
      .append('svg')
      .attr('width', options.working_width)
      .attr('height', options.height / 2)
      .attr('class', 'scratch_svg');
    ns.tooltip = d3
      .select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0);

    // Step 2: Setup the 3 rectangles
    const promotable_rect = promotable_svg
      .append('rect')
      .attr('width', options.working_width)
      .attr('height', options.height / 2)
      .attr('x', 0)
      .attr('y', 0)
      .attr('stroke', ns.theme.svgBorder)
      .attr('fill', ns.theme.promoFill);
    const scratch_rect = scratch_svg
      .append('rect')
      .attr('width', options.working_width)
      .attr('height', options.height / 2)
      .attr('x', 0)
      .attr('y', 0)
      .attr('stroke', ns.theme.svgBorder)
      .attr('fill', ns.theme.scratchFill);
    const promotable_label = promotable_svg
      .append('g')
      .attr('transform', 'translate(' + 10 + ',' + 20 + ')')
      .append('text')
      .text('Promotable')
      .style('fill', ns.theme.svgName);
    const scratch_label = scratch_svg
      .append('g')
      .attr('transform', 'translate(' + 10 + ',' + 20 + ')')
      .append('text')
      .text('Scratch Pad')
      .style('fill', ns.theme.svgName);

    // Step 3. Connect the svg's to the function object and set the zoom
    ns.promo_svg = promotable_svg
      .call(
        zoom().on('zoom', function () {
          ns.promotable_svg.attr(
            'transform',
            event.transform,
          );
        }),
      )
      .append('g');
    ns.scratch_svg = scratch_svg
      .call(
        zoom().on('zoom', function () {
          ns.scratch_svg.attr('transform', event.transform);
        }),
      )
      .append('g');

    // Append the Arrowhead in Promo and Scratch SVG's
    ns.promo_svg
      .append('defs')
      .append('marker')
      .attr('id', 'parrowhead')
      .attr('viewBox', '-0 -5 10 10') //the bound of the SVG viewport for the current SVG fragment. defines a coordinate system 10 wide and 10 high starting on (0,-5)
      .attr('refX', 50) // x coordinate for the reference point of the marker. If circle is bigger, this need to be bigger.
      .attr('refY', 0)
      .attr('orient', 'auto')
      .attr('markerWidth', 10)
      .attr('markerHeight', 10)
      .attr('xoverflow', 'visible')
      .append('svg:path')
      .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
      .attr('fill', options.checkColour)
      .style('stroke', 'none');

    ns.scratch_svg
      .append('defs')
      .append('marker')
      .attr('id', 'sarrowhead')
      .attr('viewBox', '-0 -5 10 10') //the bound of the SVG viewport for the current SVG fragment. defines a coordinate system 10 wide and 10 high starting on (0,-5)
      .attr('refX', 50) // x coordinate for the reference point of the marker. If circle is bigger, this need to be bigger.
      .attr('refY', 0)
      .attr('orient', 'auto')
      .attr('markerWidth', 10)
      .attr('markerHeight', 10)
      .attr('xoverflow', 'visible')
      .append('svg:path')
      .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
      .attr('fill', options.checkColour)
      .style('stroke', 'none');

    // Step 4. Setup the data, first separate the nodes and edges into two groups
    console.groupEnd();
  };

  // B. Update Data, Simulations and Drive Show Graph
  ns.updateGraph = function (graph, options) {
    console.group('updateGraph');
    console.log('Splitting Graph->', graph);
    // 1. Setup variables and define promotable types
    const prom_types = [
      'incident',
      'task',
      'impact',
      'event',
      'sighting',
    ];
    var returnGraph = {};
    var nodes = graph.nodes;
    var edges = graph.edges;
    var scratch_nodes = [];
    var scratch_edges = [];
    var promotable_nodes = [];
    var promotable_edges = [];
    var prom_node_IDs = [];
    var adjacency = new Graph();
    // 2. Fill adjacency list with edges
    edges.forEach(function (edge) {
      adjacency.addEdge(edge['source'], edge['target']);
    });
    //3. Find first the promotable node ID's and collect all sub-graphs into promID's
    nodes.forEach(function (node) {
      if (prom_types.includes(node.type)) {
        prom_node_IDs.push(node.id);
      }
    });
    var prom_IDs = Array.from(
      adjacency.dirs(prom_node_IDs),
      (path) => path.at(-1),
    );
    // 4. Now split the Graphs and update the
    nodes.forEach(function (node) {
      if (prom_IDs.includes(node.id)) {
        promotable_nodes.push(node);
      } else {
        scratch_nodes.push(node);
      }
    });
    edges.forEach(function (edge) {
      if (
        prom_IDs.includes(edge.source) &&
        prom_IDs.includes(edge.target)
      ) {
        promotable_edges.push(edge);
      } else {
        scratch_edges.push(edge);
      }
    });
    // 5. Setup the namesspace data
    ns.rawData = graph;
    ns.split = {};
    ns.split.promo = {};
    ns.split.promo.nodes = promotable_nodes;
    ns.split.promo.edges = promotable_edges;
    ns.split.scratch = {};
    ns.split.scratch.nodes = scratch_nodes;
    ns.split.scratch.edges = scratch_edges;
    console.log('ns.split->', ns.split);
    console.log('ns.split.scratch->', ns.split.scratch);
    console.log('ns.split.promo->', ns.split.promo);

    console.groupEnd();
  };

  ns.simGraph = function (options) {
    console.group('simGraph');

    // Step 6. Setup the simulations
    // first the variables centreStrength
    ns.pforceNode = d3.forceManyBody();
    ns.sforceNode = d3.forceManyBody();
    ns.pforceLink = d3
      .forceLink(ns.split.promo.edges)
      .id((d) => getLinkId(d))
      .distance(4 * options.icon_size);
    ns.sforceLink = d3
      .forceLink(ns.split.scratch.edges)
      .id((d) => getLinkId(d))
      .distance(4 * options.icon_size);
    ns.sforceCentre = d3.forceCenter(
      options.working_width / 2,
      options.svg_height / 4,
    );
    ns.pforceCentre = d3.forceCenter(
      options.working_width / 2,
      options.svg_height / 4,
    );
    if (options.nodeStrength !== undefined)
      ns.pforceNode.strength(options.nodeStrength);
    if (options.nodeStrength !== undefined)
      ns.sforceNode.strength(options.nodeStrength);
    if (options.linkStrength !== undefined)
      ns.pforceLink.strength(options.linkStrength);
    if (options.linkStrength !== undefined)
      ns.sforceLink.strength(options.linkStrength);
    if (options.centreStrength !== undefined)
      ns.sforceCentre.strength(options.centreStrength);
    if (options.centreStrength !== undefined)
      ns.pforceCentre.strength(options.centreStrength);


    console.log(
      'ns.split.promo.nodes',
      ns.split.promo.nodes,
    );
    console.log(
      'ns.split.promo.edges',
      ns.split.promo.edges,
    );
    console.log(
      'ns.split.scratch.nodes',
      ns.split.scratch.nodes,
    );
    console.log(
      'ns.split.scratch.edges',
      ns.split.scratch.edges,
    );

    ns.promotable_sim = d3
      .forceSimulation(ns.split.promo.nodes)
      .force('link', ns.pforceLink)
      .force('charge', ns.pforceNode)
      .force('center', ns.pforceCentre);
    ns.scratch_sim = d3
      .forceSimulation(ns.split.scratch.nodes)
      .force('link', ns.sforceLink)
      .force('charge', ns.sforceNode)
      .force('center', ns.sforceCentre);

    // 7. Now show split graphs
    console.groupEnd();
  };

  // 7. Show Graph
  ns.showGraphs = function (options) {
    console.log('Showing the Graph');
    // Initialize the links, EdgePaths
    const promoLink = ns.promo_svg
      .selectAll('.plinks')
      .data(ns.split.promo.edges)
      .join('line')
      .attr('class', 'plinks')
      .attr('source', (d) => d.source)
      .attr('target', (d) => d.target)
      .attr('stroke-width', 0.75)
      .attr('stroke', 'grey')
      .attr('marker-end', 'url(#parrowhead)'); //The marker-end attribute defines the arrowhead or polymarker that will be drawn at the final vertex of the given shape.

    const scratchLink = ns.scratch_svg
      .selectAll('.slinks')
      .data(ns.split.scratch.edges)
      .join('line')
      .attr('class', 'slinks')
      .attr('source', (d) => d.source)
      .attr('target', (d) => d.target)
      .attr('stroke-width', 0.75)
      .attr('stroke', 'grey')
      .attr('marker-end', 'url(#sarrowhead)'); //The marker-end attribute defines the arrowhead or polymarker that will be drawn at the final vertex of the given shape.

    const promoEdgepaths = ns.promo_svg
      .selectAll('.pedgepath') //make path go along with the link provide position for link labels
      .data(ns.split.promo.edges)
      .join('path')
      .attr('class', 'pedgepath')
      .attr('fill-opacity', 0)
      .attr('stroke-opacity', 0)
      .attr('id', function (d, i) {
        return 'pedgepath' + i;
      })
      .style('pointer-events', 'none');

    const scratchEdgepaths = ns.scratch_svg
      .selectAll('.sedgepath') //make path go along with the link provide position for link labels
      .data(ns.split.scratch.edges)
      .join('path')
      .attr('class', 'sedgepath')
      .attr('fill-opacity', 0)
      .attr('stroke-opacity', 0)
      .attr('id', function (d, i) {
        return 'sedgepath' + i;
      })
      .style('pointer-events', 'none');

    const promoEdgelabels = ns.promo_svg
      .selectAll('.pedgelabel')
      .data(ns.split.promo.edges)
      .join('text')
      .style('pointer-events', 'none')
      .attr('class', 'pedgelabel')
      .attr('id', function (d, i) {
        return 'pedgelabel' + i;
      })
      .attr('font-size', 18)
      .attr('fill', ns.theme.edges);

    const scratchEdgelabels = ns.scratch_svg
      .selectAll('.sedgelabel')
      .data(ns.split.scratch.edges)
      .join('text')
      .style('pointer-events', 'none')
      .attr('class', 'sedgelabel')
      .attr('id', function (d, i) {
        return 'sedgelabel' + i;
      })
      .attr('font-size', 18)
      .attr('fill', ns.theme.edges);

    promoEdgelabels
      .append('textPath') //To render text along the shape of a <path>, enclose the text in a <textPath> element that has an href attribute with a reference to the <path> element.
      .attr('xlink:href', function (d, i) {
        return '#pedgepath' + i;
      })
      .style('text-anchor', 'middle')
      .style('pointer-events', 'none')
      .attr('startOffset', '50%')
      .text((d) => d.name);

    scratchEdgelabels
      .append('textPath') //To render text along the shape of a <path>, enclose the text in a <textPath> element that has an href attribute with a reference to the <path> element.
      .attr('xlink:href', function (d, i) {
        return '#sedgepath' + i;
      })
      .style('text-anchor', 'middle')
      .style('pointer-events', 'none')
      .attr('startOffset', '50%')
      .text((d) => d.name);

    // Initialize the nodes with attached image, changed to join data
    // add hover over effect
    // for promo
    const promoNode = ns.promo_svg
      .append('g')
      .selectAll('pnodes')
      .data(ns.split.promo.nodes)
      .join('image')
      .attr('class', 'pnodes')
      .attr('xlink:href', function (d) {
        return (
          options.prefix + options.shape + d.icon + '.svg'
        );
      })
      .attr('width', options.icon_size + 5)
      .attr('height', options.icon_size + 5);
    // .on('mouseover', function (d) {
    //   d3.select(this)
    //     .transition()
    //     .duration(options.duration)
    //     .attr('width', 70)
    //     .attr('height', 70);
    // })
    // .on('mouseout', function (d) {
    //   d3.select(this)
    //     .transition()
    //     .duration(options.duration)
    //     .attr('width', function (d) {
    //       return options.radius;
    //     })
    //     .attr('height', function (d) {
    //       return options.radius;
    //     });
    // })
    // .on('mouseover.tooltip', function (d) {
    //   ns.tooltip
    //     .transition()
    //     .duration(options.duration)
    //     .style('opacity', 0.8);
    //   ns.tooltip
    //     .html(
    //       '<h1>' +
    //         d.heading +
    //         '</h1>' +
    //         '<p> ' +
    //         d.description +
    //         '</p>',
    //     )
    //     .style('left', d3.event.pageX + 'px')
    //     .style('top', d3.event.pageY + 10 + 'px');
    // })
    // .on('mouseout.tooltip', function () {
    //   ns.tooltip
    //     .transition()
    //     .duration(100)
    //     .style('opacity', 0);
    // })
    // .on('mousemove', function () {
    //   ns.tooltip
    //     .style('left', d3.event.pageX + 'px')
    //     .style('top', d3.event.pageY + 10 + 'px');
    // })
    // .call(
    //   d3
    //     .drag() //sets the event listener for the specified typenames and returns the drag behavior.
    //     .on('start', pDragstarted) //start - after a new pointer becomes active (on mousedown or touchstart).
    //     .on('drag', pDragged) //drag - after an active pointer moves (on mousemove or touchmove).
    //     .on('end', pDragended), //end - after an active pointer becomes inactive (on mouseup, touchend or touchcancel).
    // );

    // for scratch
    const scratchNode = ns.scratch_svg
      .append('g')
      .selectAll('snodes')
      .data(ns.split.scratch.nodes)
      .join('image')
      .attr('class', 'snodes')
      .attr('xlink:href', function (d) {
        return (
          options.prefix + options.shape + d.icon + '.svg'
        );
      })
      .attr('width', options.icon_size + 5)
      .attr('height', options.icon_size + 5);
    // .on('mouseover', function (d) {
    //   d3.select(this)
    //     .transition()
    //     .duration(options.duration)
    //     .attr('width', 70)
    //     .attr('height', 70);
    // })
    // .on('mouseout', function (d) {
    //   d3.select(this)
    //     .transition()
    //     .duration(options.duration)
    //     .attr('width', function (d) {
    //       return options.icon_size;
    //     })
    //     .attr('height', function (d) {
    //       return options.icon_size;
    //     });
    // })
    // .on('mouseover.tooltip', function (d) {
    //   ns.tooltip
    //     .transition()
    //     .duration(options.duration)
    //     .style('opacity', 0.8);
    //   ns.tooltip
    //     .html(
    //       '<h1>' +
    //         d.heading +
    //         '</h1>' +
    //         '<p> ' +
    //         d.description +
    //         '</p>',
    //     )
    //     .style('left', d3.event.pageX + 'px')
    //     .style('top', d3.event.pageY + 10 + 'px');
    // })
    // .on('mouseout.tooltip', function () {
    //   ns.tooltip
    //     .transition()
    //     .duration(100)
    //     .style('opacity', 0);
    // })
    // .on('mousemove', function () {
    //   ns.tooltip
    //     .style('left', d3.event.pageX + 'px')
    //     .style('top', d3.event.pageY + 10 + 'px');
    // })
    // .call(
    //   d3
    //     .drag() //sets the event listener for the specified typenames and returns the drag behavior.
    //     .on('start', sDragstarted) //start - after a new pointer becomes active (on mousedown or touchstart).
    //     .on('drag', sDragged) //drag - after an active pointer moves (on mousemove or touchmove).
    //     .on('end', sDragended), //end - after an active pointer becomes inactive (on mouseup, touchend or touchcancel).
    // );

    ns.promotable_sim.on('tick', promoTicked); //use simulation.on to listen for tick events as the simulation runs.
    // ns.scratch_sim.on('tick', scratchTicked); //use simulation.on to listen for tick events as the simulation runs.

    // This function is run at each iteration of the force algorithm, updating the nodes position (the nodes data array is directly manipulated).
    function promoTicked() {
      ns.promo_svg
        .selectAll('.plinks')
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      ns.promo_svg
        .selectAll('.pnodes')
        .attr('x', (d) => d.x - options.radius / 2)
        .attr('y', (d) => d.y - options.radius / 2);

      ns.promo_svg.selectAll('.pedgepath').attr(
        'd',
        function (d) {
          console.log('pedgepath->', d);
          return (
            'M ' +
            d.source.x +
            ' ' +
            d.source.y +
            ' L ' +
            d.target.x +
            ' ' +
            d.target.y
          );
        },
        // (d) =>
        //   'M ' +
        //   d.source.x +
        //   ' ' +
        //   d.source.y +
        //   ' L ' +
        //   d.target.x +
        //   ' ' +
        //   d.target.y,
      );
    }
    function scratchTicked() {
      ns.scratch_svg
        .selectAll('.slinks')
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      ns.scratch_svg
        .selectAll('.snodes')
        .attr('x', (d) => d.x - options.radius / 2)
        .attr('y', (d) => d.y - options.radius / 2);

      ns.scratch_svg.selectAll('.sedgepath').attr(
        'd',
        function (d) {
          console.log('sedgepath->', d);
          return (
            'M ' +
            d.source.x +
            ' ' +
            d.source.y +
            ' L ' +
            d.target.x +
            ' ' +
            d.target.y
          );
        },
        // (d) =>
        //   'M ' +
        //   d.source.x +
        //   ' ' +
        //   d.source.y +
        //   ' L ' +
        //   d.target.x +
        //   ' ' +
        //   d.target.y,
      );
    }

    //create zoom handler  for each
    var pZoom_handler = d3.zoom().on('zoom', pzoom_actions);
    var sZoom_handler = d3.zoom().on('zoom', szoom_actions);

    //specify what to do when zoom event listener is triggered foreach
    function pzoom_actions() {
      ns.promo_svg.attr('transform', d3.event.transform);
    }
    function szoom_actions() {
      ns.scratch_svg.attr('transform', d3.event.transform);
    }

    //add zoom behaviour to the svg element
    //same as svg.call(zoom_handler);
    pZoom_handler(ns.promo_svg);
    sZoom_handler(ns.scratch_svg);

    //The simulation is temporarily “heated” during interaction by setting the target alpha to a non-zero value.
    function pDragstarted(d) {
      if (!d3.event.active)
        ns.promotable_sim.alphaTarget(0.3).restart(); //sets the current target alpha to the specified number in the range [0,1].
      d.fy = d.y; //fx - the node’s fixed x-position. Original is null.
      d.fx = d.x; //fy - the node’s fixed y-position. Original is null.
    }

    //When the drag gesture starts, the targeted node is fixed to the pointer
    function pDragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    //the targeted node is released when the gesture ends
    function pDragended(d) {
      if (!d3.event.active)
        ns.promotable_sim.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    function sDragstarted(d) {
      if (!d3.event.active)
        ns.scratch_sim.alphaTarget(0.3).restart(); //sets the current target alpha to the specified number in the range [0,1].
      d.fy = d.y; //fx - the node’s fixed x-position. Original is null.
      d.fx = d.x; //fy - the node’s fixed y-position. Original is null.
    }

    //When the drag gesture starts, the targeted node is fixed to the pointer
    function sDragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    //the targeted node is released when the gesture ends
    function sDragended(d) {
      if (!d3.event.active) ns.scratch_sim.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  };

  console.groupEnd();
  return 'function value';
})(workP); //execte declaration and pass namespace
