import tkinter
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
from mysql.connector import Error

# --- Database Connection using SQLAlchemy ---
def conectar():
    try:
        engine = create_engine('mysql+pymysql://root:@localhost/data_insight_db')
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# --- Main Application Class ---
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DataInsight Corp. Feedback System")
        self.geometry("1200x800")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="DataInsight", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=self.dashboard_frame_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Manage Surveys", command=self.manage_surveys_frame_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Reporting", command=self.reporting_frame_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Manage Clients", command=self.manage_clients_frame_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        # --- Dashboard Frame ---
        self.dashboard_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dashboard_frame.grid_columnconfigure(0, weight=1)
        self.dashboard_frame.grid_rowconfigure(1, weight=1)

        self.welcome_label = customtkinter.CTkLabel(self.dashboard_frame, text="Project Dashboard", font=customtkinter.CTkFont(size=28, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.tabview = customtkinter.CTkTabview(self.dashboard_frame, width=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Likert Scale")
        self.tabview.add("Yes/No")
        self.tabview.add("Open Answers")

        # Defer loading to prevent race conditions on startup
        self.after(100, self.load_dashboard_data)


        # --- Manage Surveys Frame ---
        self.manage_surveys_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.manage_surveys_frame.grid_columnconfigure(0, weight=1)
        self.manage_surveys_frame.grid_rowconfigure(1, weight=1)


        self.surveys_label = customtkinter.CTkLabel(self.manage_surveys_frame, text="Manage Surveys", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.surveys_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.add_survey_button = customtkinter.CTkButton(self.manage_surveys_frame, text="Create New Survey", command=self.add_new_survey)
        self.add_survey_button.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        self.surveys_scrollable_frame = customtkinter.CTkScrollableFrame(self.manage_surveys_frame, label_text="Available Surveys")
        self.surveys_scrollable_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")


        self.after(100, self.load_surveys_data)

        # --- Reporting Frame ---
        self.reporting_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.reporting_frame.grid_columnconfigure(0, weight=1)
        self.reporting_frame.grid_rowconfigure(1, weight=1)

        self.reporting_label = customtkinter.CTkLabel(self.reporting_frame, text="Reporting", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.reporting_label.grid(row=0, column=0, padx=20, pady=20)

        self.reporting_textbox = customtkinter.CTkTextbox(self.reporting_frame, width=400)
        self.reporting_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.generate_report_button = customtkinter.CTkButton(self.reporting_frame, text="Generate Detailed Report", command=self.generate_report)
        self.generate_report_button.grid(row=2, column=0, padx=20, pady=10)

        # --- Manage Clients Frame ---
        self.manage_clients_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.manage_clients_frame.grid_columnconfigure(0, weight=1)
        self.manage_clients_frame.grid_rowconfigure(1, weight=1)

        self.clients_label = customtkinter.CTkLabel(self.manage_clients_frame, text="Manage Clients", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.clients_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.add_client_button = customtkinter.CTkButton(self.manage_clients_frame, text="Add New Client", command=self.add_new_client)
        self.add_client_button.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        self.clients_scrollable_frame = customtkinter.CTkScrollableFrame(self.manage_clients_frame, label_text="Clients")
        self.clients_scrollable_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        self.after(100, self.load_clients_data)


        # --- Initial Frame ---
        self.select_frame_by_name("dashboard")

    def load_initial_data(self):
        self.load_dashboard_data()
        self.load_surveys_data()
        self.load_clients_data()

    def select_frame_by_name(self, name):
        self.dashboard_frame.grid_forget()
        self.manage_surveys_frame.grid_forget()
        self.reporting_frame.grid_forget()
        self.manage_clients_frame.grid_forget()

        if name == "dashboard":
            self.dashboard_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "manage_surveys":
            self.manage_surveys_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "reporting":
            self.reporting_frame.grid(row=0, column=1, sticky="nsew")
        elif name == "manage_clients":
            self.manage_clients_frame.grid(row=0, column=1, sticky="nsew")

    def dashboard_frame_event(self):
        self.select_frame_by_name("dashboard")

    def manage_surveys_frame_event(self):
        self.select_frame_by_name("manage_surveys")

    def reporting_frame_event(self):
        self.select_frame_by_name("reporting")

    def manage_clients_frame_event(self):
        self.select_frame_by_name("manage_clients")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def load_dashboard_data(self):
        engine = conectar()
        if engine:
            try:
                # --- Likert Scale Data ---
                self.clear_frame(self.tabview.tab("Likert Scale"))
                query_likert = """
                SELECT p.texto_pregunta, r.respuesta_escala
                FROM respuestas_encuesta r
                JOIN preguntas_encuesta p ON r.pregunta_id = p.pregunta_id
                WHERE p.tipo_pregunta = 'escala_likert' AND r.respuesta_escala IS NOT NULL
                """
                df_likert = pd.read_sql(query_likert, engine)

                if not df_likert.empty:
                    fig_likert, ax_likert = plt.subplots(figsize=(10, 6))
                    df_likert.groupby('texto_pregunta')['respuesta_escala'].value_counts().unstack().plot(kind='barh', ax=ax_likert)
                    ax_likert.set_title('Likert Scale Survey Responses')
                    ax_likert.set_xlabel('Number of Responses')
                    ax_likert.set_ylabel('Questions')
                    plt.tight_layout()
                    canvas_likert = FigureCanvasTkAgg(fig_likert, master=self.tabview.tab("Likert Scale"))
                    canvas_likert.draw()
                    canvas_likert.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                # --- Yes/No Data ---
                self.clear_frame(self.tabview.tab("Yes/No"))
                query_yes_no = """
                SELECT p.texto_pregunta, r.respuesta_opcion
                FROM respuestas_encuesta r
                JOIN preguntas_encuesta p ON r.pregunta_id = p.pregunta_id
                WHERE p.tipo_pregunta = 'si_no' AND r.respuesta_opcion IS NOT NULL
                """
                df_yes_no = pd.read_sql(query_yes_no, engine)

                if not df_yes_no.empty:
                    counts = df_yes_no.groupby(['texto_pregunta', 'respuesta_opcion']).size().unstack(fill_value=0)
                    fig_yes_no, ax_yes_no = plt.subplots(figsize=(10, 6))
                    counts.plot(kind='pie', subplots=True, autopct='%1.1f%%', legend=False, ax=ax_yes_no)
                    ax_yes_no.set_title('Yes/No Survey Responses')
                    ax_yes_no.set_ylabel('')
                    plt.tight_layout()
                    canvas_yes_no = FigureCanvasTkAgg(fig_yes_no, master=self.tabview.tab("Yes/No"))
                    canvas_yes_no.draw()
                    canvas_yes_no.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                # --- Open Answers Data ---
                self.clear_frame(self.tabview.tab("Open Answers"))
                query_open = """
                SELECT p.texto_pregunta, r.respuesta_texto
                FROM respuestas_encuesta r
                JOIN preguntas_encuesta p ON r.pregunta_id = p.pregunta_id
                WHERE p.tipo_pregunta = 'abierta' AND r.respuesta_texto IS NOT NULL AND r.respuesta_texto != ''
                """
                df_open = pd.read_sql(query_open, engine)
                
                open_answers_text = customtkinter.CTkTextbox(self.tabview.tab("Open Answers"), wrap="word")
                open_answers_text.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

                if not df_open.empty:
                    for index, row in df_open.iterrows():
                        open_answers_text.insert(tkinter.END, f"Q: {row['texto_pregunta']}\n")
                        open_answers_text.insert(tkinter.END, f"A: {row['respuesta_texto']}\n\n")
                else:
                    open_answers_text.insert(tkinter.END, "No open-ended answers found.")


            except Exception as e:
                print(f"Error loading dashboard data: {e}")
            finally:
                engine.dispose()

    def load_surveys_data(self):
        # Clear existing widgets
        for widget in self.surveys_scrollable_frame.winfo_children():
            widget.destroy()

        engine = conectar()
        if engine:
            try:
                with engine.connect() as conn:
                    surveys = conn.execute(text("SELECT encuesta_id, titulo, descripcion FROM encuestas ORDER BY fecha_creacion DESC")).fetchall()
                    
                    for i, survey in enumerate(surveys):
                        survey_frame = customtkinter.CTkFrame(self.surveys_scrollable_frame, border_width=1)
                        survey_frame.pack(fill="x", expand=True, padx=10, pady=5)

                        # Hover effect
                        original_color = survey_frame.cget("fg_color")
                        hover_color = "#343638"
                        survey_frame.bind("<Enter>", lambda event, frame=survey_frame, color=hover_color: frame.configure(fg_color=color))
                        survey_frame.bind("<Leave>", lambda event, frame=survey_frame, color=original_color: frame.configure(fg_color=color))

                        survey_frame.columnconfigure(1, weight=1)

                        title_label = customtkinter.CTkLabel(survey_frame, text=f"{survey[1]} (ID: {survey[0]})", font=customtkinter.CTkFont(weight="bold"))
                        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(5,0), sticky="w")

                        desc_label = customtkinter.CTkLabel(survey_frame, text=survey[2], wraplength=600, justify="left")
                        desc_label.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,5), sticky="w")
                        
                        # Action Buttons
                        buttons_frame = customtkinter.CTkFrame(survey_frame, fg_color="transparent")
                        buttons_frame.grid(row=2, column=1, padx=10, pady=5, sticky="e")

                        add_question_button = customtkinter.CTkButton(buttons_frame, text="Add Question", width=120, command=lambda s_id=survey[0]: self.add_question_to_survey(s_id))
                        add_question_button.pack(side="left", padx=5)

                        answer_survey_button = customtkinter.CTkButton(buttons_frame, text="Answer Survey", width=120, command=lambda s_id=survey[0]: self.answer_survey_event(s_id))
                        answer_survey_button.pack(side="left", padx=5)

                        view_responses_button = customtkinter.CTkButton(buttons_frame, text="View Responses", width=120, command=lambda s_id=survey[0], s_title=survey[1]: self.view_responses_event(s_id, s_title))
                        view_responses_button.pack(side="left", padx=5)


            except Exception as e:
                print(f"Error loading surveys: {e}")
            finally:
                engine.dispose()

    def add_new_survey(self):
        # This will open a dialog to create a new survey
        dialog = customtkinter.CTkInputDialog(text="Enter survey title:", title="Create New Survey")
        title = dialog.get_input()
        if title:
            desc_dialog = customtkinter.CTkInputDialog(text="Enter survey description:", title="Create New Survey")
            description = desc_dialog.get_input()
            if description is None:
                description = "" # Allow empty description

            engine = conectar()
            if engine:
                try:
                    with engine.connect() as conn:
                        # Assuming user ID 1 is creating the survey for now
                        conn.execute(text("INSERT INTO encuestas (titulo, descripcion, creado_por_usuario_id) VALUES (:titulo, :descripcion, 1)"), 
                                     {"titulo": title, "descripcion": description})
                        conn.commit()
                        self.load_surveys_data() # Refresh the list
                except Exception as e:
                    print(f"Error adding survey: {e}")
                finally:
                    engine.dispose()

    def load_clients_data(self):
        # Clear existing widgets
        for widget in self.clients_scrollable_frame.winfo_children():
            widget.destroy()

        engine = conectar()
        if engine:
            try:
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT cliente_id, nombre, apellidos, email, telefono FROM clientes ORDER BY nombre, apellidos"))
                    clients = result.fetchall()
                    
                    for client in clients:
                        client_frame = customtkinter.CTkFrame(self.clients_scrollable_frame, border_width=1)
                        client_frame.pack(fill="x", expand=True, padx=10, pady=5)

                        # Hover effect
                        original_color = client_frame.cget("fg_color")
                        hover_color = "#343638"
                        client_frame.bind("<Enter>", lambda event, frame=client_frame, color=hover_color: frame.configure(fg_color=color))
                        client_frame.bind("<Leave>", lambda event, frame=client_frame, color=original_color: frame.configure(fg_color=color))

                        info_text = f"Name: {client[1]} {client[2]} (ID: {client[0]})\n"
                        if client[3]:
                            info_text += f"Email: {client[3]}\n"
                        if client[4]:
                            info_text += f"Phone: {client[4]}"
                        
                        label = customtkinter.CTkLabel(client_frame, text=info_text, justify="left")
                        label.pack(anchor="w", padx=10, pady=10)

            except Exception as e:
                print(f"Error loading clients: {e}")
            finally:
                engine.dispose()

    def add_new_client(self):
        dialog_name = customtkinter.CTkInputDialog(text="Enter client's first name:", title="Add New Client")
        first_name = dialog_name.get_input()
        if not first_name:
            return

        dialog_lastname = customtkinter.CTkInputDialog(text="Enter client's last name:", title="Add New Client")
        last_name = dialog_lastname.get_input()
        if not last_name:
            last_name = "" # Allow empty last name

        dialog_email = customtkinter.CTkInputDialog(text="Enter client's email (optional):", title="Add New Client")
        email = dialog_email.get_input()
        
        dialog_phone = customtkinter.CTkInputDialog(text="Enter client's phone (optional):", title="Add New Client")
        phone = dialog_phone.get_input()

        engine = conectar()
        if engine:
            try:
                with engine.connect() as conn:
                    conn.execute(text("""
                        INSERT INTO clientes (nombre, apellidos, email, telefono) 
                        VALUES (:nombre, :apellidos, :email, :telefono)
                    """), {
                        "nombre": first_name, 
                        "apellidos": last_name,
                        "email": email if email else None,
                        "telefono": phone if phone else None
                    })
                    conn.commit()
                    self.load_clients_data()
            except Exception as e:
                print(f"Error adding client: {e}")
            finally:
                engine.dispose()

    def generate_report(self):
        engine = conectar()
        if engine:
            try:
                query = """
                SELECT e.titulo as survey_title, p.texto_pregunta, p.tipo_pregunta, c.nombre, c.apellidos,
                       r.respuesta_texto, r.respuesta_opcion, r.respuesta_escala
                FROM respuestas_encuesta r
                JOIN preguntas_encuesta p ON r.pregunta_id = p.pregunta_id
                JOIN encuestas e ON p.encuesta_id = e.encuesta_id
                JOIN clientes c ON r.cliente_id = c.cliente_id
                """
                df = pd.read_sql(query, engine)

                report = "=============== DETAILED REPORT ===============\n\n"

                # General Stats
                report += "--- General Statistics ---\n"
                report += f"Total Responses: {len(df)}\n"
                report += f"Unique Respondents: {df['nombre'].nunique()}\n"
                report += f"Surveys with Responses: {df['survey_title'].nunique()}\n\n"

                # Numeric Responses (Likert)
                report += "\n--- Likert Scale Responses (Numeric) ---\n"
                numeric_df = df[df['tipo_pregunta'] == 'escala_likert']['respuesta_escala']
                report += numeric_df.describe().to_string()
                report += "\n\n"

                # Categorical Responses (Yes/No, Multiple Choice)
                report += "\n--- Categorical Responses ---\n"
                categorical_df = df[df['tipo_pregunta'].isin(['si_no', 'seleccion_multiple'])]
                if not categorical_df.empty:
                    for question in categorical_df['texto_pregunta'].unique():
                        report += f"\nQuestion: {question}\n"
                        report += categorical_df[categorical_df['texto_pregunta'] == question]['respuesta_opcion'].value_counts().to_string()
                        report += "\n"

                self.reporting_textbox.delete("1.0", tkinter.END)
                self.reporting_textbox.insert(tkinter.END, report)

            except Exception as e:
                print(f"Error generating report: {e}")
            finally:
                engine.dispose()

    def add_question_to_survey(self, survey_id):
        # Dialog to get question text
        dialog_text = customtkinter.CTkInputDialog(text="Enter the question text:", title="Add Question")
        question_text = dialog_text.get_input()
        if not question_text:
            return

        # Dialog to get question type
        question_types = ['abierta', 'seleccion_multiple', 'escala_likert', 'si_no']
        dialog_type = customtkinter.CTkInputDialog(text=f"Enter question type ({', '.join(question_types)}):", title="Add Question")
        question_type = dialog_type.get_input()
        if not question_type or question_type not in question_types:
            print("Invalid question type.")
            return # Or show an error message
        
        engine = conectar()
        if engine:
            try:
                with engine.connect() as conn:
                    # Get the current max order for this survey
                    order_result = conn.execute(text("SELECT MAX(orden) FROM preguntas_encuesta WHERE encuesta_id = :s_id"), {"s_id": survey_id}).scalar()
                    new_order = (order_result or 0) + 1
                    
                    # Insert new question
                    conn.execute(text("""
                        INSERT INTO preguntas_encuesta (encuesta_id, texto_pregunta, tipo_pregunta, orden)
                        VALUES (:s_id, :q_text, :q_type, :order)
                    """), {
                        "s_id": survey_id,
                        "q_text": question_text,
                        "q_type": question_type,
                        "order": new_order
                    })
                    conn.commit()
                    print(f"Question added to survey {survey_id}")
            except Exception as e:
                print(f"Error adding question: {e}")
            finally:
                engine.dispose()

    def view_responses_event(self, survey_id, survey_title):
        responses_window = customtkinter.CTkToplevel(self)
        responses_window.title(f"Responses for: {survey_title}")
        responses_window.geometry("800x600")
        responses_window.transient(self)
        responses_window.grab_set()

        engine = conectar()
        if not engine:
            responses_window.destroy()
            return

        try:
            query = text("""
                SELECT 
                    p.texto_pregunta, 
                    p.tipo_pregunta, 
                    c.nombre, 
                    c.apellidos, 
                    r.respuesta_texto, 
                    r.respuesta_opcion, 
                    r.respuesta_escala,
                    r.fecha_respuesta,
                    c.cliente_id
                FROM respuestas_encuesta r
                JOIN preguntas_encuesta p ON r.pregunta_id = p.pregunta_id
                JOIN clientes c ON r.cliente_id = c.cliente_id
                WHERE p.encuesta_id = :s_id
                ORDER BY c.cliente_id, r.fecha_respuesta, p.orden
            """)
            df = pd.read_sql(query, engine, params={"s_id": survey_id})

            if df.empty:
                customtkinter.CTkLabel(responses_window, text="No responses found for this survey.", font=customtkinter.CTkFont(size=16)).pack(pady=20, padx=20)
                return

            scrollable_frame = customtkinter.CTkScrollableFrame(responses_window)
            scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

            responses_by_client = {}
            for index, row in df.iterrows():
                client_id = row['cliente_id']
                if client_id not in responses_by_client:
                    responses_by_client[client_id] = {
                        'name': f"{row['nombre']} {row['apellidos']}",
                        'responses': []
                    }
                responses_by_client[client_id]['responses'].append(row)

            for client_id, data in responses_by_client.items():
                client_frame = customtkinter.CTkFrame(scrollable_frame, border_width=1)
                client_frame.pack(fill='x', expand=True, padx=10, pady=10)

                client_name_label = customtkinter.CTkLabel(client_frame, text=f"Respondent: {data['name']} (ID: {client_id})", font=customtkinter.CTkFont(weight="bold"))
                client_name_label.pack(anchor="w", padx=10, pady=5)

                for response in data['responses']:
                    response_frame = customtkinter.CTkFrame(client_frame, fg_color="transparent")
                    response_frame.pack(fill='x', expand=True, padx=20, pady=2)

                    q_label = customtkinter.CTkLabel(response_frame, text=f"Q: {response['texto_pregunta']}", wraplength=700, justify="left")
                    q_label.pack(anchor="w")

                    answer = ""
                    if response['tipo_pregunta'] == 'abierta' and response['respuesta_texto']:
                        answer = response['respuesta_texto']
                    elif response['tipo_pregunta'] == 'si_no' and response['respuesta_opcion']:
                        answer = response['respuesta_opcion']
                    elif response['tipo_pregunta'] == 'escala_likert' and pd.notna(response['respuesta_escala']):
                        answer = f"{int(response['respuesta_escala'])} / 5"

                    a_label = customtkinter.CTkLabel(response_frame, text=f"A: {answer}", font=customtkinter.CTkFont(slant="italic"))
                    a_label.pack(anchor="w")

        except Exception as e:
            print(f"Error loading responses: {e}")
            error_label = customtkinter.CTkLabel(responses_window, text=f"Error: {e}")
            error_label.pack(pady=10, padx=10)
        finally:
            engine.dispose()

    def answer_survey_event(self, survey_id):
        answer_window = customtkinter.CTkToplevel(self)
        answer_window.title(f"Answering Survey ID: {survey_id}")
        answer_window.geometry("600x700")
        answer_window.transient(self) # Keep on top of the main window
        answer_window.grab_set() # Make window modal

        engine = conectar()
        if not engine:
            answer_window.destroy()
            return

        try:
            with engine.connect() as conn:
                # Get clients for a dropdown
                clients_result = conn.execute(text("SELECT cliente_id, nombre, apellidos FROM clientes")).fetchall()
                clients = {f"{c[1]} {c[2]} (ID: {c[0]})": c[0] for c in clients_result}
                
                # Get questions
                questions_result = conn.execute(text("SELECT pregunta_id, texto_pregunta, tipo_pregunta FROM preguntas_encuesta WHERE encuesta_id = :s_id ORDER BY orden"), {"s_id": survey_id}).fetchall()

            if not clients:
                customtkinter.CTkLabel(answer_window, text="No clients found. Please add a client first.").pack(pady=20)
                answer_window.after(3000, answer_window.destroy)
                return
            
            # --- Client Selection ---
            client_frame = customtkinter.CTkFrame(answer_window)
            client_frame.pack(fill='x', padx=10, pady=10)
            customtkinter.CTkLabel(client_frame, text="Select Client:").pack(side="left", padx=10)
            client_var = tkinter.StringVar()
            client_menu = customtkinter.CTkOptionMenu(client_frame, variable=client_var, values=[""] + list(clients.keys()))
            client_menu.pack(side="left", padx=10, expand=True, fill='x')
            client_var.set("") # Set default empty value

            # --- Questions Frame ---
            questions_frame = customtkinter.CTkScrollableFrame(answer_window, label_text="Questions")
            questions_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            responses = {} # To hold the widgets for getting answers

            for q_id, q_text, q_type in questions_result:
                q_frame = customtkinter.CTkFrame(questions_frame)
                q_frame.pack(fill='x', pady=5, padx=5)
                customtkinter.CTkLabel(q_frame, text=q_text, wraplength=500, justify="left").pack(anchor="w", padx=10, pady=5)
                
                response_var = None
                if q_type == 'abierta':
                    response_var = customtkinter.CTkEntry(q_frame, width=500)
                    response_var.pack(padx=10, pady=5, anchor="w")
                elif q_type == 'si_no':
                    response_var = tkinter.StringVar()
                    customtkinter.CTkRadioButton(q_frame, text="Yes", variable=response_var, value="Sí").pack(anchor="w", padx=10)
                    customtkinter.CTkRadioButton(q_frame, text="No", variable=response_var, value="No").pack(anchor="w", padx=10)
                elif q_type == 'escala_likert':
                    response_var = tkinter.IntVar(value=0) # Default to 0 to indicate no selection
                    slider_frame = customtkinter.CTkFrame(q_frame, fg_color="transparent")
                    slider_frame.pack(padx=10, pady=5, anchor="w", fill='x', expand=True)
                    customtkinter.CTkLabel(slider_frame, text="1").pack(side="left")
                    customtkinter.CTkSlider(slider_frame, from_=1, to=5, number_of_steps=4, variable=response_var).pack(side="left", fill='x', expand=True, padx=5)
                    customtkinter.CTkLabel(slider_frame, text="5").pack(side="left")

                responses[q_id] = (response_var, q_type)

            def submit_answers():
                client_id = clients.get(client_var.get())
                if not client_id:
                    # You can replace this with a more user-friendly dialog
                    print("ERROR: A client must be selected.")
                    return # Stop execution

                # Re-establish connection for submission
                submit_engine = conectar()
                if not submit_engine:
                    print("ERROR: Could not connect to the database to submit.")
                    return

                try:
                    with submit_engine.connect() as conn:
                        for q_id, (var, q_type) in responses.items():
                            value = var.get()
                            params = {"p_id": q_id, "c_id": client_id, "r_texto": None, "r_opcion": None, "r_escala": None}
                            
                            # Skip if no answer was provided
                            if value in [None, "", 0]:
                                continue

                            if q_type == 'abierta':
                                params["r_texto"] = value
                            elif q_type == 'si_no':
                                params["r_opcion"] = value
                            elif q_type == 'escala_likert':
                                params["r_escala"] = value
                            
                            conn.execute(text("""
                                INSERT INTO respuestas_encuesta (pregunta_id, cliente_id, respuesta_texto, respuesta_opcion, respuesta_escala)
                                VALUES (:p_id, :c_id, :r_texto, :r_opcion, :r_escala)
                            """), params)
                        conn.commit()
                    
                    print("Answers submitted successfully!")
                    self.load_dashboard_data() # Refresh dashboard
                    answer_window.destroy()
                except Exception as e:
                    print(f"Error during submission: {e}")
                finally:
                    submit_engine.dispose()

            submit_button = customtkinter.CTkButton(answer_window, text="Submit Answers", command=submit_answers)
            submit_button.pack(pady=10)

        except Exception as e:
            print(f"Error opening survey answer window: {e}")
        finally:
            if engine:
                engine.dispose()

if __name__ == "__main__":
    app = App()
    app.mainloop()