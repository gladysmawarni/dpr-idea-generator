from openai import OpenAI
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta 


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def flag_url(country):
    if country == "UK":
        return "https://flagcdn.com/w20/gb.png"
    elif country == "US":
        return "https://flagcdn.com/w20/us.png"
    else:
        return ""


def event_formatter(event):
    splitted = event.split('.')
    
    if len(splitted) <= 2:
        return splitted[-1]
    else:
        key_event = splitted[1]

        event_dict = {
            "reasoning_summary_text" : "summarizing",
            "reasoning_summary_part": "summarizing",
            "web_search_call" : "researching",
            "output_item": "formatting",
            "content_part": 'formatting',
            "output_text": "formatting"
        }

        return event_dict[key_event]



def research_function(company_name, topics):
    with st.spinner("Research in progress..."):
        status_placeholder = st.empty()  # single line placeholder


        with client.responses.stream(
            model="gpt-5",
            prompt={ "id": "pmpt_69873054589c8196956015d571a4946b07bb490ade1169d3", "version": "3" },
            input= f"company: {company_name}, topic: {topics}",
        ) as stream:
            for event in stream:
                # This is where you get the event type
                status_placeholder.markdown(
                    f"<span style='color: pink; font-weight: 500;'>Status: {event_formatter(event.type)}</span>",
                    unsafe_allow_html=True
                )

            final_response = stream.get_final_response()
            raw_text = final_response.output[-1].content[0].text
            data = json.loads(raw_text)
            df = pd.DataFrame.from_dict(data)

            status_placeholder.success("Research complete ✅")

            df[['headline_example_1','headline_example_2', 'headline_example_3']] = pd.DataFrame(df['pr_headline_example'].tolist(), index= df.index)
            df[['tag_1','tag_2','tag_source']] = pd.DataFrame(df.tags.tolist(), index= df.index)
            df.drop(columns=['tags', 'pr_headline_example'], inplace=True)

            df['client'] = company_name
            df['date_added'] = datetime.today().strftime('%Y-%m-%d')

            return df
    

def formatter(df, save=False):
    ## TILES
    COLS_PER_ROW = 2

    for i in range(0, len(df), COLS_PER_ROW):
        row_df = df.iloc[i:i + COLS_PER_ROW]
        cols = st.columns(COLS_PER_ROW)

        for col, (_, row) in zip(cols, row_df.iterrows()):
            ## COUNTRY FLAG
            url = flag_url(row["country"])

            ## x MONTHS AGO
            # Convert the string to a datetime object
            latest_date = datetime.strptime(row['latest_date'], '%Y-%m-%d')
            # Get current date
            now = datetime.now()
            # Calculate difference in months
            delta = relativedelta(now, latest_date)
            months_ago = delta.years * 12 + delta.months

            with col:
                tile = st.container(height=300)

                tile.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <img style="width: 25px; height: auto; vertical-align: middle;" src="{url}">
                        <p style="
                            margin: 0;
                            margin-left: 4px;
                            padding: 4px 8px;
                            background-color: #c6c4f2; 
                            font-size: 13px;
                            color: #000000;
                            border-radius: 8px;       
                            line-height: 1;
                        ">
                            {row['client']}
                        </p>
                        
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <p style="
                            margin: 0;
                            margin-left: 4px;
                            padding: 4px 8px;
                            background-color: #f7f6c1; 
                            font-size: 13px;
                            color: #000000;
                            border-radius: 8px;       
                            line-height: 1;
                        ">
                            {row['tag_1']}
                    </p>
                    <p style="
                            margin: 0;
                            margin-left: 4px;
                            padding: 4px 8px;
                            background-color: #f7f6c1; 
                            font-size: 13px;
                            color: #000000;
                            border-radius: 8px;       
                            line-height: 1;
                        ">
                            {row['tag_2']}
                    </p>
                    <p style="
                            margin: 0;
                            margin-left: 4px;
                            padding: 4px 8px;
                            background-color: #baebae; 
                            font-size: 13px;
                            color: #000000;
                            border-radius: 8px;       
                            line-height: 1;
                        ">
                            {row['tag_source'].split(':')[1]}
                    </p>
                    </div>

                    <div>
                        <p style="
                            font-weight: 700; 
                            text-align:center; 
                            font-size:18px; 
                            line-height:1.3;
                            font-family: 'Dosis', sans-serif;
                        ">
                            {row['headline_example_1']}
                        </p>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom: 8px;">
                        <a href="{row['dataset_link']}" 
                            style="
                                font-size: 14px; 
                                text-decoration: none; 
                                color: #5e70bf; 
                            ">
                                Data Link
                        </a>
                        <p style="
                            margin: 0;
                            margin-left: 10px;
                            font-size: 14px;
                        ">
                            published on {row['latest_date']} ({months_ago} months ago)
                        </p>
                    </div>

                    <div>
                        <p style="
                            font-size: 16px; 
                            line-height: 1; 
                            color: #68686b;
                        ">
                            {row['what_happened']}
                        </p>
                    </div>

                    <div>
                        <p style="
                            font-size: 16px; 
                            line-height: 1; 
                            margin: 4px 0 2px 0;
                            ">
                            Other possible headline:
                        </p>    
                        <ul style="margin: 0; padding-left: 20px; font-size: 16px; line-height: 1.4;">
                            <li>{row['headline_example_2']}</li>
                            <li>{row['headline_example_3']}</li>
                        </ul>
                    </div>

                    <div style="margin-top:20px;">
                        <p style="
                            font-size: 16px; 
                            line-height: 1; 
                            margin: 4px 0 2px 0;
                            ">
                            Expert commentary:
                        </p>   
                        <blockquote style="
                            font-size: 16px;
                            line-height: 1.5;
                            margin: 8px 0;
                            padding: 8px 12px;
                            border-left: 4px solid #c6c4f2;  /* colored left border for visual emphasis */
                            background-color: #f7d5f6;     
                            border-radius: 4px;
                            font-style: italic; 
                            color: #333333;
                        ">
                            {row['expert_commentary_example']}
                        </blockquote>
                    </div>
                    """, unsafe_allow_html=True)
            
                # if save:
                #     tile.button('save')