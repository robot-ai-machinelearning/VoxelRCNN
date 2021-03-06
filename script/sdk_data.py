from lyft_dataset_sdk.lyftdataset import LyftDataset
from config import cfg
import time
from lyft_dataset_sdk.lyftdataset import LyftDatasetExplorer
from lyft_dataset_sdk.utils.data_classes import Box, LidarPointCloud, RadarPointCloud  # NOQA
from pyquaternion import Quaternion
import numpy as np

button = cfg.data.button

lyft_data = LyftDataset(
    data_path=cfg.data.lyft,
    json_path=cfg.data.train_path,
    verbose=False
)


if button.LIST_SCENE: lyft_data.list_scenes()
if button.LIST_CATEG: lyft_data.list_categories()

one_scene = lyft_data.scene[0]
first_sample_token = one_scene["first_sample_token"]
end_sample_token = one_scene["last_sample_token"]
if button.REND_SAMPLE:
    lyft_data.render_sample(first_sample_token, out_path="./data/01")
    lyft_data.render_sample(end_sample_token, out_path="./data/02")


# Sample
sample = lyft_data.get('sample', first_sample_token)
# print("sample keys are, ", sample.keys())
print('list sample in the first sample token')
if button.LIST_SAMPLE: lyft_data.list_sample(sample['token'])
if button.REND_PC_IMG:
    lyft_data.render_pointcloud_in_image(sample_token=sample["token"],
                                         dot_size=1,
                                         pointsensor_channel='LIDAR_TOP',
                                         camera_channel='CAM_FRONT',
                                         out_path="./data/03")


# Sample lidar in 3d
if button.REND_LIDAR_3D:
    lyft_data.render_sample_3d_interactive(sample['token'])


# Sample data
sample_data = sample['data']
# print("sample data keys are, ", sample_data.keys())


# One sensor in sample data
# lidar: type 1
lidar_top_channel = 'LIDAR_TOP'
lidar_data = sample_data[lidar_top_channel]
lidar_token = lyft_data.get('sample_data', lidar_data)
# print("lidar data keys: \n", lidar_data.keys())
# start = time.time()
# lyft_data.render_sample_data(lidar_data['token'], out_path=cfg.data.image)
# print("lidar render time: {:.3f}".format(time.time() - start))
data_path, boxes, camera_intrinsic = lyft_data.get_sample_data(lidar_token['token'])
pc = LidarPointCloud.from_file(data_path)
cs_record = lyft_data.get("calibrated_sensor", lidar_token["calibrated_sensor_token"])
# Points live in the point sensor frame
# Transform the points to the ego vehicle frame
pc.rotate(Quaternion(cs_record["rotation"]).rotation_matrix)
pc.translate(np.array(cs_record["translation"]))


# cam: type 2
cam_front_channel = 'CAM_FRONT'
cam_token = sample_data[cam_front_channel]
# start = time.time()
# lyft_data.render_sample_data(cam_token, out_path=cfg.data.image)
# print("image render time: {:.3f}".format(time.time() - start))
cam = lyft_data.get("calibrated_sensor", lidar_data["calibrated_sensor_token"])


# image to pc
# points, coloring, im, mask = lyft_data.map_pointcloud_to_image(lidar_data['token'],
#                                                          cam_token)
pass



# if __name__ == '__main__':
#     pass