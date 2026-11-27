import flet as ft
from models import Student, load_students, save_students

PAPER = "#F3EBD8"
INK = "#1F3A5F"
RED_PENCIL = "#B23A2E"
CHALK = "#E8EDE4"


def main(page: ft.Page):
    page.title = "The Class Register"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=INK)

    students = load_students()
    state = {"editing": None}

    def close_dialog(e):
        page.pop_dialog()

    def show_message(title, text):
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text(title),
                content=ft.Text(text),
                actions=[ft.TextButton("OK", on_click=close_dialog)],
            )
        )

    def chalkboard(controls, centered=False):
        return ft.Container(
            expand=True,
            image=ft.DecorationImage(src="chalkboard.png", fit=ft.BoxFit.COVER),
            padding=20,
            content=ft.Column(
                expand=True,
                controls=controls,
                alignment=ft.MainAxisAlignment.CENTER if centered else ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER if centered else ft.CrossAxisAlignment.START,
            ),
        )

    async def go_home(e=None):
        await page.push_route("/")

    async def go_add(e):
        state["editing"] = None
        await page.push_route("/add")

    async def go_edit(student):
        state["editing"] = student
        await page.push_route("/edit")

    # actions 
    def toggle_present(student, value):
        student.present = value
        save_students(students)
        route_change()

    def delete_student(student):
        if student in students:
            students.remove(student)
            save_students(students)
        page.pop_dialog()
        route_change()

    def confirm_delete(student):
        dialog = ft.AlertDialog(
            title=ft.Text("Remove student?"),
            content=ft.Text(f"{student.name} {student.surname} will be taken off the register."),
        )

        def cancel(e):
            dialog.open = False
            page.update()

        def remove(e):
            if student in students:
                students.remove(student)
                save_students(students)
            dialog.open = False
            route_change()

        dialog.actions = [
            ft.TextButton("Cancel", on_click=cancel),
            ft.TextButton("Remove", on_click=remove),
        ]
        page.show_dialog(dialog)

    # home view 
    def student_row(student):
        colour = INK if student.present else RED_PENCIL
        return ft.Container(
            bgcolor=PAPER,
            border_radius=6,
            padding=10,
            content=ft.Row(
                controls=[
                    ft.Checkbox(
                        value=student.present,
                        active_color=INK,
                        on_change=lambda e: toggle_present(student, e.control.value),
                    ),
                    ft.Column(
                        spacing=0,
                        expand=True,
                        controls=[
                            ft.Text(
                                f"{student.name} {student.surname}",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                font_family="Georgia",
                                color=colour,
                            ),
                            ft.Text(
                                f"Grade {student.grade}  |  {'Present' if student.present else 'Absent'}",
                                size=13,
                                color=colour,
                            ),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color=INK,
                        tooltip="Edit",
                        on_click=lambda e: page.run_task(go_edit, student),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=RED_PENCIL,
                        tooltip="Delete",
                        on_click=lambda e: confirm_delete(student),
                    ),
                ]
            ),
        )

    def home_view():
        present_count = sum(1 for s in students if s.present)
        if students:
            rows = [student_row(s) for s in students]
        else:
            rows = [ft.Text("The register is empty.", color=CHALK, size=18, font_family="Georgia")]

        return ft.View(
            route="/",
            padding=0,
            controls=[
                chalkboard(
                    [
                        ft.Text("The Class Register", size=34, color=CHALK,
                                weight=ft.FontWeight.BOLD, font_family="Georgia"),
                        ft.Text(f"{present_count} of {len(students)} present today", size=15, color=CHALK),
                        ft.Divider(color=CHALK, height=20),
                        ft.Column(rows, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True),
                        ft.Button(
                            "Add student",
                            icon=ft.Icons.ADD,
                            on_click=go_add,
                            style=ft.ButtonStyle(bgcolor=PAPER, color=INK),
                        ),
                    ]
                )
            ],
        )

    # add / edit view 
    def form_view(student):
        editing = student is not None

        name_field = ft.TextField(
            label="First name", value=student.name if editing else "",
            border_color=INK, focused_border_color=RED_PENCIL,
        )
        surname_field = ft.TextField(
            label="Surname", value=student.surname if editing else "",
            border_color=INK, focused_border_color=RED_PENCIL,
        )
        grade_field = ft.TextField(
            label="Grade (number)", value=student.grade if editing else "",
            border_color=INK, focused_border_color=RED_PENCIL,
        )
        present_box = ft.Checkbox(
            label="Present today", value=student.present if editing else True, active_color=INK,
        )

        async def save_click(e):
            name = name_field.value.strip()
            surname = surname_field.value.strip()
            grade = grade_field.value.strip()

            if not name or not surname or not grade:
                show_message("Missing details", "Please fill in every field.")
                return
            if not grade.isdigit() or not 1 <= int(grade) <= 12:
                show_message("Check the grade", "Grade must be a number from 1 to 12.")
                return

            new_student = Student(name, surname, grade, present_box.value)
            if editing:
                students[students.index(student)] = new_student  # replace
            else:
                students.append(new_student)
            save_students(students)
            await page.push_route("/")

        card = ft.Container(
            bgcolor=PAPER,
            border_radius=10,
            padding=20,
            width=380,
            content=ft.Column(
                tight=True,
                spacing=14,
                controls=[
                    ft.Text(
                        "Edit entry" if editing else "New entry",
                        size=26, weight=ft.FontWeight.BOLD, font_family="Georgia", color=INK,
                    ),
                    name_field,
                    surname_field,
                    grade_field,
                    present_box,
                    ft.Row(
                        controls=[
                            ft.TextButton("Back", on_click=go_home),
                            ft.Button("Save", on_click=save_click,
                                      style=ft.ButtonStyle(bgcolor=INK, color=PAPER)),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
            ),
        )

        return ft.View(
            route="/edit" if editing else "/add",
            padding=0,
            controls=[chalkboard([card], centered=True)],
        )

    # routing 
    def route_change(e=None):
        page.views.clear()
        page.views.append(home_view())
        if page.route == "/add":
            page.views.append(form_view(None))
        elif page.route == "/edit" and state["editing"] is not None:
            page.views.append(form_view(state["editing"]))
        page.update()

    page.on_route_change = route_change
    route_change()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")