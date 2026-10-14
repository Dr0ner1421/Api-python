import json
import sys
from pathlib import Path
from tkinter import StringVar, Tk, messagebox, ttk
from typing import Any

from bson import ObjectId
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pymongo.errors import PyMongoError

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.database import client, database  # noqa: E402

MAX_DOCUMENTS = 200
COLLECTIONS = {
    "usuarios": "Usuarios",
    "empresas_micro_negocios": "Empresas",
    "estudiantes": "Estudiantes",
    "usuarios_generales": "Usuarios generales",
    "solicitudes_servicio": "Solicitudes",
}
HIDDEN_FIELDS = {"contrasena", "confirmar_contrasena", "password", "token"}


def display_value(value: Any) -> str:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, default=str)
    return str(value)


class DatabaseViewer:
    def __init__(self, root: Tk) -> None:
        self.root = root
        root.title(f"BizCerca — datos de MongoDB ({database.name})")
        root.geometry("1250x760")
        root.minsize(900, 560)

        self.collection_var = StringVar()
        self.documents: list[dict[str, Any]] = []
        self.collection_counts: dict[str, int] = {}

        controls = ttk.Frame(root, padding=10)
        controls.pack(fill="x")
        ttk.Label(controls, text="Tabla:").pack(side="left")
        self.collection_picker = ttk.Combobox(
            controls,
            textvariable=self.collection_var,
            values=list(COLLECTIONS),
            state="readonly",
            width=28,
        )
        self.collection_picker.pack(side="left", padx=(6, 16))
        self.collection_picker.bind(
            "<<ComboboxSelected>>", lambda _event: self.load_collection()
        )
        ttk.Button(controls, text="Actualizar", command=self.refresh_data).pack(
            side="left", padx=8
        )

        self.status_var = StringVar(value=f"Base de datos: {database.name}")
        ttk.Label(root, textvariable=self.status_var, padding=(10, 0)).pack(
            anchor="w"
        )

        content = ttk.PanedWindow(root, orient="vertical")
        content.pack(fill="both", expand=True, padx=10, pady=10)

        table_frame = ttk.Frame(content)
        self.table = ttk.Treeview(table_frame, show="headings")
        vertical_scroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame, orient="horizontal", command=self.table.xview
        )
        self.table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )
        self.table.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        content.add(table_frame, weight=3)

        self.figure = Figure(figsize=(10, 4), tight_layout=True)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=content)
        content.add(self.canvas.get_tk_widget(), weight=2)

        self.collection_picker.current(0)
        root.protocol("WM_DELETE_WINDOW", self.close)
        self.refresh_data()

    def refresh_data(self) -> None:
        try:
            self.collection_counts = {
                name: database[name].count_documents({})
                for name in COLLECTIONS
            }
        except PyMongoError as exc:
            messagebox.showerror("Error de MongoDB", str(exc), parent=self.root)
            self.status_var.set("No se pudieron consultar los conteos de MongoDB.")
            return

        self.draw_chart()
        self.load_collection()

    def load_collection(self) -> None:
        collection_name = self.collection_var.get()
        if collection_name not in COLLECTIONS:
            return
        try:
            self.documents = list(
                database[collection_name].find().limit(MAX_DOCUMENTS)
            )
        except PyMongoError as exc:
            messagebox.showerror("Error de MongoDB", str(exc), parent=self.root)
            self.status_var.set("No se pudieron leer los registros de MongoDB.")
            return

        visible_documents = [
            {
                key: value
                for key, value in document.items()
                if key.casefold() not in HIDDEN_FIELDS
            }
            for document in self.documents
        ]
        self._fill_table(visible_documents)
        suffix = " (máximo mostrado)" if len(self.documents) == MAX_DOCUMENTS else ""
        self.status_var.set(
            f"Base: {database.name} | {COLLECTIONS[collection_name]}: "
            f"{self.collection_counts.get(collection_name, 0)} registros totales; "
            f"{len(self.documents)} mostrados{suffix}"
        )

    def _fill_table(self, documents: list[dict[str, Any]]) -> None:
        self.table.delete(*self.table.get_children())
        columns = list(dict.fromkeys(key for document in documents for key in document))
        self.table["columns"] = columns
        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=150, minwidth=80, stretch=True)
        for document in documents:
            self.table.insert(
                "",
                "end",
                values=[display_value(document.get(column, "")) for column in columns],
            )

    def draw_chart(self) -> None:
        self.axes.clear()
        self.axes.set_axis_on()
        names = list(COLLECTIONS)
        labels = [COLLECTIONS[name] for name in names]
        counts = [self.collection_counts.get(name, 0) for name in names]
        bars = self.axes.bar(labels, counts, color="#3182ce")
        self.axes.bar_label(bars, padding=3, fmt="%d")
        self.axes.set_ylabel("Cantidad de registros")
        self.axes.set_title("Registros actuales por tabla")
        self.axes.tick_params(axis="x", labelrotation=20)
        self.axes.margins(y=0.15)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def close(self) -> None:
        client.close()
        self.root.destroy()


def main() -> None:
    try:
        client.admin.command("ping")
    except PyMongoError as exc:
        root = Tk()
        root.withdraw()
        messagebox.showerror(
            "Error de MongoDB",
            f"No se pudo conectar a MongoDB.\n\n{exc}",
            parent=root,
        )
        client.close()
        root.destroy()
        return

    root = Tk()
    DatabaseViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
