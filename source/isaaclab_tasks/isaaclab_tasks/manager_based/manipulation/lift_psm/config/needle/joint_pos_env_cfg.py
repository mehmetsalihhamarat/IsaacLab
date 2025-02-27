# Copyright (c) 2024, The ORBIT-Surgical Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from isaaclab_assets import ISAACLAB_ASSETS_DATA_DIR
#
#import torch
#from isaaclab.managers import SceneEntityCfg
#
import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.sensors import CameraCfg, FrameTransformerCfg, TiledCameraCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.utils import configclass

from isaaclab_tasks.manager_based.manipulation.lift_psm import mdp
from isaaclab_tasks.manager_based.manipulation.lift_psm.lift_env_cfg import LiftEnvCfg

##
# Pre-defined configs
##
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
from isaaclab_assets.robots.psm import PSM_CFG  # isort: skip


@configclass
class NeedleLiftEnvCfg(LiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set PSM as robot
        self.scene.robot = PSM_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (PSM)
        self.actions.body_joint_pos = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=[
                "psm_yaw_joint",
                "psm_pitch_end_joint",
                "psm_main_insertion_joint",
                "psm_tool_roll_joint",
                "psm_tool_pitch_joint",
                "psm_tool_yaw_joint",
            ],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.finger_joint_pos = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["psm_tool_gripper.*_joint"],
            open_command_expr={"psm_tool_gripper1_joint": -0.5, "psm_tool_gripper2_joint": 0.5},
            close_command_expr={"psm_tool_gripper1_joint": -0.09, "psm_tool_gripper2_joint": 0.09},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "psm_tool_tip_link"

        # Set Suture Needle as object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(pos=(0.0, 0.0, 0.015), rot=(1, 0, 0, 0)),
            spawn=UsdFileCfg(
                usd_path=f"{ISAACLAB_ASSETS_DATA_DIR}/Props/Surgical_needle/needle_sdf.usd",
                scale=(0.4, 0.4, 0.4), ## !!
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=8,
                    max_angular_velocity=200,
                    max_linear_velocity=200,
                    max_depenetration_velocity=1.0,
                    disable_gravity=False,
                ),
            ),
        )
        
        # Set wrist camera
        self.scene.wrist_cam = CameraCfg(
            prim_path="{ENV_REGEX_NS}/Robot/psm_tool_tip_link/wrist_cam",
            update_period=0.0333,
            height=1280,
            width=720,
            data_types=["rgb", "distance_to_image_plane"],
            spawn=sim_utils.PinholeCameraCfg(
                focal_length=0.2, focus_distance=50.0, horizontal_aperture=3, clipping_range=(0.01, 1.0e5)
            ),
            offset=CameraCfg.OffsetCfg(pos=(0.0, 0.035, 0.01), rot=(0, 0, -2, 1), convention="ros"),
        )
        
        # Set table view camera
        self.scene.table_cam = CameraCfg(
            prim_path="{ENV_REGEX_NS}/table_cam",
            update_period=0.0333,
            height=1280,
            width=720,
            data_types=["rgb", "distance_to_image_plane"],
            spawn=sim_utils.PinholeCameraCfg(
                focal_length=20.0, focus_distance=200.0, horizontal_aperture=15, clipping_range=(0.1, 1.0e5)
            ),
            #offset=CameraCfg.OffsetCfg(pos=(0.7, 0.0, 0.4), rot=(-0.45, 0.55, 0.55, -0.45), convention="ros"),
            offset=CameraCfg.OffsetCfg(pos=(0.0, 0.4, 0.25), rot=(0, 0, -1.6, 1), convention="ros"),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.002, 0.002, 0.002)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/psm_base_link",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/psm_tool_tip_link",
                    name="end_effector",
                ),
            ],
        )

@configclass
class NeedleLiftEnvCfg_PLAY(NeedleLiftEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
