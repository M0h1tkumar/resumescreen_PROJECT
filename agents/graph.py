from langgraph.graph import StateGraph
from agents.state import ScreeningState
from agents.nodes import parser_node, scoring_node, ranking_node, interview_question_node

def create_screening_graph():
    # Initialize the graph
    workflow = StateGraph(ScreeningState)
    
    # Add nodes
    workflow.add_node("parser", parser_node)
    workflow.add_node("scorer", scoring_node)
    workflow.add_node("ranker", ranking_node)
    workflow.add_node("interviewer", interview_question_node)
    
    # Define execution flow
    # The flow is deterministic as per requirements: Parser -> Scorer -> Ranker -> Interviewer
    workflow.add_edge("__start__", "parser")
    workflow.add_edge("parser", "scorer")
    workflow.add_edge("scorer", "ranker")
    workflow.add_edge("ranker", "interviewer")
    workflow.add_edge("interviewer", "__end__")
    
    # Compile the graph
    app = workflow.compile()
    return app

# Initialize global graph instance
screening_app = create_screening_graph()
