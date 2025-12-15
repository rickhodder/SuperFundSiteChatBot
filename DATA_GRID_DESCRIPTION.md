# Data Grid Description Feature

## Overview
Added context-aware descriptive text above the data grid to show what data is being displayed based on the user's query.

## Implementation

### Session State
Added new session state variable:
```python
st.session_state.data_description  # Stores description of current data display
```

### Handler Updates
Updated all command handlers to set appropriate descriptions:

1. **Show All Policies**: `"Showing all {count} policies in the database"`
2. **Policies by State**: `"Showing {count} policies in {state}"`
3. **High-Risk Policies**: `"Showing {count} high-risk policies"`
4. **High-Value Policies**: `"Showing {count} high-value policies (>$1M)"`
5. **Policies by Coverage**: `"Showing {count} {coverage_type} policies"`
6. **Batch Score All**: `"Showing safety scores for all {count} policies"`
7. **Show Policy**: `"Showing policy {policy_number}"`
8. **Address Query**: `"Showing {count} SuperFund sites within {radius} miles of {address}"`
9. **Show All Sites**: `"Showing all {count} SuperFund sites in the database"`

### Display Logic
The description is rendered in `render_data_section()` between the section header and the data grid:

```python
# Display data description if available
if st.session_state.data_description and not section_manager.is_collapsed("data_grid") and not section_manager.is_hidden("data_grid"):
    st.markdown(f"*{st.session_state.data_description}*")
```

## Benefits
- **Context Clarity**: Users immediately understand what data they're viewing
- **Demo Friendly**: Makes demonstrations clearer by explaining query results
- **User Experience**: Reduces confusion when switching between different views
- **Professional Polish**: Adds informative labels that enhance the UI

## Example Usage

When a user asks "show policies in NY", the data grid will display:
```
📊 Data Grid
Showing 3 policies in NY
[Data table follows...]
```

When scoring an address, the grid shows:
```
📊 Data Grid
Showing 5 SuperFund sites within 50 miles of 123 Main St, New York, NY 10001
[Data table follows...]
```

## Testing
To test this feature:
1. Run the app: `streamlit run app.py`
2. Try various commands:
   - "show all policies"
   - "show policies in NY"
   - "show high risk policies"
   - "849 First Street, Portland, ME 04101"
3. Verify the description appears above the data grid for each command
4. Confirm the description accurately reflects the data being shown
