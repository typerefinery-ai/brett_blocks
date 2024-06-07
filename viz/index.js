import { select, json, zoom, drag, event } from 'd3';
import { createContextMenu } from './contextMenu.js';
import { indentTree } from './indentTree.js';
import { workP } from './working.js';

// 1. Instantiate Visualisation Variables
// 3. Setup RMB Menu Items
const menuItems = [
  {
    title: 'Copy Object',
    action: (d) => {
      // TODO: add any action you want to perform
      console.log('Copy Object', d);
    },
  },
  {
    title: 'Create Relationship',
    action: (d) => {
      // TODO: add any action you want to perform
      console.log('Create Relationship ->', d);
    },
  },
];

const options = {
  duration: 350,
  radius: 6, // radius of curve for links
  barHeight: 40,
  margin: {
    top: 100,
    left: 30,
    bottom: 50,
    right: 30,
  },
  index_width: 400, // this svg
  working_width: 800, // next door svg
  svg_height: 800,
  svg_spacing: 500,
  // Icons
  prefix:
    'https://raw.githubusercontent.com/os-threat/images/main/img/',
  shape: 'rect-',
  icon_size: 36,
  textPadding: 8,
  corner: 5,
  // the tree view
  minHeight: 20,
  width: 400,
  height: 800,
  lineSpacing: 50,
  indentSpacing: 50,
  itemFont: '18px',
  boxSize: 10,
  tree_edge_thickness: 0.75,
  graph_edge_thickness: 1,
  theme: 'light',
  light_theme: {
    treeFill: 'white',
    scratchFill: 'ivory',
    promoFill: 'blanchedalmond',
    svgName: 'black',
    svgBorder: 'black',
    checkColour: 'gray',
    checkText: 'white',
    select: 'yellow',
    edges: 'black',
  },
  dark_theme: {
    treeFill: 'gray',
    scratchFill: 'dimgray',
    promoFill: 'gray',
    svgName: 'white',
    svgBorder: 'white',
    checkColour: 'white',
    checkText: 'gray',
    select: 'yellow',
    edges: 'white',
  },
};

// 2. Setup 2 SVG and Border combos
var index_svg = d3
  .select('#index_svg')
  .append('svg')
  .attr('class', 'index_svg')
  .attr('width', options.width)
  .attr('height', options.height)
  .append('g')
  .attr(
    'transform',
    'translate(' +
      options.margin.left +
      ',' +
      options.margin.top +
      ')',
  );

//sendEvent("formName","formName")
// function sendEvent(name, type) {
//   var event = new CustomEvent('loadDetailForm', {
//     detail: {
//       type: type,
//       name: name,
//     },
//   });
//   console.log(['sendEvent to parent, event', event]);
//   window.parent.document.dispatchEvent(event);
// }

// 4. Setup initial tree view
d3.json('data/sightingIndex.json').then(function (data) {
  console.log(data);
  console.log('I am rendering first time');
  indentTree(data, index_svg, options);
});
// 5. Setup treeview change dataslice radio buttons
const tree_map = {
  sighting: 'data/sightingIndex.json',
  task: 'data/taskIndex.json',
  impact: 'data/impactIndex.json',
  event: 'data/eventIndex.json',
  me: 'data/meIndex.json',
  company: 'data/companyIndex.json',
};

const buttons = d3.selectAll('input');
buttons.on('change', function (d) {
  console.log('button changed to ' + this.value);
  //d3.select('.index_svg').selectAll('g').remove();
  d3.json(tree_map[this.value]).then(function (data) {
    console.log(data);
    console.log('I am ready to re-render the tree');
    indentTree(data, index_svg, options);
  });
});
// 6. Load the Working Pane with scratch data
const scratch = 'data/scratch.json';
d3.json(scratch).then(function (data) {
  console.log('scratch->', data);
  console.log('I am rendering the working page');
  window.workP.init(data, options);
});
