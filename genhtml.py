import argparse
import os
import sys
from pathlib import Path



# @function: write the potree converted point cloud data path (metadata.json) 
#            into html files for webshow.
def gen_html(ppc_path, # potree converted point cloud path, e.g. ./***/metadata.json, ***.js
            save_path = 'test.html',  # the path to save the generated html, e.g. ./potree-1.8/examples/***.html
            isprint = False  # whether print the html content
            ): 

    pc_str = ppc_path

    html_str = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="description" content="">
    <meta name="author" content="">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Potree Viewer</title>

    <link rel="stylesheet" type="text/css" href="../build/potree/potree.css">
    <link rel="stylesheet" type="text/css" href="../libs/jquery-ui/jquery-ui.min.css">
    <link rel="stylesheet" type="text/css" href="../libs/openlayers3/ol.css">
    <link rel="stylesheet" type="text/css" href="../libs/spectrum/spectrum.css">
    <link rel="stylesheet" type="text/css" href="../libs/jstree/themes/mixed/style.css">
</head>

<body>
    <script src="../libs/jquery/jquery-3.1.1.min.js"></script>
    <script src="../libs/spectrum/spectrum.js"></script>
    <script src="../libs/jquery-ui/jquery-ui.min.js"></script>
    
    
    <script src="../libs/other/BinaryHeap.js"></script>
    <script src="../libs/tween/tween.min.js"></script>
    <script src="../libs/d3/d3.js"></script>
    <script src="../libs/proj4/proj4.js"></script>
    <script src="../libs/openlayers3/ol.js"></script>
    <script src="../libs/i18next/i18next.js"></script>
    <script src="../libs/jstree/jstree.js"></script>
    <script src="../build/potree/potree.js"></script>
    <script src="../libs/plasio/js/laslaz.js"></script>
    
    <!-- INCLUDE ADDITIONAL DEPENDENCIES HERE -->
    <!-- INCLUDE SETTINGS HERE -->
    
    <div class="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <div id="potree_render_area" style="background-image: url('background.png');"></div>
        <div id="potree_sidebar_container"> </div>
    </div>
    
    <script type="module">

    import * as THREE from "../libs/three.js/build/three.module.js";
    
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));
        
        viewer.setEDLEnabled(true);
        viewer.setFOV(60);
        viewer.setPointBudget(1_000_000);
        viewer.loadSettingsFromURL();
        
        viewer.setDescription("");
        
        // viewer.loadGUI(() => {{
        // 	viewer.setLanguage('en');
        // 	$("#menu_appearance").next().show();
        // 	//viewer.toggleSidebar();
        // }});

        viewer.path = "{pc_str}";
        
        // Ocean
        Potree.loadPointCloud(viewer.path, "Ocean", function(e){{

            viewer.scene.addPointCloud(e.pointcloud);
            
            let material = e.pointcloud.material;
            material.size = 1;
            material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
            
            viewer.fitToScreen();
        }});
        
    </script>
        
</body>
</html>            
"""

    if isprint: 
        print(html_str)

    Html_file=open(save_path,"w")
    Html_file.write(html_str)
    Html_file.close()


def print_args(name, opt):
    # Print argparser arguments
    print(f'{name}: ' + ', '.join(f'{k}={v}' for k, v in vars(opt).items()))


def parse_opt():
    FILE = Path(__file__).resolve()
    # ROOT = FILE.parents[0]
    # print(ROOT)
    # ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  
    # print(Path.cwd())  

    parser = argparse.ArgumentParser()
    parser.add_argument('--ppc-path', type=str, default='../pointclouds/lion_takanawa/cloud.js', help='potree converted point cloud path(s)')
    parser.add_argument('--save-path', type=str, default='./potree-1.8/examples/test.html', help='html save path for webshow')
    opt = parser.parse_args()
    print_args(FILE.stem, opt)
    return opt


if __name__ == "__main__":

    input_manner = "Command"  ## "Manual", "Command"

    # Method 1: input
    if input_manner == "Manual":
        path = "../pointclouds/3sdata/metadata.json"
        save_path ='./potree-1.8/examples/test.html'
        gen_html(ppc_path=path, save_path=save_path)
        print("Finished conversion!")
        print("Original data:", path)
        print("Output data:", save_path)
    else:
        # Method 2: command line 
        opt = parse_opt()
        gen_html(**vars(opt))
    


