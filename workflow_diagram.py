"""
Generates a detailed workflow diagram for the data manipulation application.
The diagram is saved as a PNG file when this script is executed.
"""
from pathlib import Path
from datetime import datetime

try:
    from graphviz import Digraph
    from graphviz.backend import ExecutableNotFound
except ImportError:
    print("Warning: graphviz is not installed. Workflow diagram will not be generated.")
    Digraph = None
    ExecutableNotFound = None

def create_workflow_diagram(output_directory: Path | None = None) -> Path:
    """
    Create the workflow diagram and save it as a PNG image.

    Args:
        output_directory: Optional directory where the diagram should be saved.
                          Defaults to a 'diagrams' folder inside the project root.

    Returns:
        Path to the generated PNG file.
    """
    project_root = Path(__file__).resolve().parent
    if output_directory is None:
        output_directory = project_root / "diagrams"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_path = output_directory / "data_manipulation_workflow"

    dot = Digraph(
        name="DataManipulationWorkflow",
        comment="Workflow for the Data Manipulation Tool",
        format="png",
    )
    dot.attr(rankdir="LR", splines="true", nodesep="0.7", ranksep="1")
    dot.attr("graph", fontname="Segoe UI", fontsize="12", labelloc="t")
    dot.attr("node", style="filled,rounded", shape="rectangle",
             fillcolor="#F7FAFC", color="#1F4E79", fontname="Segoe UI",
             fontsize="11", fontcolor="#1F2933")
    dot.attr("edge", color="#1F4E79", arrowsize="0.8", fontname="Segoe UI", fontsize="10")

    # Start & setup phase
    dot.node("start", "Start", shape="ellipse", fillcolor="#E3F2FD")
    dot.node("config", "Load configuration\n＆ environment", shape="rectangle")
    dot.node("setup", "Setup application paths\n(result directories, datasets)", shape="rectangle")

    # Main entry
    dot.node("menu", "Display CLI menu\n(interactive or tests)", shape="rectangle", fillcolor="#E6FFFA")

    # Interactive workflow
    dot.node("interactive", "Interactive mode\n(user-provided queries)", fillcolor="#FFF4E5")
    dot.node("metadata", "Automatic metadata injection\n(df.info + statistics)", fillcolor="#FFF4E5")
    dot.node("agent", "Execute agent (smolagents)\nLiteLLM model + tools", fillcolor="#FFF4E5")

    # Tool selection nodes
    dot.node("tool_dispatch", "Tool dispatcher\n(select best operation)", fillcolor="#FFF4E5")

    with dot.subgraph(name="cluster_tools") as tools_cluster:
        tools_cluster.attr(label="Tool Library", color="#CBD5F5", fontname="Segoe UI", fontsize="12")
        tools_cluster.attr("node", style="filled", shape="rectangle", fillcolor="#F0F5FF")
        tools_cluster.node("basic_tools", "Basic tools\n(select/merge/filter/joins)")
        tools_cluster.node("advanced_scalers", "Advanced scalers\n(Standard/MinMax/Robust)")
        tools_cluster.node("advanced_encoders", "Encoding suite\n(one-hot, label, ordinal,\nfrequency, target, binary)")
        tools_cluster.node("feature_engineering", "Feature engineering\n(polynomial, outliers,\nimputation)")
        tools_cluster.node("file_ops", "File operations\n(combine, join, save)")

        tools_cluster.edges([
            ("tool_dispatch", "basic_tools"),
            ("tool_dispatch", "advanced_scalers"),
            ("tool_dispatch", "advanced_encoders"),
            ("tool_dispatch", "feature_engineering"),
            ("tool_dispatch", "file_ops"),
        ])

    dot.node("save_outputs", "Persist results\n(CSV / Excel in results/)", fillcolor="#F1FCE1")
    dot.node("return_menu", "Return to main menu\n(or exit)", fillcolor="#E6FFFA")

    # Automated testing workflow
    dot.node("run_tests", "Automated test runner", shape="rectangle", fillcolor="#FFF0F6")
    dot.node("student_setup", "Generate student datasets\n(student/ folder)", fillcolor="#FFF0F6")
    dot.node("titanic_setup", "Prepare titanic datasets\n(titanic/ folder)", fillcolor="#FFF0F6")
    dot.node("student_tests", "Run student test suite\n(9 scenarios)", fillcolor="#FFF0F6")
    dot.node("titanic_tests", "Run titanic test suite\n(13 scenarios)", fillcolor="#FFF0F6")
    dot.node("summaries", "Aggregate results & summaries\n(results/student/, results/titanic/)", fillcolor="#F1FCE1")

    dot.node("end", "End", shape="ellipse", fillcolor="#E3F2FD")

    # Connections
    dot.edges([
        ("start", "config"),
        ("config", "setup"),
        ("setup", "menu"),
        ("menu", "interactive"),
        ("interactive", "metadata"),
        ("metadata", "agent"),
        ("agent", "tool_dispatch"),
        ("tool_dispatch", "save_outputs"),
        ("save_outputs", "return_menu"),
        ("return_menu", "menu"),
        ("menu", "run_tests"),
        ("run_tests", "student_setup"),
        ("run_tests", "titanic_setup"),
        ("student_setup", "student_tests"),
        ("titanic_setup", "titanic_tests"),
        ("student_tests", "summaries"),
        ("titanic_tests", "summaries"),
        ("summaries", "return_menu"),
        ("menu", "end"),
    ])

    dot.attr(label=f"Data Manipulation Workflow\nGenerated: {datetime.now():%Y-%m-%d %H:%M:%S}")
    try:
        dot.render(filename=str(output_path), cleanup=True)
    except ExecutableNotFound as exc:  # pragma: no cover - depends on user environment
        raise SystemExit(
            "Graphviz executables (dot) were not found on your PATH.\n"
            "Install Graphviz from https://graphviz.org/download/ and ensure "
            "the installation directory (e.g., C:\\Program Files\\Graphviz\\bin) "
            "is added to your PATH environment variable."
        ) from exc

    return output_path.with_suffix(".png")


if __name__ == "__main__":
    output_file = create_workflow_diagram()
    print(f"Workflow diagram generated: {output_file}")

