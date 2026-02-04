from langgraph.graph import StateGraph, START, END
from src.routing.decision import route_by_pressure
from src.nodes.calculate_pressure import calculate_pressure
from src.nodes.normalise import normalise_inputs
from src.nodes.planning import normal_plan, triage_plan
from src.state.schema import StudentState

def app() -> StateGraph:
    # build the state graph
    graph = StateGraph(StudentState)

    # add nodes to the graph
    graph.add_node("normalise_inputs", normalise_inputs)
    graph.add_node("pressure", calculate_pressure)
    graph.add_node("normal_plan", normal_plan)
    graph.add_node("triage_plan", triage_plan)

    # add edges to the graph
    graph.add_edge(START, "normalise_inputs")
    graph.add_edge("normalise_inputs", "pressure")

    graph.add_conditional_edges(
        "pressure",
        route_by_pressure,
        {
            "triage_plan": "triage_plan",
            "normal_plan": "normal_plan",
        }
    )

    graph.add_edge("normal_plan", END)
    graph.add_edge("triage_plan", END)

    return graph.compile()