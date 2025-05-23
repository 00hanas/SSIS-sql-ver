def searchTable(table_widget, search_input, search_by_combobox):
    
    search_text = search_input.text().strip().lower()
    column_index = search_by_combobox.currentIndex() - 1  
    row_count = table_widget.rowCount()
    match_found = False  

    # Restore original table if search is cleared
    if not search_text:
        for row in range(row_count):
            table_widget.setRowHidden(row, False)
        return  

    # Loop through each row
    for row in range(row_count):
        row_match = False

        for col in range(table_widget.columnCount()):
            if column_index == -1 or col == column_index:  # Search all if "Search By" is selected
                item = table_widget.item(row, col)
                if item and search_text in item.text().strip().lower():
                    row_match = True
                    match_found = True
                    break  # Stop checking other columns if a match is found

        table_widget.setRowHidden(row, not row_match)

    # Handle "No result found" case
    if not match_found:
        for row in range(row_count):
            table_widget.setRowHidden(row, True)
