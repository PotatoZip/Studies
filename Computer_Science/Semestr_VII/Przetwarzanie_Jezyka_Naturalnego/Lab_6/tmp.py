import requests
from graphql import (
    parse,
    build_client_schema,
    get_named_type,
)

# --- Configuration ---
# Monday.com's schema endpoint is public
MONDAY_SCHEMA_URL = 'https://api.monday.com/v2/get_schema'
DEBUG = True

def fetch_monday_schema():
    """Fetches the remote schema from Monday.com without Auth"""
    print(f"Fetching Monday.com Schema from {MONDAY_SCHEMA_URL}...")
    try:
        # No headers needed for the public schema endpoint
        response = requests.get(MONDAY_SCHEMA_URL)
        response.raise_for_status()
        result = response.json()

        if 'data' not in result:
            raise Exception("No data returned from schema endpoint.")

        return build_client_schema(result['data'])
    except Exception as e:
        print(f"Error fetching schema: {e}")
        return None

def get_argument_value(field_node, arg_name, variables):
    """Helper to extract integer values from arguments"""
    if not field_node.arguments:
        return None

    for arg in field_node.arguments:
        if arg.name.value == arg_name:
            val = arg.value
            # Check node kind by string instead of importing 'Kind' enum
            # 'int_value' or 'IntValue' depending on version, so we check value attribute
            if hasattr(val, 'value'):
                try:
                    return int(val.value)
                except:
                    pass

            # Handle variables if passed
            if val.kind == 'variable' and variables:
                var_name = val.name.value
                return variables.get(var_name)

    return None

def calculate_complexity(schema, query_ast, variables=None):
    if variables is None:
        variables = {}

    if DEBUG: print("\n--- Starting Traversal ---")

    def estimate_cost(node, parent_type, depth=0):
        indent = "  " * depth
        field_name = node.name.value

        # 1. Resolve Field Definition
        if not hasattr(parent_type, 'fields'):
            return 0

        field_def = parent_type.fields.get(field_name)
        if not field_def:
            return 0

        # 2. Base Cost Logic
        cost = 1
        if field_name in ['boards', 'items', 'items_page']:
            cost = 10

        # Check if parent is mutation
        if parent_type.name == 'Mutation' and field_name in ['create_item', 'change_column_value']:
            cost = 30000

        # 3. Handle Limits
        limit = get_argument_value(node, 'limit', variables) or get_argument_value(node, 'first', variables) or 1

        # 4. Child Complexity
        child_complexity = 0

        if node.selection_set:
            # Unwrap types (e.g., [Board]! -> Board)
            current_field_type = get_named_type(field_def.type)

            for selection in node.selection_set.selections:
                # Check for 'field' kind using string comparison (case-insensitive)
                # formatting can vary by version ('Field', 'field')
                sel_kind = str(selection.kind).lower()

                if 'field' in sel_kind:
                    child_complexity += estimate_cost(selection, current_field_type, depth + 1)

        total_node_cost = cost
        if child_complexity > 0:
            total_node_cost = (child_complexity * limit) + cost

        if DEBUG:
            print(f"{indent}-> Field: {field_name} | Base: {cost} | Limit: {limit} | Children: {child_complexity} | Total: {total_node_cost}")

        return total_node_cost

    total_complexity = 0
    query_type = schema.query_type
    mutation_type = schema.mutation_type

    for definition in query_ast.definitions:
        # Check operation type using string comparison to avoid importing OperationType
        # definition.operation is usually an Enum, .value gives 'query'/'mutation'
        op_type = str(getattr(definition, 'operation', '')).lower()

        # Handle "OperationType.QUERY" (enum) or just "query" (string)
        if 'query' in op_type:
            for selection in definition.selection_set.selections:
                total_complexity += estimate_cost(selection, query_type)

        elif 'mutation' in op_type:
             for selection in definition.selection_set.selections:
                total_complexity += estimate_cost(selection, mutation_type)

    return total_complexity

# --- Main Execution ---

if __name__ == "__main__":
    # 1. Get Schema (No Token Needed)
    schema = fetch_monday_schema()

    if schema:
        # 2. Define Query
        query = """
          query {
            boards (limit: 5) {
              id
              name
              items_page (limit: 10) {
                items {
                  id
                  name
                  column_values {
                    text
                  }
                }
              }
            }
          }
        """

        # 3. Calculate
        print("Parsing query...")
        document = parse(query)

        complexity = calculate_complexity(schema, document)

        print("-" * 50)
        print(f"FINAL ESTIMATED COMPLEXITY: {complexity}")
        print("-" * 50)
