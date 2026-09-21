import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.tools import (
    get_airport_metrics,
    calculate_driver_incentive,
    trigger_surge_override
)


# ============================================================
# LOAD GEMINI
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(
    api_key=api_key
)


# ============================================================
# TOOL FUNCTIONS
# ============================================================

AVAILABLE_FUNCTIONS = {
    "get_airport_metrics": get_airport_metrics,
    "calculate_driver_incentive": calculate_driver_incentive,
    "trigger_surge_override": trigger_surge_override
}


# ============================================================
# FUNCTION DECLARATIONS
# ============================================================

get_airport_metrics_declaration = types.FunctionDeclaration(
    name="get_airport_metrics",
    description=(
        "Get the latest operational metrics for an airport. "
        "Use this when the user asks about airport operations, "
        "performance, drivers, ETA, queue, cancellations, "
        "demand, or surge."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "airport_code": types.Schema(
                type=types.Type.STRING,
                description="Airport code such as SFO, LAX, or JFK."
            )
        },
        required=["airport_code"]
    )
)


calculate_driver_incentive_declaration = types.FunctionDeclaration(
    name="calculate_driver_incentive",
    description=(
        "Calculate the recommended driver incentive and "
        "estimated total cost based on driver count and "
        "operational severity."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "driver_count": types.Schema(
                type=types.Type.INTEGER,
                description="Number of drivers receiving the incentive."
            ),
            "severity_level": types.Schema(
                type=types.Type.STRING,
                description="Severity level: low, medium, or high."
            )
        },
        required=[
            "driver_count",
            "severity_level"
        ]
    )
)


trigger_surge_override_declaration = types.FunctionDeclaration(
    name="trigger_surge_override",
    description=(
        "Trigger a mock surge override for an airport. "
        "Use only when the user explicitly requests a "
        "surge multiplier change."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "airport_code": types.Schema(
                type=types.Type.STRING,
                description="Airport code such as SFO, LAX, or JFK."
            ),
            "new_multiplier": types.Schema(
                type=types.Type.NUMBER,
                description="New surge multiplier between 1.0 and 1.5."
            ),
            "reason": types.Schema(
                type=types.Type.STRING,
                description="Reason for the surge override."
            )
        },
        required=[
            "airport_code",
            "new_multiplier",
            "reason"
        ]
    )
)


# ============================================================
# GEMINI TOOL CONFIGURATION
# ============================================================

tools = types.Tool(
    function_declarations=[
        get_airport_metrics_declaration,
        calculate_driver_incentive_declaration,
        trigger_surge_override_declaration
    ]
)


# ============================================================
# FUNCTION CALLING
# ============================================================

def ask_operations(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[tools],
            system_instruction=(
                "You are an Airport Operations AI Copilot. "
                "Use operational tools whenever the user "
                "asks for current airport operational data. "
                "Never invent operational metrics."
            )
        )
    )

    # --------------------------------------------------------
    # Check whether Gemini requested a function
    # --------------------------------------------------------

    function_calls = response.function_calls

    if function_calls:

        results = []

        for call in function_calls:

            function_name = call.name
            arguments = call.args

            print(
                f"\nTOOL CALLED: {function_name}"
            )

            print(
                f"TOOL INPUT: {arguments}"
            )

            if function_name not in AVAILABLE_FUNCTIONS:

                return {
                    "status": "error",
                    "message": (
                        f"Unknown function: {function_name}"
                    )
                }

            function_to_call = AVAILABLE_FUNCTIONS[
                function_name
            ]

            try:

                tool_result = function_to_call(
                    **arguments
                )

            except Exception as e:

                tool_result = {
                    "status": "error",
                    "message": str(e)
                }

            print(
                f"TOOL OUTPUT: {tool_result}"
            )

            results.append(
                types.Part.from_function_response(
                    name=function_name,
                    response=tool_result
                )
            )

        # ----------------------------------------------------
        # Send tool results back to Gemini
        # ----------------------------------------------------

        final_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                question,
                response.candidates[0].content,
                types.Content(
                    role="user",
                    parts=results
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=(
                    "Answer the user's question using "
                    "the tool results. "
                    "Do not invent operational data."
                )
            )
        )

        return {
            "status": "success",
            "tool_used": True,
            "answer": final_response.text
        }

    # --------------------------------------------------------
    # No tool required
    # --------------------------------------------------------

    return {
        "status": "success",
        "tool_used": False,
        "answer": response.text
    }