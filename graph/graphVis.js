// create an array with nodes
function creat_graph(container_id, course_name, course_pre, course_taken){
    var nodes = []
    var start = { id: course_name, 
                  label: course_name, 
                  shape: 'box',
                  level: 0,
                  inDegree: 0,
                  on: false}

    if (course_name in course_taken) start['color'] = 'green'
    else start['color'] = 'red'

    nodes.push(start)
    var edges = []
    var nodes = new vis.DataSet(nodes)

    // create an array with edges
    var edges = new vis.DataSet(edges)
    // create a network
    var container = document.getElementById(container_id)

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    }
    var options = { layout: {
                        hierarchical: {
                            direction: 'DU'
                        }
                    },
                    interaction: {dragNodes :false},
                    physics: {enabled: false}

                }

    // initialize your network!
    var network = new vis.Network(container, data, options)
    recursive_build(course_name, nodes, edges, course_pre, course_taken)
    network.on('click', function (params){
        if (params['nodes'].length == 0){
            //console.log('Not click on node')
            return 
        }
        var click_class = nodes.get(params['nodes'][0])
        if (!click_class['on'])
            show(click_class, nodes, edges)
        else{
            recursive_hide(click_class, nodes, edges)
            click_class['on'] = false
            nodes.update(click_class)
        }
    })

    return network
}

function show(click_class, nodes, edges){
    if (click_class['on']){
        console.log('Warning: class clicked is already on...')
        return
    }
    click_class['on'] = true
    nodes.update(click_class)

    if (typeof click_class['next_level_node'] == 'undefined'){
        console.log('No futher prerequisite')
        return
    }

    var n_nodes = nodes.get(click_class['next_level_node'])
    var n_edges = edges.get(click_class['next_level_edge'])
    for (var i = 0; i < n_nodes.length; i ++){
        n_nodes[i]['hidden'] = false
        n_nodes[i]['inDegree'] += 1
    }
    nodes.update(n_nodes)
    for (var i = 0; i < n_edges.length; i ++){
        n_edges[i]['hidden'] = false
    }
    edges.update(n_edges)
}

function recursive_hide(cls, nodes, edges){
    if (!cls['on']){
        console.log('Class clicked is already off...')
        return
    }

    if (typeof cls['next_level_node'] == 'undefined'){
        console.log('No futher prerequisite')
        return
    }

    var n_nodes = nodes.get(cls['next_level_node'])
    var n_edges = edges.get(cls['next_level_edge'])

    for (var i = 0; i < n_edges.length; i ++){
        n_edges[i]['hidden'] = true
    }
    edges.update(n_edges)

    for (var i = 0; i < n_nodes.length; i++){
        n_nodes[i]['inDegree'] -= 1
        if (n_nodes[i]['inDegree'] == 0){
            recursive_hide(n_nodes[i], nodes, edges)
            n_nodes[i]['hidden'] = true
            n_nodes[i]['on'] = false

        }
        if (n_nodes[i]['inDegree'] < 0) 
            console.log('Warning: Somethings go wrong when update in degree...')
    }
    nodes.update(n_nodes)
    

}



function recursive_build(cur_class, nodes, edges, course_pre, course_taken){
    var next_level = build(cur_class, nodes, edges, course_pre, course_taken)
    for (var i = 0; i < next_level.length; i ++){
        recursive_build(next_level[i], nodes, edges, course_pre, course_taken)
    }

}

function build(class_name, nodes, edges, course_pre, course_taken){
    var class_node = nodes.get(class_name)
    var next_level = []
    var next_level_edge = []
    if (!course_pre.hasOwnProperty(class_node['label'])){
        //console.log('no prerequisite')
        return next_level
    }

    var cls_pre = course_pre[class_node['label']]
    for (var pre in cls_pre['courses']){
        if (typeof cls_pre['courses'][pre] === 'string'){
            next_level.push(cls_pre['courses'][pre])
            var edge_id = class_node['id'] + '->' + cls_pre['courses'][pre]
            next_level_edge.push(edge_id)

            var green = false
            if (course_taken.has(cls_pre['courses'][pre])) green = true

            add_node_edge(cls_pre['courses'][pre], 
                          class_node, edge_id, cls_pre['type'],
                          nodes, edges, 2, green)
        }else{
            var nest_pre = cls_pre['courses'][pre]
            var tmp_id = Math.floor(Math.random() * 2147483647)
            next_level.push(tmp_id)
            var edge_id = class_node['id'] + '->' + tmp_id
            next_level_edge.push(edge_id)

            add_node_edge(tmp_id, class_node, 
                          edge_id, cls_pre['type'],
                          nodes, edges, 1, false, true)

            inter_node = nodes.get(tmp_id)
            if (nest_pre['type'] == 'and') inter_color = true
            else inter_color = false

            for (var sub_pre in nest_pre['courses']){
                next_level.push(nest_pre['courses'][sub_pre])
                var edge_id = tmp_id + '->' + nest_pre['courses'][sub_pre]
                next_level_edge.push(edge_id)

                var green = false
                if (course_taken.has(nest_pre['courses'][sub_pre])) green = true
                if (nest_pre['type'] == 'and') inter_color &= green
                else inter_color |= green

                add_node_edge(nest_pre['courses'][sub_pre], 
                              inter_node, edge_id, nest_pre['type'],
                              nodes, edges, 1, green)

            }

            if (inter_color){
                inter_node['color'] = 'green'
                nodes.update(inter_node)
            }

        }
    }
    nodes.update({id: class_node['id'], 
                  next_level_node: next_level, 
                  next_level_edge: next_level_edge})
    return next_level
}

function add_node_edge(cur_name, parent_node, edge_id, edge_type, nodes, edges, level, green, inter=false) {
    if (!inter){
        var node = {id: cur_name, 
                    label: cur_name, 
                    shape: 'box',
                    level: parent_node['level'] + level,
                    hidden: true,
                    inDegree: 0,
                    on: false}
    }else{
        var node = {id: cur_name, 
                    level: parent_node['level'] + level,
                    hidden: true,
                    inDegree: 0,
                    on: false}
    }

    if (green) node['color'] = 'green'
    else node['color'] = 'red'

    nodes.update(node)

    var edge = {id: edge_id,
                from: parent_node['id'], 
                to: cur_name,
                hidden: true,
                color: {inherit: 'to'}}


    if (edge_type === 'and'){
        edge['dashes'] = false
    }else if (edge_type === 'or'){
        edge['dashes'] = true   
    }

    edges.update(edge)
}