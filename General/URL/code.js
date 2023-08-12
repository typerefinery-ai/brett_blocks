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

$.send('output', "https://raw.githubusercontent.com/os-threat/Stix-ORM/main/test/data/threat_reports/poisonivy.json");