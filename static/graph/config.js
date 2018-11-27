options = { nodes: {
                    borderWidth: 2,
                    shadow:true
            },
            edges: {
                shadow:true
            },

            layout: {
                hierarchical: {
                    direction: 'DU',
                    levelSeparation: 100
                }
            },
            interaction: {dragNodes :false,
                          hover:true},
            physics: {enabled: false},
            legend: {enabled: true}
        }

color_style = { red: {
                    background:'rgba(255, 46, 46, 0.5)', 
                    border:'rgba(232, 38, 38, 1)'
                },
                green: {
                    background: 'rgba(70, 230, 30, 0.4)', 
                    border: 'rgba(68, 193, 37, 1)'
                },
            }
