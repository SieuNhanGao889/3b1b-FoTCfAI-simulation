import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from config import *

# Import all scenes
from scenes.scene_1a_point_to_block import PointToBlock
from scenes.scene_1b_recommender import RecommenderTensor
from scenes.scene_1c_data_explosion import DataExplosion
from scenes.scene_2a_cnn_tensor import CNNTensor
from scenes.scene_2b_cp_decomposition import CPDecomposition
from scenes.scene_2c_lora import LoRAScene
from scenes.scene_2d_polynomial_networks import PolynomialNetworks
from scenes.scene_3ab_circuits import CircuitsAndSPN  
from scenes.scene_3c_attention import PolynomialAttention
from scenes.scene_4ab_data_mining import DataMiningAB
from scenes.scene_4cd_coupled_cases import CoupledAndCases
from scenes.scene_5_finale import Finale

class TensorFullVideo(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # --- Scene 1 ---
        PointToBlock.construct(self)
        self.wait(0.2)
        self.clear()

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)

        # --- SCENE 1B ---
        RecommenderTensor.construct(self)
        self.clear()

        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0)

        # --- SCENE 1C ---
        DataExplosion.construct(self)
        self.clear()

        # --- Scene 2 ---
        # CNNTensor.construct(self)
        # self.clear()

        # CPDecomposition.construct(self)
        # self.clear()

        # LoRAScene.construct(self)
        # self.clear()

        # PolynomialNetworks.construct(self)
        # self.clear()

        # # --- Scene 3 ---
        # CircuitsAndSPN.construct(self)
        # self.clear()    

        # PolynomialAttention.construct(self)
        # self.clear()
        
        # # --- Scene 4 ---
        # DataMiningAB.construct(self)
        # self.clear()

        # CoupledAndCases.construct(self)
        # self.clear()

        # # --- Scene 5 ---
        # Finale.construct(self)
        # self.wait(2) 