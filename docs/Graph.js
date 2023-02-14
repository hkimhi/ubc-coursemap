anychart.onDocumentReady(function () {
  fetch("./anygraph.json")
    .then((response) => response.json())
    .then((data) => {
      var chart = anychart.graph();

      chart.data(data);
      chart.title().enabled(true).text("UBC Coursemap");

      var edgeConfig = {
        normal: {stroke: {thickness: 1, color: 'lightgrey'}},
        hovered: {stroke: {thickness: 2, color: 'blue'}},
        selected: {stroke: {thickness: 2, color: 'blue'}},
        tooltip: {enabled:true, format: '{%from} --> {%to}'}
      };
      var nodeConfig = {
        normal: {stroke: {thickness: 2, color: "black"}, fill: "#F0F0F0"},
        hoevered: {stroke: {thickness: 3, color: "#CFCFCF"}},
        selected: {stroke: {thickness: 1, color: 'darkblue'}, fill: 'blue'}
      }
      chart.edges(edgeConfig);
      chart.nodes(nodeConfig);
      chart.layout().type('fixed');
      chart.interactivity().nodes(false); // disallow moving nodes


      chart.listen('click', function(e) {
        var tag = e.domTarget.tag;
        if(tag) {
          console.log(`Clicked ${tag.type} with ID ${tag.id}`);

          if(tag.type == 'node') {
            console.log(tag);
            
            var node;
            for(let i = 0; i < data['nodes'].length; i++) {
              if(data['nodes'][i]['id'] == tag.id) {
                node = data['nodes'][i];
              }
            }

            document.getElementById('course-name').innerHTML = `${node.id} (${node.credits}) - ${node.title}`
            document.getElementById('course-desc').innerHTML = node.desc; 
          }
        }
      })

      document.body.addEventListener('keypress', function(e) {
        // check if the element is an `input` element and the key is `enter`
        if(e.target.nodeName === "INPUT" && e.key === 'Enter') {
          var name = e.target.value;
          var node;
          var found = false;
          for(let i = 0; i < data['nodes'].length; i++) {
            if(data['nodes'][i]['id'] == name) {
              node = data['nodes'][i]
              found = true;
              break;
            }
          }

          if(found) {
            console.log(`Found course with id: ${name}`);
            document.getElementById('course-name').innerHTML = `${node.id} (${node.credits}) - ${node.title}`
            document.getElementById('course-desc').innerHTML = node.desc;

            // node.selected(true);
            chart.unselect();
            chart.select(name);
            chart.select('edge')
            // chart.select(['CPSC 221']);
            // chart.nodes().select(name);
          }
        }
      });


      chart.container("container").draw();
    });
});
