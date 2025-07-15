# modules/report_generator.py

import pandas as pd
import os
from datetime import datetime

REPORTS_DIR = 'reports'

def create_excel_report(all_data):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    if not all_data:
        return None

    df_all = pd.DataFrame(all_data)
    
    df_all['score'] = pd.to_numeric(df_all['score'], errors='coerce').fillna(0)
    df_high = df_all[df_all['score'] >= 9.0].copy()
    
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    output_path = os.path.join(REPORTS_DIR, filename)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_all.to_excel(writer, sheet_name='전체_취약점', index=False)
        if not df_high.empty:
            df_high.to_excel(writer, sheet_name='고위험_취약점', index=False)
    
    return output_path