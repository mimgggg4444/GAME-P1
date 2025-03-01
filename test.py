from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextureStage, TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # 기본 카메라 컨트롤 비활성화 및 카메라 위치 설정
        self.disableMouse()
        self.camera.setPos(0, -20, 3)
        
        # 1. 3D 사람 모델(예제: ralph)을 로드하고 씬에 배치
        self.character_model = self.loader.loadModel("models/ralph")
        self.character_model.reparentTo(self.render)
        self.character_model.setPos(0, 10, 0)
        self.character_model.setScale(0.2)
        
        # 2. 캐릭터 얼굴 텍스처로 사용할 스프라이트 시트 로드 (2.jpeg)
        self.face_texture = self.loader.loadTexture("2.jpeg")
        # 전체 모델에 텍스처 적용 (실제 사용 시 얼굴 영역만 분리해 적용하는 것이 좋습니다)
        self.character_model.setTexture(self.face_texture, 1)
        self.character_model.setTransparency(TransparencyAttrib.MAlpha)
        
        # 3. 캐릭터 옆에 대사 ("안녕") 표시
        self.dialogue = OnscreenText(
            text="안녕",
            pos=(0.3, 0, 0),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft
        )
        
        # 4. 스프라이트 시트의 픽셀 정보 (2.jpeg 전체 크기: 2480×3508)
        # 캐릭터 셀 영역: 1250×1050 픽셀 (2열 x 3행 구성)
        self.cell_width = 1250.0    # 셀 너비 (픽셀)
        self.cell_height = 1050.0   # 셀 높이 (픽셀)
        self.tex_width = 2480.0     # 전체 텍스처 너비 (픽셀)
        self.tex_height = 3508.0    # 전체 텍스처 높이 (픽셀)
        
        # UV 좌표 스케일 (0~1 범위)
        self.uv_scale_u = self.cell_width / self.tex_width
        self.uv_scale_v = self.cell_height / self.tex_height
        
        # 5. 표정 인덱스와 매핑 (스프라이트 시트의 grid: 2열 x 3행)
        # 행 0: 상단, 행 1: 중단, 행 2: 하단  
        # col 0: 왼쪽, col 1: 오른쪽
        self.expressions = {
            0: (0, 0),  # 노말 앞모습 (왼쪽 상단)
            1: (1, 0),  # 옆모습 (오른쪽 상단)
            2: (0, 1),  # 부끄러워하는 모습 (왼쪽 중단)
            3: (1, 1),  # 쳐다보는 모습 (오른쪽 중단)
            4: (0, 2),  # 윙크하는 모습 (왼쪽 하단)
            5: (1, 2)   # 놀라는 모습 (오른쪽 하단)
        }
        self.current_expression = 0
        self.set_expression(self.current_expression)
        
        # 6. 키 입력 설정 (←, →로 순환, 숫자 1~6로 직접 선택)
        self.accept("arrow_left", self.prev_expression)
        self.accept("arrow_right", self.next_expression)
        self.accept("1", lambda: self.set_expression(0))
        self.accept("2", lambda: self.set_expression(1))
        self.accept("3", lambda: self.set_expression(2))
        self.accept("4", lambda: self.set_expression(3))
        self.accept("5", lambda: self.set_expression(4))
        self.accept("6", lambda: self.set_expression(5))
        
        # 7. (선택사항) 모델 회전을 줘서 3D 효과 확인
        self.character_model.hprInterval(20, (360, 0, 0)).loop()
        
    def set_expression(self, expr_index):
        if expr_index not in self.expressions:
            return
        self.current_expression = expr_index
        col, row = self.expressions[expr_index]
        
        # UV 오프셋 계산:
        # - u 방향: col에 따라 (왼쪽: 0, 오른쪽: uv_scale_u)
        offset_u = col * self.uv_scale_u
        # - v 방향: Panda3D의 UV 원점은 좌측하단이므로 상단 행은 1 - uv_scale_v,
        #   중단은 1 - 2*uv_scale_v, 하단은 1 - 3*uv_scale_v
        offset_v = 1 - (row + 1) * self.uv_scale_v
        
        # 텍스처 변환 적용: 전체 모델에 대해 적용됨
        self.character_model.setTexScale(TextureStage.getDefault(), self.uv_scale_u, self.uv_scale_v)
        self.character_model.setTexOffset(TextureStage.getDefault(), offset_u, offset_v)
        
        print(f"표정 {expr_index} 설정: col={col}, row={row}, offset=({offset_u}, {offset_v})")
        
    def next_expression(self):
        next_index = (self.current_expression + 1) % len(self.expressions)
        self.set_expression(next_index)
        
    def prev_expression(self):
        prev_index = (self.current_expression - 1) % len(self.expressions)
        self.set_expression(prev_index)

app = MyApp()
app.run()
