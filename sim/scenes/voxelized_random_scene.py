from sim.scenes.random_scene import RandomScene 
import numpy as np

class VoxelizedRandomScene(RandomScene):
    def __init__(self, scene_size_x, scene_size_y, scene_size_z, num_obstacles,
                 min_radius, max_radius, min_height, max_height, voxel_size):
        super().__init__(scene_size_x, scene_size_y, scene_size_z,
                         num_obstacles, min_radius, max_radius,
                         min_height, max_height)
        self.voxel_size = voxel_size
        self.voxel_map = np.zeros((
            int(scene_size_x / voxel_size),
            int(scene_size_y / voxel_size),
            int(scene_size_z / voxel_size)
        ), dtype=np.uint8)

    def build_scene(self):
        self._generate_obstacles()
        self._voxelize_obstacles()

    def _voxelize_obstacles(self):
        nx, ny, nz = self.voxel_map.shape
        margin = 2.0  # 安全扩展距离（单位：米）

        for obs in self.obstacle_list:
            # 获取世界坐标系中的中心点
            x = obs['x'] + self.scene_size_x / 2
            y = obs['y'] + self.scene_size_y / 2
            z = obs['z']  # 中心高度

            if obs['is_cylinder']:
                half_x = obs['radius'] + margin
                half_y = obs['radius'] + margin
            else:
                half_x = obs['length'] / 2 + margin
                half_y = obs['width'] / 2 + margin

            half_z = obs['height'] / 2 + margin

            # 将世界坐标转为体素索引
            min_i = int((x - half_x) / self.voxel_size)
            max_i = int((x + half_x) / self.voxel_size)
            min_j = int((y - half_y) / self.voxel_size)
            max_j = int((y + half_y) / self.voxel_size)
            min_k = int((z - half_z) / self.voxel_size)
            max_k = int((z + half_z) / self.voxel_size)

            # 边界限制
            min_i = max(0, min_i)
            max_i = min(nx - 1, max_i)
            min_j = max(0, min_j)
            max_j = min(ny - 1, max_j)
            min_k = max(0, min_k)
            max_k = min(nz - 1, max_k)

            # 标记体素地图
            self.voxel_map[min_i:max_i + 1, min_j:max_j + 1, min_k:max_k + 1] = 1
            


    def get_voxel_map(self):
        return self.voxel_map
