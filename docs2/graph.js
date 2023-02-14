var width = 400,
    height = 400;

var data = {
    "myDIVs": [{
        "name": "div1"
    }, {
        "name": "div2"
    }, {
        "name": "div3"
    }, {
        "name": "div4"
    }],
    "myLinks": [{
        "source": 0,
        "target": 1
    }, {
        "source": 0,
        "target": 2
    }, {
        "source": 1,
        "target": 0
    }, {
        "source": 3,
        "target": 2
    }]
};

var nodes = data.myDIVs,
    links = data.myLinks;

var svg = d3.select('body').append('svg')
    .attr('width', width)
    .attr('height', height);

var force = d3.layout.force()
    .size([width, height])
    .nodes(nodes)
    .links(links)
    .linkDistance(250)
    .charge(-50);

var link = svg.selectAll('.link')
    .data(links)
    .enter().append('line')
    .attr('class', 'link');

var node = d3.selectAll('div')
    .data(nodes)
    .each(function (d) {
        var self = d3.select('#' + d.name);
        self.style("position", "absolute");
    });

force.on('end', function () {
    node
        .style('left', function (d) {
            return d.x + "px";
        })
        .style('top', function (d) {
            return d.y + "px";
        });

    link.attr('x1', function (d) {
        return d.source.x;
    })
        .attr('y1', function (d) {
            return d.source.y;
        })
        .attr('x2', function (d) {
            return d.target.x;
        })
        .attr('y2', function (d) {
            return d.target.y;
        });
});

force.start();
for (var i = 0; i < 100; ++i) force.tick();
force.stop();