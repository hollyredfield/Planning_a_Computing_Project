# Proyecto: Sistema de Gestión de Feedback - DataInsight Corp.

¡Buenas! Este es el README de mi proyecto. Me he currado una aplicación de escritorio completa desde cero en Python, y la verdad es que estoy bastante orgulloso de cómo ha quedado. La idea era crear una herramienta de gestión y análisis de encuestas para una empresa ficticia llamada "DataInsight Corp.". El objetivo principal es que la empresa pueda recoger las opiniones de sus clientes de una forma ordenada, analizar los datos visualmente y, con esa información, tomar mejores decisiones.

He diseñado y programado toda la interfaz gráfica para que sea intuitiva y fácil de usar, con un estilo moderno y oscuro. No es solo una herramienta que funciona, sino que también he intentado que sea agradable a la vista.

---

## ¿Qué hace la aplicación? Mis funcionalidades principales

He dividido la aplicación en varios módulos para que todo esté bien organizado. A continuación, te cuento en detalle qué hace cada parte.

### 1. Dashboard Principal: Un Vistazo Rápido a los Datos

Esta es la pantalla de bienvenida y el centro neurálgico del análisis. En cuanto arrancas la aplicación, te encuentras con un panel de control que te muestra un resumen visual de todas las respuestas de las encuestas. Para que sea más fácil de digerir, lo he organizado en tres pestañas:

*   **Gráficos de Escala Likert:** Para las típicas preguntas de "valora del 1 al 5", he programado unos gráficos de barras horizontales que se generan solos. Es una pasada porque, de un solo vistazo, puedes ver las tendencias, si la gente está mayormente de acuerdo o en desacuerdo con algo.
*   **Gráficos de Sí/No:** Para las preguntas de respuesta rápida y directa, he usado gráficos de tarta. Son perfectos para ver los porcentajes de forma clara y rotunda. Te dicen al instante cuánta gente ha dicho que sí y cuánta que no.
*   **Respuestas Abiertas:** Esta es la parte cualitativa. Los números están muy bien, pero a veces necesitas entender el porqué de las cosas. En esta pestaña, he puesto un cuadro de texto donde se listan todas las respuestas de texto libre, cada una con su pregunta correspondiente. Es genial para leer las opiniones, sugerencias y críticas directamente de los clientes.

### 2. Gestión de Encuestas: El Centro de Control

Aquí es donde se cuece todo. Es la sección para administrar las encuestas y las preguntas. Desde aquí puedo:

*   **Crear encuestas nuevas:** Con un simple botón, se abre una ventana para crear una encuesta desde cero, pidiéndote un título y una descripción.
*   **Añadir preguntas de todo tipo:** A cada encuesta que creo, le puedo añadir las preguntas que necesite. He implementado un sistema para elegir el tipo de pregunta: abierta (texto), sí/no (botones de radio) o escala Likert (una barra deslizante).
*   **Responder las encuestas:** He creado una ventana específica para rellenar las encuestas. Primero eliges a qué cliente se le está haciendo la encuesta y luego vas respondiendo. Los controles son interactivos y cambian según el tipo de pregunta, lo que hace que el proceso sea muy cómodo.
*   **Ver todas las respuestas:** Hay un botón para cada encuesta que te permite cotillear todas las respuestas que se han recogido hasta el momento. Se muestran organizadas por la persona que respondió, para que puedas ver todo lo que dijo un cliente en particular.

### 3. Gestión de Clientes: ¿Quién es Quién?

Para que los datos tengan contexto, es fundamental saber quién los ha proporcionado. En esta sección, puedo dar de alta a los clientes o participantes de las encuestas. Se puede guardar su nombre, apellidos, email y teléfono. En lugar de una lista aburrida, he diseñado unas tarjetas para cada cliente que le dan un toque más visual y moderno.

### 4. Informes (Reporting): El Resumen Final

Por último, he añadido una funcionalidad de reporting. Con un solo clic, la aplicación analiza todos los datos de las encuestas y genera un informe de texto muy completo. Este informe incluye:
*   Estadísticas generales (cuánta gente ha respondido, cuántas encuestas tienen respuestas, etc.).
*   Un análisis descriptivo de las respuestas numéricas (media, mediana, desviación estándar...).
*   Un recuento de las respuestas de sí/no.

Es perfecto para tener un resumen rápido y compartir los hallazgos.

---

## ¿Qué tecnologías he usado para montar todo esto?

Para desarrollar este proyecto, he tirado de varias librerías y tecnologías bastante potentes de Python:

*   **Python:** El cerebro de toda la operación.
*   **CustomTkinter:** Para toda la interfaz gráfica. Elegí esta librería porque permite crear interfaces con un aspecto mucho más moderno y profesional que el Tkinter clásico. Es la responsable del tema oscuro y los widgets redondeados.
*   **Matplotlib:** La he usado para crear todos los gráficos del dashboard. Es una librería increíblemente potente para la visualización de datos y la he integrado directamente en la interfaz de CustomTkinter.
*   **Pandas:** Es mi navaja suiza para manejar los datos. Cuando saco la información de la base de datos, uso Pandas para limpiarla, agruparla y prepararla antes de pasarla a Matplotlib para pintarla en los gráficos.
*   **SQLAlchemy:** Para hablar con la base de datos de una forma segura y ordenada. Me ayuda a construir las consultas SQL y a evitar problemas de seguridad.
*   **MySQL:** Como sistema de gestión de base de datos. He montado una base de datos local en mi ordenador para guardar toda la información: los clientes, las encuestas, las preguntas y, por supuesto, todas las respuestas.

