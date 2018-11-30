function show_prerequisites(container_id, course_name, course_history, db){
    preparePrerequisiteData(db, course_name)
    .then( function (course_pre){
        creat_graph(container_id, course_name, course_pre, course_history, db);
    })
}

function creat_graph(container_id, course_name, course_pre, course_taken, db){
    var nodes = []
    var start = { id: course_name, 
                  label: course_name, 
                  shape: 'box',
                  level: 0,
                  inDegree: 0,
                  on: false,
                  build: false,
                  }

    if (course_taken.has(course_name)) start['color'] = color_style['green']
    else start['color'] = color_style['red']

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
    // initialize your network!
    var network = new vis.Network(container, data, options)

    //recursive_build(course_name, nodes, edges, course_pre, course_taken)
    network.on('click', function (params){
        if (params['nodes'].length == 0){
            //console.log('Not click on node')
            return 
        }
        var click_class = nodes.get(params['nodes'][0])
        if (!click_class['build']){
            build(click_class, nodes, edges, course_pre, course_taken)
            click_class = nodes.get(params['nodes'][0])
        }

        if (!click_class['on']){
            show(click_class, nodes, edges)
            if(click_class.hasOwnProperty('cut_branches')){
                console.log(click_class['cut_branches'])
            }

        }else{
            recursive_hide(click_class, nodes, edges)
            click_class['on'] = false
            nodes.update(click_class)
        }

    })
    network.on('hoverNode', function (params){
        var hover_class = nodes.get(params['node'])
        if (!hover_class.hasOwnProperty('title')){

            var data_promise = getClassbyIdentifier(db, hover_class['id'])
            .then( function (value){
                hover_class['title'] = course_detail(value)
                nodes.update(hover_class)
            })
        }
    })

    return network
}

function course_detail(data){
    var string = ('<p>' + data['fullname'] + '</p>')
    string += ("<p>Grade Basis: " + data['grade_basis'] + '</p>')
    if (!data.hasOwnProperty('sections'))
        string += ('<p>No sections provided this semester.</p>')
    else
        string += ('<p>' + data['sections'].length.toString() + " sections provided this semester.</p>")

    return string

}

function show(click_class, nodes, edges){
    if (click_class['on']){
        console.log('Warning: The clicked-on class is already displayed...')
        return
    }
    click_class['on'] = true
    nodes.update(click_class)

    if (typeof click_class['next_level_node'] == 'undefined'){
        console.log('No further prerequisites')
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
        console.log('The clicked-on class is already hidden...')
        return
    }

    if (typeof cls['next_level_node'] == 'undefined'){
        console.log('No further prerequisite')
        return
    }

    var n_nodes = nodes.get(cls['next_level_node'])
    var n_edges = edges.get(cls['next_level_edge'])

    for (var i = 0; i < n_edges.length; i ++){
        n_edges[i]['hidden'] = true
    }
    edges.update(n_edges)

    var next_update = []
    for (var i = 0; i < n_nodes.length; i++){
        n_nodes[i]['inDegree'] -= 1
        if (n_nodes[i]['inDegree'] == 0){
            next_update.push(n_nodes[i])
        }
        if (n_nodes[i]['inDegree'] < 0) 
            console.log('Warning: Somethings go wrong when update in degree...')
    }
    nodes.update(n_nodes)

    for (var i = 0; i < next_update.length; i++){
        recursive_hide(next_update[i], nodes, edges)
        nodes.update({id: next_update[i]['id'], 
                      hidden: true,
                      on: false})
    }
    

}

function recursive_build(cur_class, nodes, edges, course_pre, course_taken){
    var next_level = build(nodes.get(cur_class), nodes, edges, course_pre, course_taken)
    for (var i = 0; i < next_level.length; i ++){
        recursive_build(next_level[i], nodes, edges, course_pre, course_taken)
    }

}

function build(class_node, nodes, edges, course_pre, course_taken){
    var next_level = []
    var next_level_edge = []
    if (!course_pre.hasOwnProperty(class_node['label'])){
        //console.log('no prerequisite')
        return next_level
    }

    var cls_pre = course_pre[class_node['label']]
    var first_list = []

    for (var pre in cls_pre['courses']){
        if (typeof cls_pre['courses'][pre] === 'string'){
            next_level.push(cls_pre['courses'][pre])
            if (cls_pre['type'] == 'or') first_list.push(cls_pre['courses'][pre])

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

            var second_list = []
            for (var sub_pre in nest_pre['courses']){
                next_level.push(nest_pre['courses'][sub_pre])
                second_list.push(nest_pre['courses'][sub_pre])

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
            first_list.push(second_list)

            if (inter_color){
                inter_node['color'] = color_style['green']
                nodes.update(inter_node)
            }

        }
    }
    nodes.update({id: class_node['id'], 
                  next_level_node: next_level, 
                  next_level_edge: next_level_edge,
                  build: true})

    // This part still haven't Done
    // if (cls_pre['type'] == 'or') {
    //     var all = first_list.flat()

    //     for (var i = 0; i < first_list.length; i++){
    //         if (typeof first_list[i] === 'string'){
    //             nodes.update({id: first_list[i], cut_branches: all})
    //         }else{
    //             var second_all = first_list.slice(0, i).concat(first_list.slice(i + 1, first_list.length)).flat()

    //             for (var j = 0; j < first_list[i].length; j++){
    //                 nodes.update({id: first_list[i][j], cut_branches: second_all})
    //             }
    //         }
    //     }
    // }else {
    //     for (var i = 0; i < first_list.length; i++){
    //         for (var j = 0; j < first_list[i].length; j++){
    //             nodes.update({id: first_list[i][j], cut_branches: first_list[i]})
    //         }
    //     }
    // }
    return next_level
}

function add_node_edge(cur_name, parent_node, edge_id, edge_type, nodes, edges, level, green, inter=false) {
    if (nodes.get(cur_name) == null){
        if (!inter){
            var node = {id: cur_name, 
                        label: cur_name, 
                        shape: 'box',
                        level: parent_node['level'] + level,
                        hidden: true,
                        inDegree: 0,
                        on: false,
                        build: false}
        }else{
            var node = {id: cur_name, 
                        level: parent_node['level'] + level,
                        hidden: true,
                        inDegree: 0,
                        on: false,
                        build: false}
        }

        if (green) node['color'] = color_style['green']
        else node['color'] = color_style['red']

        nodes.update(node)
    }
    if (edges.get(edge_id) == null){
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
}

function addLegend(container_id){
    var nodes = [{ id: 'test', 
                  label: 'test', 
                  shape: 'box',
                  level: 0,
                  inDegree: 0,
                  on: false,
                  build: false,
                  color: color_style['green']
                  },
                  { id: 'test1', 
                  label: 'test', 
                  shape: 'box',
                  level: 0,
                  inDegree: 0,
                  on: false,
                  build: false,
                  color: color_style['green']
                  },
                  { id: 'test2', 
                  label: 'test', 
                  shape: 'box',
                  level: 0,
                  inDegree: 0,
                  on: false,
                  build: false,
                  color: color_style['green']
                  }]

    var nodes = new vis.DataSet(nodes)
    var edges = new vis.DataSet([])
    // create a network
    var container = document.getElementById(container_id)

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    }
    // initialize your network!
    var network = new vis.Network(container, data, options)
}