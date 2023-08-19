// instance {FlowStreamInstance};
// $ {FlowStreamMessage};
// vars {Object};
// repo {Object};
// data {String/Number/Boolean/Date/Buffer/Object};
// $.send('output', data); // or simply send(data); which uses the first output
// $.destroy();
// $.throw(err);

// IMPORTANT: If you do not perform re-send, you need to destroy this message via $.destroy() method
// IMPORTANT: methods $.send(), $.destroy() and $.throw() can be executed only once

// Note ther is no check on whether the id is properly formed


$.send('output', "report--f2b63e80-b523-4747-a069-35c002c690db");