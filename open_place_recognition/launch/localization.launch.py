from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get the path to the share directory of the package
    config_dir = os.path.join(
        get_package_share_directory('open_place_recognition'),
        'configs/pipelines'
    )
    qos_front_camera_arg = DeclareLaunchArgument(
        'qos_front_camera',
        default_value='2',
        description='QoS for front camera (0=SystemDefault,1=BestEffort,2=Reliable)'
    )
    qos_back_camera_arg = DeclareLaunchArgument(
        'qos_back_camera',
        default_value='2',
        description='QoS for back camera (0=SystemDefault,1=BestEffort,2=Reliable)'
    )
    qos_lidar_arg = DeclareLaunchArgument(
        'qos_lidar',
        default_value='2',
        description='QoS for lidar (0=SystemDefault,1=BestEffort,2=Reliable)'
    )
    qos_global_ref_arg = DeclareLaunchArgument(
        'qos_global_ref',
        default_value='2',
        description='QoS for global reference subscription (0=SystemDefault,1=BestEffort,2=Reliable)'
    )

    # Declare launch arguments for configurable parameters
    launch_args = [
        qos_front_camera_arg,
        qos_back_camera_arg,
        qos_lidar_arg,
        qos_global_ref_arg,
        # Topics for images and masks
        DeclareLaunchArgument(
            'image_front_topic',
            default_value='/zed_node/left/image_rect_color/compressed',
            description='Front camera image topic.'
        ),
        DeclareLaunchArgument(
            'image_back_topic',
            default_value='/realsense_back/color/image_raw/compressed',
            description='Back camera image topic.'
        ),
        DeclareLaunchArgument(
            'mask_front_topic',
            default_value='/zed_node/left/semantic_segmentation',
            description='Front semantic segmentation mask topic.'
        ),
        DeclareLaunchArgument(
            'mask_back_topic',
            default_value='/realsense_back/semantic_segmentation',
            description='Back semantic segmentation mask topic.'
        ),
        # Lidar topic
        DeclareLaunchArgument(
            'lidar_topic',
            default_value='/velodyne_points',
            description='Lidar pointcloud topic.'
        ),
        # Global reference system (e.g. GPS, barometer) parameters
        DeclareLaunchArgument(
            'enable_global_ref',
            default_value='true',
            description='Enable subscription to global reference system (e.g. GPS, barometer).'
        ),
        DeclareLaunchArgument(
            'global_ref_topic',
            default_value='/global_ref',
            description='Global reference system topic (WGS84).'
        ),
        DeclareLaunchArgument(
            'dataset_dir',
            default_value=os.path.join(os.path.expanduser("~"), "Datasets/itlp_campus_outdoor/01_2023-02-21"),
            description='Path to the dataset directory (database path)'
        ),
        DeclareLaunchArgument(
            'pipeline_cfg',
            default_value=os.path.join(config_dir, 'localization_pipeline.yaml'),
            description='Path to the pipeline configuration file.'
        ),
        DeclareLaunchArgument(
            'image_resize',
            default_value='[320, 192]',
            description='Image resize dimensions.'
        ),
        DeclareLaunchArgument(
            'exclude_dynamic_classes',
            default_value='false',
            description='Exclude dynamic objects from the input data.'
        ),
        # New sensor enable/disable flags
        DeclareLaunchArgument(
            'enable_front_camera',
            default_value='true',
            description='Enable the front camera.'
        ),
        DeclareLaunchArgument(
            'enable_back_camera',
            default_value='true',
            description='Enable the back camera.'
        ),
        DeclareLaunchArgument(
            'enable_lidar',
            default_value='true',
            description='Enable the lidar sensor.'
        ),
        # Reserve variable for future use
        DeclareLaunchArgument(
            'reserve',
            default_value='false',
            description='Reserve variable for future use.'
        )
    ]

    params = {
        "qos_front_camera":         LaunchConfiguration("qos_front_camera"),
        "qos_back_camera":          LaunchConfiguration("qos_back_camera"),
        "qos_lidar":                LaunchConfiguration("qos_lidar"),
        "qos_global_ref":           LaunchConfiguration("qos_global_ref"),
        "image_front_topic":        LaunchConfiguration("image_front_topic"),
        "image_back_topic":         LaunchConfiguration("image_back_topic"),
        "mask_front_topic":         LaunchConfiguration("mask_front_topic"),
        "mask_back_topic":          LaunchConfiguration("mask_back_topic"),
        "lidar_topic":              LaunchConfiguration("lidar_topic"),
        "dataset_dir":              LaunchConfiguration("dataset_dir"),
        "pipeline_cfg":             LaunchConfiguration("pipeline_cfg"),
        "image_resize":             LaunchConfiguration("image_resize"),
        "exclude_dynamic_classes":  LaunchConfiguration("exclude_dynamic_classes"),
        "enable_front_camera":      LaunchConfiguration("enable_front_camera"),
        "enable_back_camera":       LaunchConfiguration("enable_back_camera"),
        "enable_lidar":             LaunchConfiguration("enable_lidar"),
        "enable_global_ref":        LaunchConfiguration("enable_global_ref"),
        "global_ref_topic":         LaunchConfiguration("global_ref_topic"),
        "reserve":                  LaunchConfiguration("reserve"),
    }

    localization_node = Node(
        package='open_place_recognition',
        executable='localization_node.py',
        name='hierarchical_localization',
        output='screen',
        emulate_tty=True,
        parameters=[params]
    )

    return LaunchDescription(launch_args + [localization_node])

if __name__ == '__main__':
    generate_launch_description()
