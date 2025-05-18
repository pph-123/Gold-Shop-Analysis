import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, date
st.title('Gold Shop Analysis')
File_Path = 'shop_analysis 2.csv'
Shop_Analysis = pd.read_csv(File_Path)
#Shop_Analysis_Clean = Shop_Analysis.dropna()
df = Shop_Analysis.copy()
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home", "Daily Data Analysis", "Monthly Data Analysis", "Yearly Data Analysis", "Error Calculation", "Item Data Analysis"])
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file = f"data_{timestamp}.csv"

#➕ New: Convert to grams
def to_grams(row):
        kyat = float(row['kyat_sum'])
        pel = float(row['pel_sum'])
        yway = float(row['Yway_sum'])
        grams = ((((yway / 8) + pel) / 16) + kyat) * 16.606
        return round(grams, 10)

    

# ➕ New: Apply conditional transformation
def adjusted_grams(row):
    
    gram = row['Gram']
    category = row['Category']
    quality = row['Quality']

    if pd.isnull(gram) or pd.isnull(category) or pd.isnull(quality):
        return None
    if (quality == '18k'): 
        if category == 'ရွှေထည်ပြန်သိမ်းစာရင်း':
            return round(gram * (12 / 16) / 16.606, 10)
        elif (category == 'ရွှေထည်အရောင်းစာရင်း'):
            return round(gram * (12 / 16) / 16.606, 10)
        else:
            return None
    if (quality == 'Academy'): 
        if category == 'ရွှေထည်ပြန်သိမ်းစာရင်း':
            return round(gram * (16 / 16) / 16.606, 10)
        elif (category == 'ရွှေထည်အရောင်းစာရင်း'):
            return round(gram * (16 / 16) / 16.606, 10)
        else:
            return None

    # Define divisor mapping for each quality
    divisor_map = {
        '15ပဲရည်': 17,
        'ရွှေဒင်္ဂါးရေမှီ': 17.5,
        'ရေမှီ': 18,
        'ရေမှီ ၁၈းစပ်': 18.25,
        '၁၃ပဲရည်': 19,
        'စိန်ထည်': 19,
    }

    # Get the divisor for this quality
    divisor = divisor_map.get(quality)
    if not divisor:
        return None

    # Conversion logic for both categories
    if category == 'ရွှေထည်အရောင်းစာရင်း':
        return round(gram * 16 / divisor / 16.606, 10)
    elif category == 'ရွှေထည်ပြန်သိမ်းစာရင်း':
        base_value = gram * 16 / divisor / 17

        if quality in ['15ပဲရည်', 'ရွှေဒင်္ဂါးရေမှီ']:
            return round(128 - 4 / 128 * base_value, 10)
        elif quality in ['ရေမှီ', 'ရေမှီ ၁၈းစပ်', '၁၃ပဲရည်', 'စိန်ထည်']:
            return round (128 - 8 / 128 * base_value, 10)
        else:
            return None
    else:
        return None

with tab1:
    st.header("About")
    col1, col2= st.columns(2)

    with col1:
        st.header("Date")
       
        d = st.date_input("Input Date", date.today())
        formatted = d.strftime("%d.%m.%Y")
        st.write("Date:", formatted)
        Pel_1 = st.number_input("Insert Pel_Value", value = 0.0, placeholder="Choose Pel:")
        Yway_1 = st.number_input("Insert yway_Value", value = 0.0, placeholder="Choose Yway:")
        Kyat_1 = st.number_input("Insert Kyat_Value", value = 0.0, placeholder="Choose Kyat:")
        Cash = st.number_input("Insert Cash", value = 0.0, placeholder="Choose Cash:")
        Quantity = st.number_input("Insert Quantity", value = 0.0, placeholder="Choose Quantity:")
    
    
    with col2:
        st.header("Quantity")
        Quality = st.selectbox(
        "Select Gold Quality", ['Academy','15ပဲရည်', 'ရွှေဒင်္ဂါးရေမှီ','ရေမှီ', 'ရေမှီ ၁၈းစပ်', '၁၃ပဲရည်', '18k', 'စိန်ထည်'])
        Item = st.selectbox("Item", ['အကယ်ဒမီပိုင်း', 'ကြားပိုင်း', 'နားကပ်', 'လက်စွပ်', 'ဆွဲကြိုး', 'ဟန်းချိန်း', 'လက်ကောက်',
       'နားဆွဲ', 'နားကွင်း','Foot Chain', 'စိန်နားကပ်', 'စိန်ဆွဲကြိုး', 'စိန်လက်စွပ်', 'စိန်ဟန်းချိန်း'])
        Design = st.text_input("Insert Design", value = None, placeholder="Type Design...")
        Category = st.selectbox(
        "Select Category", ["ရွှေထည်အရောင်းစာရင်း", "ရွှေထည်ပြန်သိမ်းစာရင်း"])
    if st.button('Save'):
        Temp = {'Date' : formatted, 'ကျပ်' : Kyat_1, 'ပဲ' : Pel_1, 'ရွေး':Yway_1, 'သင့်ငွေ':Cash, 'Quality': Quality, 'Item': Item, 'Quantity':Quantity, 'Design' :Design, 'Category' :Category}
        Temp_1 = pd.DataFrame([Temp])
        df = pd.concat([df, Temp_1], ignore_index = True)
        df.to_csv(File_Path)
        st.success(f"Data saved to `{File_Path}`!")
    else:
        st.warning("Please enter a name before saving.")
with tab2:
    st.markdown(
        """
        <style>
        .tab1-font {
            font-size: 28px !important;
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

  

    st.header("Daily Data Analysis")
    st.write(df[['Date', 'ကျပ်', 'ပဲ', 'ရွေး', 'သင့်ငွေ', 'Quality', 'Item', 'Quantity', 'Design', 'Category']].tail(20))
    # Define start and end date
    start_date = st.date_input("Input Start Date", date.today())
    sformatted = start_date.strftime("%d.%m.%Y")
    print('sformatted',sformatted)
    
    end_date = st.date_input("Input End Date", date.today())
    eformatted = end_date.strftime("%d.%m.%Y")
    print('eformatted',eformatted)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    if st.button("Calculate"):
        # Filter rows
        filter_df = df[df['Date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
        print(filter_df)
        Total_Amount = filter_df.groupby('Date').agg({'သင့်ငွေ': ['sum','mean']}).reset_index()
        Total_Amount.columns = ['Date', 'Total in Cash', 'Average']
        Fig_1 = px.bar(Total_Amount, x = 'Date', y = "Total in Cash")
        st.plotly_chart(Fig_1)
        st.title('Daily Total Amount')
        st.write(Total_Amount)
        st.title('Daily Total Weight')
        #Total_Weight = filter_df.groupby('Date').agg({'ကျပ်': ['sum','mean'], 'ပဲ' : ['sum', 'mean'],'ရွေး' : ['sum', 'mean']}).reset_index()
        Total_Weight = filter_df.groupby('Date').agg({'ကျပ်': 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum'}).reset_index()
        Total_Weight.columns = ['Date','kyat_sum', 'pel_sum','Yway_sum']
        def tola (row):
            a = float(row['kyat_sum'])
            b = float(row['pel_sum'])
            c = float(row['Yway_sum'])
            result = (((c/8) + b)/16) + a
            #print((a,b,c))
            return round(result,14) 
        Total_Weight['tola'] = Total_Weight[['kyat_sum','pel_sum','Yway_sum']].apply(tola, axis = 1)
        Total_Weight['tola'] = Total_Weight['tola'].map('{:.10f}'.format) 
        st.write(Total_Weight)
        
        
        Total_qcWeight = filter_df.groupby(['Date','Quality','Category']).agg({'ကျပ်': 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum'}).reset_index()
        Total_qcWeight.columns = ['Date','Quality','Category','kyat_sum', 'pel_sum','Yway_sum']
        Total_qcWeight['Gram'] = Total_qcWeight.apply(to_grams, axis=1)
        Daily_g = Total_qcWeight.copy()
        Daily_g['Gram'] =  Daily_g['Gram'].map('{:.10f}'.format)
        Total_qcWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcWeight.apply(adjusted_grams, axis=1)
        Total_qcWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].map('{:.10f}'.format)
        st.title("Daily calculate weight by Gold quality and category with gram")
        st.write(Daily_g)
        DSold_out = Total_qcWeight.loc[Total_qcWeight['Category'] == 'ရွှေထည်အရောင်းစာရင်း']
        DCash_back = Total_qcWeight.loc[Total_qcWeight['Category'] == 'ရွှေထည်ပြန်သိမ်းစာရင်း']
        st.title("မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း")
        st.write(DSold_out)
        st.title("မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း")
        st.write(DCash_back)
        st.title("Gross Profit")
        DSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = pd.to_numeric(DSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
        DCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)']= pd.to_numeric(DCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
        
        DTotal_Soldout = DSold_out.groupby('Date')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
        DTotal_CashBack = DCash_back.groupby('Date')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
        DGrossProfit = pd.merge(DTotal_Soldout, DTotal_CashBack, on='Date', how='inner', suffixes=('_အရောင်း', '_ပြန်သိမ်း'))

    # Compute difference
        #MTotal_Soldout['diff'] = merged['A'] - merged['B']
        DGrossProfit['Final Gross Profit'] = DGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_အရောင်း'] - DGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_ပြန်သိမ်း']
        st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း စုစုပေါင်းအလေးချိန်')
        st.write(DTotal_Soldout)
        st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း စုစုပေါင်းအလေးချိန်')
        st.write(DTotal_CashBack)
        #st.title('Gross Profit')
        st.write(DGrossProfit)
        #st.write(f"<div class='tab1-font'>{MGrossProfit}</div>", unsafe_allow_html=True)
        
        
       
     
        st.title('Changing Kyat')
        pel = st.number_input("Insert pel", value = 0.0, placeholder="Type pel...")
        Yway = st.number_input("Insert Yway", value = 0.0, placeholder="Type Yway...")
        def tola2 (c,b): 
            result = (((c/8) + b)/16) 
            return round(result,14) 
        if pel and Yway:
            Kyat = tola2(Yway, pel)
            st.write('Changing Kyat is ')
            st.write(f"{Kyat:.14f}")
        Option = st.radio("What's your Option is ",[":rainbow[Yway]", "***pel***"],index=None,)
        #print(Option)
        Value = st.number_input("Enter Yway", value = 0.0, placeholder="Enter Yway...")
        if(Option == '***pel***'):
            pel = Value
            Yway = 0.0
        else:
            Yway = Value
            pel = 0.0
        st.write((Yway, pel))
        Kyat2 = tola2(Yway, pel)
        st.write('Changing Kyat of Yway is ')
        st.write(f"{Kyat2:.14f}")
        
    


with tab3:
    st.header("Monthly Data Analysis")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    Total_MAmount = df.groupby(['Year','Month']).agg({'သင့်ငွေ': ['sum','mean']}).reset_index()
    Total_MAmount.columns = ['Year','Month', 'Total in Cash', 'Average']
    Fig_2 = px.bar(Total_MAmount, x = 'Month', y = "Total in Cash")
    st.plotly_chart(Fig_2)
    st.title('Monthly Total Amount')
    st.write(Total_MAmount)
    st.title('Monthly Total Weight')
    Total_MWeight = df.groupby(['Year','Month','Category']).agg({'ကျပ်': 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum'}).reset_index()
    Total_MWeight.columns = ['Year','Month','Category','kyat_sum', 'pel_sum','Yway_sum']
    def tola (row):
        a = float(row['kyat_sum'])
        b = float(row['pel_sum'])
        c = float(row['Yway_sum'])
        result = (((c/8) + b)/16) + a
        #print((a,b,c))
        return round(result,14) 
    Total_MWeight['tola'] = Total_MWeight[['kyat_sum','pel_sum','Yway_sum']].apply(tola, axis = 1)
    Total_MWeight['tola'] = Total_MWeight['tola'].map('{:.10f}'.format) 
    st.write(Total_MWeight)
    
    Total_qcMWeight = df.groupby(['Year','Month', 'Quality', 'Category']).agg({'ကျပ်': 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum'}).reset_index()
    Total_qcMWeight.columns = ['Year','Month', 'Quality', 'Category','kyat_sum', 'pel_sum','Yway_sum']
    Total_qcMWeight['Gram'] = Total_qcMWeight.apply(to_grams, axis=1)
    Monthly_g = Total_qcMWeight.copy()
    Monthly_g['Gram'] = Monthly_g['Gram'].map('{:.10f}'.format)
    st.title("Monthly calculate weight by Gold quality and category with gram")
    st.write(Monthly_g)
    #st.title("မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း")
    Total_qcMWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcMWeight.apply(adjusted_grams, axis=1)
    Total_qcMWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcMWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].map('{:.10f}'.format)
    #st.write(Total_qcMWeight)
    MSold_out = Total_qcMWeight.loc[Total_qcMWeight['Category'] == 'ရွှေထည်အရောင်းစာရင်း']
    MCash_back = Total_qcMWeight.loc[Total_qcMWeight['Category'] == 'ရွှေထည်ပြန်သိမ်းစာရင်း']
    st.title("မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း")
    st.write(MSold_out)
    st.title("မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း")
    st.write(MCash_back)
   
    st.title("Gross Profit")
    MSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = pd.to_numeric(MSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
    MCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)']= pd.to_numeric(MCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
    MTotal_Soldout = MSold_out.groupby('Month')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
    MTotal_CashBack = MCash_back.groupby('Month')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
    MGrossProfit = pd.merge(MTotal_Soldout, MTotal_CashBack, on='Month', how='inner', suffixes=('_အရောင်း', '_ပြန်သိမ်း'))

# Compute difference
    #MTotal_Soldout['diff'] = merged['A'] - merged['B']
    MGrossProfit['Final Gross Profit'] = MGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_အရောင်း'] - MGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_ပြန်သိမ်း']
    st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း စုစုပေါင်းအလေးချိန်')
    st.write(MTotal_Soldout)
    st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း စုစုပေါင်းအလေးချိန်')
    st.write(MTotal_CashBack)
    #st.title('Gross Profit')
    st.write(MGrossProfit)
    #st.write(f"<div class='tab1-font'>{MGrossProfit}</div>", unsafe_allow_html=True)
            
with tab4:
    st.header("Yearly Data Analysis")
    
    Total_Amount = df.groupby('Year').agg({'သင့်ငွေ': ['sum','mean']}).reset_index()
    Total_Amount.columns = ['Year','Total', 'Average']
    Fig_2 = px.bar(Total_Amount, x = 'Year', y = "Total")
    st.plotly_chart(Fig_2)
    st.title('Yearly Total Weight')
    Total_YWeight = df.groupby('Year').agg({'ကျပ်': 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum'}).reset_index()
    Total_YWeight.columns = ['Year','kyat_sum', 'pel_sum','Yway_sum']
    def tola (row):
        a = float(row['kyat_sum'])
        b = float(row['pel_sum'])
        c = float(row['Yway_sum'])
        result = (((c/8) + b)/16) + a
        #print((a,b,c))
        return round(result,14) 
    Total_YWeight['tola'] = Total_YWeight[['kyat_sum','pel_sum','Yway_sum']].apply(tola, axis = 1)
    Total_YWeight['tola'] = Total_YWeight['tola'].map('{:.10f}'.format) 
    st.write(Total_YWeight)
    st.title("Yearly calculate weight by Gold quality and category")
    Total_qcYWeight = df.groupby(['Year','Quality','Category']).agg({'ကျပ်': 'sum', 'ပဲ' : 'sum', 'ရွေး' : 'sum'}).reset_index()
    Total_qcYWeight.columns = ['Year', 'Quality', 'Category','kyat_sum', 'pel_sum','Yway_sum']
    Total_qcYWeight['Gram'] = Total_qcYWeight.apply(to_grams, axis=1)
    #Total_qcYWeight['Gram'] = Total_qcYWeight['Gram']
    Yearly_g = Total_qcYWeight.copy()
    Yearly_g['Gram'] = Yearly_g['Gram'].map('{:.10f}'.format)
    st.title("Yearly calculate weight by Gold quality and category with gram")
    st.write(Yearly_g)
    st.title('မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)')
    Total_qcYWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcYWeight.apply(adjusted_grams, axis=1)
    Total_qcYWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = Total_qcYWeight['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].map('{:.10f}'.format)
    st.write(Total_qcYWeight)
    YSold_out = Total_qcYWeight.loc[Total_qcYWeight['Category'] == 'ရွှေထည်အရောင်းစာရင်း']
    YCash_back = Total_qcYWeight.loc[Total_qcYWeight['Category'] == 'ရွှေထည်ပြန်သိမ်းစာရင်း']
    st.title("မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း")
    st.write(YSold_out)
    st.title("မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း")
    st.write(YCash_back)
   
    st.title("Gross Profit")
    YSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'] = pd.to_numeric(YSold_out['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
    YCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)']= pd.to_numeric(YCash_back['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'], errors = 'coerce')
    
   
    YTotal_Soldout = YSold_out.groupby('Year')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
    YTotal_CashBack = YCash_back.groupby('Year')['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)'].sum().reset_index()
    YGrossProfit = pd.merge(YTotal_Soldout, YTotal_CashBack, on='Year', how='inner', suffixes=('_အရောင်း', '_ပြန်သိမ်း'))

# Compute difference
    #MTotal_Soldout['diff'] = merged['A'] - merged['B']
    YGrossProfit['Final Gross Profit'] = YGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_အရောင်း'] - YGrossProfit['မီးလင်းသင့်ပြီး ရွှေအလေးချိန်(ကျပ်)_ပြန်သိမ်း']
    st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်အရောင်းစာရင်း စုစုပေါင်းအလေးချိန်')
    st.write(YTotal_Soldout)
    st.markdown('မီးလင်းသင့်ပြီး ရွှေထည်ပြန်သိမ်းစာရင်း စုစုပေါင်းအလေးချိန်')
    st.write(YTotal_CashBack)
    #st.title('Gross Profit')
    st.write(YGrossProfit)
    #st.write(f"<div class='tab1-font'>{MGrossProfit}</div>", unsafe_allow_html=True)
    
    
with tab5:
    st.header("Calculate Error")

    # Title

    # Input fields
    cash_back = st.number_input("Enter Cash Back (MMK)", min_value=0.0, step=0.1)
    gold_price = st.number_input("Enter Current Gold Price (MMK)", min_value=0.0, step=0.1)

    # Calculate error
    if gold_price == 0:
        st.warning("Current Gold Price must be greater than 0.")
    else:
        error = cash_back / gold_price
        st.success(f"Calculated Error (Cash Back ÷ Gold Price): {error:.10f}ကျပ်သား")

    
    
    
with tab6:
    st.header("Item Data Analysis")
    Individual_Item = df.groupby(['Date','Item', 'Quality']).agg({'Quantity': 'sum', 'ကျပ်' : 'sum', 'ပဲ' : 'sum','ရွေး' : 'sum', 'သင့်ငွေ' : 'sum'}).reset_index()
    #Individual_Item.column = ['Date', 'Item', 'Quality']
    st.write(Individual_Item)
    Fig_2 = px.bar(Individual_Item, x = 'Date', y = 'Quantity', color = 'Item')
    st.plotly_chart(Fig_2)
    
    
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  