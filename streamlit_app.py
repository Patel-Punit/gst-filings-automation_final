import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Define necessary data structures
known_sources = ['Zoho Books B2B,Export Sales Data', 'Kithab Sales Report', 'Amazon', 'Flipkart - 7(A)(2)', 'Flipkart - 7(B)(2)', 'Meesho']

known_source_relevenat_columns = {
      'Zoho Books B2B,Export Sales Data': {
          'GST Identification Number (GSTIN)' : 'GSTIN/UIN of Recipient',
          'Customer Name' : 'Receiver Name',
          'Supplier GST Registration Number' : 'GSTIN/UIN of Supplier',
          'Invoice Number' : 'Invoice Number',
          'Invoice Date' : 'Invoice Date',
          'Total' : 'Invoice Value',
          'Place of Supply(With State Code)' : 'Place Of Supply',
          'Item Tax %' : 'Rate',
          'SubTotal' : 'Taxable Value',
          'Item Tax Amount' : 'Tax amount',
          'GST Treatment' : 'GST treatment'
      },
      'Kithab Sales Report': {
          'GSTIN Number' : 'GSTIN/UIN of Recipient',
          'Customer name' : 'Receiver Name',
          'Invoice Number' : 'Invoice Number',
          'Invoice Date' : 'Invoice Date',
          'GST Rate' : 'Rate',
          'Item Price' : 'Taxable Value'
      },
      'Amazon': {
          'Seller Gstin' : 'GSTIN/UIN of Supplier',
          'Invoice Number' : 'Invoice Number',
          'Invoice Date' : 'Invoice Date',
          'Invoice Amount' : 'Invoice Value',
          'Ship To State' : 'Place Of Supply',
          'Tax Exclusive Gross' : 'Taxable Value',
          'Total Tax Amount' : 'Tax amount',
          'Cgst Rate' : 'Cgst Rate',
          'Sgst Rate' : 'Sgst Rate',
          'Utgst Rate' : 'Utgst Rate',
          'Igst Rate' : 'Igst Rate'
      },
      'Meesho': {
          'gstin' : 'GSTIN/UIN of Supplier',
          'end_customer_state_new' : 'Place Of Supply',
          'gst_rate' : 'Rate',
          'tcs_taxable_amount' : 'Taxable Value'
      },
      'Flipkart - 7(A)(2)': {
          'GSTIN' : 'GSTIN/UIN of Supplier',
          'Aggregate Taxable Value Rs.' : 'Taxable Value',
          'CGST %' : 'Cgst Rate',
          'SGST/UT %' : 'Sgst Rate'
      },
      'Flipkart - 7(B)(2)':{
          'GSTIN' : 'GSTIN/UIN of Supplier',
          'Delivered State (PoS)' : 'Place Of Supply',
          'IGST %' : 'Rate',
          'Aggregate Taxable Value Rs.' : 'Taxable Value',
          'IGST Amount Rs.' : 'Tax amount'
      }
  }

state_codes = [
    {
        "State": "Andaman and Nicobar Islands",
        "code": "35-Andaman and Nicobar Islands",
        "code_number": "35"
    },
    {
        "State": "Andhra Pradesh",
        "code": "37-Andhra Pradesh",
        "code_number": "37"
    },
    {
        "State": "Arunachal Pradesh",
        "code": "12-Arunachal Pradesh",
        "code_number": "12"
    },
    {
        "State": "Assam",
        "code": "18-Assam",
        "code_number": "18"
    },
    {
        "State": "Bihar",
        "code": "10-Bihar",
        "code_number": "10"
    },
    {
        "State": "Chandigarh",
        "code": "04-Chandigarh",
        "code_number": "04"
    },
    {
        "State": "Chhattisgarh",
        "code": "22-Chhattisgarh",
        "code_number": "22"
    },
    {
        "State": "Dadra and Nagar Haveli and Daman and Diu",
        "code": "26-Dadra and Nagar Haveli and Daman and Diu",
        "code_number": "26"
    },
    {
        "State": "Daman and Diu",
        "code": "25-Daman and Diu",
        "code_number": "25"
    },
    {
        "State": "Delhi",
        "code": "07-Delhi",
        "code_number": "07"
    },
    {
        "State": "Goa",
        "code": "30-Goa",
        "code_number": "30"
    },
    {
        "State": "Gujarat",
        "code": "24-Gujarat",
        "code_number": "24"
    },
    {
        "State": "Haryana",
        "code": "06-Haryana",
        "code_number": "06"
    },
    {
        "State": "Himachal Pradesh",
        "code": "02-Himachal Pradesh",
        "code_number": "02"
    },
    {
        "State": "Jammu and Kashmir",
        "code": "01-Jammu and Kashmir",
        "code_number": "01"
    },
    {
        "State": "Jharkhand",
        "code": "20-Jharkhand",
        "code_number": "20"
    },
    {
        "State": "Karnataka",
        "code": "29-Karnataka",
        "code_number": "29"
    },
    {
        "State": "Kerala",
        "code": "32-Kerala",
        "code_number": "32"
    },
    {
        "State": "Ladakh",
        "code": "38-Ladakh",
        "code_number": "38"
    },
    {
        "State": "Lakshadweep",
        "code": "31-Lakshadweep",
        "code_number": "31"
    },
    {
        "State": "Madhya Pradesh",
        "code": "23-Madhya Pradesh",
        "code_number": "23"
    },
    {
        "State": "Maharashtra",
        "code": "27-Maharashtra",
        "code_number": "27"
    },
    {
        "State": "Manipur",
        "code": "14-Manipur",
        "code_number": "14"
    },
    {
        "State": "Meghalaya",
        "code": "17-Meghalaya",
        "code_number": "17"
    },
    {
        "State": "Mizoram",
        "code": "15-Mizoram",
        "code_number": "15"
    },
    {
        "State": "Nagaland",
        "code": "13-Nagaland",
        "code_number": "13"
    },
    {
        "State": "Odisha",
        "code": "21-Odisha",
        "code_number": "21"
    },
    {
        "State": "Other Territory",
        "code": "97-Other Territory",
        "code_number": "97"
    },
    {
        "State": "Puducherry",
        "code": "34-Puducherry",
        "code_number": "34"
    },
    {
        "State": "Punjab",
        "code": "03-Punjab",
        "code_number": "03"
    },
    {
        "State": "Rajasthan",
        "code": "08-Rajasthan",
        "code_number": "08"
    },
    {
        "State": "Sikkim",
        "code": "11-Sikkim",
        "code_number": "11"
    },
    {
        "State": "Tamil Nadu",
        "code": "33-Tamil Nadu",
        "code_number": "33"
    },
    {
        "State": "Telangana",
        "code": "36-Telangana",
        "code_number": "36"
    },
    {
        "State": "Tripura",
        "code": "16-Tripura",
        "code_number": "16"
    },
    {
        "State": "Uttar Pradesh",
        "code": "09-Uttar Pradesh",
        "code_number": "09"
    },
    {
        "State": "Uttarakhand",
        "code": "05-Uttarakhand",
        "code_number": "05"
    },
    {
        "State": "West Bengal",
        "code": "19-West Bengal",
        "code_number": "19"
    }
]

needed_columns = [
    'GSTIN/UIN of Recipient', 'Receiver Name', 'GSTIN/UIN of Supplier', 'Invoice Number', 'Invoice Date',
    'Invoice Value', 'Place Of Supply', 'Rate', 'Taxable Value', 'Tax amount', 'GST treatment', 'Invoice Type',
    'E-Commerce GSTIN', 'Cess Amount', 'Cgst Rate', 'Sgst Rate', 'Utgst Rate', 'Igst Rate', 'CESS Rate'
]

# Define necessary functions
def select_columns_from_unknown_source(df, needed_columns):
    columns = df.columns.tolist()
    available_columns_dict = {i+1: col for i, col in enumerate(columns)}
    available_name_of_needed_columns_dict = {}
    
    st.write("Available columns:")
    for num, col in available_columns_dict.items():
        st.write(f"{num}: {col}")
    
    for col in needed_columns:
        available_column_number = st.number_input(f"Enter number for {col} (0 if not found)", min_value=0, max_value=len(columns), step=1)
        if available_column_number > 0 and available_column_number <= len(available_columns_dict):
            available_name_of_needed_columns_dict[available_columns_dict[available_column_number]] = col
    
    if available_name_of_needed_columns_dict:
        df = df[list(available_name_of_needed_columns_dict.keys())]
        df = df.rename(columns=available_name_of_needed_columns_dict)
    else:
        df = pd.DataFrame()  # Create an empty DataFrame if no columns were selected
    
    for col in needed_columns:
        if col not in df.columns:
            df[col] = np.nan
    
    return df

def select_columns_from_known_source(df, needed_columns, source):
    available_name_of_needed_columns_dict = known_source_relevenat_columns[source]
    columns_to_keep = list(available_name_of_needed_columns_dict.keys())
    df = df[columns_to_keep]
    df = df.rename(columns=available_name_of_needed_columns_dict)

    for col in needed_columns:
        if col not in df.columns:
            df[col] = np.nan

    return df

def format_place_of_supply(df):
    for index, row in df.iterrows():
        place_of_supply = row['Place Of Supply']
        valid_states = [state['State'] for state in state_codes]
        valid_codes = [state['code_number'] for state in state_codes]
        valid_state_codes = [state['code'] for state in state_codes]

        gstin_value = row['GSTIN/UIN of Recipient']
        gstin_state_code = gstin_value[:2] if isinstance(gstin_value, str) and len(gstin_value)>=2 else None

        if gstin_state_code in valid_codes:
            for state in state_codes:
                if state['code_number'] == gstin_state_code:
                    df.at[index, 'Place Of Supply'] = state['code']
                    break
        elif place_of_supply not in valid_state_codes:
            if isinstance(place_of_supply, str) and place_of_supply.lower() in [state.lower() for state in valid_states]:
                for state in state_codes:
                    if state['State'].lower() == place_of_supply.lower():
                        df.at[index, 'Place Of Supply'] = state['code']
                        break
            elif place_of_supply in valid_codes:
                for state in state_codes:
                    if state['code_number'] == place_of_supply:
                        df.at[index, 'Place Of Supply'] = state['code']
                        break

    return df

def fill_missing_values(df):
    for index, row in df.iterrows():
        invoice_value = row['Invoice Value'] if pd.notna(row['Invoice Value']) else 0
        taxable_value = row['Taxable Value'] if pd.notna(row['Taxable Value']) else 0
        tax_amount = row['Tax amount'] if pd.notna(row['Tax amount']) else 0
        gst_rate = row['Rate'] if pd.notna(row['Rate']) else 0
        cgst_rate = row['Cgst Rate'] if pd.notna(row['Cgst Rate']) else 0
        sgst_rate = row['Sgst Rate'] if pd.notna(row['Sgst Rate']) else 0
        igst_rate = row['Igst Rate'] if pd.notna(row['Igst Rate']) else 0
        utgst_rate = row['Utgst Rate'] if pd.notna(row['Utgst Rate']) else 0
        gst_rate_combined = cgst_rate + sgst_rate + igst_rate + utgst_rate

        if gst_rate == 0 and gst_rate_combined != 0:
            gst_rate = gst_rate_combined
            df.at[index, 'Rate'] = gst_rate

        # ... (include other conditions for filling missing values)

    return df

def create_place_of_origin_column(df, customer_state):
    df['place_of_origin'] = np.nan

    for index, row in df.iterrows():
        supplier_gstin = row['GSTIN/UIN of Supplier']

        if pd.notna(supplier_gstin) and isinstance(supplier_gstin, str):
            if len(supplier_gstin) >= 2:
                supplier_state_code = supplier_gstin[:2]
                for state in state_codes:
                    if state['code_number'] == supplier_state_code:
                        df.at[index, 'place_of_origin'] = state['code']
                        break

        if pd.isna(df.at[index, 'place_of_origin']):
            df.at[index, 'place_of_origin'] = customer_state

    return df

def fill_place_of_supply_with_place_of_origin(df):
    for index, row in df.iterrows():
        if pd.isna(row['Place Of Supply']):
            df.at[index, 'Place Of Supply'] = row['place_of_origin']
    return df

def categorise_transactions(df):
    df['transaction_type'] = np.nan

    for index, row in df.iterrows():
        gstin_of_recipient = row['GSTIN/UIN of Recipient']
        place_of_supply = row['Place Of Supply']
        invoice_value = row['Invoice Value']
        place_of_origin = row['place_of_origin']
        gst_treatment = row['GST treatment']

        if gst_treatment != 'overseas':
            if pd.notna(gstin_of_recipient):
                df.at[index, 'transaction_type'] = 'b2b'
            elif place_of_supply != place_of_origin and invoice_value > 250000:
                df.at[index, 'transaction_type'] = 'b2cl'
            else:
                df.at[index, 'transaction_type'] = 'b2cs'

    return df

def create_b2b_dataframe(df):
    b2b = df[df['transaction_type'] == 'b2b']
    b2b_columns_needed = ['GSTIN/UIN of Recipient', 'Receiver Name', 'Invoice Number', 'Invoice Date',
                          'Invoice Value', 'Place Of Supply', 'Reverse Charge', 'Applicable % of Tax Rate',
                          'Invoice Type', 'E-Commerce GSTIN', 'Rate', 'Taxable Value', 'Cess Amount']
    
    for col in b2b_columns_needed:
        if col not in b2b.columns:
            b2b[col] = np.nan
    
    return b2b[b2b_columns_needed]

def create_b2cs_dataframe(df):
    b2cs = df[df['transaction_type'] == 'b2cs']
    b2cs['Type'] = 'b2cs'
    b2cs['Applicable % of Tax Rate'] = np.nan
    b2cs['E-Commerce GSTIN'] = np.nan
    
    b2cs = b2cs.groupby(['Place Of Supply', 'Rate'])[['Taxable Value', 'Cess Amount']].sum().reset_index()
    
    b2cs_columns_needed = ['Type', 'Place Of Supply', 'Applicable % of Tax Rate', 'Rate', 'Taxable Value', 'Cess Amount', 'E-Commerce GSTIN']
    for col in b2cs_columns_needed:
        if col not in b2cs.columns:
            b2cs[col] = np.nan
    
    return b2cs[b2cs_columns_needed]

def create_b2cl_dataframe(df):
    b2cl = df[df['transaction_type'] == 'b2cl']
    b2cl_columns_needed = ['Invoice Number', 'Invoice Date', 'Invoice Value', 'Place Of Supply',
                           'Applicable % of Tax Rate', 'Rate', 'Taxable Value', 'Cess Amount', 'E-Commerce GSTIN']
    
    for col in b2cl_columns_needed:
        if col not in b2cl.columns:
            b2cl[col] = np.nan
    
    return b2cl[b2cl_columns_needed]

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Streamlit app
def main():
    st.title("GST FILINGS AUTOMATION")
    uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])
    
    if uploaded_files:
        all_dataframes = []
        for uploaded_file in uploaded_files:
            st.write(f"Processing: {uploaded_file.name}")
            
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            selected_sheets = st.multiselect(f"Select relevant sheets from {uploaded_file.name}", sheet_names)
            
            for sheet in selected_sheets:
                df = excel_file.parse(sheet)
                is_known_source = st.checkbox(f"Is {sheet} from a known source?", key=f"{uploaded_file.name}_{sheet}_known")
                
                if is_known_source:
                    source = st.selectbox("Select the source", known_sources, key=f"{uploaded_file.name}_{sheet}_source")
                    df = select_columns_from_known_source(df, needed_columns, source)
                else:
                    df = select_columns_from_unknown_source(df, needed_columns)
                
                if not df.empty:
                    df = format_place_of_supply(df)
                    all_dataframes.append(df)
        
        if all_dataframes:
            main_df = pd.concat(all_dataframes)
            main_df.reset_index(drop=True, inplace=True)
            
            customer_state_code = st.selectbox("Select the state code of the customer", 
                                               [state['code_number'] for state in state_codes])
            customer_state = next((state['code'] for state in state_codes if state['code_number'] == customer_state_code), None)
            
            main_df = fill_missing_values(main_df)
            main_df = create_place_of_origin_column(main_df, customer_state)
            main_df = fill_place_of_supply_with_place_of_origin(main_df)
            main_df = categorise_transactions(main_df)
            
            b2b = create_b2b_dataframe(main_df)
            b2cs = create_b2cs_dataframe(main_df)
            b2cl = create_b2cl_dataframe(main_df)
            
            if not b2b.empty:
                st.download_button(
                    label="Download B2B Output",
                    data=convert_df_to_csv(b2b),
                    file_name="b2b_output.csv",
                    mime="text/csv",
                )
            else:
                st.write("No B2B transactions to download.")
            
            if not b2cs.empty:
                st.download_button(
                    label="Download B2CS Output",
                    data=convert_df_to_csv(b2cs),
                    file_name="b2cs_output.csv",
                    mime="text/csv",
                )
            else:
                st.write("No B2CS transactions to download.")
            
            if not b2cl.empty:
                st.download_button(
                    label="Download B2CL Output",
                    data=convert_df_to_csv(b2cl),
                    file_name="b2cl_output.csv",
                    mime="text/csv",
                )
            else:
                st.write("No B2CL transactions to download.")
        else:
            st.error("No valid data was processed from the uploaded files. Please check your input and try again.")
    else:
        st.write("Please upload Excel files to process.")

if __name__ == "__main__":
    main()