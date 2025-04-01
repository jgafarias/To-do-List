import flet as ft

# Classe que representa uma tarefa individual na lista
class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False  # Status inicial da tarefa
        self.task_name = task_name  # Nome da tarefa
        self.task_status_change = task_status_change  # Callback para alteração de status
        self.task_delete = task_delete  # Callback para deletar a tarefa

        # Checkbox para marcar a tarefa como concluída
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)  # Campo de edição do nome da tarefa

        # Visão padrão da tarefa
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        # Botão para editar a tarefa
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Editar To-Do",
                            on_click=self.edit_clicked,
                        ),
                        # Botão para deletar a tarefa
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Deletar To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        # Visão da tarefa no modo de edição
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Atualizar To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    # Alterna para o modo de edição da tarefa
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    # Salva a edição da tarefa
    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    # Atualiza o status da tarefa (concluído ou não)
    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    # Remove a tarefa da lista
    def delete_clicked(self, e):
        self.task_delete(self)

# Classe principal do aplicativo
class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.new_task = ft.TextField(
            hint_text="O que precisa ser feito? ", on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()  # Lista de tarefas

        # Filtros para exibir tarefas por status
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=1,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Todos"), ft.Tab(text="Ativos"), ft.Tab(text="Completos")],
        )

        self.items_left = ft.Text("0 item(s) faltando")

        self.width = 600
        self.controls = [
            ft.Row(
                [ft.Text(value="To-Do List", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Limpeza completa", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

    # Adiciona uma nova tarefa
    def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()

    # Atualiza a interface ao mudar o status de uma tarefa
    def task_status_change(self, task):
        self.update()

    # Remove uma tarefa da lista
    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    # Filtra as tarefas com base na aba selecionada
    def tabs_changed(self, e):
        self.update()

    # Remove todas as tarefas concluídas
    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    # Atualiza a exibição de tarefas e o contador de itens ativos
    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Todos"
                or (status == "Ativos" and task.completed == False)
                or (status == "Completos" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} item(s) ativo(s) faltando"

# Função principal para rodar o app
def main(page: ft.Page):
    page.title = "To-Do"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.add(TodoApp())

ft.app(main)