
//----------------------------------------
// key id functions
var getLinkId = function (d) {
  return d.source.index + '-' + d.target.index;
};
var getNodeId = function (d, i) {
  return d.G_id + '-' + i;
};

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
  ns.init = function (graph, options) {
    //
    // Step 1: Setup the 3 svg's and the tooltip

    // Step 4. Setup the data
    console.log('graph->', graph);
    console.log('attached-index->', graph['attached']);
    console.log('attached-dot->', graph.attached);
    console.log('type->', typeof(graph));
    for (let [key, value] of Object.entries(graph)){
      console.log('what is the key and value?');
      console.log('key->',key, '  value->', graph[key]);
    }

    workP.promotedData = graph.promoted;
    workP.attachedData = graph.attached;
    workP.unattachedData = graph.unattached;
    workP.rawData = graph;


    return 'function value';
  };
})(window.workP); //execte declaration and pass namespace
