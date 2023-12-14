from cProfile import label
import open3d as o3d
import numpy as np
from collections import deque
import time
import os
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as img
def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--voxel_size', type=float, default='0.0',
                        help='voxel_size')
    parser.add_argument('--pcd_data_dir', type=str, default="pcd_data",
                        help='pcd_data_dir')
    parser.add_argument('--img_data_dir', type=str, default='image',
                        help='img_data_dir')
    parser.add_argument('--camera_cali', type=str, default='v_600_600.json',
                        help='camera_cali')
    parser.add_argument('--render_param', type=str, default="rendop.json",
                        help='render_param')
    return parser

if __name__ == "__main__":
    count_q = deque([])
    saving_space_q = deque([])
    raw_point_cloud_q = deque([])
    voxel_point_cloud_q = deque([])
    space_saving_means = []

    # get data path 
    parser = get_argument_parser()
    args = parser.parse_args()
    PCD_DATA_PATH = args.pcd_data_dir
    DATA_PATH = args.img_data_dir
    CAMERA_PARAM = args.camera_cali
    VIEW_RANDER_PARAM = args.render_param
    voxel_size_param = args.voxel_size

    pcd_data_list = sorted(os.listdir(PCD_DATA_PATH))

    data = [ o3d.io.read_point_cloud( os.path.join(PCD_DATA_PATH,i) ) for i in pcd_data_list if ".pcd" in i]
    image_list = sorted(os.listdir(DATA_PATH))

    # animaiton configure
    # vis for origin pcd anmation
    # vis2 for voxelization pcd animation
    vis = o3d.visualization.Visualizer()
    vis2 = o3d.visualization.Visualizer()
    geometry = o3d.geometry.PointCloud()
    vis.create_window(window_name="RAW_POINT_CLOUD",width=600, height=600)
    vis2.create_window(window_name="VOXEL_POINT_CLOUD",width=600, height=600)
    ctr = vis.get_view_control()
    ctr2 = vis2.get_view_control()
    if os.path.isfile(CAMERA_PARAM) and os.path.isfile(VIEW_RANDER_PARAM):
        # point cloud animation setup 
        # camera view : CAMERA_PARAM
        # background setting : VIEW_RENDER_PARAM
        print("LOAD_CAMERA_CONFIG_AND_RENDERING_OPT")

        param = o3d.io.read_pinhole_camera_parameters(CAMERA_PARAM)
        icp_iteration = len(data)
        fig,ax = plt.subplots(ncols=1,nrows=3,gridspec_kw={'height_ratios' : [3,1,1]}, figsize=(7,15))
        for j in range(icp_iteration):
            time.sleep(0.001)

            vis.add_geometry(data[j])
            ctr.convert_from_pinhole_camera_parameters(param)
            vis.get_render_option().load_from_json(VIEW_RANDER_PARAM)
            vis.poll_events()
            vis.update_renderer()
            vis.clear_geometries()

            # Voxelization
            # parameter : voxel_size  
            downpcd = data[j].voxel_down_sample(voxel_size=voxel_size_param)

            o3d.io.write_point_cloud("./Down_pcd.pcd",downpcd)
            vis2.add_geometry(downpcd)
            ctr2.convert_from_pinhole_camera_parameters(param)
            vis2.get_render_option().load_from_json(VIEW_RANDER_PARAM)
            vis2.poll_events()
            vis2.update_renderer()
            vis2.clear_geometries()


            origin_pcd_size = os.path.getsize( os.path.join(PCD_DATA_PATH,pcd_data_list[j]))
            down_pcd_size = os.path.getsize("./Down_pcd.pcd")
            if os.path.exists("./Down_pcd.pcd"):
                os.remove("./Down_pcd.pcd")
            # Space savings 
            space_savings = (1 - (down_pcd_size / origin_pcd_size) )*100
            img_test = img.imread(os.path.join(DATA_PATH,image_list[j]))

            count_q.append(j)
            saving_space_q.append(space_savings)
            raw_point_cloud_q.append(len(np.asarray(data[j].points)))
            voxel_point_cloud_q.append(len(np.asarray(downpcd.points)))

            if len(count_q) > 20:
                count_q.popleft()
                saving_space_q.popleft()
                raw_point_cloud_q.popleft()
                voxel_point_cloud_q.popleft()

            # make multi plot
            # 0 : image
            # 1 : point cloud count
            # 2 : space savings
            
            ax[0].cla()
            ax[0].text(1200.0,0.0,"Space_savings : " + str(space_savings)[:5]+"%")
            ax[0].imshow(img_test)
            ax[0].axis("off")

            ax[1].cla()
            ax[1].plot(count_q,raw_point_cloud_q,label = "ORIGIN_PCD[num]")
            ax[1].plot(count_q,voxel_point_cloud_q,label="VOXELIZATION_PCD[num]")
            ax[1].set_title("POINT CLOUD COUNT GRAPH")
            ax[1].legend(fontsize = 8)
            ax[1].set(ylabel = "COUNT",xlabel = "TIME")

            ax[2].cla()
            ax[2].plot(count_q,saving_space_q,label="SPACE_SAVINGS[%]")
            ax[2].text(count_q[-1],saving_space_q[-1],str(space_savings)[:4] +"%",color = "red", fontsize = 10)
            ax[2].set_title("COMPRESSION GRAPH")
            ax[2].legend(fontsize = 8)
            ax[2].set(ylabel = "SPACE_SAVINGS(%)",xlabel = "TIME")
            ax[2].set_ylim([60,100])
            
            plt.tight_layout()
            print(f"Voxel_size : {voxel_size_param}, Space_savings : {str(space_savings)[:5]}, Origin Point number : {len(np.asarray(data[j].points))}, Voxelization Point number : {len(np.asarray(downpcd.points))}")
            space_saving_means.append(space_savings)
            plt.pause(0.001)

        vis.destroy_window()
        vis2.destroy_window()
        plt.close()
        print(f"POIND_CLOUD_SPACE_SAVINGS : {str(np.mean(space_saving_means))[:6] }")

        
    else:
        if not os.path.isfile(CAMERA_PARAM):
            print("CHECK_CAMERA_CONFIG")
        else:
            print("CHECK_RENDERING_OPT ")
            
        
