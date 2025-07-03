import flet as ft
from app.controller import Controller
from dataclasses import dataclass
from app.theme.AppColors import AppColors
from services.ImageType import ImageType


@dataclass
class FilterButton:
    name: str
    icon: ft.Icons
    value: str
    control: ft.Control = None
    active: bool = False

class ImgFilter(ft.Container):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller
        self.filter_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=0),
            padding=ft.padding.symmetric(horizontal=20, vertical=28),
        )
        self.selected_test_id = None
        self.filters = [
            FilterButton(name="Threshold", icon=ft.Icons.GRADIENT_OUTLINED, value=ImageType.THRESHOLD, control=None, active=True),
            FilterButton(name="Original", icon=ft.Icons.IMAGE_OUTLINED, value=ImageType.ORIGINAL, control=None, active=False),
            FilterButton(name="Exported", icon=ft.Icons.COMPARE_OUTLINED, value=ImageType.EXPORTED, control=None, active=False),
            # FilterButton(name="Outlined", icon=ft.Icons.IMAGE_SEARCH_OUTLINED, value=ImageType.OUTLINED, control=None, active=False),
        ]
        self._build()

    def _build(self):
        button_list = []
        for filter_data in self.filters:
            button = ft.ElevatedButton(
                filter_data.name,
                icon=filter_data.icon,
                style=self.filter_style,
                expand=True,
                on_click=lambda e, val=filter_data.value: self.change_active_filter(val),
            )
            filter_data.control = button
            button_list.append(button)

        self.content=ft.Row(
            button_list,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
        )
        self.padding=0
        self.margin=0
        self.update_buttons()
    
    def get_active_filter(self) -> ImageType:
        for filter_data in self.filters:
            if filter_data.active:
                return filter_data.value
        return None
    
    def reset(self):
        self.selected_test_id = None
        for filter_data in self.filters:
            filter_data.active = False if filter_data.value != ImageType.THRESHOLD else True
        self.update_buttons()
        self.update()
    
    def change_active_filter(self, filter_value: ImageType):
        for filter_data in self.filters:
            if filter_data.value == filter_value:
                if filter_data.active:
                    return
                else:
                    filter_data.active = True
                    if self.selected_test_id is not None:
                        self.controller.update_img_display(self.selected_test_id, filter_value)
            else:
                filter_data.active = False
        self.update_buttons()
        self.update()

    def update_buttons(self):
        for filter_data in self.filters:
            button = filter_data.control
            if button is not None:
                if filter_data.active:
                    button.bgcolor = AppColors.LIGHT_BLUE
                    button.color = AppColors.DARK
                else:
                    button.bgcolor = AppColors.DARK
                    button.color = ft.Colors.with_opacity(.6, AppColors.LIGHT_BLUE)